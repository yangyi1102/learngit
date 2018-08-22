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
        self.header={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
            'cookie':'cna=yXsCFP09BEoCAXr2Mlu4VsBs; UM_distinctid=1655aa5032184d-012b62c810a4bf-4a531929-1fa400-1655aa50322420; ali_apache_track=c_mid=b2b-2656045053d9683|c_lid=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565|c_ms=1; enc=jjcGkOKVhTnzmhreL4gPlo78E%2B%2BOYYAh6Q6Le3O6%2FRH3r6uiwswv3QNYEdNWwkjGKsrp%2FsAf%2Bu1bHbeNYwqfOQ%3D%3D; h_keys="%u5305%u5305#%u521b%u6052"; last_mid=b2b-2656045053d9683; __last_loginid__=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; _cn_slid_=MfQs8Uwu4V; _is_show_loginId_change_block_=b2b-2656045053d9683_false; _show_force_unbind_div_=b2b-2656045053d9683_false; _show_sys_unbind_div_=b2b-2656045053d9683_false; _show_user_unbind_div_=b2b-2656045053d9683_false; ad_prefer="2018/08/22 14:01:06"; __rn_alert__=false; _csrf_token=1534924321907; JSESSIONID=C0xYNle-bk9arZPb6QPgVd4FT9-MD2CR1R-KFGX1; cookie2=3c73420d17b8dec35238e96651b03075; t=61c1410151486d177c0fac8c802039a5; _tb_token_=e3155e754f668; lid=%E4%B8%80%E6%8A%B9%E9%98%B3%E5%85%8945425565; __cn_logon__=false; _tmp_ck_0=hFAQOkhMcTe8rE4Y5taxBfyEISf5Q8GIPgqrb93nWLXMFkrxMI3eb8Uvw7zjKj1Fl1RF%2BNTCRy1INSPE2y96WRqKHZ9w56Oma4lZz1reCdIfxM91F91fzOqNh4cn6Kbk7nRgniZR%2B%2FXM8FwpbrQ0gXxpc0%2FsOwYkPufbxo%2BG9h4%2BYPJcKubb8fiApQXxVmFXTFJsHrTyQfHEEdgUn4PIipvasJF8%2BqDQvE5N1LZt2yqNsW5RwagIA%2Flyzez8uq3l33nJ1XkFpRzkFaIB5OBr3zrtZRBZGdVjDcgpUuLB%2BTxAwYM6yzPvVLyg4H5FJcNo6wHZDn5xxSrJuUe7c5NvIFEmuFbG9OE1pOUSr2WRZAfKgPxuVzdS1DwnQBg8gKhtQr3xnuO7zsg%3D; alicnweb=touch_tb_at%3D1534924324227%7Clastlogonid%3D%25E4%25B8%2580%25E6%258A%25B9%25E9%2598%25B3%25E5%2585%258945425565%7ChomeIdttS%3D22288243912695405814892564889427358812%7ChomeIdttSAction%3Dtrue; ali_ab=122.246.50.91.1534828723400.5; isg=BJKST_XCHVDuIWEqAndyWm8M91i0C5rhcq-ZCFzrtsUwbzJpRTFyTZGl24t2ew7V',
            'referer':'https://s.1688.com/selloffer/offer_search.htm?keywords=%B4%B4%BA%E3&n=y&spm=a260k.635.3262836.d102',
            }
    def Get_FirstPage_link(self):
        lis=[]                                   #第一页获取
        #url='https://s.1688.com/selloffer/offer_search.htm?keywords=%B4%B4%BA%E3&n=y&spm=a260k.635.3262836.d102&beginPage=1&offset=4&filterP4pIds=42313419257,44717538257,44760313364'                      #搜索页
        url='https://s.1688.com/selloffer/offer_search.htm?keywords=%B0%FC%B0%FC&n=y&mastheadtype=&from=industrySearch&industryFlag=xiebaopeishi'
        response=requests.get(url,headers=self.header)
        soup=BeautifulSoup(response.text,'lxml')
        li=soup.find_all('a',{'data-spm':'of0'})  #获取首页链接
        for i in li[3::]:                      #前三个为广告
            lis.append(i['href'])
        lis=list(set(lis))
        print(len(lis))
        return lis
    def Get_first_Page(self,url):
        try:                     
            response1=requests.get(url,headers=self.header)
            return response1.text
        except Exception as e:
            print(e)
            with open("1.txt", "a",encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            url=url
            self.Get_first_Page(url)
    def Get_page(self,url):                                              
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
           # urls = 'https://login.taobao.com/jump?target=https%3A%2F%2Fcart.1688.com%2Fajax%2FquickCartCount.jsx%3Ftbpm%3D1%26callback%3DjQuery183021917934911062198_1534490932737%26_%3D1534490932990'
           # response = session.get(urls)#,proxies=proxies
           #  a = re.findall('(cookie2=.*?\s)', str(session.cookies))[0]
           # self.header['cookie'] = a
            response=requests.get(url,headers=self.header)#,proxies=proxies
            #html=re.findall(r'<a tclick.*/a>',response.text)[0]
            return response.text
        except Exception as e:
            print(e)
            with open("1.txt", "a",encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            url=url
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
            with open("1.txt", "a",encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            return li
    def GetResponse(self,url):
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
#             if dict['shopurl'] is '':
#                 with open("1.txt", "a",encoding='utf-8') as f:
#                     f.write(dict['url'])
#                     f.write('\n')
#             if dict['wangwang'] is '':
#                 with open("1.txt", "a",encoding='utf-8') as f:
#                     f.write(dict['url'])
#                     f.write('\n')
#             else:  
#                 sql='INSERT INTO yangyi1688_copy_uc_copy(Area,Title,url,Img,wangwang,seller,Price,Pricelist,Sales,Model,brand,platform,itemid,maxprice,minprice,avgprice,createtime,shopurl) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' # Title,url,Img,wangwang,seller,Price,Pricelist,Sales,Model) '#,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
#                 cur.execute(sql,[str(dict['Area']),str(dict['Title']),str(dict['url']),str(dict['Img']),str(dict['wangwang']),str(dict['seller']),str(dict['Price']),str(dict['Pricelist']),str(dict['Sales']),str(dict['Model']),dict['brand'],dict['platform'],
#                               dict['itemid'],dict['maxprice'],dict['minprice'],dict['avgprice'],dict['createtime'],dict['shopurl']])
#                 db.commit()

def Run_firstPage():
    lis=A.Get_FirstPage_link()
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
            print(inf)
        #A.Save(inf)
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
    for i in range(3):
        t=threading.Thread(target=Run,args=(count,))
        tpool.append(t)
        count=count+1 
    for i in tpool:
        i.start()  
    while True:
        time.sleep(100)
        for i in tpool:
            if i.isAlive() is False:
                print("线程:"+i.getName()+"结束")
                   
        
        
        
        