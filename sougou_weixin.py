# coding=utf-8

import requests
from lxml import etree
import time
import re
import os
import random
import json


def main():
    # 列表页拿到itemurls和thumbs,但是itemurls不能直接用
    list_url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%9F%AC%E5%9F%94%E5%AF%A8&ie=utf8&_sug_=n&_sug_type_=&page=1'
    headers1 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Host": "weixin.sogou.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
    }
    response1 = requests.get(list_url, headers=headers1)
    html = etree.HTML(response1.text)
    urls = ['https://weixin.sogou.com' + i for i in html.xpath('//div[@class="img-box"]/a/@href')]

    params = get_cookie(response1)
    url = get_k_h(urls[0])
    headers2 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}; SUID={}; JSESSIONID={}; SUV={}".format(params['ABTEST'],
                                                                                                  params['SNUID'],
                                                                                                  params['IPLOC'],
                                                                                                  params['SUID1'],
                                                                                                  params['SUID2'],
                                                                                                  params['JSESSIONID'],
                                                                                                  params['SUV']),
        "Host": "weixin.sogou.com",
        "Referer": list_url,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    }
    response2 = requests.get(url, headers=headers2)
    print(response2.status_code)

    fragments = re.findall("url \+= '(.*?)'", response2.text, re.S)
    itemurl = ''
    for i in fragments:
        itemurl += i

    # 文章url拿正文
    # url = "https://mp.weixin.qq.com/s?src=11&timestamp=1572921220&ver=1955&signature=McZREDXqOED*1xGVkhuFXpNF7KcV54DRRSYjyPbwZvSO20QRO77a3w9RjoHAKxMkyUJkWaE9llLPp8zIF97qqCrolVg-gQZgeXof3Sisb0rAJ6848aBzVULDOJZZpdKb&new=1"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }
    response3 = requests.get(itemurl, headers=headers)
    html = etree.HTML(response3.text)
    print(response3.status_code)
    print(html.xpath('//meta[@property="og:title"]/@content')[0])


def get_cookie(response1):
    SetCookie = response1.headers['Set-Cookie']
    ABTEST = re.findall('ABTEST=(.*?);', SetCookie, re.S)[0]
    SNUID = re.findall('SNUID=(.*?);', SetCookie, re.S)[0]
    IPLOC = re.findall('IPLOC=(.*?);', SetCookie, re.S)[0]
    SUID1 = re.findall('SUID=(.*?);', SetCookie, re.S)[0]

    url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
    headers = {
        "Accept": "text/css,*/*;q=0.1",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}".format(SNUID, IPLOC),
        "Host": "www.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    response2 = requests.get(url, headers=headers)
    SetCookie = response2.headers['Set-Cookie']
    SUID2 = re.findall('SUID=(.*?);', SetCookie, re.S)[0]

    url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}".format(ABTEST, SNUID, IPLOC, SUID1),
        "Host": "weixin.sogou.com",
        "Referer": "https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%9F%AC%E5%9F%94%E5%AF%A8&ie=utf8&_sug_=n&_sug_type_=",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    response3 = requests.get(url, headers=headers)
    SetCookie = response3.headers['Set-Cookie']
    JSESSIONID = re.findall('JSESSIONID=(.*?);', SetCookie, re.S)[0]

    uigs_para = get_uigs_para(response1)
    url = "https://pb.sogou.com/pv.gif"
    headers = {
        "Accept": "image/webp,*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}; SUID={}".format(SNUID, IPLOC, SUID2),
        "Host": "pb.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    response4 = requests.get(url, headers=headers, params=uigs_para)
    SetCookie = response4.headers['Set-Cookie']
    SUV = re.findall('SUV=(.*?);', SetCookie, re.S)[0]

    params = {
        "ABTEST": ABTEST,
        "SNUID": SNUID,
        "IPLOC": IPLOC,
        "SUID1": SUID1,
        "SUID2": SUID2,
        "JSESSIONID": JSESSIONID,
        "SUV": SUV,
    }

    return params


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


if __name__ == "__main__":
    main()
