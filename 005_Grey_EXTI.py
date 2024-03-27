from machine import ExtInt


def callback(args):
    if args[0] == 27:
        print('GPIO:{}触发:{}次. \r\n'.format(args, extint1.read_count(0)))  # 读取中断次数不重置
    elif args[0] == 13:
        print('GPIO:{}触发:{}次. \r\n'.format(args, extint2.read_count(0)))  # 读取中断次数不重置
    elif args[0] == 12:
        print('GPIO:{}触发:{}次. \r\n'.format(args, extint3.read_count(0)))  # 读取中断次数不重置
    elif args[0] == 14:
        print('GPIO:{}触发:{}次. \r\n'.format(args, extint4.read_count(0)))  # 读取中断次数不重置
    elif args[0] == 2:
        print('GPIO:{}触发:{}次. \r\n'.format(args, extint5.read_count(0)))  # 读取中断次数不重置
    elif args[0] == 1:
        print('GPIO:{}触发:{}次. \r\n'.format(args, extint6.read_count(0)))  # 读取中断次数不重置
    elif args[0] == 24:
        print('GPIO:{}触发:{}次. \r\n'.format(args, extint7.read_count(0)))  # 读取中断次数不重置
    else:
        print('interrupt: {}'.format(args))

extint1 = ExtInt(ExtInt.GPIO27, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, callback)  # 创建对象
extint2 = ExtInt(ExtInt.GPIO28, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, callback)  # 创建对象
extint3 = ExtInt(ExtInt.GPIO12, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, callback)  # 创建对象
extint4 = ExtInt(ExtInt.GPIO14, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, callback)  # 创建对象
extint5 = ExtInt(ExtInt.GPIO2, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, callback)  # 创建对象
extint6 = ExtInt(ExtInt.GPIO1, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, callback)  # 创建对象
extint7 = ExtInt(ExtInt.GPIO24, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, callback)  # 创建对象

extint1.enable()  # 使能中断
extint2.enable()  # 使能中断
extint3.enable()  # 使能中断
extint4.enable()  # 使能中断
extint5.enable()  # 使能中断
extint6.enable()  # 使能中断
extint7.enable()  # 使能中断
print('开启GPIO:{}中断. \r\n'.format(extint1.line()))  # 读取引脚映射行号
print('开启GPIO:{}中断. \r\n'.format(extint2.line()))  # 读取引脚映射行号
print('开启GPIO:{}中断. \r\n'.format(extint3.line()))  # 读取引脚映射行号
print('开启GPIO:{}中断. \r\n'.format(extint4.line()))  # 读取引脚映射行号
print('开启GPIO:{}中断. \r\n'.format(extint5.line()))  # 读取引脚映射行号
print('开启GPIO:{}中断. \r\n'.format(extint6.line()))  # 读取引脚映射行号
print('开启GPIO:{}中断. \r\n'.format(extint7.line()))  # 读取引脚映射行号

# while 1:
#     print('开启GPIO: {}中断. \r\n'.format(extint1.read_count(0)))  # 读取中断次数不重置

# 读取中断次数并重置
# extint1.read_count(1)

# 读取中断次数不重置
# extint1.read_count(0)

# 清空中断数
# extint1.count_reset()

# 关闭中断
# extint1.disable()
