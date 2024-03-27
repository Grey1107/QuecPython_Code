# -*- coding:utf-8 -*-

# 模块运行使用
import ubinascii
a = 'FE010C0300010E'
a_bytes = ubinascii.unhexlify(a)
print('\r\n', a_bytes, '\r\n')  # b'\xfe\x01\x0c\x03\x00\x01\x0e'
print('\r\n', a_bytes.decode(), '\r\n')  # '\x01\x0c\x03\x00\x01\x0e'

# # 仿真实验使用
# a = 'FE010C0300010E'
# a = a.replace(" ", "")
# a_bytes = bytes.fromhex(a)
# print('\r\n', a_bytes, '\r\n')
# # print(a_bytes.decode('str'))


def hex2char(data):
    temp1 = data >> 4
    if temp1 > 9:
        temp1 = temp1+65-10
    else:
        temp1 = temp1+48
    char1 = chr(temp1)
    temp2 = data & 0x0f
    if temp2 > 9:
        temp2 = temp2+65-10
    else:
        temp2 = temp2+48
    char2 = chr(temp2)
    print('****** hex2char结果{} ******\r\n'.format(char1+char2))
    return char1+char2


# res = {}
# for i in range(2):
#     res[i] = {}
#     res[i]["1"] = 0
#     res[i]["2"] = 0
#     res[i]["3"] = 0
# res[0]["2"] = 1
# print(res)
#
# a = {0: {"1": 1},
#      1: {"1": 1},
#      2: {"1": 1}
#      }
# print(a)
