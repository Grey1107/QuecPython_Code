import uio
import uos
import utime

# r     只能读
# r+    可读可写 不会创建不存在的文件 从顶部开始写 会覆盖之前此位置的内容
# w     只能写 覆盖整个文件 不存在则创建
# w+    可读可写 如果文件存在 则覆盖整个文件 不存在则创建
# a     只能写 从文件底部添加内容 不存在则创建
# a+    可读可写 从文件顶部读取内容 从文件底部添加内容 不存在则创建
# 'r'	打开阅读（默认）
# 'w'	打开写入，首先截断文件
# 'x'	打开以独占创建，如果文件已存在则失败
# 'a'	打开写入，如果存在则附加到文件的末尾
# 'b'	二进制模式
# 't'	文本模式（默认）
# '+'	打开磁盘文件进行更新（读写）
# 'U'	通用换行模式（已弃用）

print('\r\n--------------------------读取录音文件--------------------------')
fd = uio.open('/usr/audio_test.mp3', mode='r')
ff = fd.read(10)
print("录音文件内容为: {}".format(bytearray(ff)))
fd.close()
utime.sleep(1)

print('\r\n--------------------------读取写入文件--------------------------')
fd = uio.open('/usr/audio_test.txt', mode='w')
fd.write('1234567890\r\n')
fd.close()
fd = uio.open('/usr/audio_test.txt', mode='r')
ff = fd.read(12)
print("写入文件内容为: {}".format(ff))
fd.close()
utime.sleep(1)

print('\r\n----------------------------写字符串----------------------------')
res = uos.statvfs("/usr")  # 获取文件系统状态信息
res = list(res)  # 将元组转换为数组
print("模块内存信息: {}".format(res))
def_str = '1234567890' * 2
print("写入字符信息: {}".format(def_str))
print('模块可用空间: ', res[3] * res[0])
print('字符写入空间: ', len(def_str))
if res[3] * 4096 < len(def_str):
    raise OSError("存储空间不足!")
f = open('/usr/test.txt', 'w')
f.write(def_str)    # f.write('abc456789!\n' * 410 * 2)
f.close()
f = open('/usr/test.txt', 'r')
print("读取字符信息: {}".format(f.readline()))
f.close()
utime.sleep(1)

print('\r\n-----------------------------写数组-----------------------------')
res = uos.statvfs("/usr")
res = list(res)
print("模块内存信息: {}".format(res))
arr = [0x01, 0x02, 0x03]
print("原始数组信息: {}".format(arr))
str_arr = ','.join(str(i) for i in arr)  # 变成字符串
print("写入字符信息: {}".format(str_arr))
f = open('/usr/str_arr.txt', 'w')
f.write(str_arr)
f.close()
f = open('/usr/str_arr.txt', 'r')
print("读取字符信息: {}".format(f.readline()))
f.close()
str_arr = str_arr.split(',')  # 分解字符串
print("分解字符信息: {}".format(str_arr))
list_arr = [int(i) for i in str_arr]  # 把分解后的字符串为 数字
print("分解数字信息: {}".format(list_arr))
bytearr = bytearray(list_arr)  # 可以通过串口发送 bytearr
print("bytearr信息: {}".format(bytearr))
utime.sleep(1)


# 下列代码测试前需先向模块内写入文件audio_test.mp3
# >>> import uio
# >>> fd = uio.open('/usr/audio_test.mp3', mode='r')
# >>> fd.read(10)
# 'ID3\x03\x00\x00\x00\x03;X'
# >>> fd.close()
# >>> fd = uio.open('/usr/audio_test.txt', mode='w')
#
# >>> fd.write('1234567890')
# 10
# >>> fd.close()
# >>> fd = uio.open('/usr/audio_test.txt', mode='r')
# >>> fd.read(10)
# '1234567890'
# >>> fd.close()
