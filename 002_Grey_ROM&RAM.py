import gc
import uos

# 内存信息查询
def print_flash_size(flash):
    # 获取文件系统状态信息
    # uos.statvfs(path)
    # 获取文件系统状态信息。path表示文件或目录名。返回一个包含文件系统信息的元组：
    # (f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, f_files, f_ffree, f_favail, f_flag, f_namemax)

    # f_bsize – 文件系统块大小，单位字节
    # f_frsize – 分栈大小，单位字节
    # f_blocks – 文件系统数据块总数
    # f_bfree – 可用块数
    # f_bavail – 非超级用户可获取的块数
    # f_files – 文件结点总数
    # f_ffree – 可用文件结点数
    # f_favail – 超级用户的可用文件结点数
    # f_flag – 挂载标记
    # f_namemax – 最大文件长度，单位字节

    print('---------------------------------------------------------------')
    res = uos.statvfs(flash)
    res = list(res)
    print('[{}]空间信息: {}'.format(flash, res))
    print('块大小: {}'.format(res[0]))
    print('总块数: {}'.format(res[2]))
    print('总空间: {:.3f} KB'.format((res[0] * res[2]) / 1024))
    print('剩余块数: {}'.format(res[3]))
    print('剩余空间: {:.3f} KB'.format((res[0] * res[3]) / 1024))
    # statvfs_fields = ['bsize', 'frsize', 'blocks', 'bfree', 'bavail', 'files', 'ffree', favail, flag, namemax]
    # info = dict(zip(statvfs_fields, uos.statvfs(flash)))
    # print('可用空间: {}kb'.format(str(info['bsize'] * info['bfree'] / 1024)))
    print('---------------------------------------------------------------\r\n')

print('---------------------------------------------------------------')
gc.collect()
mem = gc.mem_free()
print('RAM空间剩余: {} KB'.format(mem / 1024))
print('---------------------------------------------------------------\r\n')
print('---------------------------------------------------------------')
import _thread
print('Heap空间剩余: {} KB'.format(_thread.get_heap_size() / 1024))
print('---------------------------------------------------------------\r\n')
root = uos.listdir('/')
for i in root: 
    print_flash_size(i)


# print('---------------------------------------------------------------')
# res = uos.statvfs("/usr")
# res = list(res)
# print('\'usr\'information: ', res)
# print('block size in bytes: ', res[0])
# print('f_bfree:', res[3])
# print('free Flash: {} KB'.format((res[0] * res[3]) / 1024))
# print('---------------------------------------------------------------')
# res = uos.statvfs("/bak")
# res = list(res)
# print('\'bak\'information: ', res)
# print('block size in bytes: ', res[0])
# print('f_bfree:', res[3])
# print('free Flash: {} KB'.format((res[0] * res[3]) / 1024))
# print('---------------------------------------------------------------')
# mem = gc.mem_free()
# print('free RAM: {} KB'.format(mem / 1024))
