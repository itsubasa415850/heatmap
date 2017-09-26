# encoding=utf8
# !/usr/bin/env python

def map(result):
    "做MAP"
    ret = ''

    result =  result.replace(', ', '')
    result = result[1 : len(result)]

    mapper = result.split(',')

    for item in mapper:
        ret = ret +  item + ' ' + '1' + ','

    return ret

def reduce(map):
    "做REDUCE"
    map = map[0: len(map) - 1]
    ret = ''
    result = {}
    maps = map.split(',')
    for map1 in maps:
        kvs = map1.split(' ')
        k = kvs[0]
        v = kvs[1]
        if k in result:
            result[k] += 1
        else:
            result[k] = 1
    for k,v in result.items():
        ret += k + '\t' + str(v) + ','
    return ret