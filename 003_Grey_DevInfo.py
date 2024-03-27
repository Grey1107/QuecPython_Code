import dataCall
import net
import sim
import modem


ret = modem.getDevImei()
print('\r\nDevImei:"{}"\r\n'.format(ret))

ret = modem.getDevFwVersion()
print('DevFwVersion:"{}"'.format(ret))
ret = uos.uname()
print('"{}"'.format(ret))
ret = uos.uname2()
print('"{}"\r\n'.format(ret))

ret = sim.getStatus()
print('SIMStatus:"{}"'.format(ret))
ret = net.csqQueryPoll()
print('csqQueryPoll:"{}"'.format(ret))
ret = sim.getImsi()
print('SIMImsi:"{}"'.format(ret))
ret = sim.getIccid()
print('SIMIccid:"{}"'.format(ret))
ret = dataCall.getInfo(1, 0)
print('DataCallInfo:"{}"\r\n'.format(ret))
