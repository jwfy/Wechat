# -*- coding: utf-8 -*-
__author__ = 'syb'
"""主要是处理用户发送的消息"""
import time
import urllib
import urllib2
import xml.etree.ElementTree as XMLTree

YouDaoData = {}
YouDaoData['YouDaoAPIKey'] = "987935518"
YouDaoData['YouDaoKEYFrom'] = "sybwechat"
YouDaoData['YouDaoDoctype'] = "json"
YouDaoData['YouDaoVersion'] = '1.1'
YouDaoBasicUrl = 'http://fanyi.youdao.com/openapi.do?'


def YouDaoURL(search):
    """获取需要查询xml的url地址"""
    YouDaoData['q'] = search
    url = YouDaoBasicUrl + urllib.urlencode(YouDaoData)
    return url


def YouDaoDataDeal(url):
    request = urllib2.Request(url)
    xmlData = urllib2.urlopen(request).read()
    return YouDaoXmlDataDeal(xmlData)


def YouDaoXmlDataDeal(content):
    content = XMLTree.fromstring(content)
    replayContent = ''
    if content.tag == 'youdao-fanyi':
        for child in content:
            if child.tag == 'errorCode':
                """错误码，正常的应该返回0"""
                if child.text == '20':
                    replayContent = u'抱歉，您输入的过长，无法翻译'
                elif child.text == '30':
                    replayContent = u'抱歉，无法有效的翻译'
                elif child.text == '40':
                    replayContent = u'无法翻译该语言'
                elif child.text == '50':
                    replayContent = u'抱歉，系统出错，请重试'

            elif child.tag == 'query':
                """查询的具体单词"""
                replayContent = '%s%s\n' % (replayContent,  child.text)

            elif child.tag == 'basic':
                """基本释义"""
                replayContent = '%s%s\n' % (replayContent, u'【基本词典】')
                for grands in child:
                    if grands.tag == 'phonetic':
                        replayContent = '%s%s:%s\n' % (replayContent, u'音标', grands.text)
                    elif grands.tag == 'explains':
                        for ex in grands.findall('ex'):
                            replayContent = '%s%s\n' % (replayContent, ex.text)
            elif child.tag == 'web':
                """网络释义"""
                replayContent = '%s%s\n' % (replayContent, u'【网络释义】')
                for explain in child.findall('explain'):
                    for key in explain.findall('key'):
                        replayContent = '%s%s\n' % (replayContent, key.text)
                    for value in explain.findall('value'):
                        for ex in value.findall('ex'):
                            replayContent = '%s%s\n' % (replayContent, ex.text)
    replayContent = '%s%s\n' % (replayContent, u'该功能由有道词典提供')
    return replayContent


def dealText(Content):
    if Content[:2] == '翻译':
        return Content[2:]
    else:
        return '暂时功能还在开发中。。。'
        # text = Content[2:]
        # url = YouDaoURL(text)    #获取对应的url
        # XMLData = YouDaoDataDeal(url)    #得到url中的xml数据
        # return YouDaoDataDeal(XMLData)    #根据xml数据，获取相应的数据


def replyTextXml(msg, Content):
    xml = " <xml>\
            <ToUserName><![CDATA[%s]]></ToUserName>\
            <FromUserName><![CDATA[%s]]></FromUserName> \
            <CreateTime>%s</CreateTime>\
            <MsgType><![CDATA[%s]]></MsgType>\
            <Content><![CDATA[%s]]></Content>\
            <FuncFlag>0</FuncFlag>\
            </xml>"
    xml = xml % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text',  Content)
    return xml


