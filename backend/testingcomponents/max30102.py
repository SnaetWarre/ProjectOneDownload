import smbus2
import time
import numpy as np
from collections import deque
from scipy.signal import butter, filtfilt, find_peaks



class MAX30102:
    # Register addresses
    REG_INTR_STATUS_1 = 0x00
    REG_INTR_STATUS_2 = 0x01
    REG_INTR_ENABLE_1 = 0x02
    REG_INTR_ENABLE_2 = 0x03
    REG_FIFO_WR_PTR = 0x04
    REG_OVF_COUNTER = 0x05
    REG_FIFO_RD_PTR = 0x06
    REG_FIFO_DATA = 0x07
    REG_FIFO_CONFIG = 0x08
    REG_MODE_CONFIG = 0x09
    REG_SPO2_CONFIG = 0x0A
    REG_LED1_PA = 0x0C
    REG_LED2_PA = 0x0D
    REG_TEMP_INTR = 0x1F
    REG_TEMP_FRAC = 0x20
    REG_TEMP_CONFIG = 0x21
    REG_PROX_INT_THRESH = 0x30
    REG_REV_ID = 0xFE
    REG_PART_ID = 0xFF

    def __init__(self, bus=1, address=0x57):
        self.bus = smbus2.SMBus(bus)
        self.address = address
        self.reset()
        self.setup()

    def reset(self):
        self.write_reg(self.REG_MODE_CONFIG, 0x40)
        time.sleep(0.1)

    def setup(self, led1_pa=0x24, led2_pa=0x24):
        # Enable interrupt for new data available
        self.write_reg(self.REG_INTR_ENABLE_1, 0xc0)
        self.write_reg(self.REG_INTR_ENABLE_2, 0x00)

        # FIFO configuration
        self.write_reg(self.REG_FIFO_WR_PTR, 0x00)
        self.write_reg(self.REG_OVF_COUNTER, 0x00)
        self.write_reg(self.REG_FIFO_RD_PTR, 0x00)
        self.write_reg(self.REG_FIFO_CONFIG, 0x4f)

        # Mode configuration
        self.write_reg(self.REG_MODE_CONFIG, 0x03)

        # SPO2 configuration
        self.write_reg(self.REG_SPO2_CONFIG, 0x27)

        # LED pulse amplitude
        self.write_reg(self.REG_LED1_PA, led1_pa)
        self.write_reg(self.REG_LED2_PA, led2_pa)

    def write_reg(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def read_reg(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def read_fifo(self):
        try:
            data = self.bus.read_i2c_block_data(self.address, self.REG_FIFO_DATA, 32)
            # print(f"This is the raw data: {data}")
            ir_data, red_data = self.extract_ir_red(data)
            return ir_data, red_data
        except Exception as e:
            print(f"Error reading FIFO: {e}")
            return [], []

    def extract_ir_red(self, data):
        ir_data = []
        red_data = []

        for i in range(0, len(data) - 5, 6):
            try:
                red_sample = (data[i] << 16) | (data[i + 1] << 8) | data[i + 2]
                ir_sample = (data[i + 3] << 16) | (data[i + 4] << 8) | data[i + 5]

                red_data.append(red_sample)
                ir_data.append(ir_sample)
            except IndexError as e:
                print(f"Index error: {e}")
                continue
        
        return ir_data, red_data
    

    def bandpass_filter(self, data, lowcut=0.5, highcut=5.0, fs=100, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        y = filtfilt(b, a, data)
        return y

    def calculate_bpm(self, peaks, fs=100):
        intervals = np.diff(peaks) / fs  # Intervals in seconds
        bpm = 60 / intervals  # Convert intervals to BPM
        return bpm
