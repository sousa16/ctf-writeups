import requests

well_known_list = [
    ".well-known/acme-challenge",
    ".well-known/apple-app-site-association",
    ".well-known/apple-developer-merchant-domain-association",
    ".well-known/ashrae",
    ".well-known/assetlinks.json",
    ".well-known/brave-payments-verification.txt",
    ".well-known/brave-rewards-verification.txt",
    ".well-known/browserid",
    ".well-known/caldav",
    ".well-known/carddav",
    ".well-known/change-password",
    ".well-known/core",
    ".well-known/csvm",
    ".well-known/dnt",
    ".well-known/dnt-policy.txt",
    ".well-known/est",
    ".well-known/genid",
    ".well-known/hackers.txt",
    ".well-known/hoba",
    ".well-known/host-meta",
    ".well-known/host-meta.json",
    ".well-known/humans.txt",
    ".well-known/keybase.txt",
    ".well-known/ni",
    ".well-known/openid-configuration",
    ".well-known/openorg",
    ".well-known/posh",
    ".well-known/reload-config",
    ".well-known/repute-template",
    ".well-known/security.txt",
    ".well-known/stun-key",
    ".well-known/time",
    ".well-known/timezone",
    ".well-known/void",
    ".well-known/webfinger"
]

url = input("Enter the URL to check: ")

# check response for each well-known path
for path in well_known_list:
    full_url = f"{url}/{path}"
    try:
        response = requests.get(full_url, timeout=3)
        if response.status_code == 200:
            print(f"Found: {full_url}")
        else:
            print(
                f"Not found: {full_url} (Status code: {response.status_code})")
    except requests.RequestException as e:
        print(f"Error accessing {full_url}: {e}")
