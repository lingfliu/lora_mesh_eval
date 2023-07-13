# 串口接收脚本
import serial
import time
import datetime


port = 'COM9' # 修改端口
baud = 9600 # 波特率
timeout = 1 # 超时时间


if __name__ == '__main__':
    ser = serial.Serial(port, baud, timeout=1)
    # command = b'\x01\x00\x01\x0D\xA5\xA5\x6C\x40\x12\x07\x17\x00\x00\x00\x02\x03\x00\x22'
    # # 参数设置：设置为模块配置频率 433MHz，发射功率 7 级，路由生存周期 24 小时，网络 ID 00 00，节点 ID 00 02，串口速率 9600bps，校验方式无校验。
    # ser.write(command)
    cnt = 1  #第一帧
    i=0
    with open('C:/Users/nimiao/Desktop/lora_mesh_eval-master/lora_mesh_eval-master/test_rx_1.txt','w+') as M: #
        while True:
            if ser.in_waiting:
                rx = ser.read(ser.in_waiting)
                i += 1
                print("{0}".format(rx))
                if i == 4:
                    print("===接收第{0}帧成功，时间为：{1}".format(cnt,datetime.datetime.now().strftime('%H:%M:%S.%f')))
                    i = 0
                    cnt += 1


