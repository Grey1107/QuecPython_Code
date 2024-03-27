# 导入模块
import log
import utime
import checkNet
import _thread
import wifiScan

main_flag = 1

# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_WIFI_SCAN"
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


def wifiscan_cb(args):
    global main_flag

    print('wifi list:{}'.format(args))
    main_flag = 0


def wifiscan_test():
    global main_flag

    if wifiScan.support():
        Grey_log.info("硬件支持wifiscan\r\n")
        if not wifiScan.getState():
            Grey_log.info("wifiscan未开启\r\n")
            # wifiScan.setConfig(500, 2, 6, 3, 0)  # 设置wifiScan功能配置参数, RDA使用
            wifiScan.setConfig(5, 2, 6, 3, 0)  # 设置wifiScan功能配置参数, ASR使用
            wifiScan.control(1)  # 开启wifiscan
            Grey_log.info(wifiScan.getConfig())  # 获取wifiScan功能配置参数
            wifiScan.setCallback(wifiscan_cb)
            wifiScan.asyncStart()
            Grey_log.info("等待输出WiFi列表\r\n")
        else:
            Grey_log.info("wifiscan已开启\r\n")
            wifiScan.control(0)  # 关闭wifiscan
            main_flag = 0
    else:
        Grey_log.info("硬件不支持wifiscan\r\n")
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

    _thread.start_new_thread(wifiscan_test, ())  # 创建一个线程
    while True:
        if main_flag:
            utime.sleep_ms(1)
            pass
        else:
            break
    Grey_log.info('========================Main END========================\r\n')
