# 拆包发送图像文件
import serial
import time
import base64
import cv2
import numpy as np
from proto_yl80mn import encode_msg, encode_data, decode_msg, chunk_split, DATA_TYPE_CHUNK_META, DATA_TYPE_CHUNK_DATA, DATA_TYPE_PLAIN, MSG_TYPE_RW, MSG_TYPE_CFG
from byte_parse import int2bytes


port = 'COM6' # 修改端口
baud = 115200 # 波特率
timeout = 1 # 超时时间

rx_addr = b'\x00\x02' # 接收端地址

if __name__ == '__main__':

    # 读取图像文件并编码为base64
    img = cv2.imread('test_img.jpg')
    jpg_img = cv2.imencode('.jpg', img)[1]
    b64_img = base64.b64encode(jpg_img.tobytes())

    # 解码方式演示
    # b64_decode = base64.b64decode(b64_img)
    # img_decode = cv2.imdecode(np.frombuffer(b64_decode, dtype=np.uint8), cv2.IMREAD_COLOR)
    # cv2.imwrite('test_img_base64.jpg', img_decode)

    # 数据拆包
    chunk_list = chunk_split(b64_img)

    meta = len(chunk_list)
    data = int2bytes(meta, 4, 'big', signed=False)
    # send meta
    dat_bs = encode_data(rx_addr, DATA_TYPE_CHUNK_META, data)
    msg_bs = encode_msg(MSG_TYPE_RW, dat_bs)

    # 传输meta数据
    ser = serial.Serial(port, baud, timeout=1)
    ser.write(msg_bs)

    # # 解码演示，这里对整体报文进行解码
    # data = decode_msg(msg_bs)

    msg_list = []
    for idx, chunk in enumerate(chunk_list):
        chunk = int2bytes(idx, 4) + chunk
        dat_bs = encode_data(rx_addr, DATA_TYPE_CHUNK_DATA, chunk)
        msg_bs = encode_msg(MSG_TYPE_RW, dat_bs)
        msg_list.append(msg_bs)

    # 发送数据
    for msg in msg_list:
        ser.write(msg_bs)
        time.sleep(0.35) # 最小间隔发射保障

    # 接收解码数据演示
    # data_decode = b''
    # for msg in msg_list:
    #     (idx, chunk) = decode_msg(msg)
    #     data_decode = data_decode + chunk
    #
    #
    # # 解码拼接的数据
    # b64_decode = base64.b64decode(data_decode)
    # img_decode = cv2.imdecode(np.frombuffer(b64_decode, dtype=np.uint8), cv2.IMREAD_COLOR)
    # cv2.imwrite('test_img_decode.jpg', img_decode)