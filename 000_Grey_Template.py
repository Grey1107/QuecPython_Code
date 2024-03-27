# -*- coding: UTF-8 -*-
# 导入模块 & 全局变量
if True:  # 方便代码折叠, 可不要. 
    import log, utime, _thread, checkNet
    from machine import WDT
    # 实际项目代码建议main.py开启便开启看门狗功能. 
    DebugFlag = True  # True & False 看门功能
    if DebugFlag == False:
        wdt = WDT(30)  # 启动看门狗. 参数说明: 设置软狗检测时间, 单位(s) 

    # 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
    # 在执行用户代码前，会先打印这两个变量的值。
    PROJECT_NAME = "Grey_Tempplate"
    PROJECT_VERSION = "0.0.0"
    checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

    # | 参数      | 参数类型 | 说明                | 类型      |
    # | -------- | -------- | ------------------- | -------- |
    # | CRITICAL | 常量     | 日志记录级别的数值 50 | critical |
    # | ERROR    | 常量     | 日志记录级别的数值 40 | error    |
    # | WARNING  | 常量     | 日志记录级别的数值 30 | warning  |
    # | INFO     | 常量     | 日志记录级别的数值 20 | info     |
    # | DEBUG    | 常量     | 日志记录级别的数值 10 | debug    |
    # | NOTSET   | 常量     | 日志记录级别的数值 0  | notset   |
    log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
    Grey_log = log.getLogger("Grey")


# 线程保护测试例程
def Grey():
    global Grey_log
    a = 0
    while True:
        utime.sleep_ms(60000)
        a += 1
        Grey_log.debug('Grey running: {:03d} Minute'.format(a))
        if a == 60:
            _thread.delete_lock(0)  # 就是为了抛异常
            break


# 线程监控函数, 实际线程以参数传入
def thread(func):
    global Grey_log
    while True:
        try:
            func()
        except Exception as e:
            Grey_log.error("{}Because of the[{}] caught exception,restart now!!!!".format(func, e))
        finally:
            Grey_log.critical('End of the thread\r\n\r\n')
            pass  # 客户自己实现. 


if __name__ == "__main__":
    Grey_log.info('------------------------运行时间统计开始------------------------')
    tm = utime.ticks_ms()  # 返回不断递增的毫秒计数器, 在某些值后会重新计数(未指定). 计数值本身无特定意义, 只适合用在ticks_diff()函数中. 
    if DebugFlag == False:
        utime.sleep(5)  # 手动运行本例程时, 可以去掉该延时, 如果将例程文件名改为main.py, 希望开机自动运行时, 需要加上该延时. 
    checknet.poweron_print_once()  # CDC口打印poweron_print_once()信息, 注释则无法从CDC口看到下面的poweron_print_once()中打印的信息. 

    # 如果用户程序包含网络相关代码必须执行wait_network_connected()等待网络就绪(拨号成功). 
    # 如果是网络无关代码, 可以屏蔽 wait_network_connected(). 
    if DebugFlag == False:
        stagecode, subcode = checknet.wait_network_connected(120)
    elif DebugFlag == True:
        stagecode, subcode = checknet.wait_network_connected(1)
    else:
        pass
    Grey_log.debug('stagecode: {}   subcode: {}'.format(stagecode, subcode))
    # 网络已就绪: stagecode = 3, subcode = 1
    # 没插sim卡: stagecode = 1, subcode = 0
    # sim卡被锁: stagecode = 1, subcode = 2
    # 超时未注网: stagecode = 2, subcode = 0
    if stagecode != 3 or subcode != 1:
        Grey_log.warning('【Look Out】 Network Not Available\r\n')
    else:
        Grey_log.error('【Look Out】 Network Ready\r\n')
    Grey_log.info('--------------------------------------------------------------')
    Grey_log.info('最终耗时: {:.3f}s'.format(utime.ticks_diff(utime.ticks_ms(), tm)/1000))
    Grey_log.info('------------------------运行时间统计结束------------------------')
    Grey_log.info('User Code Start\r\n\r\n')

    if DebugFlag == False:
        while True:
            Grey_log.debug('Feed Dogs')
            wdt.feed()  # 喂狗
            utime.sleep(5)
            # wdt.stop()  # 关闭软狗

            Grey_log.info('User Code End\r\n\r\n')
    elif DebugFlag == True:
        _thread.start_new_thread(thread, (Grey,))  # 线程保护测试示例. 

        Grey_log.info('User Code End\r\n\r\n') 
