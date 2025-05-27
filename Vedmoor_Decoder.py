from pystyle import Colors, Colorate, Center
import base64
import zlib
import marshal
import re
import dis
import os
from datetime import date


def RendyObf():
    file = input("[+] Введите путь к файлу: ")
    output = input("[+] Введите путь для сохранения: ")
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        code = content.replace("exec(_(", "vedmoor = (_(")
        try:
            local_vars = {}
            exec(code, globals(), local_vars)
            if "vedmoor" in local_vars:
                vedmoor_result = local_vars["vedmoor"]
            else:
                vedmoor_result = None
        except Exception as e:
            print(f"\n[-] Ошибка при выполнении кода: {e}")
        else:
            try:
                if vedmoor_result is not None:
                    result = (
                        vedmoor_result.decode("utf-8")
                        if isinstance(vedmoor_result, bytes)
                        else str(vedmoor_result)
                    )
                else:
                    result = "Выполнение кода завершилось без возврата результата vedmoor"
            except UnicodeDecodeError as e:
                print(f"\n[-] Ошибка декодирования: {e}")
            except Exception as e:
                print(f"\n[-] Ошибка преобразования в строку: {e}")
        with open(output, "w", encoding="utf-8") as outfile:
            outfile.write(
                f"""
#------------------
# -- DECODER tg @vedmoor
# -- {date.today()}
#-------------------\n\n"""
                + result
            )
        print(f"[+] Результат сохранен в: {output}")
    except FileNotFoundError:
        print("[-] Файл не найден.")
    except Exception as e:
        print(f"[-] Произошла ошибка: {e}")


def Base64Obf():
    file = input("[+] Введите путь к файлу: ")
    output = input("[+] Введите путь для сохранения: ")
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file}' не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла '{file}': {e}")
    pattern = r"_ = lambda.*?exec\(b\'(.*?)\'\)"
    match = re.search(pattern, content)
    extracted_text = match.group(1)
    try:
        result = base64.b64decode(extracted_text)
        with open(output, "w", encoding="utf-8") as outfile:
            outfile.write(
                f"""
#------------------
# -- DECODER tg @vedmoor
# -- {date.today()}
#-------------------\n\n"""
                + result.decode()
            )
        print(f"[+] Результат сохранен в: {output}")
    except Exception as e:
        print(f"[-] Ошибка при сохранении: {e}")


def ZlibObf():
    file = input("[+] Введите путь к файлу: ")
    output = input("[+] Введите путь для сохранения: ")
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file}' не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла '{file}': {e}")
    pattern = r"_ = lambda.*?exec\(b\'(.*?)\'\)"
    match = re.search(pattern, content)
    extracted_text = match.group(1)
    try:
        result = zlib.decompress(extracted_text.encode())
        with open(output, "w", encoding="utf-8") as outfile:
            outfile.write(
                f"""
#------------------
# -- DECODER tg @vedmoor
# -- {date.today()}
#-------------------\n\n"""
                + result.decode()
            )
        print(f"[+] Результат сохранен в: {output}")
    except Exception as e:
        print(f"[-] Ошибка при сохранении: {e}")


def Base64ZlibObf():
    file = input("[+] Введите путь к файлу: ")
    output = input("[+] Введите путь для сохранения: ")
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file}' не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла '{file}': {e}")
    pattern = r"_ = lambda.*?exec\(b\'(.*?)\'\)"
    match = re.search(pattern, content)
    extracted_text = match.group(1)
    try:
        reversed_string = extracted_text[::-1]
        decoded_data = base64.b64decode(reversed_string)
        result = zlib.decompress(decoded_data)
        with open(output, "w", encoding="utf-8") as outfile:
            outfile.write(result.decode())
        print(f"[+] Результат сохранен в: {output}")
    except Exception as e:
        print(f"[-] Ошибка при сохранении: {e}")


def MarshalZlibBase64():
    file = input("[+] Введите путь к файлу: ")
    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"[-] Ошибка: Файл '{file}' не найден.")
        return
    except Exception as e:
        print(f"[-] Ошибка при чтении файла: {e}")
        return
    reversed_data = code[::-1]
    decoded_data = base64.b64decode(reversed_data)
    decompressed_data = zlib.decompress(decoded_data)
    code_object = marshal.loads(decompressed_data)
    print("\n[!] Не автоматизированный разбор кода\n\n")
    print(f"{dis.dis(code_object)}")
    print(f"{code_object.co_consts}")
    print(f"{code_object.co_names}")


banner = """


╭───────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│    ████████▄     ▄████████  ▄████████  ▄██████▄  ████████▄     ▄████████    ▄████████     │
│    ███   ▀███   ███    ███ ███    ███ ███    ███ ███   ▀███   ███    ███   ███    ███     │
│    ███    ███   ███    █▀  ███    █▀  ███    ███ ███    ███   ███    █▀    ███    ███     │
│    ███    ███  ▄███▄▄▄     ███        ███    ███ ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀     │
│    ███    ███ ▀▀███▀▀▀     ███        ███    ███ ███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀       │
│    ███    ███   ███    █▄  ███    █▄  ███    ███ ███    ███   ███    █▄  ▀███████████     │
│    ███   ▄███   ███    ███ ███    ███ ███    ███ ███   ▄███   ███    ███   ███    ███     │
│    ████████▀    ██████████ ████████▀   ▀██████▀  ████████▀    ██████████   ███    ███     │
│                                                                            ███    ███     │
│                                                                                           │
│                        [1] Base64                                                         │
│                        [2] Zlib                                                           │
│                        [3] Base64 + Zlib                                                  │
│                        [4] Rendy(Marshal + Lzma + Zlib + Base64)                          │
│                        [5] Marshal + Zlib + Base64 [M]                                    │
│                                                                                           │
│                        [●] Coder: @vedmoor                                                │
│                        [●] Для возврата напишите 99                                       │
│                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────╯     
"""


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))

        decoder = input("\nВыбери пункт ->  ")
        if decoder == "1":
            Base64Obf()
            input("\nНажмите enter чтобы продолжить")
        elif decoder == "2":
            ZlibObf()
            input("\nНажмите enter чтобы продолжить")
        elif decoder == "3":
            Base64ZlibObf()
            input("\nНажмите enter чтобы продолжить")
        elif decoder == "4":
            RendyObf()
            input("\nНажмите enter чтобы продолжить")
        elif decoder == "5":
            MarshalZlibBase64()
            input("\nНажмите enter чтобы продолжить")
        elif decoder == "99":
            os.system("python main.py")


if __name__ == "__main__":
    main()