import time
from datetime import datetime

import numpy as np

from instrument_lib.dac.amc7836_init import Amc7836Init
from instrument_lib.daq.keysight_daq970a import KeysightDaq970a
from instrument_lib.power_supply.keysight_e36234a import KeysightE36234a
from instrument_lib.power_supply.keysight_e36312a import KeysightE36312a

def main():
    amc7836 = Amc7836Init.init()

    interface_cfg = amc7836.read_register(amc7836.REGISTER_ADDRESSES["ITFC_CFG0"], 2)
    print(f"Interface Configuration 0 0x{interface_cfg[0]:02X}")
    print(f"Interface Configuration 1 0x{interface_cfg[1]:02X}")

    amc7836.write_register(amc7836.REGISTER_ADDRESSES["ADC_PD2"], 0x02)  # enable PREF for DAC operation
    amc7836.write_register(amc7836.REGISTER_ADDRESSES["DAC_RNG0"], [0x44, 0x44])  # set DAC range for -10 ~ 0V
    amc7836.write_register(amc7836.REGISTER_ADDRESSES["DAC_PD0"], [0xFF, 0xFF])  # enable all DACs
    dac_range = amc7836.read_register(amc7836.REGISTER_ADDRESSES["DAC_RNG0"], 2)  # check DAC Group A & B

    print(f"DAC -10V RangeA 0b{(dac_range[0] & 7):03b}")
    print(f"DAC -10V RangeB 0b{((dac_range[0] >> 4) & 7):03b}")
    print(f"DAC -10V RangeC 0b{(dac_range[1] & 7):03b}")
    print(f"DAC -10V RangeD 0b{((dac_range[1] >> 4) & 7):03b}")

    print("Apply -6.5V VGG to pinch off all amplifiers")
    list_dac = [0x99, 0x05, 0x99, 0x05, 0x99, 0x05]  # corresponding to -6.5V
    amc7836.write_register(amc7836.REGISTER_ADDRESSES["DACA0_DATA_LO"], list_dac)
    amc7836.write_register(amc7836.REGISTER_ADDRESSES["REG_UPDATE"], 0x01)
    time.sleep(0.1)

    print("Apply 0V VGG to pinch off all amplifiers")
    list_dac = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # corresponding to -6.5V
    amc7836.write_register(amc7836.REGISTER_ADDRESSES["DACA0_DATA_LO"], list_dac)
    amc7836.write_register(amc7836.REGISTER_ADDRESSES["REG_UPDATE"], 0x01)
    time.sleep(0.1)


if __name__ == "__main__":
    main()
