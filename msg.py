import requests
import re

URL = "https://raw.githubusercontent.com/thethaaat-git/snos-chat/refs/heads/main/config.py"
response = requests.get(URL)
lines = response.text.splitlines()

config = {}
for line in lines:
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    if '=' in line:
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        if key in ('cid', 'owner', 'admin', 'cown'):
            value = int(value)
        elif key == 'unban':
            value = eval(value)
        config[key] = value

bot_token = config['bot']
cid = config['cid']
txt1 = config['txt1']

print("✅ Конфигурация загружена")

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
requests.post(send_url, data={"chat_id": cid, "text": txt1})

print("📤 txt1 отправлено в чат")
print("✅ ГОТОВО")
