import os

from pystyle import Center, Colorate, Colors
from telethon import TelegramClient, events, functions

banner = """
╭───────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                           │                                   
│                 ▄██████▄  ███▄▄▄▄    ▄█        ▄█  ███▄▄▄▄      ▄████████                 │
│                ███    ███ ███▀▀▀██▄ ███       ███  ███▀▀▀██▄   ███    ███                 │
│                ███    ███ ███   ███ ███       ███▌ ███   ███   ███    █▀                  │
│                ███    ███ ███   ███ ███       ███▌ ███   ███  ▄███▄▄▄                     │  
│                ███    ███ ███   ███ ███       ███▌ ███   ███ ▀▀███▀▀▀                     │
│                ███    ███ ███   ███ ███       ███  ███   ███   ███    █▄                  │
│                ███    ███ ███   ███ ███▌    ▄ ███  ███   ███   ███    ███                 │
│                 ▀██████▀   ▀█   █▀  █████▄▄██ █▀    ▀█   █▀    ██████████                 │
│                                     ▀                                                     │
│                                                                                           │
│        [●] Для создания api id, hash создайте новое приложение на my.telegram.org/apps    │
│        [●] Coder: @vedmoor                                                                │
│        [●] Для возврата напишите 99                                                       │
│                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
            


"""

print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))


api_id = input("Введите API ID: ").strip()

if api_id == "99":
    os.system("python main.py")


api_hash = input("Введите API Hash: ").strip()


client = TelegramClient("infinity", int(api_id), api_hash)


@client.on(events.UserUpdate)
async def handler(event):
    if event.online or event.last_seen or event.recently:
        await client(functions.account.UpdateStatusRequest(offline=False))


client.start()

print("Вечный онлайн установлен!")

client.run_until_disconnected()
