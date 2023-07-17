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
ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Discord Token Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error}')

def update_console_title():
    global valid, invalid, custom, premium, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Phantom AIO 』 ~ Discord Token Checker | Valid : {valid} | Invalid : {invalid} | Proxy Error : {proxy_error} | CPM : {cpm}')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def discord_token_checker(token):
    global valid, invalid, accounts_processed
    response = requests.get('https://discord.com/api/v9/users/@me/library', headers = {
                             "accept": "*/*",
                             "accept-encoding": "gzip, deflate, br",
                             "accept-language": "en-US,en;q=0.9",
                             "authorization": token,
                             "cookie": "__dcfduid=88221810e37411ecb92c839028f4e498; __sdcfduid=88221811e37411ecb92c839028f4e498dc108345b16a69b7966e1b3d33d2182268b3ffd2ef5dfb497aef45ea330267cf; locale=en-US; OptanonConsent=isIABGlobal=false&datestamp=Fri+Jun+03+2022+15%3A36%3A59+GMT-0400+(Eastern+Daylight+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; __stripe_mid=3a915c95-4cf7-4d27-9d85-cfea03f7ce829a88e5; __stripe_sid=b699111a-a911-402d-a08a-c8801eb0f2e8baf912; __cf_bm=nEUsFi1av6PiX4cHH1PEcKFKot6_MslL4UbUxraeXb4-1654285264-0-AU8vy1OnS/uTMTGu2TbqIGYWUreX3IAEpMo++NJZgaaFRNAikwxeV/gxPixQ/DWlUyXaSpKSNP6XweSVG5Mzhn/QPdHU3EmR/pQ5K42/mYQaiRRl6osEVJWMMtli3L5iIA==",
                             "referer": "https://discord.com/channels/967617613960187974/981260247807168532",
                             "sec-fetch-dest": "empty",
                             "sec-fetch-mode": "cors",
                             "sec-fetch-site": "same-origin",
                             "sec-gpc": "1",
                             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
                             "x-discord-locale": "en-US",
                             "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMi4wLjUwMDUuNjEgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEwMi4wLjUwMDUuNjEiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTMwNDEwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
                        }
                    )
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            email = False
            phone = False
        else:
            email = data.get("verified", False)
            phone = data.get("phone", False)

            if email or phone:
                email = phone = True
            else:
                email = phone = False
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {token}")
        valid += 1
        accounts_processed += 1
        update_console_title()
        folder = "Checked/Discord-Tokens"
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open("Checked/Discord-Tokens/discord_tokens.txt", "a+", encoding='utf-8') as save:
            save.write(token + f"\n")
    else:
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {token}")
        invalid += 1
        accounts_processed += 1
        update_console_title()

def process_line(line):
    token= line.strip()
    discord_token_checker(token)

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