# -*- coding: utf-8 -*-
__author__ = 'syb'
WeChatToken = 'sybing'
import time
import hashlib
from django.http import HttpResponse
from django.utils.encoding import smart_str
import xml.etree.ElementTree as XMLTree
from django.views.decorators.csrf import csrf_exempt
from WeChat.deal import dealText, replyTextXml


@csrf_exempt
def main(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    elif request.method == 'POST':
        response = HttpResponse(responseMsg(request), content_type="application/xml")
        return response
    else:
        return None


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
        return HttpResponse('Hello World ---by jwfy')


def responseMsg(request):
    raw_xml = smart_str(request.raw_post_data)
    refined_xml = dealxml(XMLTree.fromstring(raw_xml))

    #  现在开始分开每种类型的消息
    msgType = refined_xml['MsgType']
    if msgType == 'text':
        # content = "你发送的是"+refined_xml['Content']
        msgText = refined_xml['Content']
        content = dealText(msgText)
        return replyTextXml(refined_xml, content)
    elif msgType == 'image':
        content = "你发送的是图片"
        return replyTextXml(refined_xml, content)
    elif msgType == 'location':
        content = "你发送的是地理位置"
        return replyTextXml(refined_xml, content)
    elif msgType == 'link':
        content = "你发送的是链接"
        return replyTextXml(refined_xml, content)


def dealxml(xmlstr):
    """把接收到的xml消息解析"""
    msg = {}
    if xmlstr.tag == 'xml':
        for child in xmlstr:
            msg[child.tag] = smart_str(child.text)
    return msg







