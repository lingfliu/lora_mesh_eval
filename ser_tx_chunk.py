# 拆包发送图像文件
import serial
import time
import base64
import cv2
from proto import chunk_split, encode, MSG_TYPE_PLAIN, MSG_TYPE_CHUNK_DATA, MSG_TYPE_CHUNK_META
from byte_parse import int2bytes


port = 'COM3' # 修改端口
baud = 115200 # 波特率
timeout = 1# 超时时间

rx_addr = 0x0002 # 接收端地址


if __name__ == '__main__':
    ser = serial.Serial(port, baud, timeout=1)

    # 读取图像文件并编码为base64
    img = cv2.imread('test_img.jpg')
    jpg_img = cv2.imencode('.jpg', img)[1]
    b64_img = base64.b64encode(jpg_img)

    # img_decode = cv2.imdecode(jpg_img, cv2.IMREAD_COLOR)
    #
    # cv2.imwrite('test_img_base64.jpg', img_decode)

    # TODO: 配置 lora mesh dtu (AT mode), 发射功率 2w，频段 433，自动路由
    # config_str = [
    #     "AT+CFG=433000000,20,7,7,1,1,0,0,0,0,3000,8,4\r\n",
    #     "AT+CFG=433000000,20,7,7,1,1,0,0,0,0,3000,8,4\r\n"
    # ]
    #
    # for cfg in config_str:
    #     res = ser.write(cfg.encode('ascii'))
    #     if not res == len(cfg):
    #         print("config dtu failed")
    #         exit(1)

    # 报文传输计数器
    chunk_list = chunk_split(b64_img)

    meta = len(chunk_list)
    data = int2bytes(meta, 4, 'big', signed=False)
    # send meta
    msg_byte = encode(rx_addr, MSG_TYPE_CHUNK_META, data)
    ser.write(msg_byte)

    # 发送成功, 否则此处死循环
    # TODO: ACK handling to avoid dead loop
    while True:
        if ser.in_waiting:
            rx = ser.read(ser.in_waiting).decode('ascii')
            break

    for idx, chunk in enumerate(chunk_list):
        data = int2bytes(idx, 4, 'big', signed=False) + chunk
        msg_byte = encode(rx_addr, MSG_TYPE_CHUNK_DATA, data) # 拆包发送
        ser.write(msg_byte)
        time.sleep(0.2) # TODO: 这里测试最短发射间隔
