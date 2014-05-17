# -*- coding: utf-8 -*-
__author__ = 'syb'
"""主要是处理用户发送的消息"""
import time
from function.YouDaoTranslate import YouDaoDataDeal
from function.wether import WEtherDataDeal


def dealText(Content):
    if Content.decode('utf-8')[:2].encode('utf-8') == '翻译':
        text = Content.decode('utf-8')[2:].encode('utf-8')
        XMLData = YouDaoDataDeal(text)    #得到url中的xml数据
        return XMLData
    elif Content.decode('utf-8')[-2:].encode('utf-8') == '天气':
        text = Content.decode('utf-8')[:-2].encode('utf-8')
        JSONData = WEtherDataDeal(text)
        return JSONData
    else:
        return '暂时功能还在开发中。。。'
        # text = Content[2:]


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


