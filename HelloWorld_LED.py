#!/usr/bin/env python
# encoding: utf-8

import pyfirmata
import time

import sys
import paho.mqtt.client as mqtt # 第一步,导入我们需要的包

board=pyfirmata.Arduino('/dev/ttyUSB0') # 初始化设备,这个地方设备名称上可能不同,有可能是/dev/ttyACM0

led_pin = board.get_pin('d:10:o') # 初始化端口,d代表数字的,10代表10号端口,o代表输出的意思

print("端口初始化!")

def output_level(): # 控制LED的函数
    try:
        while True:
            led_pin.write(1)
            time.sleep(0.5)
            led_pin.write(0)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

# mqtt中的四个回调方法
def on_connect(mqttc,obj,flag,rc):
    print("rc : "+str(rc))

def on_message(mqttc,obj,msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    #print("mid:"+str(mid))
    output_level()

def on_publish(mqttc,obj,mid):
    print("mid:"+str(mid))
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_subscribe(mqttc,obj,mid,granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

mqttc = mqtt.Client(protocol = mqtt.MQTTv311) # 初始化mqtt客户端,注意这里必须指定协议版本为3.1.1,否则无法与服务器通信
                                                # 会出现协议头不正确的错误,导致通信无法继续
mqttc.on_message=on_message  # 回调方法的赋值
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("114.215.93.235",1883,60) # 连接服务器

mqttc.subscribe("abc",0) # 消息订阅,我们从手机上来控制

mqttc.loop_forever() # 死循环,堵塞线程,运行
