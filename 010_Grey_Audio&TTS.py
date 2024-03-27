# -*- coding: UTF-8 -*-

import net                  # 网络
import utime                # 休眠延时
import log                  # LOG
import _thread              # 线程
import dataCall             # 数据拨号
import checkNet             # 网络查验
import audio                # 音频
from machine import Pin         # 硬件PIN
from machine import UART        # 硬件UART
from machine import I2C         # 硬件IIC
from machine import SPI         # 硬件SPI
from machine import ExtInt      # 硬件ExtInt
from machine import Timer       # 硬件Timer
from machine import LCD         # 硬件LCD
from misc import PWM            # 扩展PWM
from aLiYun import aLiYun       # 阿里云


# | 参数      | 参数类型 | 说明                |
# | -------- | ------- | ------------------ |
# | CRITICAL | 常量     | 日志记录级别的数值 50 |
# | ERROR    | 常量     | 日志记录级别的数值 40 |
# | WARNING  | 常量     | 日志记录级别的数值 30 |
# | INFO     | 常量     | 日志记录级别的数值 20 |
# | DEBUG    | 常量     | 日志记录级别的数值 10 |
# | NOTSET   | 常量     | 日志记录级别的数值 0  |
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
Grey_log = log.getLogger("Grey")    # 获取logger对象，如果不指定name则返回root对象，多次使用相同的name调用getLogger方法返回同一个logger对象


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_Audio&TTS"         # 工程名
PROJECT_VERSION = "0.0.1"               # 版本号
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# | 参数       | 参数类型  | 参数说明                                                                             |
# | --------- | -------- | ---------------------------------------------------------------------------------- |
# | priority  | int      | 播放优先级，支持优先级0~4，数值越大优先级越高                                              |
# | breakin   | int      | 打断模式，0  表示不允许被打断，1表示允许被打断                                             |
# | mode      | int      | 编码模式，1 - UNICODE16(Sizeendconversion)，2 - UTF - 8，3 - UNICODE16(Don't convert) |
# | str       | string   | 待播放字符串                                                                         |
# 返回值
# 播放成功返回整型0；
# 播放失败返回整型-1；
# 无法立即播放，加入播放队列，返回整型1；
# 无法立即播放，且该请求的优先级组队列任务已达上限，无法加入播放队列，返回整型-2
# tts.play(priority, breakin, mode, str)
# TTS_Flag = tts.getState()      # 获取tts状态, 0 – 整型值，表示当前无tts播放；1 – 整型值，表示当前有tts正在播放
# tts.stop()                     # 停止TTS播放

# | 参数       | 参数类型 | 说明                |
# | --------- | ------- | ------------------ |
# | file_name | str     | 录音文件名           |
# | seconds   | int     | 需要录制时长，单位：秒 |
# 返回值
# 0： 成功
# -1: 文件覆盖失败
# -2：文件打开失败
# -3: 文件正在使用
# -4：通道设置错误（只能设置0或1）
# -5：定时器资源申请失败
# -6 ：音频格式检测错误；
# -7 ：该文件已经由其他对象创建了
# record.start(file_name, seconds)

# | 参数      | 参数类型 | 参数说明                                                                              |
# | -------- | ------  | ----------------------------------------------------------------------------------- |
# | priority | int     | 播放优先级，支持优先级0~4，数值越大优先级越高                                               |
# | breakin  | int     | 打断模式，0表示不允许被打断，1表示允许被打断                                                |
# | mode     | int     | 编码模式，1 - UNICODE16(Sizeendconversion)，2 - UTF - 8，3 - UNICODE16(Don't convert) |
# | str      | string  | 待播放字符串                                                                          |
# 返回值
# 注册成功返回整型0，失败返回整型-1
# aud.play(priority, breakin, filename)


TTS_Flag = 0        # TTS标志
Play_Flag = 0       # 播放录音标志
Audio_Flag = 0      # 录音标志


def tts_cb(event):
    global TTS_Flag        # TTS标志
    # | event | 表示状态 |
    # | ----- | ------  |
    # | 2     | 开始播放 |
    # | 3     | 停止播放 |
    # | 4     | 播放完成 |
    if event == 2:
        # print('TTS开始播放')
        TTS_Flag = 0
    elif event == 3:
        # print('TTS停止播放')
        TTS_Flag = 0
    elif event == 4:
        # print('TTS播放完成')
        TTS_Flag = 1
    else:
        # print('TTS未知状态')
        TTS_Flag = 0


def record_callback(para):
    global Audio_Flag
    # print("文件路径:", para[0])     # 返回文件路径
    # print("文件长度:", para[1])     # 返回录音长度
    # print("录音状态:", para[2])     # 返回录音状态 -1: error 0:start 3:  成功
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


def audio_tts():
    global TTS_Flag
    global Play_Flag
    global Audio_Flag

    # 硬件版本选择
    # 0: 自用调试板
    # 1: 官方板V1.1
    # 2: 官方板V1.2
    hardware_version = 2  # 使用硬件
    # 外接喇叭播放录音文件，需要下面语句来使能
    if hardware_version == 0:
        audio_en = Pin(Pin.GPIO10, Pin.OUT, Pin.PULL_PD, 1)  # 自用调试板使用
        audio_en.write(1)
    elif hardware_version == 1:
        audio_en = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PD, 1)  # 官方板V1.1使用
        audio_en.write(1)
    elif hardware_version == 2:
        # 官方板V1.2/V1.3默认使能引脚已使能, 不需要操作
        audio_en = Pin(Pin.GPIO9, Pin.OUT, Pin.PULL_PD, 1)  # 官方板V1.2/V1.3使用
        audio_en.write(1)

    record_time = 4         # 录音时长

    tts = audio.TTS(0)          # 创建TTS对象, 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
    play = audio.Audio(0)       # 创建播放对象, 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
    record = audio.Record()     # 创建录音对象

    uos.chdir('usr')
    print('文件列表: {}'.format(uos.listdir()))  # 文件列表
    # print('删除文件状态: {}'.format(uos.remove('recordfile.wav')))  # 删除文件

    # tts.close()                 # 关闭TTS 成功返回整型0，失败返回整型-1
    tts.setVolume(9)    # 设置音量值，音量值为0~9，0表示静音
    print('\r\n')
    print('当前音量值: {}'.format(tts.getVolume()))  # 获取音量值
    play.setVolume(11)  # 设置音量值，音量值为1~11，0表示静音
    print('\r\n')
    print('当前音量值: {}'.format(play.getVolume()))  # 获取音量值
    tts.setSpeed(4)     # 设置速度值，速度值为0~9，值越大，速度越快
    print('当前语速值: {}'.format(tts.getSpeed()))  # 获取速度值

    # uos.rename('/usr/recordfile.wav', '/usr/test.amr')
    # print('文件存在值: {}'.format(record.exists('recordfile.wav')))  # 判断文件存在
    # print('文件存在值: {}'.format(record.exists('U:/recordfile.wav')))  # 判断文件存在
    # print('文件存在值: {}'.format(record.exists('/usr/recordfile.wav')))  # 判断文件存在
    # print('文件存在值: {}'.format(record.exists('test.amr')))
    # print('文件存在值: {}'.format(record.exists('U:/test.amr')))
    # print('文件存在值: {}'.format(record.exists('/usr/test.amr')))
    # uos.remove('/usr/recordfile.wav')

    tts.setCallback(tts_cb)  # 设置TTS回调函数
    tts.play(1, 0, 2, '录音实验, 即将开始录音.')  # 语音播放
    while TTS_Flag == 0:  # 语音播放完成
        pass
    print("录音实验, 开始录音.")
    record.end_callback(record_callback)  # 设置录音结束回调函数
    record.start("U:/recordfile.wav", record_time)  # 创建录音文件, 录音时间record_Time秒
    # record.stop()  # 停止录音
    while Audio_Flag == 0:
        # print('录音状态值: {}'.format(record.isBusy()))  # 获取录音状态
        utime.sleep_ms(1)
        record.isBusy()
    tts.play(1, 0, 2, '录音结束,准备播放录音文件')
    print("录音成功")
    while TTS_Flag == 0:
        pass
    print("录音时间: {}秒, 播放录音.".format(record_time))

    play.setCallback(audio_cb)  # 设置播放回调函数
    play.play(1, 0, 'u:/recordfile.wav')  # 播放录音文件
    # aud.stop()  # 停止播放
    while Play_Flag == 0:
        pass
    tts.play(1, 0, 2, '录音播放完成.')  # 语音播放
    print("录音播放完成")
    # record.Delete('recordfile.wav')


def grey_run():  # 线程创建函数
    Grey_log.debug("grey_run 开始!")
    _thread.start_new_thread(audio_tts, ())  # 创建一个线程来监听执行uartWrite函数
    Grey_log.debug("grey_run 结束!")


if __name__ == '__main__':
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    # utime.sleep(5)
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    # checknet.wait_network_connected()

    # ########################【用户代码-开始】########################
    grey_run()
    utime.sleep_ms(100)
    pass
    # ########################【用户代码-结束】########################
