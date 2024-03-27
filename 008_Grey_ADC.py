from misc import ADC    # 添加ADC库
import utime

adc = ADC()             # 创建ADC对象

if adc.open() == 0:     # 开启ADC功能. 返回: 0.成功 -1.失败
    for i in range(10000):
        print('\r\n\r\n--------------------------------------') 
        print('ADC0电压: {:0>4d}mV'.format(adc.read(ADC.ADC0)))   # 读取ADC通道0电压值
        # print('ADC1电压: {:0>4d}mV'.format(adc.read(ADC.ADC1)))   # 读取ADC通道1电压值
        # print('ADC2电压: {:0>4d}mV'.format(adc.read(ADC.ADC2)))   # 读取ADC通道2电压值
        # print('ADC3电压: {:0>4d}mV'.format(adc.read(ADC.ADC3)))   # 读取ADC通道3电压值
        utime.sleep_ms(1000)
    adc.close()         # 关闭ADC功能. 返回: 0.成功 -1.失败
