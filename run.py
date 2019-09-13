# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/wechat", methods=["GET","POST"])
def weixin():
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

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
