#/bin/python3

import json
import time
from urllib import request
from urllib import parse

def loginNJUWLAN(sid, pw):
    postdata = {"username":sid, "password":pw}
    url_login = "http://p.nju.edu.cn/portal_io/login"
    postdata = parse.urlencode(postdata).encode('utf-8')
    new_url = request.Request(url_login, postdata)
    with request.urlopen(new_url) as webstream:
        response = webstream.read().decode()
        reply_code = json.loads(response)["reply_code"]
        if reply_code == 1:
            print("Login success")
            return True
        else:
            print("Login fail")
            print(response)
            return False

def alive_check_once(sid, pw, retry_time=5):
    url_getinfo = "http://p.nju.edu.cn/portal_io/getinfo"
    with request.urlopen(url_getinfo) as webstream:
        data = webstream.read().decode()
        reply_code = json.loads(data)["reply_code"]
        if reply_code != 0:
            print("try to login...")
            for i in range(retry_time):
                if loginNJUWLAN(sid, pw):
                    break
                time.sleep(10)
            else:
                raise Exception("login fail")
        else:
            print("have login")
            time.sleep(3600)

if __name__ == "__main__":
    sid = "MF1833026"
    pw = ""
    while True:
        try:
            alive_check_once(sid, pw)
        except:
            time.sleep(240)
        time.sleep(3600)
