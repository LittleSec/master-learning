#/bin/python3

from urllib import request
from urllib import parse

sid = "MF1833026"
pw = ""
postdata = {"username":sid, "password":pw}
url = 'http://p.nju.edu.cn/portal_io/login'
postdata = parse.urlencode(postdata).encode('utf-8')
new_url = request.Request(url, postdata)
response = request.urlopen(new_url)
print(response.read())
