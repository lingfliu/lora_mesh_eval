from byte_parse import int2bytes
import struct
# 数据传输协议， 声明部分

MSG_TYPE_PLAIN = 0
MSG_TYPE_CHUNK_META = 1
MSG_TYPE_CHUNK_DATA = 2

MAX_PAYLOAD_LEN = 105


"""
    数据编码
    :param dest 接收端地址 （1个字节）
    :param msg_type 消息类型: 普通数据， 图像文件元数据， 图像文件数据
    :param data 数据
    :param depth 网络深度，默认为7
    :param ack 是否需要ack，默认为需要
"""
def encode(dest, msg_type, data, ack=True, depth=7):
    bs = bytearray(data) # 转换为字节数
    l = len(bs) # 数据长度

    # 如果超出最大长度，返回错误
    if l > MAX_PAYLOAD_LEN:
        return []

    '''
    data的基本格式为：type (1byte), meta(0-4 byte), paylaod(100 - 104 byte)
    '''

    if ack:
        ack_byte = b'\x01'
    else:
        ack_byte = b'\x00'

    depth_byte = int2bytes(depth, 1, True, False)

    route_byte = b'\x01'
    dest = dest.to_bytes(2, 'big')

    if msg_type == MSG_TYPE_CHUNK_DATA:
        l = len(data)
        l_enc = l.to_bytes(4, 'big', signed=False)
        bs = msg_type.to_bytes(1, 'big') + l_enc + bs
    else:
        bs = msg_type.to_bytes(1, 'big') + bs
    super_payload = dest + ack_byte + depth_byte + depth.to_bytes(1, 'big') + route_byte + bs

    super_payload_len = len(super_payload).to_bytes(1,'big', signed=False)

    package = b'\x05\x00\x01' + super_payload_len + super_payload

    xor = package[0]
    for b in package[1:]:
        xor = xor ^ b

    return package + xor.to_bytes(1, 'big', signed=False)



"""
读取用户数据并解码
"""
def decode(bytes):
    msg_type = int.from_bytes(bytes[0:1], byteorder='big', signed=False)
    if msg_type == MSG_TYPE_PLAIN:
        return msg_type, bytes[1:]
    elif msg_type == MSG_TYPE_CHUNK_META:
        chunk_len = int.from_bytes(bytes[1:5], byteorder='big', signed=False)
        return msg_type, chunk_len
    else:
        idx = int.from_bytes(bytes[1:5], byteorder='big', signed=False)
        return msg_type, (idx, bytes[5:])

"""
数据拆包
"""
def chunk_split(data):
    idx = 0
    l = len(data)
    step = MAX_PAYLOAD_LEN - 5
    chunk_list = []
    while idx + step <= l:
        chunk = data[idx:idx+step] # 105 - 5 = 100
        idx += step
        chunk_list.append(chunk)
    if idx < l:
        chunk = data[idx:]
        chunk_list.append(chunk)

    return chunk_list