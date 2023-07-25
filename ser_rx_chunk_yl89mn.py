# 拆包接收图像文件
import serial
import time
import base64
import cv2
import numpy as np
from proto_yl80mn import encode_msg, encode_data, decode_msg, chunk_split, DATA_TYPE_CHUNK_META, DATA_TYPE_CHUNK_DATA, DATA_TYPE_PLAIN, MSG_TYPE_RW, MSG_TYPE_CFG
from byte_parse import int2bytes, bytes2int


SER_STATE_IDLE = 0
SER_STATE_PLAIN = 1
SER_STATE_CHUNK = 2

port = 'COM9' # 修改端口
baud = 115200 # 波特率
timeout = 1 # 超时时间

ser_state = SER_STATE_IDLE # idle 状态

chunk_list = b''
chunk_len = 0
chunk_idx = 0
chunk_missed = False

if __name__ == '__main__':
    ser = serial.Serial(port, baud, timeout=1)

    # 发送成功, 否则此处死循环
    print("开始接收！")
    while True:
        if ser.in_waiting:
            rx = ser.read(ser.in_waiting)
            data_type, data = decode_msg(rx)

            if data_type == DATA_TYPE_PLAIN:
                if ser_state == SER_STATE_CHUNK:
                    # 丢弃该包
                    print("receive plain data while in chunk mode", str(data))
                else:
                    ser_state = SER_STATE_PLAIN
                    print("receive plain data", str(data))
                    ser_state = SER_STATE_IDLE
            elif data_type == DATA_TYPE_CHUNK_META:
                if ser_state == SER_STATE_CHUNK:
                    # 丢弃该包
                    print("receive chunk meta data while in chunk mode", str(data))
                else:
                    chunk_len = data
                    chunk_idx = 0
                    ser_state = SER_STATE_CHUNK

            # TODO: 核对这里in_waiting是不是无法一次性接收到100个字节
            elif data_type == DATA_TYPE_CHUNK_DATA:
                idx = data[0]
                chunk = data[1]

                if idx == 0:
                    # 接收一直到ser_idx == chunk_len - 1
                    chunk_idx = idx
                    chunk_list = chunk_list + chunk
                else:
                    if chunk_idx == idx - 1:
                        chunk_list.append(chunk)
                        chunk_idx = idx
                        chunk_list = chunk_list + chunk
                    else:
                        for mi in range(idx - chunk_idx - 1):
                            print("missing chunk idx = ", chunk_idx + mi + 1)
                        chunk_idx = idx
                        chunk_missed = True
                        continue

                    if chunk_idx == chunk_len - 1:
                        # 接收完毕
                        print('接收完毕')
                        b64_decode = base64.b64decode(chunk_list)
                        img_decode = cv2.imdecode(np.frombuffer(b64_decode, dtype=np.uint8), cv2.IMREAD_COLOR)
                        cv2.imwrite('rx_img.jpg', img_decode)
                        ser_state = SER_STATE_IDLE
                        chunk_list = b''
                        chunk_len = 0
                        chunk_idx = 0
                        chunk_missed = False



