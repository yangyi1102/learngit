'''
Created on 2018年8月2日

@author: yangyi
'''
#coding=utf-8
import requests
import time,json,random
from config import *
import pymysql
class GuangZhou(object):
    def GetCompanyList(self,url):                                                #获取公司列表
        response = requests.post(POST,headers = headers,data = url,timeout = 50)
        list = response.json()                                                              #得到json列表
        return list['data']
    def GetCompanyinf(self,text):
        for company in text:
            for elem in company['fieldInfoDTO']:
                if elem['filedName'] == '许可ID':
                    data='permitId='+elem['filedValue']
                    response = requests.post(getPermitOverview, headers=headers, data=data,timeout = 50)
                    overview = response.json()
                    self.GetCompanyDic(overview)
    def GetCompanyDic(self,overview):
        str1=overview['tableInfoDTO']['fieldInfoDTO']
        dic={}
        for i in str1:
            key=i['filedName']
            value=i['filedValue']
            dic[key]=value
        print(dic)
        self.Save(str(dic))
    def Save(self,dic):
        
        db=pymysql.connect(host='bsswaiwang.mysql.rds.aliyuncs.com',port=3306,user= 'sp_data_group',password = '4ydEe7EfrzEH',database='brand')
        cur=db.cursor()
        sql='INSERT INTO Guangdong(dic,city) VALUES(%s,%s)'       
        cur.execute(sql, [dic,'深圳'])
        db.commit()
        print('已提交到数据库')       
if __name__ == '__main__':
    g=GuangZhou()
    count=539
    for i in range(24575):
        with open("深圳.txt","a") as f:
            f.write(str(count))
            #limit=10&page=1&keywords=&permitType=SP&areaCode=440300&permitState=%E6%9C%AA%E8%BF%87%E6%9C%9F&permitLabel=&conditionCode1=&conditionValue1=&conditionCode2=&conditionValue2=&conditionCode3=&conditionValue3=&directlyUnder=false
            #limit=10&page=1&keywords=&permitType=SP&areaCode=440000&permitState=%E6%9C%AA%E8%BF%87%E6%9C%9F&permitLabel=&conditionCode1=&conditionValue1=&conditionCode2=&conditionValue2=&conditionCode3=&conditionValue3=
        url='limit=10&page={count}&keywords=&permitType=SP&areaCode=440300&permitState=%E6%9C%AA%E8%BF%87%E6%9C%9F&permitLabel=&conditionCode1=&conditionValue1=&conditionCode2=&conditionValue2=&conditionCode3=&conditionValue3='.format(count=count)
        print(url)
        text=g.GetCompanyList(url)
        print(text)
        dic=g.GetCompanyinf(text)
        count=count+1
    