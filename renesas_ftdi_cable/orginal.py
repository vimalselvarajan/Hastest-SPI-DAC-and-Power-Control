import time
from datetime import datetime

import numpy as np

# sys.path.append(r"C:\Users\trflabsd\Documents\Measurement_Automation\pymaster")
# sys.path.append(r"C:\Users\trflabsd\Documents\Measurement_Automation\instrument_lib")
from instrument_lib.dac.amc7836_init import Amc7836Init
from instrument_lib.daq import KeysightDaq970a
from instrument_lib.power_supply import KeysightE36234a
from instrument_lib.power_supply import KeysightE36312a


def sdac_vgg(amc7836, daq, init_dac, addr_dac, vch, ich, itgt):
    bsm = [64, 32, 16, 8, 4, 2]
    amc7836.write_register(amc7836.REGISTER_ADDRESSES[addr_dac], [init_dac & 0xFF, init_dac >> 8])
    amc7836.write_register(amc7836.REGISTER_ADDRESSES["REG_UPDATE"], 0x01)
    time.sleep(0.1)
    # i_bias = float(daq.query(f"MEAS:VOLT:DC? (@1{ich:02d})"))
    i_bias = daq.measure_voltage(ich)
    print(f"Bias Current = {i_bias:.5f}")
    curr_dac = init_dac
    for s in range(len(bsm)):
        dac_vgg = curr_dac + int(np.sign(itgt - i_bias)) * bsm[s]
        if dac_vgg < 3072:
            list_dac = [dac_vgg & 0xFF, dac_vgg >> 8]
            amc7836.write_register(amc7836.REGISTER_ADDRESSES[addr_dac], list_dac)
            amc7836.write_register(amc7836.REGISTER_ADDRESSES["REG_UPDATE"], 0x01)
            time.sleep(0.1)
            # i_bias = float(daq.query(f"MEAS:VOLT:DC? (@1{ich:02d})"))
            i_bias = daq.measure_voltage(ich)
            print(f"Bias Current = {i_bias:.5f}")
        curr_dac = dac_vgg


def main():
    ps1_out = 0
    ps3_out = 0
    daq_out = 0

    ps1 = None
    ps3 = None
    daq = None

    if not ps1_out:
        ps1 = KeysightE36312a("USB0::0x2A8D::0x1102::MY61001796::INSTR")
        print(ps1.query("*IDN?"))
        ps1.write("*RST")
        time.sleep(.3)

    if not ps3_out:
        ps3 = KeysightE36234a("USB0::0x2A8D::0x3402::MY61002290::INSTR")
        print(ps3.query("*IDN?"))
        ps3.write("*RST")
        time.sleep(.3)

    if not daq_out:
        daq = KeysightDaq970a("USB0::0x2A8D::0x5101::MY58016887::INSTR")
        print(daq.query("*IDN?"))

    vdd = 5
    vee = -12
    vcc = 5
    limit_ivdd = 0.1
    limit_ivcc = 0.1
    limit_ivee = 0.1

    if not ps1_out:
        ps1.set_output_voltage_ch(1, vdd, limit_ivdd)
        ps1.out_on_off(1, 0)  # ch1 for 5V to AVDD
        ps1.set_output_voltage_ch(2, vcc, limit_ivcc)
        ps1.out_on_off(2, 0)  # ch2 for 5V to AVCC
        ps1.set_output_voltage_ch(3, abs(vee), limit_ivee)
        ps1.out_on_off(3, 0)  # ch3 for -12V to AVEE (i.e. AVSS)

        ps1.out_on_off(3, 1)
        time.sleep(.3)  # VEE
        ps1.out_on_off(2, 1)
        time.sleep(.3)  # VCC
        ps1.out_on_off(1, 1)

    # ----- Prepare DAQ measurement -----
    ch_str = "101:115"
    if not daq_out:
        # [Mano] This will not be effective as MEAS uses factory reset settings for all measurement parameters
        # except for the range and resolution if provided

        #daq.write(f"CONF:VOLT:DC (@{ch_str})")
        daq.set_voltage_range(10, ch_str)
        daq.set_voltage_integration_time(1, ch_str)
        daq.set_impedance_mode("ON", ch_str)
        daq.set_voltage_auto_zero("ON", ch_str)

    time.sleep(1)

    if not ps1_out:
        current = ps1.meas_current_ch(1) * 1e3
        print(f"VDD Current {current:.3f}")
        current = ps1.meas_current_ch(2) * 1e3
        print(f"VCC Current {current:.3f}")
        current = ps1.meas_current_ch(3) * 1e3
        print(f"VEE Current {current:.3f}")

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

    for dac in range(1):
        lo_dac = dac & 0xFF
        hi_dac = dac >> 8
        list_dac = [0x99, 0x05, 0x99, 0x05, 0x99, 0x05]
        print("Apply -6.5V VGG to pinch off all amplifiers")
        amc7836.write_register(amc7836.REGISTER_ADDRESSES["DACA0_DATA_LO"], list_dac)
        amc7836.write_register(amc7836.REGISTER_ADDRESSES["REG_UPDATE"], 0x01)
        time.sleep(0.1)
        # voltage = daq.query("MEAS:VOLT:DC? (@101)")
        voltage = daq.measure_voltage(101)
        print(f"VGG2 Voltage = {voltage:0.5f}")
        # voltage = daq.query("MEAS:VOLT:DC? (@102)")
        voltage = daq.measure_voltage(102)
        print(f"VGG3_P Voltage = {voltage:0.5f}")
        # voltage = daq.query("MEAS:VOLT:DC? (@103)")
        voltage = daq.measure_voltage(103)
        print(f"VGG3_C Voltage = {voltage:0.5f}")

        time.sleep(1)
        if not ps3_out:
            ps3.set_output_voltage(1, 50, 0.2)
            time.sleep(0.1)
        if not ps3_out:
            print("Turn ON 50V VDD!!!")
            ps3.out_on_off(1, 1)
            time.sleep(3)

        print("Start VGG2 Bias Search for 20mA")
        sdac_vgg(amc7836, daq, 2990, "DACA0_DATA_LO", 1, 104, 0.02)
        print("Start VGG3_C Bias Search for 100mA")
        sdac_vgg(amc7836, daq, 2990, "DACA2_DATA_LO", 3, 105, 0.1)

        print("Iteration,DateTime,VGG2,VGG3_P,VGG3_C,iVDD2,iVDD3")
        for j in range(1):
            meas_ch = []
            for i in range(5):
                # meas_ch.append(float(daq.query(f"MEAS:VOLT:DC? (@1{i + 1:02d}")))
                meas_ch.append(daq.measure_voltage(101 + i))

            dt = datetime.now().strftime("%y%m%d-%H%M%S")
            print(f"{j},{dt},{meas_ch[0]:.5f},{meas_ch[2]:.5f},{meas_ch[2]:.5f},{meas_ch[3]:.5f},{meas_ch[4]:.5f}")

    val_reg = amc7836.read_register(amc7836.REGISTER_ADDRESSES["DEV_CFG"], 1)
    print(f"POWER_MODE Value 0b{(val_reg & 3):02b}")  # confirm POWER_MODE 0x3 for normal operation

    time.sleep(0.3)
    if not ps3_out:
        ps3.out_on_off(1, 0)
        time.sleep(1)
    if not ps1_out:
        ps1.out_on_off(1, 0)
        ps1.out_on_off(2, 0)
        ps1.out_on_off(3, 0)


if __name__ == "__main__":
    main()