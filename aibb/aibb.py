'''
Created on 2018年8月6日

@author: yangyi
'''
#coding=utf-8
#获取1688平台商品信息
import requests
from bs4 import BeautifulSoup
import json,re
from config import *
from queue import Queue
import pymysql
import datetime
import threading
import time
from requests.exceptions import ProxyError,SSLError
class alibb(object):
    def __init__(self):               #头文件
        self.header={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
            'cookie':'cookie2=1dd725c23a279711f975f6a6b5158a8f',
            'referer':'https://s.1688.com/selloffer/offer_search.htm?keywords=%B4%B4%BA%E3&n=y&spm=a260k.635.3262836.d102',
            }     
    def Get_url(self,url):                                                 #第一页获取
        try:
            proxyHost = "http-dyn.abuyun.com"
            proxyPort = "9020"                                                   # 代理隧道验证信息
            proxyUser = "H5Y68O84688E39GD"
            proxyPass = "12A2711C8A0448A6"
            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                  "host" : proxyHost,
                  "port" : proxyPort,
                  "user" : proxyUser,
                  "pass" : proxyPass,
                }
            proxies = {
                      "http"  : proxyMeta,
                      "https" : proxyMeta,
               }
            session = requests.Session()
            urls = 'https://login.taobao.com/jump?target=https%3A%2F%2Fcart.1688.com%2Fajax%2FquickCartCount.jsx%3Ftbpm%3D1%26callback%3DjQuery183021917934911062198_1534490932737%26_%3D1534490932990'
            response = session.get(urls)#,proxies=proxies
            a = re.findall('(cookie2=.*?\s)', str(session.cookies))[0]
            self.header['cookie'] = a
            response=requests.get(url,headers=self.header)#,proxies=proxies
            html=re.findall(r'<a tclick.*/a>',response.text)[0]
            return response.text
        except IndexError as e:
            print(e)
            print(response.text)
            with open("1.txt", "a",encoding='utf-8') as f:
                f.write(url)
                f.write('\n..........................................\n')
            url=url
            self.Get_url(url)
        except ProxyError as e:
            print(e)
            url=url
            self.Get_url(url)
        except SSLError as e:
            print(e)
            with open("1.txt", "a",encoding='utf-8') as f:
                f.write(url)
                f.write('\n..........................................\n')
    def Get_Url_list(self,response,m):                                           #获取页面        
        li=[]
        try:
            html=re.findall(r'<a tclick.*/a>',response)[0]
            text = html.replace('\\\"','').replace('\\n','').replace('\\','')
            soup=BeautifulSoup(text,'lxml')       
            for i in soup.find_all("a",attrs={'href':re.compile(r'^https://deta')}):
                li.append(i['href'])
                print(i['href'])
            lis=list(set(li))
            lis.sort(key=li.index)
            db=pymysql.connect(host='bsswaiwang.mysql.rds.aliyuncs.com',port=3306,user= 'sp_data_group',password = '4ydEe7EfrzEH',database='brand')
            cur=db.cursor()
            for i  in lis:
                print(i) 
                sql='INSERT INTO y1688_copy_copy(href) VALUES(%s);'       
                cur.execute(sql, [i])
                db.commit()
        except Exception as e:
            print(e)
            with open("1.txt", "a",encoding='utf-8') as f:
                f.write(m)
                f.write('..........................................\n')
            
    def Get_Goods_inf(self,response,url):                  #获取商品信息
        dict=dic
        soup=BeautifulSoup(response,'lxml')
        dict['itemid']=re.findall(r'\d+', url)[1]          #商品id
        dict['url']=url
        dict['Title']=soup.find('h1',{'class':'d-title'}).text   #商品标题
        dict['Area']=soup.find('meta',{'name':'location'}).get('content')  #商品产地
        dict['shopurl']=soup.find('div',{'class':'base-info'}).a['href']   #店铺链接
        try:
            dict['brand']=soup.find_all('td',{'class':'de-value'})[0].text  #品牌
        except IndexError as e:
            print(e,url)
            dict['brand']=''
        dict['Img']=soup.find('a',{'class':'box-img'})['href']               #商品图片链接
        dict['platform']='1688'
        dict['createtime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #创建时间
        dict['seller']=soup.find('div',{'class':'base-info'}).text.replace('\n','')  #旺旺名
        dict['wangwang']=soup.find('a',{'class':'link name'}).text
        try:                                                                           #获得销量
            sales=soup.find('div',{'class':'mod-detail-dealrecord mod-info'})['data-mod-config']  
            sales=eval(sales)                                        #变为字典
            sale=re.findall(r'\d+',sales['title'])[0]    
            dict['Sales']=sale                                       #销量
        except TypeError as e:                                       #没有销量栏
            print('Type错误',e,'--------',url)             
            dict['Sales']=0                                           #销量为0
        self.GetPrices(soup,dict,url)                                #调用价格获取函数
        print (dict)
    def GetPrices(self,soup,dict,url):                                #获取商品价格信息
        prices=[]
        Model=[]
        try:
            m=soup.find_all('script',{'type':'text/javascript'})[2].text   #寻找价格js
            pattern=re.compile(r'\{.*\}')                                  #正则得到json
            n=re.findall(pattern, m)[1]                                        
            n=json.loads(n)                                                 #将str解析为json
            for k,v in n.items():                                           #获取列表
                Model.append(re.findall(r'\d.*',k)[0])                      #获得商品类型表
                prices.append(v['price'])
            price=[float(i) for i in prices ]
            dict['Price']=min(price),max(price)                        #价格区间
            dict['minprice']=min(price)                                #最低价
            dict['maxprice']=max(price)                                #最高价
            dict['avgprice']=float(sum(price))/len(price)              #获得平均价
            dict['Pricelist']=str(prices)                              #获得价格列表
            dict['Model']=str(Model)                                    #获得商品列表   
        except KeyError as e:                                           #json里面没有找到price
            print ('Key错误:',e,'--------',url)
            try:
                prices=soup.find_all('div',{'class':'d-content'})[2]['data-price'] #
                price=re.findall(r'[0-9]+\.[0-9]+',prices)
                price=[float(i) for i in price ]
                dic['Price']=min(price),max(price)
                dict['minprice']=min(price)
                dict['maxprice']=max(price)
                dict['avgprice']=float(sum(price))/len(price)
                dict['Model']=0
                dict['Pricelist']=0
            except Exception as e:
                print('错误:',e,'................',url)
                dic['Price']=0
                dict['minprice']=0
                dict['maxprice']=0
                dict['avgprice']=0
                dict['Model']=0
                dict['Pricelist']=0
        except IndexError as e:         #未找到
            print('Index错误:',e,'................',url)
            dict['Model']='0'
            try:
                prices=soup.find_all('div',{'class':'d-content'})[2]['data-price'] #
                price=re.findall(r'[0-9]+\.[0-9]+',prices)
                price=[float(i) for i in price ]
                dic['Price']=min(price),max(price)
                dict['minprice']=min(price)
                dict['maxprice']=max(price)
                dict['avgprice']=float(sum(price))/len(price)
                dict['Pricelist']='0'
            except Exception as e:
                print('错误:',e,'................',url)
                dic['Price']=0
                dict['minprice']=0
                dict['maxprice']=0
                dict['avgprice']=0
                dict['Model']=0
                dict['Pricelist']=0 
def Run():
    
    count=2
    for i in range(27):
        for i in url_config:
            url=i.format(count=count)
            print(url)
            response=a.Get_url(url,)
            a.Get_Url_list(response,i)
        count=count+1
#     while True:
#         Link_lis=q.get()
#         print(Link_lis)
#         for i in Link_lis:
#             print(i)
#             response=a.Get_url2(i,ip)
#             a.Get_Goods_inf(response,i)
#         if q.qsize() is 0:
#             print('结束')
#             break
if __name__ == '__main__':
    a=alibb()
    q=Queue()
    Run()
#     db=pymysql.connect(host='bsswaiwang.mysql.rds.aliyuncs.com',port=3306,user= 'sp_data_group',password = '4ydEe7EfrzEH',database='brand')
#     cur=db.cursor()
    
    