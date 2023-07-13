import struct

def int2bytes(val, l=4, msb=True, signed=True):
    if msb:
        return int.to_bytes(val, length=l, byteorder='big', signed=signed)
    else:
        return int.to_bytes(val, l, 'little', signed=signed)

def bytes2int(bs, offset=0, l=4, msb=True, signed=True):
    bbs = bs[offset:offset+l]
    if msb:
        return int.from_bytes(bbs, byteorder='big', signed=signed)
    else:
        return int.from_bytes(bbs, byteorder='little', signed=signed)


def double2bytes(val, l=8, msb=True):
    if (msb):
        return struct.pack(">d", val)
    else:
        return struct.pack("<d", val)

def bytes2double(bs, offset=0, l=8, msb=True):
    dbs = bs[offset:offset+l]
    if msb:
        return struct.unpack('>d', dbs)[0]
    else:
        return struct.unpack('<d', dbs)[0]

def bytes2string(bs, offset, l):
    bbs = bs[offset:offset+l]
    return bbs.decode('ASCII')
