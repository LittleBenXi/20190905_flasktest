# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
import hashlib
import requests
import json
import time
import re
import xml.etree.ElementTree as ET
from vehicleQA import searchCarInNeo4j

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/wechat", methods=["GET","POST"])
def weixin():
    answer = ''
    if request.method == "GET":     # 判断请求方式是GET请求
        my_signature = request.args.get('signature')     # 获取携带的signature参数
        my_timestamp = request.args.get('timestamp')     # 获取携带的timestamp参数
        my_nonce = request.args.get('nonce')        # 获取携带的nonce参数
        my_echostr = request.args.get('echostr')         # 获取携带的echostr参数

        token = 'LJHljh123'     # 一定要跟刚刚填写的token一致

        # 进行字典排序
        data = [token,my_timestamp ,my_nonce ]
        data.sort()
        print(data)

        # 拼接成字符串
        temp = ''.join(data)
        print(temp,type(temp))

        # 进行sha1加密
        s1 = hashlib.sha1()
        s1.update(temp.encode('utf-8'))
        mysignature = s1.hexdigest()
        #mysignature = hashlib.sha1(temp).hexdigest()

        # 加密后的字符串可与signature对比，标识该请求来源于微信
        if my_signature == mysignature:
            return my_echostr
    else:
        # 解析xml
        xml = ET.fromstring(request.data)
        toUser = xml.find('ToUserName').text
        fromUser = xml.find('FromUserName').text
        msgType = xml.find("MsgType").text
        createTime = xml.find("CreateTime")
        # 判断类型并回复
        if msgType == "text":
            content = xml.find('Content').text
            search_car = searchCarInNeo4j()
            try:
                result = search_car.search(content)
            except:
                result = ['不好意思，小柯基遇到了点小问题。咱们来聊点别的吧。']
            print(content)
            if result == []:
                answer = '小柯基没找到相关信息，Sorry啦。'
            else:
                for i in result:
                    answer += i + '\n\n'
            return reply_text(fromUser, toUser, answer)
        else:
            return reply_text(fromUser, toUser, "我只懂文字")

def reply_text(to_user, from_user, content):
    """
    以文本类型的方式回复请求
    """
    return """
    <xml>
        <ToUserName><![CDATA[{}]]></ToUserName>
        <FromUserName><![CDATA[{}]]></FromUserName>
        <CreateTime>{}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{}]]></Content>
    </xml>
    """.format(to_user, from_user, int(time.time() * 1000), content)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
