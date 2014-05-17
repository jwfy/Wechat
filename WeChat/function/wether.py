__author__ = 'syb'
# -*- coding: utf-8 -*-
from WeatherCity import getCityCode
import json
import urllib2

WEtherBasicUrl = 'http://m.weather.com.cn/atad/'


def WEtherUrl(search):
    """返回获取地址的具体url"""
    url = WEtherBasicUrl + getCityCode(search) + ".html"
    return url


def WEtherDataDeal(search):
    url = WEtherUrl(search)
    request = urllib2.Request(url)
    jsonData = urllib2.urlopen(request).read()
    return WEtherJsonDataDeal(jsonData)


def WEtherJsonDataDeal(content):
    """这时候content 是json文件了"""
    jsoncontent = json.loads(content)
    replycontain = ''
    title = jsoncontent['weatherinfo']['city']+u"天气"+'\n'
    time = u"【"+jsoncontent['weatherinfo']['date_y']+u"】"+'\n'
    temp1 = u'【温度】：'+jsoncontent['weatherinfo']['temp1']+'\n'
    wether = jsoncontent['weatherinfo']['weather1']+'\n'
    wind = jsoncontent['weatherinfo']['wind1']+'\n'
    fx = jsoncontent['weatherinfo']['fx1']+'\n'
    replycontain = title + time + temp1 + wether + wind + fx
    return replycontain


