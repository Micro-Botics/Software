import time
from machine import I2C

VL53L5CX_ADDR = 0x29

# Important ST registers
BOOT_STATE_REG = 0x06
FW_START_REG   = 0x2E    # Firmware memory area start

class VL53L5CXFirmwareLoader:
    def __init__(self, i2c: I2C, addr=VL53L5CX_ADDR):
        self.i2c = i2c
        self.addr = addr

    def _wr(self, reg, data):
        self.i2c.writeto_mem(self.addr, reg, data)

    def _rd(self, reg, n):
        return self.i2c.readfrom_mem(self.addr, reg, n)

    # Wait for sensor boot (boot state = 1)
    def wait_for_boot(self):
        print("Waiting for VL53L5CX boot...")
        while True:
            if self._rd(BOOT_STATE_REG, 1)[0] == 0x01:
                print("VL53L5CX booted.")
                return
            time.sleep_ms(5)

    # Upload ST ULD firmware to sensor RAM
    def load_firmware(self, filename="vl53l5cx_firmware.bin"):
        print("Uploading firmware:", filename)

        with open(filename, "rb") as fw:
            offset = 0
            while True:
                chunk = fw.read(128)
                if not chunk:
                    break
                self._wr(FW_START_REG + offset, chunk)
                offset += len(chunk)

        print("Firmware upload complete ({} bytes)".format(offset))
        time.sleep_ms(5)
