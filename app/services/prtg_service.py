"""
HubNOC — prtg_service.py
Comunicacao com a API do PRTG (somente leitura)
"""
import requests, os
from dotenv import load_dotenv

load_dotenv()

PRTG_URL      = os.getenv('PRTG_URL', 'https://186.148.228.10')
PRTG_USER     = os.getenv('PRTG_USER', 'cliquedf')
PRTG_PASSHASH = os.getenv('PRTG_PASSHASH', '1855869054')
VERIFY_SSL    = os.getenv('PRTG_VERIFY_SSL', 'false').lower() != 'true'

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def _auth():
    return f"username={PRTG_USER}&passhash={PRTG_PASSHASH}"

def get_sensores(status_filter=None):
    """Retorna lista de sensores. status_filter: 5=DOWN, 4=Aviso"""
    url = f"{PRTG_URL}/api/table.json?content=sensors&output=json&columns=objid,name,device,group,status,status_raw,lastvalue,downtimesince&{_auth()}"
    if status_filter:
        url += f"&filter_status={status_filter}"
    r = requests.get(url, verify=False, timeout=15)
    r.raise_for_status()
    return r.json().get('sensors', [])

def get_status_geral():
    """Retorna resumo geral do PRTG"""
    url = f"{PRTG_URL}/api/getstatus.json?{_auth()}"
    r = requests.get(url, verify=False, timeout=10)
    r.raise_for_status()
    return r.json()

def get_devices():
    """Retorna lista de devices/equipamentos"""
    url = f"{PRTG_URL}/api/table.json?content=devices&output=json&columns=objid,name,host,group,status,status_raw&{_auth()}"
    r = requests.get(url, verify=False, timeout=15)
    r.raise_for_status()
    return r.json().get('devices', [])

def get_historico_sensor(sensor_id, horas=6):
    """Retorna historico de trafego de um sensor"""
    import datetime
    fim = datetime.datetime.now()
    ini = fim - datetime.timedelta(hours=horas)
    sdate = ini.strftime('%Y-%m-%d-%H-%M-%S')
    edate = fim.strftime('%Y-%m-%d-%H-%M-%S')
    url = (f"{PRTG_URL}/api/historicdata.json?id={sensor_id}"
           f"&sdate={sdate}&edate={edate}&avg=0&{_auth()}")
    r = requests.get(url, verify=False, timeout=20)
    r.raise_for_status()
    return r.json()

def mapear_status(status_raw):
    mapa = {
        3: 'OK', 4: 'Aviso', 5: 'DOWN',
        7: 'Pausado', 8: 'Incomum', 9: 'Parcial'
    }
    return mapa.get(int(status_raw or 0), 'Desconhecido')
