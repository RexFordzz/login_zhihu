import scrapy
from scrapy.http import Request, FormRequest
from zhihu.items import *
import time
from PIL import Image
import json


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def start_requests(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login&lang=en'
        return [Request(captcha_url, callback=self.parser_captcha)]

    def parser_captcha(self, response):
        with open('captcha.jpg', 'wb') as f:
            f.write(response.body)
            f.close()
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
        captcha = input("input the captcha with quotation mark\n>")
        return Request(url='https://www.zhihu.com/', callback=self.login, meta={'captcha': captcha})

    def login(self, response):
        xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print
        'xsrf:' + xsrf
        print
        response.meta['captcha']
        return [FormRequest('https://www.zhihu.com/login/phone_num',
                            method='POST',
                            formdata={
                                'phone_num': '18512876524',
                                'password': 'jl2145201s',
                                '_xsrf': xsrf,
                                'captcha_type': 'en',
                                'captcha': response.meta['captcha'],
                            },

                            callback=self.after_login,
                            )]

    def after_login(self, response):
        json_file = json.loads(response.text)
        if json_file['r'] == 0:
            print('success........登录成功')
        else:
            print('登录失败！')