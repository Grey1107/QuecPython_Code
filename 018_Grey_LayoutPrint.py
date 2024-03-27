# flag = 5
# while flag:
#     print("hello word\r\n")
#     flag -= 1


data = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ\r\n'
try:
    while True:
        length = len(data)
        print('打印字节长度: {:03d}\r\n'.format(length))
        for i in range(0, length, 10):
            print('{}'.format(data[i:i + 10]))
        for i in range(0, length, length):
            print('\r\n{}'.format(data[i:i + length]))
        break
except StopIteration:
    print('\r\n停止迭代!!!！')
print('\r\n结束!!!！')
