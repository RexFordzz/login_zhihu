# -*- encoding:utf-8 -*-
##############################
__author__ = "zwj"
__date__ = "2017/9/25"
###############################

import requests
from bs4 import BeautifulSoup
import urllib
import re

loginUrl = 'http://accounts.douban.com/login'

formData = {
    "redir":"http://movie.douban.com/mine?status=collect",
    "form_email":'username',
    "form_password":'password',
    "login":u'登录'
}

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}

r = requests.post(loginUrl,data=formData,headers=headers)
page = r.text
# print = r.url

"""获取验证码图片"""
# 利用bs4获取captcha地址
soup = BeautifulSoup(page,"html.parser")
captchaAddr = soup.find('img',id = 'captcha_image')['src']

# 利用正则表达式获取captcha的ID
reCaptchaID = r'<input type = "hidden" name = "captcha-id" value = "(.*?)"/'
captchaID = re.findall(reCaptchaID,page)
# print captchaID

# 保存到本地
urllib.urlretrieve(captchaAddr,"captcha.jpg")
captcha = input('please input the captcha:')

formData['captcha-solution'] = captcha
formData['captcha-id'] = captchaID

r = requests.post(loginUrl,data=formData,headers=headers)
page = r.text

if r.url == 'http://movie.douban.com/mine?status=collect':
    print ('Login successful')
    # print ('我看过的电影','-'*60)
    # # 获取看过的电影