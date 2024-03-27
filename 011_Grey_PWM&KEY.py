# 导入模块
import log
import utime
import dataCall             # 数据拨号
import checkNet
from misc import PWM
from machine import Pin


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "QuecPython_PWM_example"
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
pwm_log = log.getLogger("PWM")


if __name__ == '__main__':
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    # utime.sleep(5)
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    # 【本例程可以屏蔽下面这一行！】
    # checknet.wait_network_connected()

    PWM0_State = 0
    PWM0_Mun = 100
    PWM0_Toggle = 1
    pwm0 = PWM(PWM.PWM0, 0, PWM0_Mun, 150)  # 初始化一个pwm对象
    pwm0.open()  # 开启PWM输出
    # gpio13 = Pin(Pin.GPIO2, Pin.IN, Pin.PULL_PU, 1)  # V1.0板使用
    # gpio12 = Pin(Pin.GPIO1, Pin.IN, Pin.PULL_PU, 1)  # V1.0板使用
    # gpio13 = Pin(Pin.GPIO13, Pin.IN, Pin.PULL_PU, 1)
    # gpio12 = Pin(Pin.GPIO12, Pin.IN, Pin.PULL_PU, 1)
    gpio13 = Pin(Pin.GPIO4, Pin.IN, Pin.PULL_PU, 1)  # EC600U开发板使用
    gpio12 = Pin(Pin.GPIO30, Pin.IN, Pin.PULL_PU, 1)  # EC600U开发板使用
    gpio28 = Pin(Pin.GPIO28, Pin.OUT, Pin.PULL_PU, 1)  # EC600U开发板使用
    while True:
        if PWM0_Toggle == 1:
            if PWM0_Mun == 1:
                PWM0_Toggle = 0
            else:
                PWM0_Mun -= 1
                pwm0 = PWM(PWM.PWM0, 0, PWM0_Mun, 150)
                utime.sleep_ms(20)
        if PWM0_Toggle == 0:
            if PWM0_Mun == 75:
                PWM0_Toggle = 1
            else:
                PWM0_Mun += 1
                pwm0 = PWM(PWM.PWM0, 0, PWM0_Mun, 150)
                utime.sleep_ms(20)
        if gpio13.read() == 0:
            utime.sleep_ms(10)
            if gpio13.read() == 0:
                pwm_log.info("跳出循环,GPIO13电平:{}".format(gpio13.read()))
                break
        if gpio12.read() == 0:
            while gpio12.read() == 0:
                pass
            if PWM0_State == 0:
                PWM0_State = 1
                pwm0.close()
                gpio28.write(0)
                pwm_log.info("PWM关闭")
            elif PWM0_State == 1:
                PWM0_State = 0
                pwm0.open()
                gpio28.write(1)
                pwm_log.info("PWM开启")
        pass
