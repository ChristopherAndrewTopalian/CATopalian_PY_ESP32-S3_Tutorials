# bmp180.py - Standard MicroPython Driver for Bosch BMP180
from struct import unpack as unp
from machine import I2C
import time

class BMP180():
    def __init__(self, i2c_bus):
        self._bmp_addr = 119  # 0x77 I2C address
        self._bmp_i2c = i2c_bus
        self.chip_id = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xD0, 2)
        
        # Read calibration coefficients from sensor EEPROM
        self._AC1 = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xAA, 2))[0]
        self._AC2 = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xAC, 2))[0]
        self._AC3 = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xAE, 2))[0]
        self._AC4 = unp('>H', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xB0, 2))[0]
        self._AC5 = unp('>H', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xB2, 2))[0]
        self._AC6 = unp('>H', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xB4, 2))[0]
        self._B1 = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xB6, 2))[0]
        self._B2 = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xB8, 2))[0]
        self._MB = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xBA, 2))[0]
        self._MC = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xBC, 2))[0]
        self._MD = unp('>h', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xBE, 2))[0]
        self.oversample_sett = 0
        self.baseline = 101325

    def gauge(self):
        while True:
            # Read uncompensated temperature
            self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, bytearray([0x2E]))
            time.sleep_ms(5)
            UT = unp('>H', self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF6, 2))[0]
            X1 = (UT - self._AC6) * self._AC5 // 2**15
            X2 = self._MC * 2**11 // (X1 + self._MD)
            B5_raw = X1 + X2
            self.T = ((B5_raw + 8) // 2**4) / 10

            # Read uncompensated pressure
            self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, bytearray([0x34 + (self.oversample_sett << 6)]))
            time.sleep_ms(2 + (3 << self.oversample_sett))
            MSB = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF6, 1)[0]
            LSB = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF7, 1)[0]
            XLSB = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF8, 1)[0]
            UP = ((MSB << 16) + (LSB << 8) + XLSB) >> (8 - self.oversample_sett)
            B6 = B5_raw - 4000
            X1 = (self._B2 * (B6**2 // 2**12)) // 2**11
            X2 = (self._AC2 * B6) // 2**11
            X3 = X1 + X2
            B3 = ((self._AC1 * 4 + X3) << self.oversample_sett + 2) // 4
            X1 = (self._AC3 * B6) // 2**13
            X2 = (self._B1 * (B6**2 // 2**12)) // 2**16
            X3 = ((X1 + X2) + 2) // 2**2
            B4 = (self._AC4 * (X3 + 32768)) // 2**15
            B7 = (UP - B3) * (50000 >> self.oversample_sett)
            if B7 < 0x80000000:
                p = (B7 * 2) // B4
            else:
                p = (B7 // B4) * 2
            X1 = (p // 2**8)**2
            X1 = (X1 * 3038) // 2**16
            X2 = (-7357 * p) // 2**16
            self.p = p + ((X1 + X2 + 3791) // 2**4)
            yield None

    @property
    def temperature(self):
        next(self.gauge())
        return self.T

    @property
    def pressure(self):
        next(self.gauge())
        return self.p

    @property
    def altitude(self):
        return 44330 * (1 - (self.pressure / self.baseline)**(1/5.255))