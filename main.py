import os
import random
import time
import webbrowser
from datetime import datetime

import requests
from pystyle import Anime, Center, Colorate, Colors

def clear_screen():
    """Очищает экран и устанавливает цвет фона и текста."""
    os.system("cls" if os.name == "nt" else "clear")
    # Устанавливаем цвет фона RGB(0, 12, 24) и белый текст
    print("\033[48;2;0;12;24m\033[38;2;255;255;255m", end='')
    os.system("cls" if os.name == "nt" else "clear")



def get_user_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        print(f"Ошибка при получении IP-адреса: {e}")
        return "Не удалось получить IP"


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


clear_screen()
user_ip = get_user_ip()
current_time = get_current_time()[10::]

online = random.randint(3, 9)


# Intro
print("Подключение к серверам Vedmak Client...")
print(f"Ваше место в очереди {online}")

time.sleep(2)

clear_screen()


Intro = """
                         ╭─                                                                             ─╮

                             ▄█    █▄     ▄████████ ████████▄    ▄▄▄▄███▄▄▄▄      ▄████████    ▄█   ▄█▄
                            ███    ███   ███    ███ ███   ▀███ ▄██▀▀▀███▀▀▀██▄   ███    ███   ███ ▄███▀
                            ███    ███   ███    █▀  ███    ███ ███   ███   ███   ███    ███   ███▐██▀  
                            ███    ███  ▄███▄▄▄     ███    ███ ███   ███   ███   ███    ███  ▄█████▀   
                            ███    ███ ▀▀███▀▀▀     ███    ███ ███   ███   ███ ▀███████████ ▀▀█████▄   
                            ███    ███   ███    █▄  ███    ███ ███   ███   ███   ███    ███   ███▐██▄  
                            ███    ███   ███    ███ ███   ▄███ ███   ███   ███   ███    ███   ███ ▀███▄
                             ▀██████▀    ██████████ ████████▀   ▀█   ███   █▀    ███    █▀    ███   ▀█▀
                                                                                              ▀        
 
                                    Coder @vedmoor. Киньте заявку на канал в @vedmoor_perehod...

                                                    Press "Enter" to continue.
                         ╰─                                                                              ─╯

"""

Anime.Fade(
    Center.Center(Intro),
    Colors.purple_to_blue,
    Colorate.Vertical,
    interval=0.1,
    enter=True,
)


webbrowser.open("https://t.me/+d_HxYLRyzBA0MGEy", new=2)


# End Intro


clear_screen()

banner1 = f"""


    ╭─                                                                               ─╮

         ▄█    █▄     ▄████████ ████████▄    ▄▄▄▄███▄▄▄▄      ▄████████    ▄█   ▄█▄
        ███    ███   ███    ███ ███   ▀███ ▄██▀▀▀███▀▀▀██▄   ███    ███   ███ ▄███▀
        ███    ███   ███    █▀  ███    ███ ███   ███   ███   ███    ███   ███▐██▀  
        ███    ███  ▄███▄▄▄     ███    ███ ███   ███   ███   ███    ███  ▄█████▀   
        ███    ███ ▀▀███▀▀▀     ███    ███ ███   ███   ███ ▀███████████ ▀▀█████▄   
        ███    ███   ███    █▄  ███    ███ ███   ███   ███   ███    ███   ███▐██▄  
        ███    ███   ███    ███ ███   ▄███ ███   ███   ███   ███    ███   ███ ▀███▄
         ▀██████▀    ██████████ ████████▀   ▀█   ███   █▀    ███    █▀    ███   ▀█▀
                                                                            ▀        
    ╰─                                                                                ─╯
            
    [●] Coder: @vedmoor                                     [●] Ваш IP: {user_ip}          
    [●] Version 1.0                                         [●] Время запуска: {current_time}    
    [●] Price: Free                                         [●] Юзеров сейчас: {online}   
    [●] Channel @vedmoor_perehod                            [●] Ведьмак Клиент



╭────────────────────────────────────────────────────────────────────────────────────────────╮   
│                                                                                            │
│  1. Vedmoor Kill - управление акк через сессии (код входа, удалить, писать, спамить и тд)  │
│                                                                                            │
│  2. Vedmoor Always Online - скрипт для вечного онлайна в тг                                │
│                                                                                            │
│  3. Vedmoor Tg Fluder - мощный спам кодами тг                                              │
│                                                                                            │
│  4. Vedmoor WebHack - пентест сайта (взлом)                                                │
│                                                                                            │
│  5. Vedmoor Wifi - подбор пароля к вайфаю                                                  │
│                                                                                            │       
│  6. Vedmoor IP Dos - дос атака на интернет жертвы по IP                                    │           
│                                                                                            │
│  7. Vedmoor Decoder - расшифровать/декодировать любой софт                                 │
│                                                                                            │
│  8. Vedmoor Obfuscate - зашифровать любой софт (15 способов)                               │ 
│                                                                                            │ 
│  9. Vedmoor GB Fish - создание бота, который если запустит жертва, то у вас будет ее номер │
│                                                                                            │   
│  10. Vedmoor Pass - генерировать и сохранять сложные пароли                                │  
│                                                                                            │     
│  00. Про создателей                                                                        │
│                                 [CTRL + Z] - Выход                                         │                                    
╰────────────────────────────────────────────────────────────────────────────────────────────╯
                            


"""


banner_about = """
                                                                                                                                
╭───────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                           │                                   
│                                                                                           │                              
│    ▄█    █▄     ▄████████ ████████▄    ▄▄▄▄███▄▄▄▄    ▄██████▄   ▄██████▄     ▄████████   │                         
│   ███    ███   ███    ███ ███   ▀███ ▄██▀▀▀███▀▀▀██▄ ███    ███ ███    ███   ███    ███   │
│   ███    ███   ███    █▀  ███    ███ ███   ███   ███ ███    ███ ███    ███   ███    ███   │                
│   ███    ███  ▄███▄▄▄     ███    ███ ███   ███   ███ ███    ███ ███    ███  ▄███▄▄▄▄██▀   │
│   ███    ███ ▀▀███▀▀▀     ███    ███ ███   ███   ███ ███    ███ ███    ███ ▀▀███▀▀▀▀▀     │
│   ███    ███   ███    █▄  ███    ███ ███   ███   ███ ███    ███ ███    ███ ▀███████████   │
│   ███    ███   ███    ███ ███   ▄███ ███   ███   ███ ███    ███ ███    ███   ███    ███   │
│    ▀██████▀    ██████████ ████████▀   ▀█   ███   █▀   ▀██████▀   ▀██████▀    ███    ███   │
│                                                                              ███    ███   │                                                                │
│                                                                                           │
│                                Coder:   @vedmoor   | ведмур                               │
│                                Vedmak Client | Ведьмак клиент                             │
│                                                                                           │
│                                Channel: @vedmoor_perehod                                  │
│                                                                                           │
│            Уязвимости не в коде, а в головах тех, кто считает себя неуязвимым.            │
╰───────────────────────────────────────────────────────────────────────────────────────────╯


"""

print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner1)))

def main():
    while True:
        try:
            
            choice = input("root@Vedmak_Client -> ")

            if choice == "00":
                print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner_about)))
            scripts = {
                "1": "Vedmoor_Kill.py",
                "2": "Vedmoor_Always_Online.py",
                "3": "Vedmoor_Flude.py",
                "4": "Vedmoor_WebHack.py",
                "5": "Vedmoor_Wifi.py",
                "6": "Vedmoor_IP_Dos.py",
                "7": "Vedmoor_Decoder.py",
                "8": "Vedmoor_Obfuscate.py",
                "9": "Vedmoor_Fish.py",
                "10": "Vedmoor_Pass.py"
            }
            if choice in scripts:
                os.system(f"python {scripts[choice]}")
            elif choice != "00":
                print("Неверный выбор. ")

        except Exception as e:
            print(f"Произошла ошибка: {e}. Попробуйте снова.")


if __name__ == "__main__":
    main()
