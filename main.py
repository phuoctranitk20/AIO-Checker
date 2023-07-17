import os, sys, time, json, random, string, logging, getpass, ctypes, concurrent.futures, threading

try:
    import tls_client
    import pystyle
    import colorama
    import requests
    import bs4
    import datetime
    import fake_useragent
    import easygui
    import httpx
    import asyncio
    import tkinter as tk
    import keyboard
except ModuleNotFoundError:
    os.system('pip install tls_client')
    os.system('pip install pystyle')
    os.system('pip install colorama')
    os.system('pip install requests')
    os.system('pip install bs4')
    os.system('pip install datetime')
    os.system('pip install fake_useragent')
    os.system('pip install easygui')
    os.system('pip install httpx')
    os.system('pip install asyncio')
    os.system('pip install tkinter')
    os.system('pip install keyboard')
    os.system('pip install aiohttp')
    os.system('pip install rsa')

from tls_client import Session
from json import dumps
from random import choice
from colorama import Fore, Style
from pystyle import Colors, Write, System, Anime, Colorate, Center
from bs4 import BeautifulSoup as Soup
from tkinter import messagebox

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

def message():
    txt = "modules/ignore.txt"
    if os.path.exists(txt):
        return
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Phantom AIO", "Welcome to Phantom AIO, this is a tool especially for checkers, it has multi proxy support, super fast and effective checkers with full capture and super easy to use!\n\nIf you have doubts or any error do not forget to tell us on our github or discord.\n\n➥ .gg/nebularw ~ .gg/pandasmurfs\n➥ github.com/H4cK3dR4Du ~ github.com/ItsYasu/\n\nFeatures:\n\n➥ Auto Proxy Scraper\n➥ Auto Libraries Installer\n➥ Fastest Checkers Ever\n\nMade By : H4cK3dR4Du, yasufake & tupadre").capitalize()

    with open(txt, "w") as file:
        file.write('')

message()
colorama.init()
username = getpass.getuser()
date = datetime.datetime.now()
formated_date = date.strftime('%d/%m/%Y')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def capture_remover():
    with open("combos.txt", "r") as file:
        with open("accounts_modified.txt", "w") as new_file:
            for line in file:
                line = line.strip()
                line = line.split(" ")[0]
                email, password = line.split(":")
                modified_line = f"{email}:{password}\n"
                new_file.write(modified_line)

    os.replace("accounts_modified.txt", "combos.txt")

capture_remover()

def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        proxies = f.read().splitlines()
    if not proxies:
        proxy_log = {}
    else:
        proxy = random.choice(proxies)
        proxy_log = {
            "http://": f"http://{proxy}", "https://": f"http://{proxy}"
        }
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, proxies=proxy_log, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except httpx.ProxyError:
        get_proxies()
    except httpx.ReadError:
        get_proxies()
    except httpx.ConnectTimeout:
        get_proxies()
    except httpx.ReadTimeout:
        get_proxies()
    except httpx.ConnectError:
        get_proxies()
    except httpx.ProtocolError:
        get_proxies()

def check_proxies_file():
    file_path = "proxies.txt"
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        get_proxies()

check_proxies_file()

accs = len(open('combos.txt').readlines())
proxies = len(open('proxies.txt').readlines())

def menu():
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Made By H4cK3dR4Du, yasufake & tupadre | .gg/nebularw - .gg/pandasmurfs | Accounts : [ {accs} ] ~ Proxies : [ {proxies} ]')
    Write.Print(f"""
    \t   ▄▀▀▄▀▀▀▄  ▄▀▀▄ ▄▄   ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▀▀█▀▀▄  ▄▀▀▀▀▄   ▄▀▀▄ ▄▀▄      ▄▀▀█▄   ▄▀▀█▀▄   ▄▀▀▀▀▄  
    \t  █   █   █ █  █   ▄▀ ▐ ▄▀ ▀▄ █  █ █ █ █    █  ▐ █      █ █  █ ▀  █     ▐ ▄▀ ▀▄ █   █  █ █      █ 
    \t  ▐  █▀▀▀▀  ▐  █▄▄▄█    █▄▄▄█ ▐  █  ▀█ ▐   █     █      █ ▐  █    █       █▄▄▄█ ▐   █  ▐ █      █ 
    \t     █         █   █   ▄▀   █   █   █     █      ▀▄    ▄▀   █    █       ▄▀   █     █    ▀▄    ▄▀ 
    \t   ▄▀         ▄▀  ▄▀  █   ▄▀  ▄▀   █    ▄▀         ▀▀▀▀   ▄▀   ▄▀       █   ▄▀   ▄▀▀▀▀▀▄   ▀▀▀▀   
    \t  █          █   █    ▐   ▐   █    ▐   █                  █    █        ▐   ▐   █       █         
    \t  ▐          ▐   ▐            ▐        ▐                  ▐    ▐                ▐       ▐         

                                            [ Welcome {username} | {formated_date} ]\n
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    \t(1) Netflix Checker\t\t\t(10) Facebook Checker
    \t(2) IPVanish Checker
    \t(3) Crunchyroll Checker
    \t(4) Discord Token Checker
    \t(5) Disney+ Checker
    \t(6) Discord Nitro Checker
    \t(7) Paramount+ Checker
    \t(8) Steam Checker
    \t(9) Windscribe Checker

    \t\t(x) Exit\t\t\t(+) Check Updates\t\t\t(!) Creators
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════""", Colors.red_to_blue, interval=0.000)
    Write.Print(f"\nroot@phantom_AIO ~> ", Colors.red_to_blue, interval=0.000); opc = input(magenta)
    if opc=="x":
        exit()
    elif opc=="1":
        import modules.netflix
        valid_accs = modules.netflix.valid
        invalid_accs = modules.netflix.invalid
        custom_accs = modules.netflix.custom
        proxy_error = modules.netflix.proxy_error
    elif opc=="2":
        import modules.ipvanish
        valid_accs = modules.ipvanish.valid
        invalid_accs = modules.ipvanish.invalid
        custom_accs = modules.ipvanish.custom
        proxy_error = modules.ipvanish.proxy_error
    elif opc=="3":
        import modules.crunchy
        valid_accs = modules.crunchy.valid
        invalid_accs = modules.crunchy.invalid
        custom_accs = modules.crunchy.custom
        proxy_error = modules.crunchy.proxy_error
    elif opc=="4":
        import modules.discord_token
        valid_accs = modules.discord_token.valid
        invalid_accs = modules.discord_token.invalid
        custom_accs = modules.discord_token.custom
        proxy_error = modules.discord_token.proxy_error
    elif opc=="5":
        import modules.disney

    elif opc=="6":
        import modules.discord_nitro
        valid_accs = modules.discord_nitro.valid
        invalid_accs = modules.discord_nitro.invalid
        custom_accs = modules.discord_nitro.custom
        proxy_error = modules.discord_nitro.proxy_error
    elif opc=="7":
        import modules.paramount
        valid_accs = modules.paramount.valid
        invalid_accs = modules.paramount.invalid
        custom_accs = modules.paramount.custom
        proxy_error = modules.paramount.proxy_error
    elif opc=="8":
        import modules.steam
        valid_accs = modules.steam.valid
        invalid_accs = modules.steam.invalid
        custom_accs = modules.steam.custom
        proxy_error = modules.steam.proxy_error
    elif opc=="9":
        import modules.windscribe
    else:
        System.Clear()
        menu()

    def finish_ui():
        ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Made By H4cK3dR4Du, yasufake & tupadre | .gg/nebularw - .gg/pandasmurfs | Accounts : [ {accs} ] ~ Proxies : [ {proxies} ] | Checker Stats')
        System.Clear()
        Write.Print(f"""
    \t\t\t   ____ _               _               ____  _        _       
    \t\t\t  / ___| |__   ___  ___| | _____ _ __  / ___|| |_ __ _| |_ ___ 
    \t\t\t | |   | '_ \ / _ \/ __| |/ / _ \ '__| \___ \| __/ _` | __/ __|
    \t\t\t | |___| | | |  __/ (__|   <  __/ |     ___) | || (_| | |_\__ \\
    \t\t\t  \____|_| |_|\___|\___|_|\_\___|_|    |____/ \__\__,_|\__|___/

    (+) Total Checked : {accs}
    (+) Loaded Proxies : {proxies}   

    (+) Valid : {valid_accs}
    (+) Invalid : {invalid_accs}
    (+) Custom : {custom_accs}
    (+) Proxy Errors : {proxy_error}

    (+) Made By H4cK3dR4Du, yasufake & tupadre
    (+) .gg/nebularw ~ .gg/pandasmurfs
""", Colors.red_to_blue, interval=0.000)
    finish_ui()
    Write.Print(f"\n    Press Enter ~> ", Colors.red_to_blue, interval=0.000); input(magenta)
    System.Clear()
    menu()
menu()