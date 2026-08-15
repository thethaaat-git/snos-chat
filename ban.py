import requests
import re
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest, SetChatPermissionsRequest
from telethon.tl.types import ChatBannedRights, ChatPermissions
import time

# ------------------ ЗАГРУЗКА КОНФИГА ------------------
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
        if key in ('cid', 'owner', 'admin', 'cown', 'api_id'):
            value = int(value)
        elif key == 'unban':
            value = eval(value)
        config[key] = value

bot_token = config['bot']
cid = config['cid']
owner = config['owner']
unban = config.get('unban', [])
api_id = config['api_id']
api_hash = config['api_hash']

print("✅ Конфигурация загружена")

# ------------------ РАБОТА С ССЫЛКАМИ (Bot API) ------------------
api_url = f"https://api.telegram.org/bot{bot_token}"

# 1) Сброс ссылок
requests.post(f"{api_url}/revokeChatInviteLink", data={"chat_id": cid})
print("🔁 Ссылки сброшены")

# 2) Создание новой ссылки
new_link_data = requests.post(
    f"{api_url}/createChatInviteLink",
    data={"chat_id": cid, "member_limit": 1}
).json()
if new_link_data.get('ok'):
    new_link = new_link_data['result']['invite_link']
else:
    new_link = "Не удалось создать ссылку"
print(f"🔗 Новая ссылка: {new_link}")

# 3) Отправка ссылки владельцу
requests.post(
    f"{api_url}/sendMessage",
    data={"chat_id": owner, "text": new_link}
)
print("📤 Ссылка отправлена владельцу")

# ------------------ МАССОВЫЙ КИК ЧЕРЕЗ TELETHON ------------------
async def main():
    # Создаём клиент с токеном бота
    client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)

    # Получаем объект чата
    chat = await client.get_entity(cid)

    # --- Шаг 4: Запрещаем всем (кроме админов) отправлять сообщения ---
    # Устанавливаем права: разрешено только админам
    permissions = ChatPermissions(
        send_messages=False,
        send_media=False,
        send_stickers=False,
        send_gifs=False,
        send_games=False,
        send_inline=False,
        send_polls=False,
        change_info=False,
        invite_users=False,
        pin_messages=False
    )
    try:
        await client(SetChatPermissionsRequest(chat, permissions))
        print("🔒 Права на отправку сообщений отключены для всех (кроме админов)")
    except Exception as e:
        print(f"⚠️ Не удалось установить права: {e}")

    # Получаем всех участников
    participants = await client.get_participants(chat, aggressive=True)
    total = len(participants)
    print(f"👥 Найдено участников: {total}")

    # Права для бана (запрет всего)
    ban_rights = ChatBannedRights(
        until_date=None,
        view_messages=True,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        send_polls=True,
        change_info=True,
        invite_users=True,
        pin_messages=True
    )

    for i, user in enumerate(participants):
        user_id = user.id
        # Пропускаем ботов и тех, кто в unban
        if user.bot or user_id in unban:
            continue

        try:
            # Исключаем (бан)
            await client(EditBannedRequest(chat, user_id, ban_rights))
            print(f"✅ Исключён {user_id}")

            # Удаляем последнее сообщение в чате (системное уведомление о бане)
            try:
                last_msg = await client.get_messages(chat, limit=1)
                if last_msg:
                    await client.delete_messages(chat, [last_msg[0].id])
                    print(f"🗑️ Удалено системное сообщение о бане {user_id}")
            except Exception as e:
                print(f"⚠️ Не удалось удалить сообщение: {e}")

        except Exception as e:
            print(f"❌ Ошибка при кике {user_id}: {e}")
            continue

        # Прогресс
        progress = int((i + 1) / total * 100)
        print(f"⏳ Прогресс: {progress}%")

    print("✅ ГОТОВО")

    # Отправляем владельцу финальное сообщение
    requests.post(
        f"{api_url}/sendMessage",
        data={"chat_id": owner, "text": "готово"}
    )
    print("📤 'готово' отправлено владельцу")

    await client.disconnect()

# Запуск асинхронной функции
asyncio.run(main())
