#-*- coding: utf-8 -*-
__author__ = 'qiangwang'

import time
import hashlib
import struct


def generateKey(uid):

    #魔术数字
    magic = 123456789
    interval = 3 * 24 * 3600 * 1000
    length = 16
    fint = 123456
    uid = int(uid)
    t = int(time.time() * 1000) + interval
    data = struct.pack('>iIq', fint, uid, t)
    moredata = struct.pack('>bbbb', -45, -31, -105, 22)
    data += moredata
    dataarray = struct.unpack('>20b', data)

    md5obj = hashlib.md5()
    md5obj.update(data)
    hash = md5obj.digest()

    hasharray = struct.unpack('>16b', hash)
    result = []
    for index in range(0, length * 2):
        result.append(0)
    for index in range(0, length):
        result[2 * index] = (hasharray[index] & 0x03) | ((dataarray[index] & 0x0f) << 2) | ((hasharray[index] & 0x0C) << 4)
        result[2 * index + 1] = (hasharray[index] & 0xC0) | ((dataarray[index] & 0xf0) >> 2) | ((hasharray[index] &0x30) >> 4)

    buf = []
    for index in range(0, length * 2 * 2):
        buf.append('\0')
    for index in range(0, length * 2):
        b = hex(((result[index] & 0xf0) >> 4))
        buf[2 * index] = b
        b = hex((result[index] & 0x0f))
        buf[2 * index + 1] = b
    out = ''
    for index in range(0, length * 2 * 2):
        out += str(buf[index]).replace('0x', '')

    return out

if __name__ == '__main__':
    alk = generateKey(123456)
    print alk