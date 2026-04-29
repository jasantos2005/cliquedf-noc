#!/bin/bash
# HubNOC Cliquedf — deploy.sh
# Servidor: 72.61.24.119
# Uso: bash deploy.sh

set -e

DIR="/opt/automacoes/cliquedf/noc"
SERVICO="hubnoc_cliquedf"
PORTA=8006
DOMINIO="noc.iatechhub.com.br"

echo "=== HubNOC — Deploy ==="

# 1. Criar diretorios
mkdir -p $DIR/app/routes
mkdir -p $DIR/app/services
mkdir -p $DIR/app/bootstrap
mkdir -p $DIR/static

# 2. Venv
if [ ! -d "$DIR/venv" ]; then
    echo "[1/6] Criando venv..."
    python3 -m venv $DIR/venv
fi

# 3. Dependencias
echo "[2/6] Instalando dependencias..."
$DIR/venv/bin/pip install -q -r $DIR/requirements.txt

# 4. Banco
echo "[3/6] Inicializando banco..."
cd $DIR && venv/bin/python -m app.bootstrap.create_tables

# 5. Systemd
echo "[4/6] Configurando servico systemd..."
cat > /etc/systemd/system/${SERVICO}.service << EOF
[Unit]
Description=HubNOC Cliquedf
After=network.target

[Service]
User=root
WorkingDirectory=${DIR}
EnvironmentFile=${DIR}/.env
ExecStart=${DIR}/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port ${PORTA}
Restart=always
RestartSec=5
StandardOutput=append:/var/log/${SERVICO}.log
StandardError=append:/var/log/${SERVICO}_err.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable $SERVICO
systemctl restart $SERVICO
sleep 2
systemctl status $SERVICO --no-pager

# 6. Nginx
echo "[5/6] Configurando Nginx..."
cat > /etc/nginx/sites-available/$SERVICO << EOF
server {
    listen 80;
    server_name ${DOMINIO};
    location / {
        proxy_pass http://127.0.0.1:${PORTA};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

ln -sf /etc/nginx/sites-available/$SERVICO /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 7. SSL
echo "[6/6] Configurando SSL..."
certbot --nginx -d $DOMINIO --non-interactive --agree-tos -m admin@cliquedf.com.br || echo "[AVISO] Certbot falhou — configure SSL manualmente"

# 8. Crontabs
echo "[OK] Configurando crontabs..."
(crontab -l 2>/dev/null | grep -v "hubnoc"; cat << 'CRON'
# HubNOC — Sync PRTG a cada 2min
*/2 * * * * cd /opt/automacoes/cliquedf/noc && venv/bin/python -m app.bootstrap.cron_sync_prtg >> /var/log/hubnoc_sync.log 2>&1
# HubNOC — Alertas Telegram a cada 1min
*/1 * * * * cd /opt/automacoes/cliquedf/noc && venv/bin/python -m app.bootstrap.cron_telegram --tipo=alertas >> /var/log/hubnoc_tg.log 2>&1
# HubNOC — Resumo turno 08h/14h/20h BRT = 11h/17h/23h UTC
0 11,17,23 * * * cd /opt/automacoes/cliquedf/noc && venv/bin/python -m app.bootstrap.cron_telegram --tipo=turno >> /var/log/hubnoc_tg.log 2>&1
CRON
) | crontab -

echo ""
echo "========================================="
echo " HubNOC deploy concluido!"
echo " URL: https://${DOMINIO}"
echo " Health: curl https://${DOMINIO}/health"
echo " Logs: tail -f /var/log/${SERVICO}_err.log"
echo "========================================="
