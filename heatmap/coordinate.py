# encoding=utf8
# !/usr/bin/env python

import urllib2
import json
#使用百度地图开放平台生成各个城市的坐标
def coordinate(in_):
    str1 = ''
    #百度地图开放平台的注册码
    ak = 'dWYmlLpkwZ1MD0G4BoZgYO6tzgGhbtUP'
    addr1 = 'http://api.map.baidu.com/geocoder/v2/?address='
    addr2 = '&output=json&ak=' + ak + '&callback=showLocation'
    cities = in_.split(',')
    for city in cities:
        ci = city.split('\t')
        request = urllib2.Request(url=addr1 + ci[0] + addr2)
        response = urllib2.urlopen(request)
        #这就是当前城市的坐标JSON值了！！
        v = response.read()
        v = v[27: len(v) - 1]
        jsonv = json.loads(v)
        # print jsonv
        #只需把坐标值取出来即可
        coor = jsonv['result']['location']
        str1 = '{"lng":' + str(coor['lng']) + ', "lat":' + str(coor['lat']) + ', "count":' + ci[1] + '}'
        print str1