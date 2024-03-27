# -*- coding: UTF-8 -*-
# 导入模块
import log
import utime
import ujson
import audio
import _thread
import checkNet
from machine import Pin


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_Test"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# | Parameter | parameter | description               | type     |
# | --------- | --------- | ------------------------- | -------- |
# | CRITICAL  | constant  | value of logging level 50 | critical |
# | ERROR     | constant  | value of logging level 40 | error    |
# | WARNING   | constant  | value of logging level 30 | warning  |
# | INFO      | constant  | value of logging level 20 | info     |
# | DEBUG     | constant  | value of logging level 10 | debug    |
# | NOTSET    | constant  | value of logging level 0  | notset   |

# | 参数      | 参数类型 | 说明                | 类型      |
# | -------- | ------- | ------------------ | -------- |
# | CRITICAL | 常量     | 日志记录级别的数值 50 | critical |
# | ERROR    | 常量     | 日志记录级别的数值 40 | error    |
# | WARNING  | 常量     | 日志记录级别的数值 30 | warning  |
# | INFO     | 常量     | 日志记录级别的数值 20 | info     |
# | DEBUG    | 常量     | 日志记录级别的数值 10 | debug    |
# | NOTSET   | 常量     | 日志记录级别的数值 0  | notset   |
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
Grey_log = log.getLogger("Grey")


Play_Flag = 0           # 播放录音标志
Audio_Flag = 0          # 录音标志
record_time = 4         # 录音时长


def record_callback(para):
    global Audio_Flag
    print("文件路径:", para[0])     # 返回文件路径
    print("文件长度:", para[1])     # 返回录音长度
    print("录音状态:", para[2])     # 返回录音状态 -1: error 0:start 3:  成功
    if para[2] == 3:
        Audio_Flag = 1


def audio_cb(event):
    global Play_Flag
    if event == 0:
        # print('文件播放开始.')
        Play_Flag = 0
    elif event == 7:
        # print('文件播放成功.')
        Play_Flag = 1


if __name__ == "__main__":
    # 手动运行本例程时, 可以去掉该延时, 如果将例程文件名改为main.py, 希望开机自动运行时, 需要加上该延时.
    # utime.sleep(5)
    # CDC口打印poweron_print_once()信息, 注释则无法从CDC口看到下面的poweron_print_once()中打印的信息.
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码必须执行wait_network_connected()等待网络就绪(拨号成功).
    # 如果是网络无关代码, 可以屏蔽 wait_network_connected().
    # 注: 未插入SIM卡时函数不会阻塞.
    stagecode, subcode = checknet.wait_network_connected(5)
    Grey_log.debug('stagecode: {}   subcode: {}'.format(stagecode, subcode))
    # 网络已就绪: stagecode = 3, subcode = 1
    # 没插sim卡: stagecode = 1, subcode = 0
    # sim卡被锁: stagecode = 1, subcode = 2
    # 超时未注网: stagecode = 2, subcode = 0
    if stagecode != 3 or subcode != 1:
        Grey_log.warning('【Look Out】 Network Not Available\r\n')
    else:
        Grey_log.error('【Look Out】 Network Ready\r\n')

    Grey_log.info('User Code Start\r\n\r\n')

    # ec200u = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_PU, 1)
    # ec200u.write(1)
    # ec600u = Pin(Pin.GPIO24, Pin.OUT, Pin.PULL_PU, 1)
    # ec600u.write(1)
    # you_238 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PU, 1)
    # you_238.write(1)
    play = audio.Audio(0)       # 创建播放对象, 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭  "铀"开发板选通道2. 
    play.setVolume(11)  # 设置音量值，音量值为1~11，0表示静音
    print('当前音量值: {}'.format(play.getVolume()))  # 获取音量值

    record = audio.Record()     # 创建录音对象
    # record.gain(4,12)  # ASR设置录音增益: 上行编解码器增益 [0,4]  上行数字增益 [-36,12]
    record.end_callback(record_callback)  # 设置录音结束回调函数

    # play.play(4, 0, 'U:/call02.mp3')  # 播放文件
    # while Play_Flag == 0:
    #     utime.sleep_ms(1)

    print("录音开始")
    record.start("U:/recordfile.wav", record_time)  # 创建录音文件, 录音时间record_Time秒
    # utime.sleep(record_time)
    # # record.stop()  # 停止录音
    while Audio_Flag == 0:
        # print('录音状态值: {}'.format(record.isBusy()))  # 获取录音状态
        utime.sleep_ms(1)
        record.isBusy()
    
    print("录音时间: {}秒, 播放录音.".format(record_time))

    play.setCallback(audio_cb)  # 设置播放回调函数
    play.play(4, 0, 'U:/recordfile.wav')  # 播放录音文件
    while Play_Flag == 0:
        utime.sleep_ms(1)
    print("录音播放完成")
    record.Delete('U:/recordfile.wav')
    
    # play.play(4, 0, 'U:/call02.mp3')  # 播放文件
    # while Play_Flag == 0:
    #     utime.sleep_ms(1)
