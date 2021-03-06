# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import control as driver
import os
IS_SERVERLESS = bool(os.environ.get('SERVERLESS'))
cookie = os.environ.get('cookie')
app = Flask(__name__)

config = {
    #为了方便二次开发，此处可添加多个用户信息，格式[{'name':'名称1','cookie':'京豆cookie'}, {'name':'名称2','cookie':'京豆cookie'}]
    'userInfo': [
        {
            "name": "FSHOW",#账号标识名称，可任意填写
            "cookie": cookie
        }
    ],

    #程序功能设置(暂未开发)
    'set':{
        '消息通知':{
            '企业微信':{},
            '钉钉':{},
            '邮件':{}
        },
    }
}


@app.route("/")
def index():
  data = driver.control(config)
  kwgt_activateDay =""
  kwgt_beanNum =""
  num = 1
  ##将数据改成此格式是为了kwgt更容易的提取指定信息
  for i in data['changesData'][0]:
      createText1 = f'''++changesDay{num}++{i}--changesDay{num}--'''
      createText2 = f'''++changesBean{num}++{data['changesData'][1][num-1]}--changesBean--'''
      kwgt_activateDay += createText1
      kwgt_beanNum += createText2
      num += 1
  kwgt = f'''{kwgt_activateDay}{kwgt_beanNum}'''

  return kwgt

@app.route("/cookie")
def getCookie():
    return str(cookie)
# 启动服务，监听 9000 端口，监听地址为 0.0.0.0
app.run(debug=IS_SERVERLESS != True, port=9000, host='0.0.0.0')
