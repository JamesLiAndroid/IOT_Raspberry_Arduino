#!/usr/bin/env python
# encoding: utf-8

import pyfirmata
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

board = pyfirmata.Arduino('/dev/ttyUSB0')
switch_pin = board.get_pin('d:4:i')
it = pyfirmata.util.Iterator(board) # 使用单独的迭代器线程来监听开关的状态读取
it.start() # 开启线程 
switch_pin.enable_reporting() # 启用报告功能

try:
    while True:
        input_state = switch_pin.read()
        print("input_state: %s" % input_state)
        if input_state == False: # 按键按下
            # 发送消息 
            print('Button Pressed')
            publish.single("abc","1234567",hostname="114.215.93.235",protocol=mqtt.MQTTv311) # 发送广播消息到服务器
            print("============================")
            time.sleep(0.2)
except KeyboardInterrupt:
    board.exit()
