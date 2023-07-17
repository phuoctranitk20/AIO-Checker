import os, sys, json, time, random, string, ctypes, concurrent.futures, easygui, requests, datetime, threading
from colorama import Fore, Style
from requests import Session
from random import choice
from json import dumps
from pystyle import System, Colors, Colorate, Write
from concurrent import futures
from uuid import uuid4

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
proxy_error = 0
accounts_processed = 0
print()

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Discord Nitro Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, custom, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Discord Nitro  Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error} | CPM : {cpm}')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def check_nitro(nitro):
    global valid, invalid, proxy_error, custom, accounts_processed
    url = "https://discordapp.com/api/v9/entitlements/gift-codes/" + nitro + "?with_application=false&with_subscription_plan=true"
    r = requests.get(url)
    if r.status_code == 200:
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {nitro}")
        folder = "Checked/Discord-Nitro"
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open("Checked/Discord-Nitro/valid_nitro.txt", "a+", encoding='utf-8') as save_nitro:
            save_nitro.write(nitro + "\n")
        valid += 1
        accounts_processed += 1
        update_console_title()
    else:
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {nitro}")
        invalid += 1
        accounts_processed += 1
        update_console_title()

def process_line(line):
    nitro = line.strip()
    check_nitro(nitro)

def process_file(file_path):
    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        threads = []
        for line in lines:
            t = threading.Thread(target=process_line, args=(line,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

file_path = easygui.fileopenbox()
process_file(file_path)