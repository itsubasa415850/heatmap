# encoding=utf8
# !/usr/bin/env python
import os
import re
import urllib2
from bs4 import BeautifulSoup as bs
import time

#抓取数据
#首先根据汽车之家手机论坛定位只包含精华贴的GTI论坛页面，
#然后对这些贴子逐个请求，从中找到发贴人的所在地，然后
#组成一个大串返回。
def capture():

    homepage='http://club.m.autohome.com.cn'

    #伪装成浏览器
    headers = {
        'User-Agent':'Mozilla/5.0(Windows; U; Windows NT 6.1; en-US; '
                     'rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

    dir = os.path.abspath('.')
    #由于汽车之家部分贴子解析出来是序列，无法解释成HTML，
    #所以退而求其次，使用手机论坛页面。。。

    result = ''
    #外层循环开始（精华贴页面的循环）
    for num in range(1, 9):
        print '现在开始处理第' + str(num) + '页的精华贴。'
        jing='http://club.m.autohome.com.cn/bbs/forum-c-9902871-' + \
             str(num) + '.html?qaType=-1&type=Jing&sort=LastestReply'
        # 设置网址
        request = urllib2.Request(url=jing, headers=headers)
        # 使用GBK读取网页
        response = urllib2.urlopen(request)
        html_data = response.read()
        # 使用BeautifulSoup的html.parser解释网页
        soup = bs(html_data, 'html.parser')
        # 把所有含有贴子地址的锚点找出来
        articles = soup.findAll('a', href=re.compile('^/bbs/thread-c-9902871-[0-9]*-[0-9].html\?type=Jing$'))
        #内层循环开始（每一精华贴的循环）
        for article in articles:
            articlerequest = urllib2.Request(url=homepage + article.attrs['href'], headers=headers)
            #针对每一个精华贴的锚点值，与汽车之家的论坛首页进行拼接，并实时请求该页
            # 使用GBK读取网页
            articleresponse = urllib2.urlopen(articlerequest)
            print homepage + article.attrs['href']
            #访问频率过高，以此防止被防火墙断掉
            # time.sleep(1)
            #精华贴页面内容
            articlehtml = articleresponse.read()
            #找到发贴者的首页
            soup = bs(articlehtml, 'html.parser')
            mes = soup.findAll('a', href=re.compile('^//i.m.autohome.com.cn/[0-9]*$'))
            mehtml = ''
            for me in mes:
                mereq = urllib2.Request(url='http:' + me.attrs['href'], headers=headers)
                meres = urllib2.urlopen(mereq)
                #发贴者的首页找到了！！！
                mehtml = meres.read()
                break
            #找所在地
            soup = bs(mehtml, 'html.parser')
            location = soup.findAll('dl', class_='area')
            if len(location) <> 0:
                for loc in location[0]:
                    for loc1 in loc:
                        pattern = re.compile(u'[^\u6240\u5728\u5730][\u4e00-\u9fa5]+')
                        washed = re.findall(pattern, loc1)
                        for w in washed:
                            result = result + ',' + w
    return result