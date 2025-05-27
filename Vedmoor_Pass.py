import csv
import os
import random
import string

from prettytable import PrettyTable
from pystyle import Center, Colorate, Colors

ALLOWED_SPECIAL = "!#$%&*+-=~"


def generate_password(length, use_special):
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)

    special = ""
    if use_special:
        special = random.choice(ALLOWED_SPECIAL)

    chars = string.ascii_letters + string.digits
    if use_special:
        chars += ALLOWED_SPECIAL

    remaining = length - 3 - (1 if use_special else 0)
    extra = "".join(random.choices(chars, k=remaining)) if remaining > 0 else ""

    password = list(uppercase + lowercase + digit + special + extra)
    random.shuffle(password)
    return "".join(password)


def save_password(service, password):
    with open("passwords.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([service, password])


def view_passwords():
    try:
        with open("passwords.csv", "r") as file:
            reader = csv.reader(file)
            table = PrettyTable()
            table.field_names = ["Сервис", "Пароль"]
            for row in reader:
                if row:
                    table.add_row(row)
            print(table)
    except FileNotFoundError:
        print("Файл с паролями не найден!")


def main():
    banner = """

╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                      │
│      ▄█    █▄     ▄████████ ████████▄          ▄███████▄    ▄████████    ▄████████   │
│     ███    ███   ███    ███ ███   ▀███        ███    ███   ███    ███   ███    ███   │
│     ███    ███   ███    █▀  ███    ███        ███    ███   ███    ███   ███    █▀    │
│     ███    ███  ▄███▄▄▄     ███    ███        ███    ███   ███    ███   ███          │
│     ███    ███ ▀▀███▀▀▀     ███    ███      ▀█████████▀  ▀███████████ ▀███████████   │
│     ███    ███   ███    █▄  ███    ███        ███          ███    ███          ███   │
│     ███    ███   ███    ███ ███   ▄███        ███          ███    ███    ▄█    ███   │
│     ▀██████▀    ██████████ ████████▀         ▄████▀        ███    █▀   ▄████████▀    │
│                                                                                      │
│                                                                                      │
│              [●] Все пароли сохраняются в passwords.csv в текущей дериктории.        │
│                                                                                      │
│                        [●] Coder: @vedmoor                                           │
│                        [●] Для возврата напишите 99                                  │
│                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────╯                                                     

    """

    while True:
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))
        print("\n1. Сгенерировать новый пароль")
        print("2. Посмотреть все пароли")
        choice = input("Выберите действие: ")

        if choice == "1":
            service_choice = input("Добавить название сервиса? (да/нет): ").lower()
            service = (
                input("Введите название сервиса: ")
                if service_choice == "да"
                else "Без названия"
            )

            special_choice = input(
                "Включать специальные символы (!#$%&*+-=~)? (да/нет): "
            ).lower()
            use_special = special_choice == "да"

            while True:
                try:
                    length = int(input("Длина пароля (минимум 8 символов): "))
                    if length < 8:
                        print("Пароль должен быть не менее 8 символов!")
                        continue
                    break
                except ValueError:
                    print("Введите число!")

            password = generate_password(length, use_special)
            save_password(service, password)
            print(f"Пароль сохранён: {password}")

        elif choice == "2":
            view_passwords()

        elif choice == "99":
            os.system("python main.py")

        else:
            print("Неверный ввод!")


if __name__ == "__main__":
    main()
