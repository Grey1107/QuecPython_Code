# coding: utf-8
import request
import audio
import utime
import _thread
import audio
import _thread
import checkNet
from machine import Pin

# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_流播放"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

aud = audio.Audio(0)  # SPK接口使用, 官方EC600U开发板需强制将PIN40拉高(也就是将J6>PIN2与J6>PIN10短接)
# aud = audio.Audio(2)  # LSPK接口使用, 注: 此接口只有EC600U支持
aud.setVolume(1)
lock = _thread.allocate_lock()


class hls_audio:
    # 对象初始化
    def __init__(self, range_init):
        self.range_paly = range_init  # 断点续传
        # self.is_pause = False
        self.is_close = False
        self.url_paly = None
        self.params = None
        self.headers = {}

    # 音频播放
    def play_init(self, url):
        self.url_paly = url
        self.params = self.parse_format()
        if self.range_paly:  # 断点续传
            self.headers['Range'] = 'bytes={}-'.format(self.range_paly)
            print(self.headers)
        _thread.start_new_thread(self.play_run, ())

    # 音频格式, 简单的后缀判断
    def parse_format(self):
        af = {
            'pcm': {'sizeof': 10*1024, 'format': 1},   # 单通道，8000
            'wav': {'sizeof': 20*1024, 'format': 2},
            'mp3': {'sizeof': 15*1024, 'format': 3},
            'amr': {'sizeof': 5*960, 'format': 4},
            'aac': {'sizeof': 10*1024, 'format': 6},
            'm4a': {'sizeof': 10*1024, 'format': 7},
        }
        # sizeof: 单次切片的大小；format：固件包接口不同格式的定义
        f = self.url_paly.split('?')[0].split('.')[-1]
        if f not in af.keys():
            raise Exception('unsupported audio format.{}'.format(f))
        return af[f]

    # 播放函数
    def play_run(self, timeout=30):
        run_params = self.params
        # 请求获取资源
        lock.acquire()  # 获取锁
        request_read = request.get(self.url_paly, headers=self.headers, timeout=timeout)
        lock.release()  # 释放锁
        # 播放文件头
        if run_params['format'] == 4:  # amr
            head_content = request_read.raw.read(run_params['sizeof'])
            run_params['format'] = self.parse_amr_head(head_content, run_params['format'])
        # 循环播放文件内容
        while True:
            if self.is_close:
                break
            # if self.is_pause:
            #     utime.sleep_ms(50)
            #     continue
            try:  # 读取可能会有报错，直接break
                i = request_read.raw.read(run_params['sizeof'])
                if not i:
                    break
            except Exception as e:
                print('read error:{}'.format(e))
                break
            aud.playStream(run_params['format'], i)
            # print('类型: {}  数据: {}'.format(run_params['format'], i))
        request_read.close()  # Get关闭
        self.close()
        print('done run stop')

    # amr格式
    @staticmethod
    def parse_amr_head(head_content, format_amr):
        # if head_content[:5] != b'#!AMR':
        #     # amr
        #     pass
        # elif head_content[:4] != b'RIFF' and head_content[8:15] == b'WAVEfmt':
        #     # wav
        #     pass
        # elif head_content[:3] == b'ID3':
        #     # mp3 的文件格式可能不统一，不一定是在文件头进行标记；
        #     # ID3V2 在文件头以 ID3 开头；
        #     # ID3V1 在文件尾以 TAG 开头。
        #     pass

        single_amr_nb = '2321414d520a'
        single_amr_wb = '2321414d522d57420a'
        mult_amr_nb = '2321414d525f4d43312e300a'
        mult_amr_wb = '2321414d522d57425f4d43312e300a'

        head_hexs = []
        for i in head_content[:16]:
            char = hex(i).replace('0x', '')
            if len(char) <= 1:
                char = '0{}'.format(char)
            head_hexs.append(char.lower())
        # 单声道还是多声道
        if ''.join(head_hexs[:6]) == single_amr_nb:
            format_amr = 4  # 单声道 AMR-NB
        elif ''.join(head_hexs[:9]) == single_amr_wb:
            format_amr = 5  # 单声道 AMR-WB
        elif ''.join(head_hexs[:12]) == mult_amr_nb:
            format_amr = 4  # 多声道 AMR-NB
        elif ''.join(head_hexs[:15]) == mult_amr_wb:
            format_amr = 5  # 多声道 AMR-WB
        # 播放头
        aud.playStream(format_amr, head_content)
        return format_amr

    # 暂停
    @staticmethod
    def pause(f):
        # self.is_pause = True if f == 1 else False
        if f == 1:
            aud.StreamPause()
        else:
            aud.StreamContinue()

    # 停止
    def close(self):
        self.url_paly = None
        self.is_close = True
        aud.stopPlayStream()
        # self.is_pause = False

    # 快进，快退(功能暂时未经测试，保留)
    def seek_secs(self):
        if not self.url_paly:
            raise Exception("You can't fast forward or rewind without playing audio")
        url = self.url_paly
        self.close()
        utime.sleep(1)
        self.play_init(url)
        _thread.start_new_thread(self.play_run, ())


if __name__ == '__main__':
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    # utime.sleep(5)
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    # 【本例程可以屏蔽下面这一行！】
    checknet.wait_network_connected()
    ec200u = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_PU, 1)
    ec200u.write(1)
    ec600u = Pin(Pin.GPIO24, Pin.OUT, Pin.PULL_PU, 1)
    ec600u.write(1)
    hls = hls_audio(None)  # 创建hls对象
    # hls.play_init("http://home.xiupa617.top:38080/file/down4.m4a")  # 仅EC600U使用
    hls.play_init("http://home.xiupa617.top:38080/file/down.mp3")  # EC600N/U使用

    ''' 测试命令如下
    from usr.Grey_hls import hls_audio  # 从文件导入hls库, Grey_hls为文件名

    hls = hls_audio(None)  # 创建hls对象
    # hls.play_init("http://home.xiupa617.top:38080/file/down4.m4a")  # 仅EC600U使用
    hls.play_init("http://home.xiupa617.top:38080/file/down.mp3")  # EC600N/U使用
    # EC600N模块只支持wav, amr, mp3三种格式, 所以不能播放m4a的文件. 

    hls.pause(1)  # 暂停播放
    hls.pause(0)  # 继续播放
    hls.stop()  # 停止播放
    hls.seek_secs(second)  # 跳转到多少秒 暂未调通 '''
