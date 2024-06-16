import spidev
import time


class MCP:

    def __init__(self, bus=0, device=0, max_speed_hz=10**5):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz

    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8 | channel) << 4, 0])
        data = ((adc[1] & 3) << 8) | adc[2]
        return data

    def convert_to_voltage(self, data, decimal_places=2):
        voltage = (data / 1023.0) * 3.3
        return round(voltage, decimal_places)

    def map_servo(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def closespi(self):
        self.spi.close




