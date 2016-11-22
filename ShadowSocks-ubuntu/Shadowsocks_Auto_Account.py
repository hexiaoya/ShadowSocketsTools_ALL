# -*- coding: utf-8 -*-
"""
功能：翻墙，自动配置ShadowSocks
测试环境：win10 python2.7
使用：放到ShadowSocks同目录下，运行，第一次需要打开ShadowSocks随便配置，生成配置文件
原理：
自动获取 http://ishadowsocks.com/ 账号信息
更新 gui-config.json 配置文件
重启 Shadowsocks.exe
"""

import re
import urllib2
import os

def find_gui_json_file(data):
    pattern=re.findall('''\s*"server": "(.*)",\s*"server_port": (\d*),\s*"password": "(.*)",''',data)
    print pattern
    return pattern

def get_data_from_web():
    data=urllib2.urlopen('http://ishadowsocks.com/').read()
    pattern=re.compile('''
\s*<div class=".*">
\s*<h4>[ABC]服务器地址:(.*)</h4>
\s*<h4>端口:(.*)</h4>
\s*<h4>[ABC]密码:(.*)</h4>
    ''')
    match=pattern.findall(data)
    print match
    return match

def read_json_conf():
    ssfile=open('./gui-config.json','r')
    datastr=ssfile.read()
    ssfile.close()
    return datastr

def write_json_conf(datastr):
    ssfile=open('./gui-config.json','w')
    ssfile.write(datastr)
    ssfile.close()

def update_conf():
    match=get_data_from_web()
    datastr=read_json_conf()
    #print datastr
    pattern=find_gui_json_file(datastr)
    
    str_index=0
    for i in range(min(len(match),len(pattern))):
        str_index=datastr.find(pattern[i][0],str_index+1)
        #print str_index
        for j in range(3):
            data_temp=datastr[str_index:].replace(pattern[i][j],match[i][j],1)
            datastr=datastr[:str_index]+data_temp
            
    pattern=find_gui_json_file(datastr)
    write_json_conf(datastr)

if __name__ == '__main__':   
    print '当前文件路径: '+os.getcwd()
    os.popen('sslocal -d stop -c gui-config.json')
    update_conf()
    os.popen('sslocal -d start -c gui-config.json')
    os.popen("export http_proxy='http://127.0.0.1:9988'")
