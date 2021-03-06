import time
import requests

from bs4 import BeautifulSoup
from http import cookiejar

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    print(session.cookies)
    session.cookies.load(ignore_discard=True)

except:
    print("还没有cookie信息")

# 获取网站的登录信息
def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=headers, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf

def get_captcha():
    """
    把验证码图片保存到当前目录，手动识别验证码
    :return:
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login&lang=en"
    print(captcha_url)
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码：")
    return captcha


def login(phone_num, password):
    login_url = 'https://www.zhihu.com/login/phone_num'
    data = {
        'phone_num': phone_num,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'remember_me': 'true'}
    # print(session.cookies)
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code['msg'])
    # print(session.cookies)
    r = session.get("https://www.zhihu.com/settings/profile", headers=headers)
    print(r.status_code)
    print(r.text)
    with open("xx.html", "wb") as f:
        f.write(r.content)


if __name__ == '__main__':

        phone_num = "18512876524"
        password = "jl2145201s"
        login(phone_num,password)
        json_str = ""