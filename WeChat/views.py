# -*- coding: utf-8 -*-
__author__ = 'syb'
WeChatToken = 'sybing'
import time
import hashlib
from django.http import HttpResponse
from django.utils.encoding import smart_str
import xml.etree.ElementTree as XMLTree


def main(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    else:
        response = HttpResponse(responseMsg(request), content_type="application/xml")
        return response


def checkSignature(request):

    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    token = WeChatToken

    list = [token, timestamp, nonce]
    list.sort()
    str = "%s%s%s" % tuple(list)
    str = hashlib.sha1(str).hexdigest()
    if str == signature:
        return echostr
    else:
        return "hehe"


def responseMsg(request):
    raw_xml = smart_str(request.body)
    refined_xml = dealxml(XMLTree.fromstring(raw_xml))

    #  现在开始分开每种类型的消息
    msgType = refined_xml['MsgType']
    if msgType == 'text':
        content = dealText(refined_xml['Content'])
        return replyTextXml(refined_xml, content)


def dealxml(xmlstr):
    msg = {}
    if xmlstr.tag == 'xml':
        for child in xmlstr:
            msg[child.tag] = smart_str(child.text)
    return msg


def dealText(Content):
    return Content


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



