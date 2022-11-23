# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import time
import pickle
from colorama import  init,Fore,Back,Style
init(autoreset=True)
class Colored(object):

    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.RED + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    #  前景色:黄色  背景色:默认
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET
    #  前景色:白色  背景色:默认
    def white(self, s):
        return Fore.WHITE + s + Fore.RESET
    #  前景色:黑色  背景色:默认
    def black(self, s):
        return Fore.BLACK
    #  前景色:白色  背景色:绿色
    def black_white(self, s):
        return Fore.BLACK + Back.WHITE + s + Back.RESET + Fore.RESET
    #  前景色:白色  背景色:绿色
    def green_white(self, s):
        return Fore.BLACK + Back.GREEN + s + Back.RESET + Fore.RESET
    #  前景色:白色  背景色:绿色
    def yellow_white(self, s):
        return Fore.BLACK + Back.YELLOW + s + Back.RESET + Fore.RESET
    def red_white(self, s):
        return Fore.BLACK + Back.RED + s + Back.RESET + Fore.RESET
class GetSessionAndToken():
    def __init__(self):
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--disable-gpu')
        options.add_argument('log-level=3')
        self.browser=webdriver.Edge(options=options)
    #登录系统,具体到自己系统时需要自行修改
    def login_system(self):
        mode = input('请选择模式：1.手机验证码，2.账号密码(输入数字后回车)\n')
        if mode=='1':
            phone = input('请输入手机号码：')
            s = requests.session()
            h = {
                # 'Host': 'convenient.wsjkw.zj.gov.cn'
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
                , 'Accept': 'application/json, text/plain, */*'
                , 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
                , 'Accept-Encoding': 'gzip, deflate, br'
            }
            urlSend = 'https://puser.zjzwfw.gov.cn/sso/usp.do?action=sendsmscode&mobilephone={}&msgtype=login'.format(phone)
            s.post(urlSend, headers=h)
            vari = input('请输入验证码：')
            # 登录页面ur1,改成目标系统登录页面
            url = "https://puser.zjzwfw.gov.cn/sso/mobile.do?action=oauth&scope=1&servicecode=wjwyfjz&goto=https%3A%2F%2Fmapi.zjzwfw.gov.cn%2Fweb%2Fmgop%2Fgov-open%2Fzj%2F2001101254%2Freserved%2Fvaccine-external-front%2Fhtml%2Fhome%2Findex.html"
            self.browser.get(url)
            # 显性等待,直到用户名控件加载出来才进行下一步
            WebDriverWait(self.browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, "moblielogin")))
            self.browser.find_element(By.ID, "moblielogin").click()
            WebDriverWait(self.browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, "mobilephone")))
            # 填写用户名
            self.browser.find_element(By.ID, "mobilephone").send_keys(phone)
            # 填写密码
            self.browser.find_element(By.ID, "code").send_keys(vari)
            # 点击登录
            self.browser.find_element(By.ID, "smslogin").click()
        else:
            phone = input('请输入账号：')
            vari = input('请输入密码：')
            # 登录页面ur1,改成目标系统登录页面
            url = "https://puser.zjzwfw.gov.cn/sso/mobile.do?action=oauth&scope=1&servicecode=wjwyfjz&goto=https%3A%2F%2Fmapi.zjzwfw.gov.cn%2Fweb%2Fmgop%2Fgov-open%2Fzj%2F2001101254%2Freserved%2Fvaccine-external-front%2Fhtml%2Fhome%2Findex.html"
            self.browser.get(url)
            # 显性等待,直到用户名控件加载出来才进行下一步
            WebDriverWait(self.browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, "login")))
            # 填写用户名
            self.browser.find_element(By.ID, "loginname").send_keys(phone)
            # 填写密码
            self.browser.find_element(By.ID, "loginpwd").send_keys(vari)
            # 点击登录
            self.browser.find_element(By.ID, "login").click()

        #强制等待5秒,待session和token都成功返回并存到浏览器中
        print('等待返回数据。。。')
        time.sleep(5)

    def get_cookies(self):
        cookies=self.browser.get_cookies()
        c = {}
        for i in cookies:
            c[i['name']] = i['value']
        return c

    # 获取token
    def get_token(self):
        token = self.browser.execute_script('return sessionStorage.getItem("access_token");')
        return token
    def __del__(self):
        self.browser.close()

def timeStructure(ts,divide=False):
    ts = int(ts)
    if divide:
        ts = ts/1000
    ts = time.localtime(ts)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    return otherStyleTime
def getData(cookies,token):
    color = Colored()
    h = {
        # 'Host': 'convenient.wsjkw.zj.gov.cn'
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        , 'Accept': 'application/json, text/plain, */*'
        , 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'X-Requested-With': 'XMLHttpRequest'
        ,'Authorization': token
        , 'Origin': 'https://mapi.zjzwfw.gov.cn'
        , 'Connection': 'keep-alive'
        , 'Referer': 'https://mapi.zjzwfw.gov.cn/'
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'cross-site'
    }
    url = 'https://convenient.wsjkw.zj.gov.cn/api/biz-vaccine/convenient/lottery/activity/list?timestamp=1668851042&gbCode=5503&orgCode=330100&pageNo=1&pageSize=50'
    session = requests.session()
    x = session.get(url=url,headers=h,cookies=cookies)
    j = x.json()
    data = j['result']['pageData']['data']
    c = 0
    main = ['西湖区', '上城区', '下城区', '江干区', '拱墅区','滨江区']
    available_list = []
    req_all = 0
    quota_all = 0
    for i in data:
        req_all += i['req']
        quota_all += i['quota']
        c += 1
        if i['areaName'] in main:
            available_list.append(i)
        else:
            h = i['honestChoices']
            if h is not None:
                for n in h:
                    if '杭州' in n['content']:
                        available_list.append(i)
            else:
                i['orgName'] = i['orgName'] + '(不在城区内但是可以报名)'
                available_list.append(i)
    available_list_with_data = []
    for i in available_list:
        status = ''
        honestChoices = i['honestChoices']
        applyBeginTimeStamp = i['applyBeginTime']
        applyBeginTime = timeStructure(i['applyBeginTime'], True)
        applyEndTimeStamp = i['applyEndTime']
        applyEndTime = timeStructure(i['applyEndTime'], True)
        countDownSecond = ((applyEndTimeStamp / 1000)-time.time())
        countDownSec = countDownSecond % 60
        countDownMinute = countDownSecond // 60
        countDownMin = countDownMinute % 60
        countDownHour = countDownMinute // 60
        if time.time() > applyEndTimeStamp / 1000:
            status = color.red('[已结束]')
        elif time.time() > applyBeginTimeStamp / 1000:
            status = color.green('[已开始]')
        else:
            status = color.yellow('[未开始]')
        if i['req'] == 0:
            percentage = 100
        else:
            percentage = i['quota'] / i['req']
        if percentage > 1:
            percentage = 1
        percentage = percentage * 100
        if percentage>66.6 and status==color.green('[已开始]'):
            percentage = color.green_white('{:.2f}'.format(percentage)+'%')
        elif percentage>33.3 and status==color.green('[已开始]'):
            percentage = color.yellow_white('{:.2f}'.format(percentage)+'%')
        elif status==color.green('[已开始]'):
            percentage = color.red_white('{:.2f}'.format(percentage)+'%')
        else:
            percentage = '{:.2f}'.format(percentage)
        info = {'info': {'status':status,'percentage':percentage,'begin':applyBeginTime,'end':applyEndTime,'countDown':'剩余时间{:.0f}小时{:.0f}分{:.0f}秒'.format(countDownHour,countDownMin,countDownSec)}, 'content': i}
        available_list_with_data.append(info)
    available_list_with_data = sorted(available_list_with_data, key=lambda k: k['content']['applyBeginTime'])
    # print(available_list)

    print('------------------------------')
    req_availavle = 0
    quota_available = 0
    for i in available_list_with_data:
        honestChoices = i['content']['honestChoices']
        content = i['content']
        info = i['info']
        req_availavle += content['req']
        quota_available += content['quota']
        printText = '{} 地点：{} | {}/{}('.format(info['status'],content['orgName'],content['req'],content['quota'])+'{}'.format(info['percentage'])+')\n报名开始时间：{}\n报名结束时间:{}\n要求：\n'.format(info['begin'],info['end']+' | '+info['countDown'])
        if honestChoices is not None:
            for n in honestChoices:
                printText += n['type']+':'+n['content'] + '\n'
        printText += '------------------------------'
        print(printText)
        print('已显示{}个可报名活动\n包括{}\n和除此之外的无条件限制活动'.format(len(available_list),main))
        print('本次报名数据：')
        print(' 总共参加人数：{}\n 总共疫苗数量：{}\n 可报名的活动参加人数：{}\n 可报名的活动疫苗数量：{}'.format(req_all,quota_all,req_availavle,quota_available))
        print('------------------------------')

def updateToken():
    o = GetSessionAndToken()
    o.login_system()
    token = o.get_token()
    cookie = o.get_cookies()
    with open("save.txt", 'wb') as f:  # 打开文件
        pickle.dump({'token':token,'cookies':cookie}, f)  # 用 dump 函数将 Python 对象转成二进制对象文件
    print(cookie)
    print(token)
def main():
    try:
        print('使用保存的用户信息',end='\r')
        with open("save.txt", 'rb') as f:  # 打开文件
            info = pickle.load(f)  # 将二进制文件对象转换成 Python 对
            # print(info)
        getData(info['cookies'], info['token'])
    except:
        print('更新用户信息',end='\r')
        updateToken()
        with open("save.txt", 'rb') as f:  # 打开文件
            info = pickle.load(f)  # 将二进制文件对象转换成 Python 对
            print(info,end='\r')
        getData(info['cookies'], info['token'])
    finishStatus = input('1.刷新数据 \n或按任意键后回车：退出\n')
    if finishStatus == '1': main()
if __name__ == '__main__':
    print('程序加载中',end='\r')
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
