import net
import utime

stattus = None

net.nitzTime()
local_time = utime.localtime()
stattus = '{0:0>4d}-{1:0>2d}-{2:0>2d} {3:0>2d}:{4:0>2d}:{5:0>2d}'.\
    format(local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5])
print(stattus)
