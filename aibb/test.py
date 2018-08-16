'''
Created on 2018年8月15日

@author: yangyi
'''
#coding=utf-8
import re
url='https://detail.1688.com/offer/1043485734.html'
pattern=re.compile(r'\d+')
m=re.findall(r'\d+', url)[1]
print(m)