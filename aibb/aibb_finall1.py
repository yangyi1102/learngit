'''
Created on 2018年8月24日

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
            'cookie':'cna=yXsCFP09BEoCAXr2Mlu4VsBs; UM_distinctid=1655aa5032184d-012b62c810a4bf-4a531929-1fa400-1655aa50322420; ali_apache_track=c_mid=b2b-2656045053d9683|c_lid=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565|c_ms=1; enc=jjcGkOKVhTnzmhreL4gPlo78E%2B%2BOYYAh6Q6Le3O6%2FRH3r6uiwswv3QNYEdNWwkjGKsrp%2FsAf%2Bu1bHbeNYwqfOQ%3D%3D; JSESSIONID=C0xYXCe-7l9a34sDbwRdFBCJ7D-dsAhc1R-wuNm1; cookie1=BxEzpaMjcJGqaS25VErLMuGHYCe0STzulbkBiFTPKaA%3D; cookie2=3c7886c5400f81ded1374267d0a65b21; cookie17=UU6kVW3yPgjkVg%3D%3D; t=61c1410151486d177c0fac8c802039a5; _tb_token_=5e63e3646e585; sg=53e; csg=68a404f6; lid=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; __cn_logon__=true; __cn_logon_id__=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=Gd8yVw3ya0nzeN19q%2BXjXAik92VjLhpwXPzlNekM39W89QAyb6jGqQ%3D%3D; unb=2656045053; tbsnid=YZlG6pZr%2F020MH%2FN1qjhrqUcxo7cvrJraUDU%2FT2%2BIN06sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ22hDnGffby3pszN6YlwQMo7S+E5FHt8j3PF14+uXT2tJxKGeQaYEWKtJzy2+t3A6wPrJXMihmNoo6GJelS+XEA7c1wCpR9Fagb+6/PQiIFP7ryqom8qPi7L2p7zT0yM9XfJhb+U4r8QY5uAbnx2sYhm3cbKiABeYLwN3Ua6uzSgLKpScU3GYJldS5fWe06+ydqHNWuXz4GuQGW1Ehi4J2ED/N0ImeVpt+DWvnigpgiwKheTiGm6la5GozvQmGGmaI="; login=kFeyVBJLQQI%3D; userID=ZWgCch12XgnKgy0TTJ2TUmAupKa5R1smSHpjggX7TfU6sOlEpJKl9g%3D%3D; _nk_=36%2Bq1XABXuMRE6FJ8MUlfzqw6USkkqX2; userIDNum=%2BTIFjQs5R0rZwT72DfDqUA%3D%3D; last_mid=b2b-2656045053d9683; __last_loginid__=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; _cn_slid_=MfQs8Uwu4V; _tmp_ck_0=HYP1z9lZIkj9ydSzpplaZwcH8KTR0vMDYNpjReanNS9ETZmEApgsMY2eIDxr3EJsrAF5tq6Vz3IrAbwqz06dfdU7lKKKdCu%2FHZIysSkNA4cPpxZWu26lLxifOn7eyltdI6BkFlh01lRq%2Br3xPYhYgvKVQqn0HVwBY6K4vTErZ1W6hc%2Fq0tEa2rkVnmtpEjuf60uG9GhfKetFacZ3Y4xk6S7axpNPMNaRjR%2BuQxGu8qZqLsF2yaiKrxmrF6Dk8wL4yXi%2FTvUaG%2BpaVhi2XWIAMs6mK9LZSBKfZiBR206ZG02hKmjAAQgQ05UdTBVdEX%2FACoFuLfjCC6tlCJodC3VOuZ6ZwcFSnIKHn3R3xOpLfDfC%2FIAuR9trPT307vC8KSvsTAl4tsx22IqA7Xf8BhJZ0%2BVR0XNJH003IflRS9eGZ5FUF11Wm6c5gtl6PIagD8QiG8RsC%2FPcXl%2F7fhOQ2agvhstH%2F0UVFDLbn4FCHw9QlHuOUSgmdy9E8MS%2FWOkjmZy%2Bu452CkifUvu9vMTdWGQKoA%3D%3D; _csrf_token=1535094302119; _is_show_loginId_change_block_=b2b-2656045053d9683_false; _show_force_unbind_div_=b2b-2656045053d9683_false; _show_sys_unbind_div_=b2b-2656045053d9683_false; _show_user_unbind_div_=b2b-2656045053d9683_false; h_keys="%u539f%u521b%u7537%u88c5#%u77ed%u8896#%u521b%u6052#%u5305%u5305"; JSESSIONID=ugslz1lnq42beuo4y5jd8ooa; ad_prefer="2018/08/24 15:23:37"; __rn_alert__=false; ali_ab=122.246.50.91.1534828723400.5; alicnweb=touch_tb_at%3D1535094285187%7Clastlogonid%3D%25E4%25B8%2580%25E6%258A%25B9%25E9%2598%25B3%25E5%2585%258945425565%7ChomeIdttS%3D22288243912695405814892564889427358812%7ChomeIdttSAction%3Dtrue; isg=BGNjVRpAPDWTYPAFC9wzHSbX5qfN8PtGi-Qop5XAv0I51IP2HCiH6kEqyuT_kE-S',
            'referer':'https://s.1688.com/selloffer/offer_search.htm?keywords=%B4%B4%BA%E3&n=y&spm=a260k.635.3262836.d102',
            }
    def Get_First_Page(self):                   #搜索页
        count=0                                           #5次失败返回
        while True:
            try:
                lis=[]                                                            #搜索页             
                first_url=search_url          #搜索页
                response=requests.get(first_url,headers=self.header)
                soup=BeautifulSoup(response.text,'lxml')
                li=soup.find_all('a',{'data-spm':'of0'})                       #获取首页链接
                for i in li[3::]:                                                                 #前三个为广告
                    lis.append(i['href'])                                                   #f
                lis=list(set(lis))
                print(len(lis))
                return lis
            except Exception as e:
                count=count+1
                if count>=5: 
                    print(e)
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
#                 proxyHost = "http-dyn.abuyun.com"
#                 proxyPort = "9020"                                                   # 隧道验证信息
#                 proxyUser = "HGQZ87732P91S43D"
#                 proxyPass = "A9FEAB063CED2968"
#                 proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#                       "host" : proxyHost,
#                       "port" : proxyPort,
#                       "user" : proxyUser,
#                       "pass" : proxyPass,
#                     }
#                 proxies = {
#                           "http"  : proxyMeta,
#                           "https" : proxyMeta,
#                    }
#                 session = requests.Session()                             #获得cookie2
#                 cookie_url = 'https://login.taobao.com/jump?target=https%3A%2F%2Fcart.1688.com%2Fajax%2FquickCartCount.jsx%3Ftbpm%3D1%26callback%3DjQuery183021917934911062198_1534490932737%26_%3D1534490932990'
#                 session.get(cookie_url,proxies=proxies)
#                 self.header['cookie'] = re.findall('(cookie2=.*?\s)', str(session.cookies))[0]
                response=requests.get(url,headers=self.header)     #获得第一页
                return response.text
            except ProxyError  as e:
                count=count+1
                time.sleep(10)
                if count>=5:
                    print(e)
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
                    print(e)
                    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("pagelink.txt", "a",encoding='utf-8') as f:
                        f.write(t)
                        f.write("\n" )
                        f.write(url)
                        f.write("\n" )
                    return False              
    def Get_page(self,url):
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
                session = requests.Session()
                urls = 'https://login.taobao.com/jump?target=https%3A%2F%2Fcart.1688.com%2Fajax%2FquickCartCount.jsx%3Ftbpm%3D1%26callback%3DjQuery183021917934911062198_1534490932737%26_%3D1534490932990'
                session.get(urls,proxies=proxies)    #
                cookie2 = re.findall('(cookie2=.*?\s)', str(session.cookies))[0]
                self.header['cookie'] = cookie2
                response=requests.get(url,headers=self.header,proxies=proxies)#
                #html=re.findall(r'<a tclick.*/a>',response.text)[0]
                return response.text
            except ProxyError as e:
                count=count+1
                if count>=5:
                    print(e)
                    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("pagelink.txt", "a",encoding='utf-8') as f:
                        f.write(t)
                        f.write("\n" )
                        f.write(url)
                        f.write("\n" )
                    return False   
            except SSLError as e:
                count=count+1
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
            t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("pagelink.txt", "a",encoding='utf-8') as f:
                f.write(t)
                f.write("\n" )
                f.write(url)
                f.write("\n" )
            return False
    def GetResponse(self,url):
        count=0
        while True:
            try:
                response=requests.get(url,headers=self.header)               #获得详情
                return response.text
            except Exception as e:
                print(e)
                count=count+1
                t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if count>=5:
                    with open("1.txt", "a",encoding='utf-8') as f:
                        f.write(t)
                        f.write("\n" )
                        f.write(url)
                        f.write("\n" )
                    return False    
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
class SpiderMan(object):
    def __init__(self):
        self.aibb=Aibb()
        self.tpool=[]
        self.q=Queue()
    def Run_first_Page(self):
        lis=self.aibb.Get_First_Page()
        if lis is not False:
            for i in lis:
                text=self.aibb.GetResponse(i)
                if text is not False:
                    inf=self.aibb.Get_Goods_inf(text,i)
                    self.q.put(inf)
        for i in fis_url:
            response=self.aibb.Get_first_Page(i)
            if response is False:
                lis=self.aibb.Get_Page_list(response,i)
                while len(lis) is not 0:
                    i=lis.pop()
                    text=self.aibb.GetResponse(i)
                    if text is not False:
                        inf=self.aibb.Get_Goods_inf(text,i)
                        self.q.put(inf)
    def Run(self,count):
        for i in url_config:
            url=i.format(count=count)
            response=self.aibb.Get_page(url)
            lis=self.aibb.Get_Page_list(response, url)
            if lis is not False:
                while len(lis) is not 0:
                    i=lis.pop()
                    text=self.aibb.GetResponse(i)
                    if text is not False:
                        inf=self.aibb.Get_Goods_inf(text,i)
                        self.q.put(inf)
    def Save_Inf(self):
        db=pymysql.connect(host='bsswaiwang.mysql.rds.aliyuncs.com',port=3306,user= 'sp_data_group',password = '4ydEe7EfrzEH',database='brand')
        cur=db.cursor()
        while True:
            dict=self.q.get()
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
def Main():
    spiderman=SpiderMan()
    tpool=[]
    tpool.append(threading.Thread(target=spiderman.Run_first_Page))
    tpool.append(threading.Thread(target=spiderman.Save_Inf))
    count=2
    for i in range(20):
        t=threading.Thread(target=spiderman.Run,args=(count,))
        tpool.append(t)
        print(count)
        count=count+1
    tpools=[tpool[i:i+3] for i in range(0,len(tpool),3)]                         #列表切片
    for tlis in tpools:
        time.sleep(20)
        for j in tlis:
            j.start()      
    while True:
        time.sleep(100)
        for i in tpool:
            if i.isAlive() is False:
                print("线程:"+i.getName()+"结束")
        
if __name__ == '__main__':
    Main()
                
                