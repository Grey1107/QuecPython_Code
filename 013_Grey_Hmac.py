import hmac
import hmacSha1
import base64
import hashlib
import ubinascii

key = "Grey"
msg = "1234567890"

Info_1 = hmacSha1.hmac_sha1(key, msg)
print("原始运算结果码: ", Info_1)
# d2460ee5d2c98f750dc5f965aa0a4035d0bbfa71
Info_2 = base64.b64encode(bytearray(Info_1))
print("转为Base64编码: ", Info_2)
# b'ZDI0NjBlZTVkMmM5OGY3NTBkYzVmOTY1YWEwYTQwMzVkMGJiZmE3MQ=='
Info_3 = base64.b64decode(Info_2)
print("反转Base64编码: ", Info_3)
# b'd2460ee5d2c98f750dc5f965aa0a4035d0bbfa71'
Info_4 = ubinascii.unhexlify(Info_1)
print("转为二进制编码: ", Info_4)
# b'\xd2F\x0e\xe5\xd2\xc9\x8fu\r\xc5\xf9e\xaa\n@5\xd0\xbb\xfaq'
Info_5 = base64.b64encode(Info_4)
print("二进制Base64码: ", Info_5)
# b'0kYO5dLJj3UNxfllqgpANdC7+nE='

token = hmac.new(bytes(key, "utf8"), msg=bytes(msg, "utf8"), digestmod=hashlib.sha256).hexdigest()
print('sha256编码: ', token)

# import hmac
# import hmacSha1
# import base64
# import hashlib
# import ubinascii
#
# Info_1 = hmacSha1.hmac_sha1('abcdefg', 'pawn')
# print("Info_1", Info_1)
# # a1408dd56a2c448f788712dc8c32ceb1a657021c
# Info_2 = base64.b64encode(bytearray(Info_1))
# print("Info_2", Info_2)
# Info_3 = base64.b64decode(Info_2)
# print("Info_3", Info_3)
# Info_4 = base64.b64encode(bytearray(Info_2))
# print("Info_4", Info_4)
# Info_5 = base64.b64decode(Info_1)
# print("Info_5", Info_5)
# Info_6 = base64.b64encode(bytearray(Info_5))
# print("Info_6", Info_6)
# Info_7 = base64.b64encode(ubinascii.unhexlify(Info_1))
# print("Info_7", Info_7)
# Info_8 = hmac.new(bytes('abcdefg', "utf-8"), bytes('pawn', "utf-8"), hashlib.sha1).digest()
# print("Info_8", Info_8)
# Info_9 = base64.b64encode(Info_8)
# print("Info_9", Info_9)

# >>> import hmac
# >>> import hashlib
# >>> key = "abcdefg"
# >>> msg = "pawn"
# >>> token = hmac.new(bytes(key, "utf8"), msg=bytes(msg, "utf8"),digestmod=hashlib.sha256).hexdigest()
#
# >>> print(token)
# a500b3a24e6edbb104ce2ed2c35497c2baa725d3b7f40bdf7a29f086f316465a
# >>> import uhashlib as hashlib
# >>> token = hmac.new(bytes(key, "utf8"), msg=bytes(msg, "utf8"),digestmod=hashlib.sha256).hexdigest()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "hmac.py", line 138, in new
#   File "hmac.py", line 57, in __init__
# AttributeError: 'sha256' object has no attribute 'digest_size'
