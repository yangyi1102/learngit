'''
Created on 2018年8月22日

@author: yangyi
'''
#coding=utf-8
import requests
from bs4 import BeautifulSoup
import pymysql
import re
from config import *
from requests.exceptions import ProxyError,SSLError
import datetime
import json
from queue import Queue
import threading
import time
class Aibb(object):
    def __init__(self):
        self.header={                                                                                          #头
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
            'cookie':'_bl_uid=6ejzXl0w3qb9hwe1U86t9s0iOw86; __sw_newuno_count__=1; cna=yXsCFP09BEoCAXr2Mlu4VsBs; UM_distinctid=1655aa5032184d-012b62c810a4bf-4a531929-1fa400-1655aa50322420; ali_apache_track=c_mid=b2b-2656045053d9683|c_lid=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565|c_ms=1; enc=jjcGkOKVhTnzmhreL4gPlo78E%2B%2BOYYAh6Q6Le3O6%2FRH3r6uiwswv3QNYEdNWwkjGKsrp%2FsAf%2Bu1bHbeNYwqfOQ%3D%3D; JSESSIONID=D0xYcna-3m9aWMw6FehN6rSvi8-KbgHV1R-8v6b1; h_keys="%u77ed%u8896#%u521b%u6052#%u5305%u5305"; ali_apache_tracktmp=c_w_signed=Y; cookie1=BxEzpaMjcJGqaS25VErLMuGHYCe0STzulbkBiFTPKaA%3D; cookie2=30fbf385db75639d7a5a9734fdccb230; cookie17=UU6kVW3yPgjkVg%3D%3D; t=61c1410151486d177c0fac8c802039a5; _tb_token_=e97aa7e8e30b6; sg=53e; csg=23534901; lid=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; LoginUmid=Gd8yVw3ya0nzeN19q%2BXjXAik92VjLhpwXPzlNekM39W89QAyb6jGqQ%3D%3D; unb=2656045053; tbsnid=xygKz0kYkaUt%2FaWlDVuqE4%2B7AcNn4juCxv%2BMykkH02k6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ22hDnGffby3pszN6YlwQMo7S+E5FHt8j3PF14+uXT2tJxKGeQaYEWKtJzy2+t3A6wPrJXMihmNoo6GJelS+XEA7c1wCpR9Fagb+6/PQiIFP7ryqom8qPi7L2p7zT0yM9XfJhb+U4r8QY5uAbnx2sYhm3cbKiABeYLwN3Ua6uzSgLKpScU3GYJldS5fWe06+ydqHNWuXz4GuQGW1Ehi4J2ED/N0ImeVpt+DWvnigpgiwL3nxlldanbuPwIBOCMPnb0="; login=kFeyVBJLQQI%3D; userID=ZWgCch12XgnKgy0TTJ2TUmAupKa5R1smSHpjggX7TfU6sOlEpJKl9g%3D%3D; _nk_=36%2Bq1XABXuMRE6FJ8MUlfzqw6USkkqX2; userIDNum=%2BTIFjQs5R0rZwT72DfDqUA%3D%3D; last_mid=b2b-2656045053d9683; __last_loginid__=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; _cn_slid_=MfQs8Uwu4V; _tmp_ck_0=uS3J%2FTASuVflHmaW3heuOYlzA2HjqfTegBGeVGWV5hS3vJq3hPrMEjowBNioUAP%2FdIDMJAbSY9ogetJs%2B9ALOe5aCIGXipVK8xblasEN%2F3azhrxwsLEUY5KqHsXhRVnKdGKpUECSz4fRkLHr5XSdf7JCPZx5uiWIVQ0Y98iiblwS0xJ3WhNPJDYBwBKMMzMBHA%2B8TEjhtEZoLe0FcKb2fWP79DKHEcv41TMIV9yIH5WqWZWWh3SROkJ0ZMFpdGpH3K80j8%2FP7LUXVSOUgEJa%2F3SQGX6ZZy6jQnY%2BB4imHdJH7UqxgGCR8qrlyLPAH4gwa%2BkIk2KMg7%2BeoeXXN3K%2FDFwznUFpkno8gZOpaNPUNDVKEuR4k9JO5abKaBGcUDmARFCjD%2B%2BvG1dae1m3ui4HWrC8XVcx080N9UU%2BUjs9bdY%2BvA%2FNnOCI%2FFFosPBxr95%2FFrko3LP37pJOyB9gbtjCnRZXhngek6kgTVx88ZVstHFmkHQanXUWuIgG9ZGgMUCx3%2FYs30BE4rwQGBaHK7I31THsnxFY5XGm; _csrf_token=1534985652114; alisw=swIs1200%3D1%7C; ad_prefer="2018/08/23 08:54:20"; _is_show_loginId_change_block_=b2b-2656045053d9683_false; _show_force_unbind_div_=b2b-2656045053d9683_false; _show_sys_unbind_div_=b2b-2656045053d9683_false; _show_user_unbind_div_=b2b-2656045053d9683_false; __rn_alert__=false; alicnweb=touch_tb_at%3D1534984779264%7Clastlogonid%3D%25E4%25B8%2580%25E6%258A%25B9%25E9%2598%25B3%25E5%2585%258945425565%7ChomeIdttS%3D22288243912695405814892564889427358812%7ChomeIdttSAction%3Dtrue; ali_ab=122.246.50.91.1534828723400.5; isg=BPn5gC6FhpZCbloHBfJ5vwCBHGUTruFkbfICJRsu8iCOohk0Y1UciVj8IObxAYXw',
            'referer':'https://s.1688.com/selloffer/offer_search.htm?keywords=%B4%B4%BA%E3&n=y&spm=a260k.635.3262836.d102',
            }
    def Get_FirstPage_link(self):            #搜索页
        count=0                                           #5次失败返回
        while True:
            try:
                lis=[]                                                            #搜索页             
                first_url='https://s.1688.com/selloffer/offer_search.htm?keywords=%B4%B4%BA%E3&n=y&spm=a260k.635.3262836.d102&beginPage=1&offset=4&filterP4pIds=42313419257,44717538257,44760313364'                      #搜索页
              #  url='https://s.1688.com/selloffer/offer_search.htm?keywords=%B0%FC%B0%FC&n=y&mastheadtype=&from=industrySearch&industryFlag=xiebaopeishi'
                response=requests.get(first_url,headers=self.header)
                soup=BeautifulSoup(response.text,'lxml')
                li=soup.find_all('a',{'data-spm':'of0'})                       #获取首页链接
                for i in li[3::]:                                                                 #前三个为广告
                    lis.append(i['href'])                              #f
                lis=list(set(lis))
                print(len(lis))
                return lis
            except Exception as e:
                count=count+1
                print(e)
                if count>=5:
                    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("pagelink.txt", "a",encoding='utf-8') as f:
                        f.write(t)
                        f.write("\n" )
                        f.write(first_url)
                        f.write("\n" )
                    return False
                        
    def Get_first_Page(self,url):                                                    #第一页获取
        count=0
        while True:
            try:
                proxyHost = "http-dyn.abuyun.com"
                proxyPort = "9020"                                                   # 代理隧道验证信息
                proxyUser = "HGQZ87732P91S43D"
                proxyPass = "A9FEAB063CED2968"
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
                session = requests.Session()                             #获得cookie2
                urls = 'https://login.taobao.com/jump?target=https%3A%2F%2Fcart.1688.com%2Fajax%2FquickCartCount.jsx%3Ftbpm%3D1%26callback%3DjQuery183021917934911062198_1534490932737%26_%3D1534490932990'
                cookieget = session.get(urls,proxies=proxies)
                a = re.findall('(cookie2=.*?\s)', str(session.cookies))[0]
                self.header['cookie'] = a
                response1=requests.get(url,headers=self.header)     #获得第一页
                return response1.text
            except ProxyError  as e:
                count=count+1
                time.sleep(5)
                if count>=5:
                    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("pagelink.txt", "a",encoding='utf-8') as f:
                        f.write(t)
                        f.write("\n" )
                        f.write(url)
                        f.write("\n" )
                    return False
            except  IndexError as e:
                count=count+1
                if count>=5:
                    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("pagelink.txt", "a",encoding='utf-8') as f:
                        f.write(t)
                        f.write("\n" )
                        f.write(url)
                        f.write("\n" )
                    return False              
    def Get_page(self,url):                                              
        try:
            proxyHost = "http-dyn.abuyun.com"
            proxyPort = "9020"                                                   # 代理隧道验证信息
            proxyUser = "HGQZ87732P91S43D"
            proxyPass = "A9FEAB063CED2968"
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
            cookget = session.get(urls,proxies=proxies)    #
            a = re.findall('(cookie2=.*?\s)', str(session.cookies))[0]
            self.header['cookie'] = a
            response=requests.get(url,headers=self.header,proxies=proxies)
            #html=re.findall(r'<a tclick.*/a>',response.text)[0]
            return response.text
        except ProxyError as e:
            print(e)
            url=url
            self.Get_page(url)
        except SSLError as e:
            print(e)
            with open("2.txt", "a",encoding='utf-8') as f:
                f.write(url)
                f.write('\n..........................................\n')
        except  IndexError as e:
            self.Get_page(url)
    def Get_Page_list(self,response,url):                                           #获取页面        
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
            return lis
        except Exception as e:
            print(e)
            with open("2.txt", "a",encoding='utf-8') as f:
                t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(url)
                f.write('\n')
            return li
    def GetResponse(self,url):
        count=0
        while True:
            try:
                response=requests.get(url,headers=self.header)   
                return response.text
            except Exception as e:
                print(e)
            self.GetResponse(url)
    def Get_Goods_inf(self,response,url):                  #获取商品信息
        dict=dic
        try:
            soup=BeautifulSoup(response,'lxml')
        except Exception as e:
            pass
        dict['itemid']=re.findall(r'\d+', url)[1]                #商品id
        dict['url']=url
        try:
            dict['Title']=soup.find('h1',{'class':'d-title'}).text   #商品标题
        except Exception as e:
            dict['Title']=''
        try:
            dict['Area']=soup.find('meta',{'name':'location'}).get('content')  #商品产地
        except Exception as e:
            dict['Area']=''
        try:
            dict['shopurl']=soup.find('div',{'class':'base-info'}).a['href']   #店铺链接
        except Exception as e:
            dict['shopurl']=''
        try:
            dict['brand']=soup.find_all('td',{'class':'de-value'})[0].text  #品牌
        except IndexError as e:
            print(e,url)
            dict['brand']=''
        try:
            dict['Img']=soup.find('a',{'class':'box-img'})['href']               #商品图片链接
        except Exception as e:
            dict['Img']=''
        dict['platform']='1688'
        dict['createtime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #创建时间
        try:
            dict['seller']=soup.find('div',{'class':'base-info'}).text.replace('\n','')  #旺旺名
        except Exception as e:
            dict['seller']=''
        try:
            dict['wangwang']=soup.find('a',{'class':'link name'}).text
        except Exception as e:
            dict['wangwang']=''
        try:                                                                           #获得销量
            sales=soup.find('div',{'class':'mod-detail-dealrecord mod-info'})['data-mod-config']  
            sales=eval(sales)                                        #变为字典
            sale=re.findall(r'\d+',sales['title'])[0]    
            dict['Sales']=sale                                       #销量
        except TypeError as e:                                       #没有销量栏         
            dict['Sales']=0                                           #销量为0
        self.GetPrices(soup,dict,url)                                #调用价格获取函数
        return dict
    def GetPrices(self,soup,dict,url):                                #获取商品价格信息
        prices=[]
        Model=[]
        try:
            m=soup.find_all('script',{'type':'text/javascript'})[2].text   #寻找价格js
            pattern=re.compile(r'\{.*\}')                                       #正则得到json
            n=re.findall(pattern, m)[1]                                        
            n=json.loads(n)                                                          #将str解析为json
            for k,v in n.items():                                                      #获取列表
                Model.append(re.findall(r'\d.*',k)[0])                     #获得商品类型表
                prices.append(v['price'])
            price=[float(i) for i in prices ]
            dict['Price']=min(price),max(price)                        #价格区间
            dict['minprice']=min(price)                                #最低价
            dict['maxprice']=max(price)                                #最高价
            dict['avgprice']=float(sum(price))/len(price)     #获得平均价
            dict['Pricelist']=str(prices)                                   #获得价格列表
            dict['Model']=str(Model)                                    #获得商品列表   
        except KeyError as e:                                              #json里面没有找到price
            try:
                prices=soup.find_all('div',{'class':'d-content'})[2]['data-price']    
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
           # print('Index错误:',e,'................',url)
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
                dic['Price']=0
                dict['minprice']=0
                dict['maxprice']=0
                dict['avgprice']=0
                dict['Model']=0
                dict['Pricelist']=0
    def Save(self,):   
        db=pymysql.connect(host='bsswaiwang.mysql.rds.aliyuncs.com',port=3306,user= 'sp_data_group',password = '4ydEe7EfrzEH',database='brand')
        cur=db.cursor()
        while True:
            dict=q.get()
            print(dict)
            if dict['shopurl'] is '':
                with open("2.txt", "a",encoding='utf-8') as f:
                    f.write(dict['url'])
                    f.write('\n')
            if dict['wangwang'] is '':
                with open("2.txt", "a",encoding='utf-8') as f:
                    f.write(dict['url'])
                    f.write('\n')
            else:  
                sql='INSERT INTO yangyi1688_copy_uc_copy(Area,Title,url,Img,wangwang,seller,Price,Pricelist,Sales,Model,brand,platform,itemid,maxprice,minprice,avgprice,createtime,shopurl) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' # Title,url,Img,wangwang,seller,Price,Pricelist,Sales,Model) '#,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                cur.execute(sql,[str(dict['Area']),str(dict['Title']),str(dict['url']),str(dict['Img']),str(dict['wangwang']),str(dict['seller']),str(dict['Price']),str(dict['Pricelist']),str(dict['Sales']),str(dict['Model']),dict['brand'],dict['platform'],
                               dict['itemid'],dict['maxprice'],dict['minprice'],dict['avgprice'],dict['createtime'],dict['shopurl']])
                db.commit()

def Run_firstPage():
    count=5
    lis=A.Get_FirstPage_link(count)
    if lis is not False:
        for i in lis:
            text=A.GetResponse(i)
            inf=A.Get_Goods_inf(text,i)
            q.put(inf)
    for i in url1:
        response=A.Get_first_Page(i)
        lis=A.Get_Page_list(response,i)
        while len(lis) is not 0:
            i=lis.pop()
            text=A.GetResponse(i)
            inf=A.Get_Goods_inf(text,i)
            q.put(inf)
         
def Run(count):
    for i in url_config:
        url=i.format(count=count)
        response=A.Get_page(url)
        lis=A.Get_Page_list(response, url)
        while len(lis) is not 0:
            i=lis.pop()
            text=A.GetResponse(i)
            inf=A.Get_Goods_inf(text,i)
            q.put(inf)
      
if __name__ == '__main__':
    count=0
    A=Aibb()
    tpool=[]
    q=Queue()
    tpool.append(threading.Thread(target=Run_firstPage))
    tpool.append(threading.Thread(target=A.Save))
    count=2
    for i in range(26):
        t=threading.Thread(target=Run,args=(count,))
        tpool.append(t)
        count=count+i 
    for i in tpool:
        time.sleep(40)
        i.start()  
    while True:
        time.sleep(100)
        for i in tpool:
            if i.isAlive() is False:
                print("线程:"+i.getName()+"结束")
                   
        
        
        
        