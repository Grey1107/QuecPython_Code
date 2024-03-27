# -*- coding: UTF-8 -*-
import utime
from machine import SPI
from machine import Pin

# 屏蔽GNSS模块数据干扰. 由于EC600S/N的SPI_MISO与SPI_MOSI引脚还被复用为UART1. 开发板还连接GNSS模块L76K, 为了断开L76K吐数据对SPI通信的干扰, 需要添加下面两句代码. 
# gpio11 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PD, 0)   # EC600S/EC600N使用
# gpio11.write(0)                                     # EC600S/EC600N使用

w_data = "Grey"
r_data = bytearray(len(w_data))
count = 1000  # 运行次数
# spi_obj = SPI(1, 0, 0)      # EC600S/EC600N使用
spi_obj = SPI(1, 0, 0, 1)    # EC600U/EC100Y/BC25使用

while count:
    count -= 1
    utime.sleep(1)
    ret = spi_obj.write_read(r_data, w_data, 10)
    print(len(r_data))
    if ret == -1:
        SPI_msg = "SPIReadError"
    else:
        SPI_msg = "SPIRead:{}  running:{:0>2d}".format(r_data, count)
    print(SPI_msg)
