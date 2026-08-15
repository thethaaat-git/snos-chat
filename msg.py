import requests
import re

url = "https://raw.githubusercontent.com/thethaaat-git/snos-chat/refs/heads/main/config.py"
response = requests.get(url)
config_text = response.text

bot_token = re.search(r'bot\s*=\s*"([^"]*)"', config_text).group(1)
cid = int(re.search(r'cid\s*=\s*(-?\d+)', config_text).group(1))
txt1 = re.search(r'txt1\s*=\s*"([^"]*)"', config_text).group(1)

print("✅ Конфигурация загружена")

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {"chat_id": cid, "text": txt1}
requests.post(send_url, data=payload)

print("📤 txt1 отправлено в чат")
print("✅ ГОТОВО")
