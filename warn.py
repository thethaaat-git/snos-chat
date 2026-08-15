import requests
import re

url = "https://raw.githubusercontent.com/thethaaat-git/snos-chat/refs/heads/main/config.py"
response = requests.get(url)
config_text = response.text

bot_token = re.search(r'bot\s*=\s*"([^"]*)"', config_text).group(1)
cid = int(re.search(r'cid\s*=\s*(-?\d+)', config_text).group(1))
txt2 = re.search(r'txt2\s*=\s*"([^"]*)"', config_text).group(1)

print("✅ Конфигурация загружена")

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {"chat_id": cid, "text": txt2}
requests.post(send_url, data=payload)

print("📤 txt2 отправлено в чат")
print("✅ ГОТОВО")
