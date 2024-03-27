# 导入模块
import usocket
import ujson
import log
import utime
import checkNet
import _thread
from machine import Pin
from machine import UART


main_flag = 1


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_GPIO"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


# | 参数      | 参数类型 | 说明                |
# | -------- | ------- | ------------------ |
# | CRITICAL | 常量     | 日志记录级别的数值 50 |
# | ERROR    | 常量     | 日志记录级别的数值 40 |
# | WARNING  | 常量     | 日志记录级别的数值 30 |
# | INFO     | 常量     | 日志记录级别的数值 20 |
# | DEBUG    | 常量     | 日志记录级别的数值 10 |
# | NOTSET   | 常量     | 日志记录级别的数值 0  |
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
Grey_log = log.getLogger("Grey")


def gpio_test():
    global main_flag
    count = 5  # 闪烁次数
    LED_State = 0

    lcd = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PU, 0)
    key1 = Pin(Pin.GPIO13, Pin.IN, Pin.PULL_PU, 1)
    key2 = Pin(Pin.GPIO12, Pin.IN, Pin.PULL_PU, 1)
    while count:
        count -= 1
        utime.sleep_ms(500)
        if lcd.read() == 0:
            gpio1_state = 1
        else:
            gpio1_state = 0
        lcd.write(gpio1_state)  # 设置gpio1 输出
        Grey_log.info("GPIO levels:{}  running:{:0>2d}".format(lcd.read(), count))  # 获取gpio的当前高低状态
    Grey_log.debug("\r\nLED闪烁结束, 进入按键控制!\r\n")
    while True:
        if key1.read() == 0:
            utime.sleep_ms(10)
            if key1.read() == 0:
                Grey_log.info("跳出循环,GPIO13电平:{}".format(key1.read()))
                break
        if key2.read() == 0:
            while key2.read() == 0:
                pass
            if LED_State == 0:
                LED_State = 1
                lcd.write(0)
                Grey_log.info("LED关闭")
            elif LED_State == 1:
                LED_State = 0
                lcd.write(1)
                Grey_log.info("LED开启")
        pass
    main_flag = 0


if __name__ == "__main__":
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    # utime.sleep(5)
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    # 【本例程可以屏蔽下面这一行！】
    checknet.wait_network_connected()
    Grey_log.info('========================Init========================\r\n')

    _thread.start_new_thread(gpio_test, ())  # 创建一个线程
    while True:
        if main_flag:
            pass
        else:
            break
    Grey_log.info('========================Main END========================\r\n')
