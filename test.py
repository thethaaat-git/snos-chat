import requests
import re

URL = "https://raw.githubusercontent.com/thethaaat-git/snos-chat/refs/heads/main/config.py"
response = requests.get(URL)
lines = response.text.splitlines()

# Парсинг построчно
config = {}
for line in lines:
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    if '=' in line:
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        # Убираем кавычки, если есть
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        # Преобразуем числа и списки
        if key in ('cid', 'owner', 'admin', 'cown'):
            value = int(value)
        elif key == 'unban':
            value = eval(value)  # список
        config[key] = value

bot_token = config['bot']
cid = config['cid']
owner = config['owner']
txt1 = config['txt1']
txt2 = config['txt2']
txt3 = config['txt3']

print("✅ Конфигурация загружена")

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# 1) txt1 -> owner
requests.post(send_url, data={"chat_id": owner, "text": txt1})
print("📤 txt1 отправлено владельцу")

# 2) txt2 -> owner
requests.post(send_url, data={"chat_id": owner, "text": txt2})
print("📤 txt2 отправлено владельцу")

# 3) txt3 -> cid
requests.post(send_url, data={"chat_id": cid, "text": txt3})
print("📤 txt3 отправлено в чат")

print("✅ ГОТОВО")
