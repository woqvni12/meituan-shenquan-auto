#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author:fugui

from typing import Counter, Text
import urllib.request
import ssl
import json
import os
import sys
import datetime
import time

#定义11点  用于开启server 酱推送
global d_time0,d_time1,d_time2,n_time
d_time0 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:00', '%Y-%m-%d%H:%M')


n_time = datetime.datetime.now()


#定义抢大额红包时间段d_time3和d_time4和d_time5和d_time6之间 ，d_time4提前11分钟意在防止下午红包池提前10分钟关闭和脚本抢大额红包有些地区到最后一刻10元以上红包都有剩余导致脚本报错，
# 若到最后一刻会自动放弃监测，抢所拥有的必中符的面值保底
###默认 抢大额(15元以上) 时间段为下午17:00点到16:49分和晚上21:00到23点59分   不建议进行更改
##以下默认中午试图抢大额红包 前提是道具库存中有10元以上必中符！！！！！！！！！

global d_time3,d_time4,d_time5,d_time6

d_time3 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '17:00', '%Y-%m-%d%H:%M')
d_time4 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '20:49', '%Y-%m-%d%H:%M')

d_time5 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '21:00', '%Y-%m-%d%H:%M')
d_time6 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:59', '%Y-%m-%d%H:%M')


#d_time6定义几点前不使用必中符,注意是不使用！！！若时间定义为17:00点,也就是17:00点之前的抽奖不会使用必中符,优先级高于自定义的大额抢红包时间,以节约道具库中的有效的必中符
##若d_time6定义为11:00点，则代表不对使用必中符时间进行限制，切记不能删除d_time7，若不需限制，只需将d_time7时间改为11:00,注意是英文的冒号
global d_time7
d_time7 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:00', '%Y-%m-%d%H:%M')


### 定义红包豆攒到多少数量才会执行兑换必中符脚本，以免一直兑换减5元的必中符
setexchangedou =int(os.environ.get("setexchangedou"))

 #关闭ssl校验，用于抓包调试请求
ssl._create_default_https_context = ssl._create_unverified_context

#定义短期(半年以上)不会变的量
parActivityId="Gh1tkq-wvFU2xEP_ZPzHPQ"
wm_ctype="mtandroid"
#以下portraitId参数含义未知，用于每日浏览天天神卷30s后可领30豆的请求
portraitId=498



#定义精简通用请求头部
head={"Host": "i.waimai.meituan.com","User-Agent":"MeituanGroup/11.9.208","x-requested-with": "XMLHttpRequest","content-type":"application/x-www-form-urlencoded"} 
#定义美团外卖服务器地址
baseurl=r"https://i.waimai.meituan.com"
#定义 pushPlus 的webhook地址，用于企业微信等渠道的推送，默认为空，若采用企业微信，请手动填写
global webhook
webhook = os.environ.get("webhook")

#定义全局变量并初始化 以下初始化赋值的变量不要改！！！！
global propIdforuse,token,batchId,propId,a
showPriceNumber = "1"
propIdforuse =2
batchId = "haha"
wm_latitude =os.environ.get("wm_latitude")
wm_longitude=os.environ.get("wm_longitude")
token =os.environ.get("token")
propId=int(os.environ.get("propId"))
exchangeCoinNumber=os.environ.get("exchangeCoinNumber")
serverkey=os.environ.get("serverkey")
pushPlusToken =os.environ.get("pushPlusToken")
yesornot = os.environ.get("yesornot")
yesornot2 = os.environ.get("yesornot2")
leftdou=0
counttime = 0
expire =0
cwd = os.path.dirname(os.path.realpath(__file__))

##############################################################################
##标记这四类红包数量不为空，用来在有10元以上必中符时循环判断红包池余量抢购大额元红包，若您不需该功能，请自行将下一行的1改为0
eight = ten = fifteen = thirty =fifty=int(os.environ.get("on"))
##############################################################################
# eight_left= 10
################################################################################
#若在您自定义的抢大额红包时间段中，您无法通过10元以上必中符抢到任何红包！！，则请将下面两行数值改大些，如改成10左右的数字
ten_left=fifteen_left=thirty_left=fifty_left=int(os.environ.get("left"))

#将print内容同步写到output.txt文件
# class Logger(object):
#     def __init__(self, fileN='Default.log'):
#         self.terminal = sys.stdout
#         self.log = open(fileN, 'w+',encoding='utf-8')

#     def write(self, message):
#         '''print实际相当于sys.stdout.write'''
#         self.terminal.write(message)
#         self.log.write(message)

#     def flush(self):
#         pass


class __Autonomy__(object):
    def __init__(self): 
        self._buff = "" 
    def write(self, out_stream):
        self._buff += out_stream
    def flush(self):
        pass

    
#定义获取batchId的函数
def getbatchId():
    global expire,wm_latitude,wm_longitude
    print("**开始执行获取batchId脚本:**\n")
    try:
        datas = "parActivityId="+parActivityId+"&wm_ctype="+wm_ctype+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token
        url_getbatchId = baseurl+r"/cfeplay/playcenter/batchgrabred/corepage"
        request =urllib.request.Request(url_getbatchId,headers=head,data=datas.encode("utf-8"),method="POST")
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            if "batchId" in result2["data"]:
                expire = 1
                print("batchId:%s\n"%(result2["data"]["batchId"]))
                return result2["data"]["batchId"]
            else:
                expire =2
                print("获取batchId失败👀，当前非限时抢红包时间段,无法进行下一步，但已为您签到完毕🙏!\n")

        elif (result2["code"]==1):
            print("%s,接口需提交的token参数已改变👀,请重新运行一遍脚本！\n"%(result2["msg"]))
            # os.remove(str(cwd)+r"/wm_latitudewm_longitude.txt")
            # os.remove(str(cwd)+r"/token.txt")
            # os.remove(str(cwd)+r"/propId_Coinnumbe.txt")
            # os.remove(str(cwd)+r"/serverkey.txt")
            # os.remove(str(cwd)+r"/pushPlusToken.txt")

        else:
            print("获取batchId错误👀，请检查网络，否则为接口失效！\n")

    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):

            print("脚本执行失败👀，错误代码为%s\n"%(e.code))



#定义每天七次签到领豆的函数，需传入获取的token
def signForBeans():
    global token
    print("**开始执行签到领豆脚本:** \n")
    datas = "token="+token
    url_signforbeans = baseurl+r"/cfeplay/playcenter/batchgrabred/drawPoints/v2"
    request =urllib.request.Request(url_signforbeans,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("👴%s\n"%(result2["msg"]))
        elif (result2["code"]==1):
            print("👴未到领取时间或已经领取完了(每天可领7次,每次间隔需半小时\n)！")
        elif (result2["code"]==7):
            print("token已失效，，请手动🙏更新token，最后温馨提示:建议接入server酱通知！\n")
        else:
            print("请求接口失效或网络不佳，请稍后再试!\n")


    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")


#def 限时抢红包函数
def drawlottery(batchId):
    global wm_latitude,wm_longitude,token
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    print("**开始执行限时抢天天神券脚本🧧:**\n")

    print(batchId)
    datas = "parActivityId="+parActivityId+"&wm_latitude="+wm_latitude+"&wm_longitude="+wm_longitude+"&token="+token+"&batchId="+batchId+"&isShareLink=true"+"&propType=1"+"&propId="+str(propIdforuse)
    url_drawlottery = baseurl+r"/cfeplay/playcenter/batchgrabred/drawlottery"
    request =urllib.request.Request(url_drawlottery,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("领取成功!\n提示信息:%s\n红包属性:%s\n使用限制:%s\n红包价值:%s\n红包立即生效时间:%s\n红包剩余有效期:%s分钟\n"%(result2["msg"],result2["data"]["name"],result2["data"]["priceLimitdesc"],result2["data"]["showTitle"],result2["data"]["endTimeDesc"],str(float(result2["data"]["leftTime"])/60000)))
            global showPriceNumber
            showPriceNumber = result2["data"]["showPriceNumber"]
            if int(showPriceNumber)<500:
                print("**当前红包面值为%d元，小于5元，👴将自动执行小额红包转红包豆脚本!!**\n"%(int(showPriceNumber)/100))
            else:
                print("**当前红包面值为%d元，大于等于5元，👴将不会执行小额红包转红包豆脚本!!**\n"%(int(showPriceNumber)/100))
        elif (result2["code"]==1 and result2["subcode"]==3):
            print("%s😅\n"%(result2["msg"]))
        elif(result2["code"]==1 and result2["subcode"]==-1):
            print("token错误或已失效,%s\n"%(result2["msg"]))
        elif (result2["code"]==7):
            print("token已失效，请手动🙏更新环境变量\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")


#定义接受红包函数，获得红包小于5元时，不执行此函数，并调用redtobean函数自动将红包转为红包豆，若两个函数都不执行，在抢红包成功5分钟左右红包会自动发放到账户
def acceptRed(batchId):
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    global wm_latitude,wm_longitude,token
    print("**开始执行发放天天神券🧧到红包库脚本:**\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&batchId="+batchId
    url_acceptRed = baseurl+r"/cfeplay/playcenter/batchgrabred/acceptRed"
    request =urllib.request.Request(url_acceptRed,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("*👴抢到的红包已经领取成功啦，快去使用吧!*\n")
        elif (result2["code"]==1):
            print("%s\n"%(result2["msg"]))
        elif (result2["code"]==7):
            print("token已失效，请手动🙏更新环境变量\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            
            print(e,"reason")

#定义红包转红包豆函数，将小于5元的红包转为红包豆
def redtobean(batchId):
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    global wm_latitude,wm_longitude
    print("**默认尝试执行面值小于5元🧧自动转红包豆脚本:**\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&batchId="+batchId
    url_drawlottery = baseurl+r"/cfeplay/playcenter/batchgrabred/redToBean"
    request =urllib.request.Request(url_drawlottery,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("👴小额红包转红包豆成功!\n")
        elif (result2["code"]==1 and result2["subcode"]==12):
            # print("%s😅\n"%(result2["msg"]))
            print("没有待转换的红包😅\n")
        elif (result2["code"]==7):
            print("token已失效，请手动🙏更新环境变量\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            
            print(e,"reason")
    



#查询已领取到的天天神券
def querymyreward():
    global token
    print("**开始执行查询已领天天神券🧧脚本:**\n")
    datas = "parActivityId="+parActivityId+"&token="+token
    url_querymyreward = baseurl+r"/cfeplay/playcenter/batchgrabred/myreward"
    request =urllib.request.Request(url_querymyreward,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0 and len(result2["data"]["myawardInfos"])):
            print("👴开始遍历红包库:\n")
            print("红包库详细信息:\n")
            print("红包库中共有%d个红包\n"%(len(result2["data"]["myawardInfos"])))
            cent=0
            count = 0
            isover15=0
            for k in result2["data"]["myawardInfos"]:
                if not k["status"]:
                    print("**第%d个红包有效!!!!**\n红包属性:%s\n使用限制:%s\n红包价值:%s元\n红包剩余有效期%s分钟\n"%(cent+1,k["name"],k["priceLimitdesc"],k["showPriceNumberYuan"],str(float(k["leftTime"])/60000)))
                    if(int(k["showPriceNumberYuan"])>15):
                        isover15 =1
                    print("\n")
                else:
                    count=count+1
                    if cent == 0:
                        print("**过期红包详情:**\n")
                    
                cent=cent+1
            if(propIdforuse!=5):
                print("总计已领取%d个红包,其中已过期%d个😅,有效%d个\n"%(cent,count,cent-count))
            else:
                if isover15==1:
                    print("恭喜你领取大额限时红包,具体价值如上所示!!总计已领取%d个红包,其中已过期%d个😅,有效%d个\n"%(cent,count,cent-count))
            print("\n")
        elif (result2["code"]==1):
            print("%s\n"%(result2["msg"]))
        elif (result2["code"]==7):
            print("token已失效，请手动🙏更新环境变量\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            
            print(e,"reason")


#获取每日浏览天天神券奖励的30豆
def sendTaskRedBean():
    global wm_latitude,wm_longitude,token
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    print("**开始执行领取每日30豆的脚本:**\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&portraitId="+str(portraitId)
    url_sendTaskRedBean = baseurl+r"/cfeplay/playcenter/batchgrabred/sendTaskRedBean"
    request =urllib.request.Request(url_sendTaskRedBean,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["status"]==0):
            print("%s\n今天领取成功%d个红包豆，请明日再来！\n"%(result2["msg"],result2["sendBeanCount"]))
        elif (result2["status"]==1):
            print("您今日已领取过😅,%s\n"%(result2["msg"]))
        elif (result2["status"]==-1):
            print("portraitId已失效,%s\n"%(result2["msg"]))
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")


#定义每日签到得必中符函数
def doAction():
    global wm_latitude,wm_longitude,token
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    print("**开始执行每日签到领必中符🧧的脚本:**\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&action=SiginInGetProp"
    url_doaction = baseurl+r"/cfeplay/playcenter/batchgrabred/doAction"
    request =urllib.request.Request(url_doaction,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0 and result2["data"]["signDays"]!=0):
            print("签到%s\n,截止今日这周已签到%d天"%(result2["msg"],result2["data"]["signDays"]))
        elif (result2["code"]==0 and result2["data"]["signDays"]==0):
            print("您今日已签到，请明天再来!")
        elif (result2["code"]==7):
            print("参数异常或接口已失效")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")


#查看道具库中的必中符记录
def querymyProps():
    global propIdforuse
    global wm_latitude,wm_longitude,token
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    print("**开始执行查询道具库中必中符🧧详情的脚本:**\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token
    url_querymyprops = baseurl+r"/cfeplay/playcenter/batchgrabred/myProps"
    request =urllib.request.Request(url_querymyprops,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0 and len(result2["data"])):
            print("👴开始遍历道具库:\n")
            print("道具库详细信息:\n")
            print("红包库中共有%d个必中符道具\n"%(len(result2["data"])))
            cent=0
            count = 0
            for k in result2["data"]:
                if k["status"]==1:
                    print("第%d个必中符道具有效!!!!\n必中符道具id号:%s\n必中符道具属性:%s\n过期时间:%s\n"%(cent+1,k["recordNo"],k["propName"],k["expireTime"]))
                    if cent==0:
                        propIdforuse = k["propId"] 
                    print("\n")
                else:
                    count=count+1   
                cent=cent+1
            if (count!=0):
                 print("总计%d个必中符道具,已过期%d个😅,有效%d个\n"%(cent,count,cent-count))
            if ((cent-count)!=0):
                print("**注意:每天中午抢红包🧧时将自动为您使用道具库中第一个道具!!** ")
            else:
                print(" **注意:道具库无有效道具，无法使用必中符,下次抢红包将使用默认参数抢红包(拼手气😅)!!** ")

            print("\n")
        elif (result2["code"]==7):
            print("参数异常或接口已失效，请手动🙏更新环境变量！")
        else:
            print("必中符道具库为空，👴未帮您领取过道具!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")

#已废弃，直接发送兑换请求即可，不在兑换时间段 subcode 为13
#定义运行时是否能兑换豆子成必中符,目前一直为14点至16点，故不定义此函数，采取每天14点至16点运行此程序时直接尝试兑换
#若需自行获取当前时间段是否可换豆子为道具，则post以下请求即可
# POST /cfeplay/playcenter/batchgrabred/canExchangeCheck HTTP/1.1
# Host: i.waimai.meituan.com
# Content-Length: 82
# User-Agent:MeituanGroup/11.9.208
# x-requested-with: XMLHttpRequest
# content-type: application/x-www-form-urlencoded


# parActivityId=Gh1tkq-wvFU2xEP_ZPzHPQ&wm_latitude=30657401&wm_longitude=104065827







#定义豆子兑换成必中符函数:
def exchange():
    global propId,wm_latitude,wm_longitude,token
    # wm_latitude = getVar()[0]
    # wm_longitude = getVar()[1]
    wm_actual_latitude = str(wm_latitude)
    wm_actual_longitude =str(wm_longitude)
    print("**开始执行每日豆子兑换必中符脚本**:\n")
    while(1):
        datas = "wm_actual_longitude="+wm_actual_longitude+"&wm_actual_latitude="+wm_actual_latitude+"&exchangeRuleId=&propId="+str(propId)+"&exchangeCoinNumber="+str(exchangeCoinNumber)+"&parActivityId="+parActivityId+"&wm_ctype="+wm_ctype+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token
        url_exchange = baseurl+r"/cfeplay/playcenter/batchgrabred/exchange"
        request =urllib.request.Request(url_exchange,headers=head,data=datas.encode("utf-8"),method="POST")
        try:
            response = urllib.request.urlopen(request,timeout=10)
            result = response.read().decode("utf-8")
            result2 = json.loads(result)
            if(result2["code"]==0 and result2["subcode"]==0):
                print("%s,您设置的红包豆兑换指定额度的必中符成功!!!请查看下方道具库详情!😄\n"%(result2["msg"]))
                break
            elif (result2["code"]==1 and result2["subcode"]==13):
                print("%s\n"%(result2["msg"]))
                break
            elif (result2["code"]==1 and result2["subcode"]==-1):
                print("%s,您现在的红包豆不足以兑换此类必中符或者此类必中符已被抢完!\n正尝试兑换*次一等级*必中符\n"%(result2["msg"]))
                if(propId ==5):
                    propId =4
                    break
            elif (result2["code"]==7):
                print("参数异常或接口已失效\n")
            else:
                print("请求接口失效或参数异常，请稍后再试!\n")
        except urllib.error.HTTPError as e:
            if hasattr(e,"code"):
                print("脚本执行失败👀,准备退出程序，错误代码为:%s\n"%(e.code))
            if hasattr(e,"reason"):
               print("脚本执行失败👀,准备退出程序,错误代码为:%s\n"%(e.reason))

###定义查询豆子详情的函数
def myRedBeanRecords():
    global wm_latitude,wm_longitude,leftdou,token
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    print("**开始执行查询豆子变化详情参数脚本**:\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+str(token)+"&userPortraitId="+str(portraitId)+"&pageNum=1"
    url_myredbeanRecords = baseurl+r"/cfeplay/playcenter/batchgrabred/myRedBeanRecords"
    request =urllib.request.Request(url_myredbeanRecords,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=10)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        cent=1
        if(result2["code"]==0 and result2["subcode"]==0 and len(result2["data"]["redBeanRecordInfos"])):
            leftdou= result2["data"]["totalObtainAmount"]-result2["data"]["usedAmount"]-result2["data"]["expiredAmount"]
            print("**总获得红包豆:%d,已使用红包豆:%d,已过期红包豆:%d,剩余可用红包豆:%d**\n"%(result2["data"]["totalObtainAmount"],result2["data"]["usedAmount"],result2["data"]["expiredAmount"],leftdou))
            for k in result2["data"]["redBeanRecordInfos"]:
                print("exchangeTime:%s\texchangeMessage:%s\texchangeNumber:%s\n"%(k["exchangeTime"],k["exchangeMessage"],k["exchangeNumber"]))
                cent=cent+1
                if(cent>5):
                    break  
            print("*只显示最近五条红包豆的变化* \n")
        elif (result2["code"]==1 and result2["subcode"]==-1):
            print("%s\n"%(result2["msg"]))
        else:
            print("请求接口失效或参数异常，建议🙏重置参数!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")    




#定义查询红包池函数 
_last_pool_call=[0.0]
def queryredpool():
    global wm_latitude,wm_longitude,token
    # 抢大额红包的逻辑会循环调用本函数，加个最小间隔，避免请求过快被美团风控拉黑 token
    if time.time() - _last_pool_call[0] < 3:
        time.sleep(3 - (time.time() - _last_pool_call[0]))
    _last_pool_call[0] = time.time()
    # wm_latitude = $wm_latitude
    # wm_longitude=$wm_longitude
    print("**开始执行查询红包池详情脚本:**\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+str(token)+"&wm_ctype="+wm_ctype
    url_myredbeanRecords = baseurl+r"/cfeplay/playcenter/batchgrabred/corepage"
    request =urllib.request.Request(url_myredbeanRecords,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        global eight,ten,fifteen,thirty,fifty,ten_left,fifteen_left,thirty_left,fifty_left
        response = urllib.request.urlopen(request)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)

        if(result2["code"]==0 and result2["subcode"]==0 and len(result2["data"]["awardInfos"])):
            for k in result2["data"]["awardInfos"]:
                # 2026 版接口已不再返回 leftStock / sendStock，缺字段时只打印总量，不再让脚本崩掉
                left = k.get("leftStock")
                send = k.get("sendStock")
                if left is not None:
                    # if (round(float(k["showPriceNumberYuan"]))==8 and left==eight_left):
                    #     eight = 0
                    if (round(float(k["showPriceNumberYuan"]))==10 and left==ten_left):
                        ten = 0
                    if (round(float(k["showPriceNumberYuan"]))==15 and left==fifteen_left):
                        fifteen = 0
                    if (round(float(k["showPriceNumberYuan"]))==30 and left==thirty_left):
                        thirty = 0
                    if (round(float(k["showPriceNumberYuan"]))==50 and left==fifty_left):
                        fifty = 0
                if counttime<3:
                    if left is None or send is None:
                        print("*红包池中%s元总量:%d张(接口未返回剩余数量，已跳过余量判断)*\n"%(k["showPriceNumberYuan"],k.get("totalStock",-1)))
                    else:
                        print("*红包池中%s元总量:%d张,已被领取:%d张,剩余%d张*\n"%(k["showPriceNumberYuan"],k.get("totalStock",-1),send,left))
                counttime =counttime +1
        elif (result2["code"]==1 and result2["subcode"]==-1):
            print("token失效,导致获取活动信息失败！%s\n"%(result2["msg"]))
        else:
            print("红包池未开放，等待中!\n")
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")    
   
#定义pushPlus的消息推送函数
def pushPlus():
    global pushPlusToken,webhook,a
    message = a._buff
    pushurl="https://www.pushplus.plus/send"
    head_server ={"Host": "www.pushplus.plus","User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36","content-type":"application/x-www-form-urlencoded"}
    print("**开始执行pushPlus推送脚本:**\n")
    datas=bytes(urllib.parse.urlencode({"title":"天天神券推送","content":message,"token":pushPlusToken,"template":"markdown","channel":"wechat","webhook":str(webhook),"callbackUrl":""}),encoding="UTF-8")
    request =urllib.request.Request(pushurl,headers=head_server,data=datas,method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=30)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==200) :
            print("pushPlus消息推送成功!\n\n")
        else:
            print("请求接口失效或参数异常，建议重置参数!\n")
    except  urllib.error.HTTPError as e:
        if  hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason") 

#定义server 酱的消息推送函数
def serverjiang():
    global a
    # serverkey = $serverkey
    message = a._buff
    pushurl="https://sctapi.ftqq.com/"
    head_server ={"Host": "sctapi.ftqq.com","User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36","content-type":"application/x-www-form-urlencoded"}
    url_serverkey = pushurl+serverkey+".send"
    print("**开始执行server酱推送脚本:**\n")
    datas=bytes(urllib.parse.urlencode({"title":"天天神券推送","desp":message,"channel":""}),encoding="UTF-8")
    request =urllib.request.Request(url_serverkey,headers=head_server,data=datas,method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=30)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0) :
            pushid = result2["data"]["pushid"]
            readkey = result2["data"]["readkey"]
            url_checkurl = pushurl+"push?id="+pushid+"&readkey="+readkey
            request2 = urllib.request.Request(url_checkurl,headers=head_server,data=datas)
            try:
                response2 = urllib.request.urlopen(request2,timeout=30)
                text=json.loads(response2.read().decode("utf-8"))
                if(text["data"]["title"] =="天天神券推送"):
                    print("server酱推送成功😄！请在移动设备端查看\n")
                else:
                    print("server酱推送失败👀，请检查serverkey是否正确！\n")

            except urllib.error.HTTPError as e2:
                if hasattr(e2,"code"):
                    print("脚本执行失败👀，错误代码如下:\n")
                print(e2.code)
                if hasattr(e2,"reason"):
                    print(e2,"reason") 
        else:
            print("请求接口失效或参数异常，建议重置参数!\n")
    except  urllib.error.HTTPError as e:
        if  hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason") 



#定义pushPlus的消息推送函数
def pushPlusforexpire():
    global webhook,pushPlusToken
    message = "### 尊敬的天天神券脚本用户: ###\n\n**若您收到此推送,则代表您之前部署在服务器上的美团网页cookie 由于请求过快被拉黑或者使用时间过长到期!**\n\n **若您想继续使用本脚本服务，还请按照[readme.md](https://github.com/fuguiKz/meituan-shenquan)手动获取cookie并覆盖原配置文件进行更新!**\n\n"

    
    pushurl="https://www.pushplus.plus/send"
    head_server ={"Host": "www.pushplus.plus","User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36","content-type":"application/x-www-form-urlencoded"}
    print("**开始执行pushPlus推送脚本:**\n")
    datas=bytes(urllib.parse.urlencode({"title":"token失效告警","content":message,"token":pushPlusToken,"template":"markdown","channel":"wechat","webhook":webhook,"callbackUrl":""}),encoding="UTF-8")
    request =urllib.request.Request(pushurl,headers=head_server,data=datas,method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=30)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==200) :
            print("pushPlus消息推送成功!\n\n")
        else:
            print("请求接口失效或参数异常，疑似用户取消关注，建议重置参数!\n")
    except  urllib.error.HTTPError as e:
        if  hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason") 




#定义server 酱的消息推送函数
def serverjiangforexpire():
    global serverkey
    message = "### 尊敬的天天神券脚本用户: ###\n\n**若您收到此推送,则代表您之前部署在服务器上的美团网页cookie 由于请求过快被拉黑或者使用时间过长到期!**\n\n **若您想继续使用本脚本服务，还请按照[readme.md](https://github.com/fuguiKz/meituan-shenquan)手动获取cookie并覆盖原配置文件进行更新!**\n\n"
    pushurl="https://sctapi.ftqq.com/"
    head_server ={"Host": "sctapi.ftqq.com","User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36","content-type":"application/x-www-form-urlencoded"}
    url_serverkey = pushurl+serverkey+".send"
    print("**开始执行server酱推送脚本:**\n")
    datas=bytes(urllib.parse.urlencode({"title":"token失效告警","desp":message,"channel":""}),encoding="UTF-8")
    request =urllib.request.Request(url_serverkey,headers=head_server,data=datas,method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=30)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0) :
            pushid = result2["data"]["pushid"]
            readkey = result2["data"]["readkey"]
            url_checkurl = pushurl+"push?id="+pushid+"&readkey="+readkey
            request2 = urllib.request.Request(url_checkurl,headers=head_server,data=datas)
            try:
                response2 = urllib.request.urlopen(request2,timeout=30)
                text=json.loads(response2.read().decode("utf-8"))
                if(text["data"]["title"] =="token失效告警"):
                    print("server酱推送成功😄！请在移动设备端查看\n")
                else:
                    print("server酱推送失败👀，请检查serverkey是否正确！\n")

            except urllib.error.HTTPError as e2:
                if hasattr(e2,"code"):
                    print("脚本执行失败👀，错误代码如下:\n")
                print(e2.code)
                if hasattr(e2,"reason"):
                    print(e2,"reason") 
        else:
            print("请求接口失效或参数异常，建议重置参数!\n")
    except  urllib.error.HTTPError as e:
        if  hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason") 





def main():
    global propIdforuse,token,a,br
    br =0
    temp = sys.stdout
    print("本脚本提供pushPlus、serverkey这两种推送方式,可以二选一或者全选，首次运行脚本请依次选择是否开启对应推送!\n由于server酱每日免费限额5条,若需开启推送,请首选pushPlus!\n")
    # getpushPlusToken()
    # getserverkey()
    # token = gettoken()
    # getlatlongitude()
    # getpropId_Coinnumber(token)
    a = __Autonomy__()
    sys.stdout = a
    print("脚本启动时间:%s\n"%(n_time))  
    signForBeans()
    batchId = getbatchId()
    ##先去保持每天签到 以获得必中符或者豆子
    if expire ==0:
    # print (yesornot)
     # print (yesornot2)
        if yesornot =="y":
            serverjiangforexpire()
        if yesornot2 =="y":
            pushPlusforexpire()
        sys.exit(0)
    if expire ==2:
        sys.exit(0)



    doAction()
    myRedBeanRecords()
    if leftdou >=setexchangedou:
        exchange()   
    else:
        print("您当前红包豆为%d未满预设的%d数量，不会执行红包豆兑换必中符脚本，多攒几天豆子再来吧!\n"%(leftdou,setexchangedou))   
    querymyProps()

    #定义bool类型变量判断当前时间段是不是自定义的大额抢红包时间段
    istimeforbig1= (n_time <=d_time4) and(n_time>=d_time3)
    istimeforbig2= (n_time <=d_time6) and(n_time>=d_time5)
    if n_time > d_time7:
        if istimeforbig1:
            if propIdforuse ==5:
                print("**当前符合抢30元以上大额红包的条件**\n")
                print("**正使用15元必中符为您尝试抢30元以上的红包**\n")
                    ##拥有15块以上的必中符，先等待着试图抢30,要是15没了，就直接去抢30的红包，或许有可能抢到50
                while  fifteen ==1 :
                    if not istimeforbig1:
                        print("*👴尽力了，等到红包池要关闭了都未等到15元以上大额红包被抢完，开始保底15元，注意查收！*\n")
                        break
                    if(thirty ==1 and fifty ==1):
                        print("*15有剩余，30元已被抢完，50元已被抢完，跳出监测，正在为您抢保底15元红包!*\n")
                        break
                    queryredpool()


        if istimeforbig2 :
            if propIdforuse ==5:
                print("**当前符合抢30元以上大额红包的条件**\n")
                print("**正使用15元必中符为您尝试抢30元以上的红包**\n")
                    ##拥有15块以上的必中符，先等待着试图抢30,要是15没了，就直接去抢30的红包，或许有可能抢到50
                while  fifteen ==1 :
                    if not istimeforbig2 :
                        print("*👴尽力了，等到红包池要关闭了都未等到15元以上大额红包被抢完，开始保底15元，注意查收！*\n")
                        break
                    if(thirty ==1 and fifty ==1):
                        print("*15有剩余，30元已被抢完，50元已被抢完，跳出监测，正在为您抢保底15元红包!*\n")
                        break
                    queryredpool()

        if istimeforbig1:    
            if propIdforuse ==3:
                print("**当前符合抢30元以上大额红包的条件**\n")
                print("**正使用10元必中符为您尝试抢30元以上的红包**\n")
                    ##拥有10块以上的必中符，先等待着试图抢30,要是10和15都没了，就直接去抢30的红包，或许有可能抢到50

                while  fifteen ==1 :
                    if(thirty ==1 and fifty ==1 ):
                        print("&15有剩余，30元已被抢完，50元已被抢完，跳出监测，正在为您抢保底15元红包！*\n")
                        break 
                    if(br ==1):
                        break
                    if not istimeforbig1:
                            print("*👴尽力了，等到红包池要关闭了都未等到15元以上大额红包被抢完，开始保底15元，注意查收！*\n")
                            break
                    if ten ==0 :
                        queryredpool()
                    while ten ==1:
                        if not istimeforbig1:
                            br = 1
                            print("*👴尽力了，等到红包池要关闭了都未等到任意大额红包被抢完，开始保底10元，注意查收！*\n")
                        queryredpool()  
        
        if istimeforbig2:    
            if propIdforuse ==3:
                print("**当前符合抢30元以上大额红包的条件**\n")
                print("**正使用10元必中符为您尝试抢30元以上的红包**\n")
                    ##拥有10块以上的必中符，先等待着试图抢30,要是10和15都没了，就直接去抢30的红包，或许有可能抢到50

                while  fifteen ==1 :
                    if(thirty ==1 and fifty ==1 ):
                        print("&15有剩余，30元已被抢完，50元已被抢完，跳出监测，正在为您抢保底15元红包！*\n")
                        break 
                    if(br ==1):
                        break
                    if not istimeforbig2:
                            print("*👴尽力了，等到红包池要关闭了都未等到15元以上大额红包被抢完，开始保底15元，注意查收！*\n")
                            break
                    if ten ==0 :
                        queryredpool()
                    while ten ==1:
                        if not istimeforbig2:
                            br = 1
                            print("*👴尽力了，等到红包池要关闭了都未等到任意大额红包被抢完，开始保底10元，注意查收！*\n")
                        queryredpool()  




 
    if n_time < d_time7  :
        propIdforuse =1 
    
    drawlottery(batchId)

    if(int(showPriceNumber)<500):
        redtobean(batchId)
    else:
        acceptRed(batchId)
    querymyreward()
    sendTaskRedBean()
    querymyProps()
    myRedBeanRecords()
    sys.stdout = temp
    # 原版把运行日志缓存在 a._buff 里，只在推送时用；没开推送就什么都看不到。
    # GitHub Actions 里把缓冲区打到标准输出，方便在 Actions 页面 / gh run view --log 里查。
    print("================ 运行日志开始 ================")
    print(a._buff)
    print("================ 运行日志结束 ================")
    if(yesornot2 == "y"):
        pushPlus()
    else:
        print("您已默认关闭pushPlus推送!若需开启,请手动配置环境变量yesornot2!\n")

    if(yesornot == "y"):
        if n_time>d_time0:
            serverjiang()
        else:
            print("当前时间段非抢红包时间,默认关闭server酱推送以节约server酱每日5条推送的限额！")
    else:
        print("您已默认关闭server酱推送!若需开启,请手动配置环境变量yesornot\n")
    


if __name__ == "__main__":
    main()
