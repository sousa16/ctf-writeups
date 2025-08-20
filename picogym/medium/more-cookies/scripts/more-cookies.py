import requests
import base64

s = requests.Session()
s.get("http://mercury.picoctf.net:21553/")

cookie = s.cookies["auth_name"]
print(f"Original cookie: {cookie}")

un64 = base64.b64decode(cookie)
print(f"Decoded cookie: {un64}")

un64b = base64.b64decode(un64)
print(f"Decoded cookie bytes: {un64b}")

for i in range(128):
    pos = i // 8
    bit_pos = i % 8
    flip_value = 1 << bit_pos
    guessdec = un64b[:pos] + \
        bytes([un64b[pos] ^ flip_value]) + un64b[pos+1:]
    guessenc1 = base64.b64encode(guessdec)
    guess = base64.b64encode(guessenc1)

    r = requests.get("http://mercury.picoctf.net:21553/",
                     cookies={"auth_name": guess.decode()})
    if "picoCTF{" in r.text:
        flag_start = r.text.find("picoCTF{")
        flag_end = r.text.find("}", flag_start) + 1
        flag = r.text[flag_start:flag_end]
        print(f"FLAG: {flag}")
        break
    else:
        print(f"Attempt {i}: pos={pos}, bit={bit_pos}, no flag")
