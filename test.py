import requests
import re

# Загрузка конфигурации
url = "https://raw.githubusercontent.com/thethaaat-git/snos-chat/refs/heads/main/config.py"
response = requests.get(url)
config_text = response.text

# Парсим значения
bot_token = re.search(r'bot\s*=\s*"([^"]*)"', config_text).group(1)
cid = int(re.search(r'cid\s*=\s*(-?\d+)', config_text).group(1))
owner = int(re.search(r'owner\s*=\s*(\d+)', config_text).group(1))
txt1 = re.search(r'txt1\s*=\s*"([^"]*)"', config_text).group(1)
txt2 = re.search(r'txt2\s*=\s*"([^"]*)"', config_text).group(1)
txt3 = re.search(r'txt3\s*=\s*"([^"]*)"', config_text).group(1)

print("✅ Конфигурация загружена")

# Отправка через Bot API
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# 1) txt1 -> owner
payload = {"chat_id": owner, "text": txt1}
requests.post(send_url, data=payload)
print("📤 txt1 отправлено владельцу")

# 2) txt2 -> owner
payload = {"chat_id": owner, "text": txt2}
requests.post(send_url, data=payload)
print("📤 txt2 отправлено владельцу")

# 3) txt3 -> cid
payload = {"chat_id": cid, "text": txt3}
requests.post(send_url, data=payload)
print("📤 txt3 отправлено в чат")

print("✅ ГОТОВО")
