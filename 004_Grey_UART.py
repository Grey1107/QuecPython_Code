import log
import utime
import _thread
import checkNet
import ubinascii
from machine import Pin
from machine import UART

state = 1
uart = None

# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_Socket<=>UART"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


# | 参数      | 参数类型 | 说明                | 类型      |
# | -------- | ------- | ------------------ | -------- |
# | CRITICAL | 常量     | 日志记录级别的数值 50 | critical |
# | ERROR    | 常量     | 日志记录级别的数值 40 | error    |
# | WARNING  | 常量     | 日志记录级别的数值 30 | warning  |
# | INFO     | 常量     | 日志记录级别的数值 20 | info     |
# | DEBUG    | 常量     | 日志记录级别的数值 10 | debug    |
# | NOTSET   | 常量     | 日志记录级别的数值 0  | notset   |
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
log = log.getLogger("Grey")  # 获取logger对象，如果不指定name则返回root对象，多次使用相同的name调用getLogger方法返回同一个logger对象


def hex2char(char):
    temp1 = char >> 4
    if temp1 > 9:
        temp1 = temp1+65-10
    else:
        temp1 = temp1+48
    char1 = chr(temp1)
    temp2 = char & 0x0f
    if temp2 > 9:
        temp2 = temp2+65-10
    else:
        temp2 = temp2+48
    char2 = chr(temp2)
    print('****** hex2char结果{} ******\r\n'.format(char1+char2))
    return char1+char2

# * 参数1：引脚号
#         EC100YCN平台引脚对应关系如下：
#         GPIO1 – 引脚号22
#         GPIO2 – 引脚号23
#         GPIO3 – 引脚号178
#         GPIO4 – 引脚号199
#         GPIO5 – 引脚号204
#
#         EC600SCN平台引脚对应关系如下：
#         GPIO1 – 引脚号12
#         GPIO2 – 引脚号13
#         GPIO3 – 引脚号14
#         GPIO4 – 引脚号15
#         GPIO5 – 引脚号16
# * 参数2：direction
#         IN – 输入模式
#         OUT – 输出模式
# * 参数3：pull
#         PULL_DISABLE – 禁用模式
#         PULL_PU – 上拉模式
#         PULL_PD – 下拉模式
# * 参数4：level
#         0 设置引脚为低电平
#         1 设置引脚为高电平

# * 参数1：端口
#        注：EC100YCN平台与EC600SCN平台，UARTn作用如下
#        UART0 - debug PORT
#        UART1 – BT PORT
#        UART2 – MAIN PORT
#        UART3 – USB CDC PORT
# * 参数2：波特率
# * 参数3：data bits  （5~8）
# * 参数4：Parity  （0：NONE  1：EVEN  2：ODD）
# * 参数5：stop bits （1~2）
# * 参数6：flow control （0: FC_NONE  1：FC_HW）


def uart_read():
    log.debug("uartread start!")
    global state
    global uart

    while 1:
        # while readnum:
        # readnum -= 1
        # 返回是否有可读取的数据长度
        msglen = uart.any()
        # 当有数据时进行读取
        if msglen:
            msg = uart.read(msglen)
            # print(type(msg))
            # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            utf8_msg = msg.decode()
            if "Usart End" in utf8_msg:
                break
            else:
                # 发送数据
                log.info("-----------------------UartRead Msg----------------------\r\n{}".format(utf8_msg))
                uart.write("uartread msg: {}".format(utf8_msg))
        else:
            utime.sleep_ms(1)
            continue
    state = 0
    log.debug("uartread end!")


if __name__ == "__main__":
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    # utime.sleep(5)
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    # 【本例程可以屏蔽下面这一行！】
    # checknet.wait_network_connected()
    log.debug("main start!")

    gpio11 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PD, 0)  # EC600S/EC600N使用
    gpio11.write(0)  # EC600S/EC600N使用
    gpio12 = Pin(Pin.GPIO12, Pin.OUT, Pin.PULL_PD, 0)  # EC600U_you使用
    gpio12.write(1)  # EC600U_you使用
    # uart = UART(UART.UART1, 115200, 8, 0, 1, 1)
    uart = UART(UART.UART2, 115200, 8, 0, 1, 0)  # EC600S/EC600N使用

    # 串口发送数据定义
    Hex_Data = '\xab\xcd\xef\x12\x34\x56\x78\x90\xAB\xCD\xEF'
    data = 'abcdef1234567890ABCDEF'
    data_bytes = ubinascii.unhexlify(data)
    data_byte = data_bytes.decode()

    # ASCII码格式发送
    uart.write("{}\r\n".format(data))
    uart.write("{}\r\n".format(data_bytes))

    # HEX码格式发送
    uart.write("{}".format('\xab''\xcd''\xef''\x12''\x34''\x56''\x78''\x90''\xAB''\xCD''\xEF'))
    uart.write("{}".format(Hex_Data))
    uart.write("{}".format(data_byte))
    print("{}".format(data_byte))

    _thread.start_new_thread(uart_read, ())  # 创建一个线程来监听接收uart消息
    while 1:
        if state:
            utime.sleep_ms(1)
            pass
        else:
            break
    log.debug("main end!")
