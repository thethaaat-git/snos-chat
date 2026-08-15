import requests
import re
import time

url = "https://raw.githubusercontent.com/thethaaat-git/snos-chat/refs/heads/main/config.py"
response = requests.get(url)
config_text = response.text

bot_token = re.search(r'bot\s*=\s*"([^"]*)"', config_text).group(1)
cid = int(re.search(r'cid\s*=\s*(-?\d+)', config_text).group(1))
owner = int(re.search(r'owner\s*=\s*(\d+)', config_text).group(1))
unban = eval(re.search(r'unban\s*=\s*(\[[^\]]*\])', config_text).group(1))

print("✅ Конфигурация загружена")

api_url = f"https://api.telegram.org/bot{bot_token}"

# 1) Сброс ссылок
requests.post(f"{api_url}/revokeChatInviteLink", data={"chat_id": cid})
print("🔁 Ссылки сброшены")

# 2) Создание новой основной ссылки
new_link = requests.post(
    f"{api_url}/createChatInviteLink",
    data={"chat_id": cid, "member_limit": 1}
).json()
print(f"🔗 Новая ссылка: {new_link}")

# 3) Отправка ссылки владельцу
requests.post(
    f"{api_url}/sendMessage",
    data={"chat_id": owner, "text": new_link}
)
print("📤 Ссылка отправлена владельцу")

# 4) Получение участников
members = requests.get(
    f"{api_url}/getChatAdministrators",
    data={"chat_id": cid}
).json()["result"]

# Добавляем обычных участников (если нужно, можно через getChatMembersCount, но API не даёт список всех)
# В этом примере кикаем только админов (для полного списка нужен более сложный подход)
# Для демонстрации — кикаем всех админов, кроме ботов и unban
total = len(members)
for i, admin in enumerate(members):
    user = admin["user"]
    user_id = user["id"]

    if user["is_bot"] or user_id in unban:
        continue

    try:
        requests.post(
            f"{api_url}/banChatMember",
            data={"chat_id": cid, "user_id": user_id}
        )
        # Удаляем сообщение о кике (опционально)
        # requests.post(f"{api_url}/deleteMessage", ...)
    except:
        pass

    # Прогресс
    progress = int((i + 1) / total * 100)
    print(f"⏳ Прогресс: {progress}%")

print("✅ ГОТОВО")
