# coding=utf-8

import requests
from lxml import etree
import re
import random
import json
from urllib import parse


def get_cookie(response1, uigs_para, UserAgent):
    SetCookie = response1.headers['Set-Cookie']
    cookie_params = {
        "ABTEST": re.findall('ABTEST=(.*?);', SetCookie, re.S)[0],
        "SNUID": re.findall('SNUID=(.*?);', SetCookie, re.S)[0],
        "IPLOC": re.findall('IPLOC=(.*?);', SetCookie, re.S)[0],
        "SUID": re.findall('SUID=(.*?);', SetCookie, re.S)[0]
    }
    
    url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
    headers = {
        "Accept": "text/css,*/*;q=0.1",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}".format(cookie_params['SNUID'], cookie_params['IPLOC']),
        "Host": "www.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response2 = requests.get(url, headers=headers)
    SetCookie = response2.headers['Set-Cookie']
    cookie_params['SUID'] = re.findall('SUID=(.*?);', SetCookie, re.S)[0]
    
    url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}".format(cookie_params['ABTEST'], cookie_params['SNUID'], cookie_params['IPLOC'],
                                                                  cookie_params['SUID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent
    }
    response3 = requests.get(url, headers=headers)
    SetCookie = response3.headers['Set-Cookie']
    cookie_params['JSESSIONID'] = re.findall('JSESSIONID=(.*?);', SetCookie, re.S)[0]
    
    url = "https://pb.sogou.com/pv.gif"
    headers = {
        "Accept": "image/webp,*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}; SUID={}".format(cookie_params['SNUID'], cookie_params['IPLOC'], cookie_params['SUID']),
        "Host": "pb.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response4 = requests.get(url, headers=headers, params=uigs_para)
    SetCookie = response4.headers['Set-Cookie']
    cookie_params['SUV'] = re.findall('SUV=(.*?);', SetCookie, re.S)[0]
    
    return cookie_params


def get_k_h(url):
    b = int(random.random() * 100) + 1
    a = url.find("url=")
    url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url


def get_uigs_para(response):
    uigs_para = re.findall('var uigs_para = (.*?);', response.text, re.S)[0]
    if 'passportUserId ? "1" : "0"' in uigs_para:
        uigs_para = uigs_para.replace('passportUserId ? "1" : "0"', '0')
    uigs_para = json.loads(uigs_para)
    exp_id = re.findall('uigs_para.exp_id = "(.*?)";', response.text, re.S)[0]
    uigs_para['right'] = 'right0_0'
    uigs_para['exp_id'] = exp_id[:-1]
    return uigs_para


def main_v4(list_url, UserAgent):
    headers1 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Host": "weixin.sogou.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent,
    }
    response1 = requests.get(list_url, headers=headers1)
    html = etree.HTML(response1.text)
    urls = ['https://weixin.sogou.com' + i for i in html.xpath('//div[@class="img-box"]/a/@href')]
    
    uigs_para = get_uigs_para(response1)
    params = get_cookie(response1, uigs_para, UserAgent)
    approve_url = 'https://weixin.sogou.com/approve?uuid={}'.format(uigs_para['uuid'])
    headers2 = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; IPLOC={}; SUID={}; SUV={}; SNUID={}; JSESSIONID={};".format(params['ABTEST'], params['IPLOC'],
                                                                                          params['SUID'], params['SUV'], params['SNUID'],
                                                                                          params['JSESSIONID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent,
        "X-Requested-With": "XMLHttpRequest"
    }
    for url in urls:
        response2 = requests.get(approve_url, headers=headers2)
        url = get_k_h(url)
        headers3 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}; JSESSIONID={}; SUV={}".format(params['ABTEST'], params['SNUID'],
                                                                                             params['IPLOC'], params['SUID'],
                                                                                             params['JSESSIONID'],
                                                                                             params['SUV']),
            "Host": "weixin.sogou.com",
            "Referer": list_url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UserAgent
        }
        response3 = requests.get(url, headers=headers3)
        
        fragments = re.findall("url \+= '(.*?)'", response3.text, re.S)
        itemurl = ''
        for i in fragments:
            itemurl += i
        
        # 文章url拿正文
        headers4 = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "user-agent": UserAgent
        }
        response4 = requests.get(itemurl, headers=headers4)
        html = etree.HTML(response4.text)
        print(response4.status_code)
        print(html.xpath('//meta[@property="og:title"]/@content')[0])


if __name__ == "__main__":
    key = "咸蛋超人"
    url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&_sug_=n&_sug_type_=&page=1'.format(parse.quote(key))
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    main_v4(url, UserAgent)
