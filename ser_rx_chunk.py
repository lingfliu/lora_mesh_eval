# 拆包接收图像文件
import serial
import time
import base64
import cv2
from proto import chunk_split, encode, decode, MSG_TYPE_PLAIN, MSG_TYPE_CHUNK_DATA, MSG_TYPE_CHUNK_META
from byte_parse import int2bytes

SER_STATE_IDLE = 0
SER_STATE_PLAIN = 1
SER_STATE_CHUNK = 2

port = 'COM9' # 修改端口
baud = 115200 # 波特率
timeout = 1# 超时时间

ser_state = SER_STATE_IDLE # idle 状态
chunk_list = [] # chunk list
chunk_len = 0
chunk_idx = 0

if __name__ == '__main__':
    ser = serial.Serial(port, baud, timeout=1)

    # 发送成功, 否则此处死循环
    # TODO: ACK handling to avoid dead loop
    print("开始接收！")
    while True:
        if ser.in_waiting:
            rx = ser.read(ser.in_waiting).decode('ascii')
            msg_type, data = decode(rx)

            if msg_type == MSG_TYPE_PLAIN:
                if ser_state == SER_STATE_CHUNK:
                    # 丢弃该包
                    print("receive plain data while in chunk mode", str(data))
                else:
                    ser_state = SER_STATE_PLAIN
                    print("receive plain data", str(data))
                    ser_state = SER_STATE_IDLE

            elif msg_type == MSG_TYPE_CHUNK_META:
                ser_state = SER_STATE_CHUNK
                chunk_len = data
                chunk_idx = 0

            # TODO: 核对这里in_waiting是不是无法一次性接收到100个字节
            elif msg_type == MSG_TYPE_CHUNK_DATA:
                if not ser_state == SER_STATE_CHUNK:
                    # 不允许两种状态混合传输，如果传输图像，一定要等所有数据传输完，否则丢弃该包
                    print("receive chunk data while in plain", str(data))
                else:
                    idx = data[0]
                    chunk = data[1]

                    if idx == 0:
                        ser_idx = 0
                        chunk_list.append(chunk)
                    else:
                        if ser_idx == idx - 1:
                            chunk_list.append(chunk)
                            ser_idx = idx

                        if ser_idx == chunk_len - 1:
                            # 接收完毕
                            ser_state = SER_STATE_IDLE
                            str = b''.join(chunk_list)
                            img_decode = cv2.imdecode(base64.b64decode(str), cv2.IMREAD_COLOR)
                            cv2.imwrite('test_img_base64.jpg', img_decode)
                            break



