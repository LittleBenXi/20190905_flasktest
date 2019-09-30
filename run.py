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
            except Exception as e:
                print(e)
                result = ['不好意思，小柯基出问题啦。']
            #print(content)
            if result == []:
                answer = '小柯基没找到相关信息，Sorry啦。'
            else:
                for i in result:
                    answer += i + '\n'
                '''
                for i in range(len(result)):
                    if i == len(result)-1:
                        answer += result[i] + '\n'
                    else:
                        answer += result[i] + '\n\n'                
                '''           
            reply_text(fromUser, toUser, answer)
            dict_1 = {'q':content,'a':answer,'user':fromUser,'time':createTime}
            with open('record.json','a') as f_obj:
                json.dump(dict_1,f_obj)
                f_obj.close()
            return True
        else:
            answer = '''Hello！我是小柯基，我可以回答一些关于汽车的问题，你可以这样问我：\n
            1.直接输入厂商名，查其生产的车型，例如：东风本田\n
            2.直接输入车型，查所有款式和价格，例如：帕萨特\n
            3.输入车型+年款+价格，查车型信息，例如：帕萨特 2019 25.39\n
            4.输入车型+地点，查经销商信息，例如：君威 青岛市城阳区; 思域 合肥\n
            5.输入生产商+地点，查经销商信息，例如：上汽大众 西安; 保时捷 青岛\n
            由于我还小，还有很多不懂的地方，你的问题我答不上来也正常。'''
            return reply_text(fromUser, toUser, answer)

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
