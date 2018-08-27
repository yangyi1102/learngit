'''
Created on 2018年8月15日

@author: yangyi
'''
#coding=utf-8
import re
import requests
import json
session = requests.Session()
url = 'https://login.taobao.com/jump?target=https%3A%2F%2Fcart.1688.com%2Fajax%2FquickCartCount.jsx%3Ftbpm%3D1%26callback%3DjQuery183021917934911062198_1534490932737%26_%3D1534490932990'
response = session.get(url)
a = re.findall('(cookie2=.*?\s)', str(session.cookies))
print(a[0])