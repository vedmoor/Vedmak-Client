import base64
import marshal
import os
import zlib

from pystyle import Center, Colorate, Colors

def zlb(in_):
    return zlib.compress(in_)
def b16(in_):
    return base64.b16encode(in_)
def b32(in_):
    return base64.b32encode(in_)
def b64(in_):
    return base64.b64encode(in_)
def mar(in_):
    return marshal.dumps(compile(in_, "<x>", "exec"))


banner = """




╭───────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│           ▄█    █▄     ▄████████ ████████▄        ▄██████▄  ▀█████████▄     ▄████████     │           
│          ███    ███   ███    ███ ███   ▀███      ███    ███   ███    ███   ███    ███     │
│          ███    ███   ███    █▀  ███    ███      ███    ███   ███    ███   ███    █▀      │
│          ███    ███  ▄███▄▄▄     ███    ███      ███    ███  ▄███▄▄▄██▀   ▄███▄▄▄         │
│          ███    ███ ▀▀███▀▀▀     ███    ███      ███    ███ ▀▀███▀▀▀██▄  ▀▀███▀▀▀         │
│          ███    ███   ███    █▄  ███    ███      ███    ███   ███    ██▄   ███            │
│          ███    ███   ███    ███ ███   ▄███      ███    ███   ███    ███   ███            │
│           ▀██████▀    ██████████ ████████▀        ▀██████▀  ▄█████████▀    ███            │
│                                                                                           │
│                                 1.  Marshal                                               │
│                                 2.  Zlib                                                  │
│                                 3.  Base64 (b16)                                          │
│                                 4.  Base64 (b32)                                          │
│                                 5.  Base64 (b64)                                          │
│                                 6.  Base64 (b16) + Zlib                                   │
│                                 7.  Base64 (b32) + Zlib                                   │
│                                 8.  Base64 (b64) + Zlib                                   │
│                                 9.  Zlib + Marshal                                        │
│                                 10. Base64 (b16) + Marshal                                │
│                                 11. Base64 (b32) + Marshal                                │
│                                 12. Base64 (b64) + Marshal                                │
│                                 13. Base64 (b16) + Zlib + Marshal                         │
│                                 14. Base64 (b32) + Zlib + Marshal                         │
│                                 15. Base64 (b64) + Zlib + Marshal                         │
│                                                                                           │
│                    [●] Coder @vedmoor                                                     │
│                    [●] Для возврата напишите 99                                           │
│                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────╯




"""


def show_menu():
    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner)))


def Encode(option, data, output):
    loop = int(input("\n\t    [*] Кол-во циклов шифрования → "))

    encoding_functions = {
        1: (
            "mar(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__[::-1]);",
        ),
        2: (
            "zlb(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__[::-1]);",
        ),
        3: (
            "b16(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b16decode(__[::-1]);",
        ),
        4: (
            "b32(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b32decode(__[::-1]);",
        ),
        5: (
            "b64(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b64decode(__[::-1]);",
        ),
        6: (
            "b16(zlb(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));",
        ),
        7: (
            "b32(zlb(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));",
        ),
        8: (
            "b64(zlb(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));",
        ),
        9: (
            "zlb(mar(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__[::-1]));",
        ),
        10: (
            "b16(mar(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b16decode(__[::-1]));",
        ),
        11: (
            "b32(mar(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b32decode(__[::-1]));",
        ),
        12: (
            "b64(mar(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b64decode(__[::-1]));",
        ),
        13: (
            "b16(zlb(mar(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1])));",
        ),
        14: (
            "b32(zlb(mar(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])));",
        ),
        15: (
            "b64(zlb(mar(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])));",
        ),
    }

    if option not in encoding_functions:
        raise ValueError("Неправильный номер")

    xx, heading = encoding_functions[option]

    for _ in range(loop):
        try:
            data = "exec((_)(%s))" % repr(eval(xx))

        except TypeError as e:
            raise TypeError("Encoding error: " + str(e))

    with open(output, "w") as f:
        f.write(heading + data)


if __name__ == "__main__":
    show_menu()
    try:
        option = int(input("\t    [*] Выбери тип шифрования → "))
        if option == 99:
            os.system("python main.py")
            exit(0)

        file = input("\t    [*] Имя файла → ")
        output = file.replace(".py", "") + "_vedmoor_encoded.py"

        with open(file, "r", encoding="utf-8") as f:
            data = f.read()

        Encode(option, data, output)
        print(f"\n\t    [+] Зашифрованный файл сохранен, как: {output}")

    except Exception as e:
        print(f"\n\t    [!] Ошибка: {str(e)}")
