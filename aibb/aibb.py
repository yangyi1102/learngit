'''
Created on 2018年8月6日

@author: yangyi
'''
#coding=utf-8
#获取1688平台商品信息
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as PQ
import json,re
from config import *
from queue import Queue
import pymysql
import datetime
import threading
class alibb(object):
    def __init__(self):               #头文件
        self.header={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36',
            'template_path': 'mNJ82OKsx5s2joeKgTh0i1G0U4Q2ouVLv8Ws7eQmXS2C7sJaeRYoU++E41/G5bjA',
            'cookie': '__sw_newuno_count__=1; UM_distinctid=1651dbce6962a4-046e9a983493c-7d12364c-144000-1651dbce697c81; cna=BOXyE30SEV0CAXr2Mzb14DSP; ali_ab=122.246.51.54.1533802244251.5; JSESSIONID=9L78A7N92-6m9al2RFpcXT3vRl09-eIuFD0R-op0V; cookie2=1f5e976a25f11a22af4f171413ad8a77; t=b609b5fdb4d9e82cc4653300aa958216; _tb_token_=f87b1375b31ee; cookie1=VTrgqrtmSEkb1vW9bLIn%2F%2BnNw%2BKBZf5Ur5Noef3xlUQ%3D; cookie17=UNX57RsrJgaEtQ%3D%3D; sg=469; csg=3b0a5363; lid=weiteniu4; __cn_logon__=true; __cn_logon_id__=weiteniu4; ali_apache_track=c_mid=b2b-3527265906b3cc4|c_lid=weiteniu4|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=%2BrCFOTWmtzucC%2FE3zxiOV1OGGXDrW0klxXUL9cXapyZqJGrd38HGVQ%3D%3D; unb=3527265906; tbsnid=WeSlDCFaf17nfBs0kCjPuNt4G10Mq7t5uL42H6KzfUE6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ3pVcpj1FDJbylKVPNhjM+1HZotR6rW4IL9ihNX6MHJO2LVMC4AHHiVloe6fXT3DVkXtem4OH0fJaXfhJ84mf8MVnbUa2TTrHIqszRXV4cCcZ1nu6KaYYMvq9FvV62uwyIC12H8rsCXE2nH1bfYTqkxEoaC2T3pgjzVPY65X0hLNDWNPScfy3veOEagmBNKedDgTHaojf7v2visbfS90ud9JjWsgHn+xLfusOferB6bvZ7ZeZj18BXU12c4aJgNgZo="; login=kFeyVBJLQQI%3D; userID=FRXpE4wIc%2FDm%2BQ33NaABoQlk57C%2FZn5J6LyWy9BGNDk6sOlEpJKl9g%3D%3D; _nk_=%2B01ddgv%2FKXgDBPJBu4sTUQ%3D%3D; userIDNum=E4BejoMSHJPTREwxOZGXtg%3D%3D; last_mid=b2b-3527265906b3cc4; __last_loginid__=weiteniu4; _cn_slid_=q6ihNvlWbb; _tmp_ck_0=ekwXrK5b5k3NtG%2BeBFSpxKovo6gROS3KavhmXHsMr53Lswj64nct%2FCidXSaIfqZeRbqHPxoVCICeoyLgtLCpah9KOXtyx6g3WZ4t1ALtMJE0gt2%2BuGNh3KP8bwpDzvZa57%2B7%2BycD8w3BxlOUAFYLuMkACYSyeVUbGaUNltNfT7aoQgBhbXFYf3EnbL9ogpXcg07qI%2FmdP4S6uT14dW2%2BCLrhW7GYFUOJjN1Q40bgFP8pksy374hWExxxMbkJ%2Bojjrj01vO6APuZS8EnPciBFF41Fk0gRdTETjHfyubOPuKM9ctCO%2FZsNsEUdShCx7TJMS3Hh%2FJyTI8Cm33PWc3HMq2Z2vTaUBYXm%2B6rHue5xgTDqnAhn1bg2x4eUJCBcK%2FLY17gDZmm4jYbSof6Q6SkxDBSsRyfT7agxRcD5oOlB2uY7K1XGlhJ%2FUG51TLud2SVOseervT8uKzpL8%2BppLJz0ed6KaL%2Fn90kiTOxpJqYqtBC1o5HmAVqchDBzd8QqeGTwvqwoTVKMBrVACFQ36hpzyg%3D%3D; _csrf_token=1533802274542; h_keys="%u8863%u670d"; alisw=swIs1200%3D1%7C; _is_show_loginId_change_block_=b2b-3527265906b3cc4_false; _show_force_unbind_div_=b2b-3527265906b3cc4_false; _show_sys_unbind_div_=b2b-3527265906b3cc4_false; _show_user_unbind_div_=b2b-3527265906b3cc4_false; __rn_alert__=false; alicnweb=homeIdttS%3D02852562865789933537399413842419099810%7ChomeIdttSAction%3Dtrue%7Ctouch_tb_at%3D1533802253693%7Clastlogonid%3Dweiteniu4%7Cshow_inter_tips%3Dfalse; ad_prefer="2018/08/09 16:54:08"; isg=BFtbdMdZhI5YPfjIkyn5TUVq6r8FmGPuBq5X302akNqZLHsO1QK9gr3uwswHaMcq',
            'referer':'https://www.1688.com/?spm=b26110380.sw1688.2.1.3f734220qNnN6M',
            }
    def Get_first_Page(self):       #第一页获取
        pass
    def Get_Url_list(self):         #获取页面        
        count=2
        for i in range(10): 
            li=[]
            litext=[]
            for i in Url_config:
                url=i.format(count=count)
                response=requests.get(url,headers=self.header)
                print(response.text)
                html=re.findall(r'<a tclick.*/a>',response.text)[0]
                text = html.replace('\\\"','').replace('\\n','').replace('\\','')
                soup=BeautifulSoup(text,'lxml')       
                for i in soup.find_all("a",attrs={'href':re.compile(r'^https://deta')}):
                    li.append(i['href'])
                    litext.append(i.text)
            lis=list(set(li))
            lis.sort(key=li.index)
            q.put(lis)
            print(count)
            count=count+1         #得到urllist表
#     def Save_href(self):
#         while True:
#             if q.qsize() is not 0:
#                 url=q.get()
#                 sql='INSERT INTO y1688(href) VALUES(%s)'       
#                 cur.execute(sql, [url])
#                 db.commit()
#             else:
#                 break
    def Get_html(self):
       pass
    def Get_Goods_inf(self):   #获取商品信息
        num=1
        while True:
                Link_lis=q.get()
                print(Link_lis)
                for i in Link_lis:
                    dict=dic
                    url=i
                    print(num,url)
                    response=requests.get(url,headers=self.header)
                    soup=BeautifulSoup(response.text,'lxml')
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
                    num=num+1
                if q.qsize() is 0:
                    print('结束')
                    break
    def GetPrices(self,soup,dict,url):         #获取商品价格信息
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
    a.Get_Url_list()
    #print(q.qsize())
    a.Get_Goods_inf() 
if __name__ == '__main__':
    a=alibb()
    q=Queue()
   # qtext=Queue()
    Run()
    
    