import log
import utime as time
from machine import I2C, Pin, UART


# | 参数      | 参数类型 | 说明                | 类型      |
# | -------- | ------- | ------------------ | -------- |
# | CRITICAL | 常量     | 日志记录级别的数值 50 | critical |
# | ERROR    | 常量     | 日志记录级别的数值 40 | error    |
# | WARNING  | 常量     | 日志记录级别的数值 30 | warning  |
# | INFO     | 常量     | 日志记录级别的数值 20 | info     |
# | DEBUG    | 常量     | 日志记录级别的数值 10 | debug    |
# | NOTSET   | 常量     | 日志记录级别的数值 0  | notset   |
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
# uart_x = UART(UART.UART0, 115200, 8, 0, 1, 0)
# log.set_output(uart_x)
Grey_log = log.getLogger("Grey")


class Grey_IIC:
    def __init__(self, ClkPin = Pin.GPIO13, SdaPin = Pin.GPIO14):
        self.CLK_PIN = ClkPin
        self.SDA_PIN = SdaPin
        self.CLK = Pin(self.CLK_PIN, Pin.OUT, Pin.PULL_PU, 1)
        self.SDA = Pin(self.SDA_PIN, Pin.OUT, Pin.PULL_PU, 1)
        self.CLK.write(0)
        self.SDA.write(0)
        self.CLK.write(1)
        self.SDA.write(1)

    def IIC_Start(self):
        self.CLK.write(0)
        self.SDA.write(1)
        self.CLK.write(1)
        self.SDA.write(0)

    def IIC_Stop(self):
        self.CLK.write(0)
        self.SDA.write(0)
        self.CLK.write(1)
        self.SDA.write(1)

    def IIC_Wait_Ack(self):
        ErrTime=0
        self.SDA = Pin(self.SDA_PIN, Pin.IN, Pin.PULL_PU, 1)
        self.CLK.write(0)
        self.CLK.write(1)
        while self.SDA.read()==1:
            ErrTime += 1
            if ErrTime>1000:
                self.IIC_Stop()
                return 1
        self.SDA = Pin(self.SDA_PIN, Pin.OUT, Pin.PULL_PU, 1)
        return 0

    def IIC_Ack(self):
        self.CLK.write(0)
        self.CLK.write(1)

    def IIC_Send_Byte(self, data):
        for i in range(8):
            self.CLK.write(0)
            if(data&0x80):
                self.SDA.write(1)
            else:
                self.SDA.write(0)
            self.CLK.write(1)
            data = data<<1

    def IIC_Read_Byte(self):
        receive=0x00
        self.CLK.write(0)
        self.SDA = Pin(self.SDA_PIN, Pin.IN, Pin.PULL_PU, 1)
        for i in range(8):
            self.CLK.write(0)
            self.CLK.write(1)
            receive << 1
            if self.SDA.read()==1:
                receive += 1
        self.SDA = Pin(self.SDA_PIN, Pin.OUT, Pin.PULL_PU, 0)
        self.IIC_Ack()
        return receive


    def write(self, slaveaddress, addr, addr_len, data, data_len):
        addrlen = addr_len
        datalen = data_len

        self.IIC_Start()
        self.IIC_Send_Byte((slaveaddress<<1)+0)
        if self.IIC_Wait_Ack() != 0:
            return -1
        while addrlen > 0:
            self.IIC_Send_Byte(addr[addr_len-addrlen])
            addrlen -= 1
            if self.IIC_Wait_Ack() != 0:
                return -2
        while datalen > 0:
            self.IIC_Send_Byte(data[data_len-datalen])
            datalen -= 1
            if self.IIC_Wait_Ack() != 0:
                return -3
        self.IIC_Stop()

    def read(self, slaveaddress, addr, addr_len, r_data, data_len, delay):
        addrlen = addr_len
        datalen = data_len

        if addr_len != 0:
            self.IIC_Start()
            self.IIC_Send_Byte((slaveaddress<<1)+0)
            if self.IIC_Wait_Ack() != 0:
                return -1
            while addrlen > 0:
                self.IIC_Send_Byte(addr[addr_len-addrlen])
                addrlen -= 1
                if self.IIC_Wait_Ack() != 0:
                    return -2
            self.IIC_Stop()
        self.IIC_Start()
        self.IIC_Send_Byte((slaveaddress<<1)+1)
        if self.IIC_Wait_Ack() != 0:
            return -1
        while datalen > 0:
            r_data[data_len-datalen] = self.IIC_Read_Byte()
            datalen -= 1
        self.IIC_Stop()
        for i in range(data_len):
            print("0x{:02X}".format(r_data[i]))
        return r_data


class aht10class:
    i2c_dev = None
    i2c_addre = None

    AHT10_CALIBRATION_CMD = 0xE1  # 初始化命令
    AHT10_START_MEASURMENT_CMD = 0xAC  # 触发测量
    AHT10_RESET_CMD = 0xBA  # 复位

    def write_data(self, data):
        self.i2c_dev.write(self.i2c_addre, bytearray(0x00), 0, bytearray(data), len(data))
        # Grey_log.debug('[write]addr:0x{:X} deta:{}'.format((self.i2c_addre << 1)+0, data))
        pass

    def read_data(self, length):
        r_data = [0x00 for _ in range(length)]
        r_data = bytearray(r_data)
        self.i2c_dev.read(self.i2c_addre, bytearray([0x00, 0x00]), 0, r_data, length, 50)
        # Grey_log.debug('[read]addr:0x{:X} deta:{}'.format((self.i2c_addre << 1)+1, r_data))
        return list(r_data)

    def aht10_init(self, addre=0x38):
        # self.i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)  # EC600U
        # self.i2c_dev = I2C(I2C.I2C0, I2C.STANDARD_MODE)  # EC200U
        self.i2c_dev = Grey_IIC(ClkPin = Pin.GPIO24, SdaPin = Pin.GPIO23)
        # i2c_x = I2C(I2C.I2C0, I2C.STANDARD_MODE)  # 此处我将IIC0跟IIC1进行了并联, 未屏蔽干扰需要此句代码.
        self.i2c_addre = addre
        # 校准
        self.write_data([self.AHT10_CALIBRATION_CMD, 0x08, 0x00])
        time.sleep_ms(300)  # at last 300ms

    @staticmethod
    def aht10_transformation_temperature(data):
        r_data = data
        # 根据数据手册的描述来转化温度
        humidity = (r_data[0] << 12) | (
            r_data[1] << 4) | ((r_data[2] & 0xF0) >> 4)
        humidity = (humidity/(1 << 20)) * 100.0
        temperature = ((r_data[2] & 0xf) << 16) | (
            r_data[3] << 8) | r_data[4]
        temperature = (temperature * 200.0 / (1 << 20)) - 50
        Grey_log.info("当前温度: {:.2f} ℃".format(temperature))
        Grey_log.info("当前湿度: {:.2f} ％".format(humidity))
        time.sleep_ms(500)

    def ath10_reset(self):
        self.write_data([self.AHT10_RESET_CMD])
        time.sleep_ms(20)  # at last 20ms

    def trigger_measurement(self):
        # Trigger data conversion
        self.write_data([self.AHT10_START_MEASURMENT_CMD, 0x33, 0x00])
        time.sleep_ms(200)  # at last delay 75ms
        # check has success
        r_data = self.read_data(6)
        # check bit7
        if (r_data[0] >> 7) != 0x0:
            # Grey_log.error("换算错误")
            pass
        else:
            self.aht10_transformation_temperature(r_data[1:6])


def i2c_aht10_test():
    ath_dev = aht10class()
    ath_dev.aht10_init(addre=0x38)

    # 测试十次
    for i in range(1):
    # while True:
        ath_dev.trigger_measurement()


if __name__ == "__main__":
    i2c_aht10_test()
