# 串口发送脚本
import serial
import time
import numpy as np
import pandas as pd
import datetime


port = 'COM6' # 修改端口
baud = 9600 # 波特率
timeout = 1 # 超时时间

test1=b'\x05\x00\x01\x1a\x00\x02\x00\x07\x01\x14\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x0d'
# # 帧测试：发送数据2*9+2个字节，共20个字节，帧20+11=31个字节
#此时接收端应接收有效数据100个字节(0x64)，在接收端第八个字节显示，第七个字节是接收信号强度

test2=b'\x05\x00\x01\x6a\x00\x02\x00\x07\x01\x64\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x02\x03\x04\x05\x06\x07\x08\x09\x01\x0e'
# # 长帧测试：发送数据11*9+1=100个字节，共100个字节，帧100+11=111个字节
#此时接收端应接收有效数据20个字节(0x14)，在接收端第八个字节显示，第七个字节是接收信号强度


if __name__ == '__main__':
    ser = serial.Serial(port, baud, timeout=1)
    cnt=1
    t=10 #发射次数
    with open('C:/Users/nimiao/Desktop/lora_mesh_eval-master/lora_mesh_eval-master/test_tx_1.txt','w+') as f:
        while cnt<=t:
            result = ser.write(test2)
            usedata=result-11
            print("发射第{0}帧,有效数据为{1}字节，{2}".format(cnt,usedata,datetime.datetime.now().strftime('%H:%M:%S.%f'))) #datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S.%f')
            f.write("{}\n".format(datetime.datetime.now().strftime('%H:%M:%S.%f')))
            cnt += 1
            time.sleep(0.35)


