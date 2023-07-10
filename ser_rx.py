# 串口接收脚本
import serial
import time


port = 'COM3' # 修改端口
baud = 115200 # 波特率
timeout = 1 # 超时时间

# 这里配置固定的测试字符串， 接收端也要配置固定的测试字符串
test_str = "12345678901234567890123456789012345678901234567890123456789012345678901234567890"

if __name__ == '__main__':
    ser = serial.Serial(port, baud, timeout=1)

    # 配置 lora mesh dtu (AT mode)
    config_str = [
        "AT+CFG=433000000,20,7,7,1,1,0,0,0,0,3000,8,4\r\n",
        "AT+CFG=433000000,20,7,7,1,1,0,0,0,0,3000,8,4\r\n"
    ]

    for cfg in config_str:
        res = ser.write(cfg.encode('ascii'))
        if not res == len(cfg):
            print("config dtu failed")
            exit(1)

    # 报文传输计数器
    cnt = 0

    while True:
        if ser.in_waiting:
            rx = ser.read(ser.in_waiting).decode('ascii')
            print("read result{0} count{1} at {2}".format(rx, cnt, time.time()))
            cnt += 1