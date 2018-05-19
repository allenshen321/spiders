# encoding:utf-8

import time
import math
import hashlib


def getASCP():
    t = int(math.floor(time.time()/1e3))
    e = hex(t).upper()
    m = hashlib.md5()
    m.update(str(t).encode('utf-8'))
    i = m.hexdigest().upper()
    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS, CP
    n = i[:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
    for c in range(5):
        r += e[c+3] + a[c]
    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS, CP


if __name__ == '__main__':
    AS, CP = getASCP()
    print(AS, CP)
