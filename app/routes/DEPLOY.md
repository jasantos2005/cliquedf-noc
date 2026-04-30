# HubNOC — Deploy v2 (Sidebar + Alertas + TV Multi-telas)

## Arquivos para substituir em /opt/automacoes/cliquedf/noc/static/

| Arquivo local         | Destino no servidor            | Ação      |
|-----------------------|-------------------------------|-----------|
| dashboard.html        | static/dashboard.html          | SUBSTITUIR|
| alertas.html          | static/alertas.html            | NOVO      |
| tv.html               | static/tv.html                 | SUBSTITUIR|

## Adicionar rota /alertas no main.py

```python
@app.get('/alertas', response_class=HTMLResponse)
async def alertas_page(): return html('alertas.html')
```

## Verificar crons ativos no servidor

```bash
crontab -l
# Deve ter:
# */2 * * * * cd /opt/automacoes/cliquedf/noc && venv/bin/python -m app.bootstrap.cron_sync_prtg
```

Se não tiver:
```bash
(crontab -l 2>/dev/null; echo "*/2 * * * * cd /opt/automacoes/cliquedf/noc && venv/bin/python -m app.bootstrap.cron_sync_prtg >> /var/log/hubnoc_sync.log 2>&1") | crontab -
```

## Patch no tv.py para tela de clientes (opcional)

Adicionar ao final de app/routes/tv.py o conteúdo de tv_patch.py

## Restart

```bash
systemctl restart hubnoc_cliquedf
systemctl status hubnoc_cliquedf
```
