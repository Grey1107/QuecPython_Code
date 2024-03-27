import sim
import net
import dataCall


def sim_get_status(value):
    # 功能sim卡状态表
    if value == 0:
        print("SIM卡已移除")
    elif value == 1:
        print("SIM卡已准备好")
        net_csq_querypoll(net.csqQueryPoll())
    elif value == 2:
        print("通用PIN码解锁. SIM卡锁定, 等待CHV1密码")
    elif value == 3:
        print("期望代码解锁通用PIN码. SIM卡被阻断, 则需要CHV1解锁密码")
    elif value == 4:
        print("SIM/USIM个性化检查失败导致SIM被锁定")
    elif value == 5:
        print("由于PCK错误导致SIM被阻塞; 需要设置MEP解锁密码")
    elif value == 6:
        print("期待能找到隐藏电话簿条目的钥匙")
    elif value == 7:
        print("期望代码解锁隐藏的密钥")
    elif value == 8:
        print("SIM卡锁定;等待CHV2密码")
    elif value == 9:
        print("SIM卡锁定;需要设置CHV2解锁密码")
    elif value == 10:
        print("由于网络个性化检查失败，SIM卡被锁定")
    elif value == 11:
        print("由于NCK错误，SIM卡被阻塞;需要设置MEP解锁密码")
    elif value == 12:
        print("由于网络子集个性化检查失败，SIM被锁定")
    elif value == 13:
        print("由于不正确的NSCK, SIM被阻塞;需要设置MEP解锁密码")
    elif value == 14:
        print("由于服务提供商个性化检查失败，SIM被锁定")
    elif value == 15:
        print("由于SPCK错误导致SIM卡被阻塞;需要设置MEP解锁密码")
    elif value == 16:
        print("由于企业个性化检查失败，SIM被锁定")
    elif value == 17:
        print("由于不正确的CCK导致SIM被阻塞;需要设置MEP解锁密码")
    elif value == 18:
        print("SIM正在初始化;等待完成")
    elif value == 19:
        print("使用CHV1/CHV2/通用PIN/代码来解锁, CHV1/代码来解锁, CHV2/解锁通用, PIN/被阻止的代码")
    elif value == 20:
        print("无效的SIM卡")
    elif value == 21:
        print("未知状态")
    else:
        print("未知")
    return value

# sim.enablePin("1234")  # 重启后生效，重启后需要“sim.verifyPin("1234")”，如需下次不输入密码的话，则sim.disablePin("1234")


def net_csq_querypoll(value):
    # 一般来说: CSQ范围在1-31之间, 31信号最好. CSQ<11不容易附着网络. 11<CSQ<18在此区间网络不稳定会导致误码较多, CSQ>18能稳定通信. 
    if value == 0 or value == 99:
        print("注释1: 请确认天线是否已连接")
        print("注释2: 请在开阔的地方测试")
        print("注释3: 请确认您的模块型号是否与固件一致")
    elif 1 <= value <= 10:
        print("信号: 很弱")
        net_get_state(net.getState()[1][0])
    elif 11 <= value <= 17:
        print("信号: 一般")
        net_get_state(net.getState()[1][0])
    elif 18 <= value <= 31:
        print("信号: 优质")
        net_get_state(net.getState()[1][0])
    else:
        print("网络: 错误")
    return value


def net_get_state(value):
    if value == 0:
        print("未注册, MT当前未搜索网络")
    elif value == 1:
        print("已注册: 家庭网络")
        datacall_getinfo()
    elif value == 2:
        print("未注册, 但MT当前正在尝试附着或搜索网络以进行注册")
    elif value == 3:
        print("注册被拒绝")
    elif value == 4:
        print("未知(例如: 超出E-UTRAN覆盖范围)")
    elif value == 5:
        print("已注册: 漫游状态")
        datacall_getinfo()
    elif value == 6:
        print("登记为仅限短信, 家庭网络(不适用)")
        datacall_getinfo()
    elif value == 7:
        print("登记为仅限短信, 漫游服务(不适用)")
        datacall_getinfo()
    elif value == 8:
        print("仅供紧急服务使用")
        datacall_getinfo()
    elif value == 9:
        print("已登记为CSFB, 家庭网络(不适用)")
        datacall_getinfo()
    elif value == 10:
        print("已登记为CSFB, 漫游网络(不适用)")
        datacall_getinfo()
    elif value == 11:
        print("只提供紧急服务")
        datacall_getinfo()
    else:
        print("Net状态错误")
    return value


def datacall_getinfo():
    nwState = dataCall.getInfo(1, 0)[2][0]
    if nwState == 0:
        print('数据调用失败')
    else:
        print('ip地址: %s' % (dataCall.getInfo(1, 0)[2][2]))
        print('DNS消息1: %s' % (dataCall.getInfo(1, 0)[2][3]))
        print('DNS消息2: %s' % (dataCall.getInfo(1, 0)[2][4]))


sim_get_status(sim.getStatus())
