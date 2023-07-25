from byte_parse import int2bytes, bytes2int
import struct

""" 
YL_800MN 串口数据协议
依据文档：2031352324YL-800MN系列MESH自组网模块规格书CN-20190730.pdf
"""

# 常量定义

# 数据类型
DATA_TYPE_PLAIN = b'\x00'
DATA_TYPE_CHUNK_META = b'\x01'
DATA_TYPE_CHUNK_DATA = b'\x02'

DATA_MAX_PAYLOAD_LEN = 105

# 消息类型
MSG_TYPE_RW = b'\x01' #串口读写
MSG_TYPE_CFG = b'\x05' #组网配置

# 消息命令类型

#TYPE = 01
MSG_CMD_WRITE_CFG_REQ = b'\x01' #写入配置请求
MSG_CMD_WRITE_CFG_ACK = b'\x81' #写入配置应答
MSG_CMD_READ_CFG_REQ = b'\x02' #读配置请求
MSG_CMD_READ_CFG_ACK = b'\x82' #读配置应答
MSG_CMD_READ_ROUTE_TABLE_REQ = b'\x03' #读路由表请求
MSG_CMD_READ_ROUTE_TABLE_ACK = b'\x83' #读路由表应答
MSG_CMD_READ_VER_REQ = b'\x06' #读版本请求
MSG_CMD_READ_VER_ACK = b'\x86' #读版本应答
MSG_CMD_RESET_REQ = b'\x07' #复位请求
MSG_CMD_RESET_ACK = b'\x87' #复位应答
MSG_CMD_READ_ROUTE_REQ = b'\x08' #读路由请求
MSG_CMD_RESET_ROUTE_ACK = b'\x88' #读路由应答
#TYPE = 05
MSG_CMD_READ_ROUTE_ALL_REQ = b'\x01' #读整个路由表请求
MSG_CMD_READ_ROUTE_ALL_ACK = b'\x81' #读整个路由表应答


def encode_data(dest, data_type, data, ack=True, depth=7):
    bs = bytearray(data) # 转换为字节数
    l = len(bs) # 数据长度
    if l > DATA_MAX_PAYLOAD_LEN:
        return []

    if ack:
        ack_byte = b'\x01'
    else:
        ack_byte = b'\x00'

    depth_byte = int2bytes(depth, 1)

    route_mode_byte = b'\x01' # 00禁止路由，01自动路由，02强制路由，03源路由

    l_byte = int2bytes(l+1, 1)

    if data_type == DATA_TYPE_CHUNK_DATA:
        bs = data_type + bs
    elif data_type == DATA_TYPE_CHUNK_META:
        meta = data
        bs = data_type + meta
    elif data_type == DATA_TYPE_PLAIN:
        bs = data_type + bs
    else:
        bs = []

    bs = dest + ack_byte + depth_byte + route_mode_byte + l_byte + bs

    return bs

""" 
calculate the xor of a list of bytes
"""
def xor(bs):
    x = 0
    for b in bs:
        x ^= b
    return x


def encode_msg(msg_type, bs):
    # pp 11
    msg = msg_type + b'\x00' + int2bytes(len(bs), 2) + bs
    msg += xor(msg).to_bytes(1, 'big')

    return msg

"""
对报文进行解码
"""
def decode_msg(bs):
    # parse the data
    msg_type = list(bs)[0]
    data_len = list(bs)[3]
    if data_len + 5 != len(bs):
        return []

    msg_cmd_type = bs[2]

    data = bs[4:-1]
    data = data[6:]

    data_type = data[0].to_bytes(1, 'big')

    if data_type == DATA_TYPE_PLAIN:
        return DATA_TYPE_PLAIN, data[1:]
    elif data_type == DATA_TYPE_CHUNK_META:
        return DATA_TYPE_CHUNK_META, bytes2int(data, offset=1, l=4)
    elif data_type == DATA_TYPE_CHUNK_DATA:
        data_idx = data[1:5]
        payload = data[5:]
        return DATA_TYPE_CHUNK_DATA, (bytes2int(data_idx, offset=0, l=4, msb=True), payload)
    else:
        return []

"""
数据拆包
"""
def chunk_split(data):
    idx = 0
    l = len(data)
    step = DATA_MAX_PAYLOAD_LEN - 5
    chunk_list = []
    while idx + step <= l:
        chunk = data[idx:idx+step] # 105 - 5 = 100
        idx += step
        chunk_list.append(chunk)
    if idx < l:
        chunk = data[idx:]
        chunk_list.append(chunk)

    return chunk_list