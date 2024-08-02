import pandas
import sys
import warnings
from instrument_lib.dac.amc7836_ftdi_spi import Amc7836FtdiSpi
from instrument_lib.dac.amc7836_ftdi_spi import ADDRESS_MODE

from time import sleep





class Amc7836():
    """
    Class that represents the AMC7834 on the evaluation board.
    Exposes methods to write and read registers, properties for each bit field in each register.
    Dictionaries define register addresses, read bit masks, and shadow register contents.
    Class permits writing to an individual bit field and will use the contents of the shadow registers for the other values.
    If this behavior is not desired, set the boolean property readModifyWrite to True which will then read the register,
    modify the field content, then write the register.
    The class supports robust communication if desired.  Set the boolean property READBACK_EVERY_WRITE to True if desired.
    """

    VALUE_HEADER = "HEX VALUE"
    ADDRESS_HEADER = "ADDRESS"

    def _defineRegisterDictionaries(self):
        """
        Private method called by the constructor to define the class dictionaries to hold the registerAddresses,
        readBitMask values, and shadowRegisters
        """
        self.REGISTER_ADDRESSES = {}
        self.REGISTER_ADDRESSES['ITFC_CFG0'] = 0x00
        self.REGISTER_ADDRESSES['ITFC_CFG1'] = 0x01
        self.REGISTER_ADDRESSES['DEV_CFG'] = 0x02
        self.REGISTER_ADDRESSES['CHIP_TYPE'] = 0x03
        self.REGISTER_ADDRESSES['CHIP_ID_LO'] = 0x04
        self.REGISTER_ADDRESSES['CHIP_ID_HI'] = 0x05
        self.REGISTER_ADDRESSES['CHIP_VERSION'] = 0x6
        self.REGISTER_ADDRESSES['MFGR_ID_LO'] = 0x0C
        self.REGISTER_ADDRESSES['MFGR_ID_HI'] = 0x0D
        self.REGISTER_ADDRESSES['REG_UPDATE'] = 0x0F
        self.REGISTER_ADDRESSES['ADC_CFG'] = 0x10
        self.REGISTER_ADDRESSES['FALSE_ALARM_CFG'] = 0x11
        self.REGISTER_ADDRESSES['GPIO_CFG'] = 0x12
        self.REGISTER_ADDRESSES['ADC_MUX0'] = 0x13
        self.REGISTER_ADDRESSES['ADC_MUX1'] = 0x14
        self.REGISTER_ADDRESSES['ADC_MUX2'] = 0x15
        self.REGISTER_ADDRESSES['ADC_TRIG'] = 0xC0
        self.REGISTER_ADDRESSES['DAC_CLR_EN0'] = 0x18
        self.REGISTER_ADDRESSES['DAC_CLR_EN1'] = 0x19
        self.REGISTER_ADDRESSES['DAC_CLR_SRC0'] = 0x1A
        self.REGISTER_ADDRESSES['DAC_CLR_SRC1'] = 0x1B
        self.REGISTER_ADDRESSES['ALARMOUT_SRC0'] = 0x1C
        self.REGISTER_ADDRESSES['ALARMOUT_SRC1'] = 0x1D
        self.REGISTER_ADDRESSES['DAC_RNG0'] = 0x1E
        self.REGISTER_ADDRESSES['DAC_RNG1'] = 0x1F
        self.REGISTER_ADDRESSES['DACA0_DATA_LO'] = 0x50
        self.REGISTER_ADDRESSES['DACA0_DATA_HI'] = 0x51
        self.REGISTER_ADDRESSES['DACA1_DATA_LO'] = 0x52
        self.REGISTER_ADDRESSES['DACA1_DATA_HI'] = 0x53
        self.REGISTER_ADDRESSES['DACA2_DATA_LO'] = 0x54
        self.REGISTER_ADDRESSES['DACA2_DATA_HI'] = 0x55
        self.REGISTER_ADDRESSES['DACA3_DATA_LO'] = 0x56
        self.REGISTER_ADDRESSES['DACA3_DATA_HI'] = 0x57
        self.REGISTER_ADDRESSES['DACB4_DATA_LO'] = 0x58
        self.REGISTER_ADDRESSES['DACB4_DATA_HI'] = 0x59
        self.REGISTER_ADDRESSES['DACB5_DATA_LO'] = 0x5A
        self.REGISTER_ADDRESSES['DACB5_DATA_HI'] = 0x5B
        self.REGISTER_ADDRESSES['DACB6_DATA_LO'] = 0x5C
        self.REGISTER_ADDRESSES['DACB6_DATA_HI'] = 0x5D
        self.REGISTER_ADDRESSES['DACB7_DATA_LO'] = 0x5E
        self.REGISTER_ADDRESSES['DACB7_DATA_HI'] = 0x5F
        self.REGISTER_ADDRESSES['DACC8_DATA_LO'] = 0x60
        self.REGISTER_ADDRESSES['DACC8_DATA_HI'] = 0x61
        self.REGISTER_ADDRESSES['DACC9_DATA_LO'] = 0x62
        self.REGISTER_ADDRESSES['DACC9_DATA_HI'] = 0x63
        self.REGISTER_ADDRESSES['DACC10_DATA_LO'] = 0x64
        self.REGISTER_ADDRESSES['DACC10_DATA_HI'] = 0x65
        self.REGISTER_ADDRESSES['DACC11_DATA_LO'] = 0x66
        self.REGISTER_ADDRESSES['DACC11_DATA_HI'] = 0x67
        self.REGISTER_ADDRESSES['DACD12_DATA_LO'] = 0x68
        self.REGISTER_ADDRESSES['DACD12_DATA_HI'] = 0x69
        self.REGISTER_ADDRESSES['DACD13_DATA_LO'] = 0x6A
        self.REGISTER_ADDRESSES['DACD13_DATA_HI'] = 0x6B
        self.REGISTER_ADDRESSES['DACD14_DATA_LO'] = 0x6C
        self.REGISTER_ADDRESSES['DACD14_DATA_HI'] = 0x6D
        self.REGISTER_ADDRESSES['DACD15_DATA_LO'] = 0x6E
        self.REGISTER_ADDRESSES['DACD15_DATA_HI'] = 0x6F
        self.REGISTER_ADDRESSES['DAC_CLR0'] = 0xB0
        self.REGISTER_ADDRESSES['DAC_CLR1'] = 0xB1
        self.REGISTER_ADDRESSES['DAC_PD0'] = 0xB2
        self.REGISTER_ADDRESSES['DAC_PD1'] = 0xB3
        self.REGISTER_ADDRESSES['ADC_PD2'] = 0xB4
        self.REGISTER_ADDRESSES['ADC_TRG'] = 0xC0

        """
        self.REGISTER_ADDRESSES['ADC_IN0_DATA_H'] = 0x21
        self.REGISTER_ADDRESSES['ADC_IN0_DATA_L'] = 0x20
        self.REGISTER_ADDRESSES['ADC_IN0_HYST'] = 0x68
        self.REGISTER_ADDRESSES['ADC_IN0_LO_THR_H'] = 0x53
        self.REGISTER_ADDRESSES['ADC_IN0_LO_THR_L'] = 0x52
        self.REGISTER_ADDRESSES['ADC_IN0_UP_THR_H'] = 0x51
        self.REGISTER_ADDRESSES['ADC_IN0_UP_THR_L'] = 0x50
        self.REGISTER_ADDRESSES['ADC_IN1_DATA_H'] = 0x23
        self.REGISTER_ADDRESSES['ADC_IN1_DATA_L'] = 0x22
        self.REGISTER_ADDRESSES['ADC_IN1_HYST'] = 0x69
        self.REGISTER_ADDRESSES['ADC_IN1_LO_THR_H'] = 0x57
        self.REGISTER_ADDRESSES['ADC_IN1_LO_THR_L'] = 0x56
        self.REGISTER_ADDRESSES['ADC_IN1_UP_THR_H'] = 0x55
        self.REGISTER_ADDRESSES['ADC_IN1_UP_THR_L'] = 0x54
        self.REGISTER_ADDRESSES['ADC_MUX_CFG'] = 0x15
        self.REGISTER_ADDRESSES['ADC_TRIG'] = 0x7D
        self.REGISTER_ADDRESSES['ALR_CFG_1'] = 0x1D
        self.REGISTER_ADDRESSES['ALR_STAT_0'] = 0x40
        self.REGISTER_ADDRESSES['ALR_STAT_1'] = 0x41
        self.REGISTER_ADDRESSES['CHIP_ID_H'] = 0x5
        
        self.REGISTER_ADDRESSES['CHIP_TYPE'] = 0x3
        self.REGISTER_ADDRESSES['CS_A_HYST'] = 0x6A
        self.REGISTER_ADDRESSES['CS_A_LO_THR_H'] = 0x5B
        self.REGISTER_ADDRESSES['CS_A_LO_THR_L'] = 0x5A
        self.REGISTER_ADDRESSES['CS_A_UP_THR_H'] = 0x59
        self.REGISTER_ADDRESSES['CS_A_UP_THR_L'] = 0x58
        self.REGISTER_ADDRESSES['CS_B_HYST'] = 0x6B
        self.REGISTER_ADDRESSES['CS_B_LO_THR_H'] = 0x5F
        self.REGISTER_ADDRESSES['CS_B_LO_THR_L'] = 0x5E
        self.REGISTER_ADDRESSES['CS_B_UP_THR_H'] = 0x5D
        self.REGISTER_ADDRESSES['CS_B_UP_THR_L'] = 0x5C
        self.REGISTER_ADDRESSES['DAC0_DATA_H'] = 0x31
        self.REGISTER_ADDRESSES['DAC0_DATA_L'] = 0x30
        self.REGISTER_ADDRESSES['DAC1_DATA_H'] = 0x33
        self.REGISTER_ADDRESSES['DAC1_DATA_L'] = 0x32
        self.REGISTER_ADDRESSES['DAC2_DATA_H'] = 0x35
        self.REGISTER_ADDRESSES['DAC2_DATA_L'] = 0x34
        self.REGISTER_ADDRESSES['DAC3_DATA_H'] = 0x37
        self.REGISTER_ADDRESSES['DAC3_DATA_L'] = 0x36
        self.REGISTER_ADDRESSES['DAC4_DATA_H'] = 0x39
        self.REGISTER_ADDRESSES['DAC4_DATA_L'] = 0x38
        self.REGISTER_ADDRESSES['DAC5_DATA_H'] = 0x3B
        self.REGISTER_ADDRESSES['DAC5_DATA_L'] = 0x3A
        self.REGISTER_ADDRESSES['DAC6_DATA_H'] = 0x3D
        self.REGISTER_ADDRESSES['DAC6_DATA_L'] = 0x3C
        self.REGISTER_ADDRESSES['DAC7_DATA_H'] = 0x3F
        self.REGISTER_ADDRESSES['DAC7_DATA_L'] = 0x3E
        self.REGISTER_ADDRESSES['DAC_CLR'] = 0x70
        self.REGISTER_ADDRESSES['DAC_CLR_EN'] = 0x18
        self.REGISTER_ADDRESSES['DAC_CLR_SRC_0'] = 0x1A
        self.REGISTER_ADDRESSES['DAC_CLR_SRC_1'] = 0x1B
        self.REGISTER_ADDRESSES['DAC_OUT_OK_CFG'] = 0x17
        self.REGISTER_ADDRESSES['DAC_RANGE'] = 0x1E
        self.REGISTER_ADDRESSES['DAC_SW_EN'] = 0x46
        self.REGISTER_ADDRESSES['FALSE_ALR_CFG'] = 0x11
        
        self.REGISTER_ADDRESSES['GEN_STAT_1'] = 0x43
        self.REGISTER_ADDRESSES['GEN_STAT_2'] = 0x44
        self.REGISTER_ADDRESSES['IF_CFG_0'] = 0x0
        self.REGISTER_ADDRESSES['IF_CFG_1'] = 0x1
        self.REGISTER_ADDRESSES['LT_DATA_H'] = 0x29
        self.REGISTER_ADDRESSES['LT_DATA_L'] = 0x28
        self.REGISTER_ADDRESSES['LT_HYST'] = 0x6C
        self.REGISTER_ADDRESSES['LT_LO_THR_H'] = 0x63
        self.REGISTER_ADDRESSES['LT_LO_THR_L'] = 0x62
        self.REGISTER_ADDRESSES['LT_UP_THR_H'] = 0x61
        self.REGISTER_ADDRESSES['LT_UP_THR_L'] = 0x60
        
        self.REGISTER_ADDRESSES['MIPI_MAN_ID_L'] = 0xC
        self.REGISTER_ADDRESSES['OUT_AEN_GROUPA'] = 0x47
        self.REGISTER_ADDRESSES['OUT_AEN_GROUPB'] = 0x48
        self.REGISTER_ADDRESSES['OUT_BEN_GROUPA'] = 0x49
        self.REGISTER_ADDRESSES['OUT_BEN_GROUPB'] = 0x4A
        self.REGISTER_ADDRESSES['PD_ADC'] = 0x72
        self.REGISTER_ADDRESSES['PD_CS'] = 0x73
        self.REGISTER_ADDRESSES['PD_DAC'] = 0x71
        
        self.REGISTER_ADDRESSES['REG_UPDATE'] = 0xF
        self.REGISTER_ADDRESSES['RT_DATA_H'] = 0x2B
        self.REGISTER_ADDRESSES['RT_DATA_L'] = 0x2A
        self.REGISTER_ADDRESSES['RT_HYST'] = 0x6D
        self.REGISTER_ADDRESSES['RT_LO_THR_H'] = 0x67
        self.REGISTER_ADDRESSES['RT_LO_THR_L'] = 0x66
        self.REGISTER_ADDRESSES['RT_UP_THR_H'] = 0x65
        self.REGISTER_ADDRESSES['RT_UP_THR_L'] = 0x64


        """

        self.READ_COMP_MASK = {}
        self.READ_COMP_MASK['ADC_AVG'] = 0xFF
        self.READ_COMP_MASK['ADC_CAL_CNTL'] = 0xFF
        self.READ_COMP_MASK['ADC_CFG'] = 0xFF
        self.READ_COMP_MASK['ADC_CTRL_SIG'] = 0xFF
        self.READ_COMP_MASK['ADC_DATA_H'] = 0xFF
        self.READ_COMP_MASK['ADC_DATA_L'] = 0xFF
        self.READ_COMP_MASK['ADC_IN0_DATA_H'] = 0xFF
        self.READ_COMP_MASK['ADC_IN0_DATA_L'] = 0xFF
        self.READ_COMP_MASK['ADC_IN0_HYST'] = 0xFF
        self.READ_COMP_MASK['ADC_IN0_LO_THR_H'] = 0xFF
        self.READ_COMP_MASK['ADC_IN0_LO_THR_L'] = 0xFF
        self.READ_COMP_MASK['ADC_IN0_UP_THR_H'] = 0xFF
        self.READ_COMP_MASK['ADC_IN0_UP_THR_L'] = 0xFF
        self.READ_COMP_MASK['ADC_IN1_DATA_H'] = 0xFF
        self.READ_COMP_MASK['ADC_IN1_DATA_L'] = 0xFF
        self.READ_COMP_MASK['ADC_IN1_HYST'] = 0xFF
        self.READ_COMP_MASK['ADC_IN1_LO_THR_H'] = 0xFF
        self.READ_COMP_MASK['ADC_IN1_LO_THR_L'] = 0xFF
        self.READ_COMP_MASK['ADC_IN1_UP_THR_H'] = 0xFF
        self.READ_COMP_MASK['ADC_IN1_UP_THR_L'] = 0xFF
        self.READ_COMP_MASK['ADC_LT_CAL'] = 0xFF
        self.READ_COMP_MASK['ADC_MUX_CFG'] = 0xFF
        self.READ_COMP_MASK['ADC_OFFSET_ADC_IN_CAL'] = 0xFF
        self.READ_COMP_MASK['ADC_OFFSET_CS_CAL'] = 0xFF
        self.READ_COMP_MASK['ADC_OFFSET_LT_CAL'] = 0xFF
        self.READ_COMP_MASK['ADC_OFFSET_RT_CAL'] = 0xFF
        self.READ_COMP_MASK['ADC_RT_CAL'] = 0xFF
        self.READ_COMP_MASK['ADC_TEST_CNTL'] = 0xFF
        self.READ_COMP_MASK['ADC_TRIG'] = 0xFF
        self.READ_COMP_MASK['ADC_TRIM_LDO'] = 0xFF
        self.READ_COMP_MASK['ADC_TRIM_REFBUF'] = 0xFF
        self.READ_COMP_MASK['ADC_TRIM_VCM'] = 0xFF
        self.READ_COMP_MASK['ALR_CFG_0'] = 0xFF
        self.READ_COMP_MASK['ALR_CFG_1'] = 0xFF
        self.READ_COMP_MASK['ALR_STAT_0'] = 0xFF
        self.READ_COMP_MASK['ALR_STAT_1'] = 0xFF
        self.READ_COMP_MASK['ANATOP6'] = 0xFF
        self.READ_COMP_MASK['ANATOP7'] = 0xFF
        self.READ_COMP_MASK['ANATOP8'] = 0xFF
        self.READ_COMP_MASK['ANATOP9'] = 0xFF
        self.READ_COMP_MASK['ANA_DFT_CTRL'] = 0xFF
        self.READ_COMP_MASK['ANA_DFT_MUX_CTRL'] = 0xFF
        self.READ_COMP_MASK['ATEST_CNTL0'] = 0xFF
        self.READ_COMP_MASK['ATEST_CNTL1'] = 0xFF
        self.READ_COMP_MASK['CHIP_ID_H'] = 0xFF
        self.READ_COMP_MASK['CHIP_ID_L'] = 0xFF
        self.READ_COMP_MASK['CHIP_TYPE'] = 0xFF
        self.READ_COMP_MASK['CHIP_VARIANT'] = 0xFF
        self.READ_COMP_MASK['CHIP_VERSION'] = 0xFF
        self.READ_COMP_MASK['COMP_STATUS'] = 0xFF
        self.READ_COMP_MASK['CS_A_DATA_H'] = 0xFF
        self.READ_COMP_MASK['CS_A_DATA_L'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM0'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM1'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM10'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM11'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM12'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM13'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM14'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM15'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM16'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM17'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM18'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM19'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM2'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM3'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM4'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM5'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM6'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM7'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM8'] = 0xFF
        self.READ_COMP_MASK['CS_A_DEL_ER_VCM9'] = 0xFF
        self.READ_COMP_MASK['CS_A_ER_VCM_BASE_H'] = 0xFF
        self.READ_COMP_MASK['CS_A_ER_VCM_BASE_L'] = 0xFF
        self.READ_COMP_MASK['CS_A_GAIN_ERROR'] = 0xFF
        self.READ_COMP_MASK['CS_A_HYST'] = 0xFF
        self.READ_COMP_MASK['CS_A_LO_THR_H'] = 0xFF
        self.READ_COMP_MASK['CS_A_LO_THR_L'] = 0xFF
        self.READ_COMP_MASK['CS_A_LUT0_OFFSET'] = 0xFF
        self.READ_COMP_MASK['CS_A_LUT1_OFFSET'] = 0xFF
        self.READ_COMP_MASK['CS_A_UP_THR_H'] = 0xFF
        self.READ_COMP_MASK['CS_A_UP_THR_L'] = 0xFF
        self.READ_COMP_MASK['CS_A_VCM_BASE_H'] = 0xFF
        self.READ_COMP_MASK['CS_A_VCM_BASE_L'] = 0xFF
        self.READ_COMP_MASK['CS_A_VCM_SLOPE_H'] = 0xFF
        self.READ_COMP_MASK['CS_A_VCM_SLOPE_L'] = 0xFF
        self.READ_COMP_MASK['CS_B_DATA_H'] = 0xFF
        self.READ_COMP_MASK['CS_B_DATA_L'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM0'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM1'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM10'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM11'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM12'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM13'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM14'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM15'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM16'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM17'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM18'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM19'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM2'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM3'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM4'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM5'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM6'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM7'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM8'] = 0xFF
        self.READ_COMP_MASK['CS_B_DEL_ER_VCM9'] = 0xFF
        self.READ_COMP_MASK['CS_B_ER_VCM_BASE_H'] = 0xFF
        self.READ_COMP_MASK['CS_B_ER_VCM_BASE_L'] = 0xFF
        self.READ_COMP_MASK['CS_B_GAIN_ERROR'] = 0xFF
        self.READ_COMP_MASK['CS_B_HYST'] = 0xFF
        self.READ_COMP_MASK['CS_B_LO_THR_H'] = 0xFF
        self.READ_COMP_MASK['CS_B_LO_THR_L'] = 0xFF
        self.READ_COMP_MASK['CS_B_LUT0_OFFSET'] = 0xFF
        self.READ_COMP_MASK['CS_B_LUT1_OFFSET'] = 0xFF
        self.READ_COMP_MASK['CS_B_UP_THR_H'] = 0xFF
        self.READ_COMP_MASK['CS_B_UP_THR_L'] = 0xFF
        self.READ_COMP_MASK['CS_B_VCM_BASE_H'] = 0xFF
        self.READ_COMP_MASK['CS_B_VCM_BASE_L'] = 0xFF
        self.READ_COMP_MASK['CS_B_VCM_SLOPE_H'] = 0xFF
        self.READ_COMP_MASK['CS_B_VCM_SLOPE_L'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_DIFF10_H'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_DIFF10_L'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_ER_FRAC'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_ER_H'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_ER_L'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_ER_LUTP'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_LUTS_H'] = 0xFF
        self.READ_COMP_MASK['CS_CAL_LUTS_L'] = 0xFF
        self.READ_COMP_MASK['CS_CFG_0'] = 0xFF
        self.READ_COMP_MASK['CS_CFG_1'] = 0xFF
        self.READ_COMP_MASK['CS_CFG_2'] = 0xFF
        self.READ_COMP_MASK['CS_DAC_CODE'] = 0xFF
        self.READ_COMP_MASK['CS_DAC_MID_H'] = 0xFF
        self.READ_COMP_MASK['CS_DAC_MID_L'] = 0xFF
        self.READ_COMP_MASK['CS_DAC_SHIFT_COR_H'] = 0xFF
        self.READ_COMP_MASK['CS_DAC_SHIFT_COR_L'] = 0xFF
        self.READ_COMP_MASK['CS_DAC_SHIFT_H'] = 0xFF
        self.READ_COMP_MASK['CS_DAC_SHIFT_L'] = 0xFF
        self.READ_COMP_MASK['CS_DIFF10_H'] = 0xFF
        self.READ_COMP_MASK['CS_DIFF10_L'] = 0xFF
        self.READ_COMP_MASK['CS_DIFF10_OVRD_H'] = 0xFF
        self.READ_COMP_MASK['CS_DIFF10_OVRD_L'] = 0xFF
        self.READ_COMP_MASK['CS_DTEST_CTRL'] = 0xFF
        self.READ_COMP_MASK['CS_GAIN_ER_H'] = 0xFF
        self.READ_COMP_MASK['CS_GAIN_ER_L'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_N10_H'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_N10_L'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_N_DAC_H'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_N_DAC_L'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_P10_H'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_P10_L'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_P_DAC_H'] = 0xFF
        self.READ_COMP_MASK['CS_SENSE_P_DAC_L'] = 0xFF
        self.READ_COMP_MASK['CS_TEST_CTRL'] = 0xFF
        self.READ_COMP_MASK['CS_VCM_H'] = 0xFF
        self.READ_COMP_MASK['CS_VCM_L'] = 0xFF
        self.READ_COMP_MASK['CS_VCM_OVRD_H'] = 0xFF
        self.READ_COMP_MASK['CS_VCM_OVRD_L'] = 0xFF
        self.READ_COMP_MASK['DAC0_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC0_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC0_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC0_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC0_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC0_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC1_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC1_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC1_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC1_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC1_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC1_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC2_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC2_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC2_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC2_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC2_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC2_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC3_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC3_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC3_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC3_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC3_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC3_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC4_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC4_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC4_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC4_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC4_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC4_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC5_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC5_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC5_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC5_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC5_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC5_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC6_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC6_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC6_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC6_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC6_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC6_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC7_DATA_H'] = 0xFF
        self.READ_COMP_MASK['DAC7_DATA_L'] = 0xFF
        self.READ_COMP_MASK['DAC7_GAIN_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC7_GAIN_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC7_OFFSET_CAL_R00'] = 0xFF
        self.READ_COMP_MASK['DAC7_OFFSET_CAL_R11'] = 0xFF
        self.READ_COMP_MASK['DAC_CLR'] = 0xFF
        self.READ_COMP_MASK['DAC_CLR_EN'] = 0xFF
        self.READ_COMP_MASK['DAC_CLR_SRC_0'] = 0xFF
        self.READ_COMP_MASK['DAC_CLR_SRC_1'] = 0xFF
        self.READ_COMP_MASK['DAC_OUT_OK_CFG'] = 0xFF
        self.READ_COMP_MASK['DAC_RANGE'] = 0xFF
        self.READ_COMP_MASK['DAC_SW_EN'] = 0xFF
        self.READ_COMP_MASK['DAC_TEST_CNTL'] = 0xFF
        self.READ_COMP_MASK['DTEST_CNTL0'] = 0xFF
        self.READ_COMP_MASK['E2P_PD_DAC'] = 0xFF
        self.READ_COMP_MASK['EEPROM_CFG'] = 0xFF
        self.READ_COMP_MASK['EEPROM_CNTL'] = 0xFF
        self.READ_COMP_MASK['FALSE_ALR_CFG'] = 0xFF
        self.READ_COMP_MASK['GEN_STAT'] = 0xFF
        self.READ_COMP_MASK['GEN_STAT_1'] = 0xFF
        self.READ_COMP_MASK['GEN_STAT_2'] = 0xFF
        self.READ_COMP_MASK['GPIO_IEB'] = 0xFF
        self.READ_COMP_MASK['GPIO_IN'] = 0xFF
        self.READ_COMP_MASK['GPIO_OEB'] = 0xFF
        self.READ_COMP_MASK['GPIO_OUT'] = 0xFF
        self.READ_COMP_MASK['GPIO_TRACE'] = 0xFF
        self.READ_COMP_MASK['IF_CFG_0'] = 0xFF
        self.READ_COMP_MASK['IF_CFG_1'] = 0xFF
        self.READ_COMP_MASK['LDO_TRIM_IOVDD'] = 0xFF
        self.READ_COMP_MASK['LDO_TRIM_VDDD'] = 0xFF
        self.READ_COMP_MASK['LT_DATA_H'] = 0xFF
        self.READ_COMP_MASK['LT_DATA_L'] = 0xFF
        self.READ_COMP_MASK['LT_HYST'] = 0xFF
        self.READ_COMP_MASK['LT_LO_THR_H'] = 0xFF
        self.READ_COMP_MASK['LT_LO_THR_L'] = 0xFF
        self.READ_COMP_MASK['LT_THERM_THR_H'] = 0xFF
        self.READ_COMP_MASK['LT_THERM_THR_L'] = 0xFF
        self.READ_COMP_MASK['LT_UP_THR_H'] = 0xFF
        self.READ_COMP_MASK['LT_UP_THR_L'] = 0xFF
        self.READ_COMP_MASK['MIPI_MAN_ID_H'] = 0xFF
        self.READ_COMP_MASK['MIPI_MAN_ID_L'] = 0xFF
        self.READ_COMP_MASK['MISC_CNTL'] = 0xFF
        self.READ_COMP_MASK['OSC_CMP_HYST'] = 0xFF
        self.READ_COMP_MASK['OSC_CNT_CMP_H'] = 0xFF
        self.READ_COMP_MASK['OSC_CNT_CMP_L'] = 0xFF
        self.READ_COMP_MASK['OSC_CNT_H'] = 0xFF
        self.READ_COMP_MASK['OSC_CNT_L'] = 0xFF
        self.READ_COMP_MASK['OSC_TRIM_TEST'] = 0xFF
        self.READ_COMP_MASK['OUT_AEN_GROUPA'] = 0xFF
        self.READ_COMP_MASK['OUT_AEN_GROUPB'] = 0xFF
        self.READ_COMP_MASK['OUT_BEN_GROUPA'] = 0xFF
        self.READ_COMP_MASK['OUT_BEN_GROUPB'] = 0xFF
        self.READ_COMP_MASK['PD_ADC'] = 0xFF
        self.READ_COMP_MASK['PD_CS'] = 0xFF
        self.READ_COMP_MASK['PD_DAC'] = 0xFF
        self.READ_COMP_MASK['PD_DAC_CFG'] = 0xFF
        self.READ_COMP_MASK['POR_BYPASS_H'] = 0xFF
        self.READ_COMP_MASK['POR_BYPASS_L'] = 0xFF
        self.READ_COMP_MASK['REG_UPDATE'] = 0xFF
        self.READ_COMP_MASK['RT_DATA_H'] = 0xFF
        self.READ_COMP_MASK['RT_DATA_L'] = 0xFF
        self.READ_COMP_MASK['RT_HYST'] = 0xFF
        self.READ_COMP_MASK['RT_LO_THR_H'] = 0xFF
        self.READ_COMP_MASK['RT_LO_THR_L'] = 0xFF
        self.READ_COMP_MASK['RT_UP_THR_H'] = 0xFF
        self.READ_COMP_MASK['RT_UP_THR_L'] = 0xFF
        self.READ_COMP_MASK['SPIKE_FILTER_CAL_SCL'] = 0xFF
        self.READ_COMP_MASK['SPIKE_FILTER_CAL_SDA'] = 0xFF
        self.READ_COMP_MASK['TEST_KEY'] = 0xFF
        self.READ_COMP_MASK['TRIM_BG'] = 0xFF
        self.READ_COMP_MASK['TRIM_OSC'] = 0xFF

    def defineAMC7836Defaults(self):
        self._BITFIELD = {}
        self._BITFIELD['SOFT_RESET'] = 0x0
        self._BITFIELD['RSVD_6_IF_CFG_0'] = 0x0
        self._BITFIELD['ADDR_ASCEND'] = 0x1
        self._BITFIELD['RSVD_4_0_IF_CFG_0'] = 0x10
        self._BITFIELD['SINGLE_INSTR'] = 0x0
        self._BITFIELD['RSVD_6_IF_CFG_1'] = 0x0
        self._BITFIELD['READBACK'] = 0x0
        self._BITFIELD['ADDR_MODE'] = 0x0
        self._BITFIELD['RSVD_3_0_IF_CFG_1'] = 0x0
        self._BITFIELD['RSVD_7_4_CHIP_TYPE'] = 0x0
        self._BITFIELD['CHIP_TYPE'] = 0x8
        self._BITFIELD['CHIPDID_LOW'] = 0x37
        self._BITFIELD['CHIPDID_HIGH'] = 0xC
        self._BITFIELD['VERSIONID'] = 0x4
        self._BITFIELD['RSVD_7_4_CHIP_VARIANT'] = 0x0
        self._BITFIELD['CHIP_VARIANT'] = 0x1
        self._BITFIELD['MAN_ID_LOW'] = 0x66
        self._BITFIELD['RSVD_0_MIPI_MAN_ID_L'] = 0x0
        self._BITFIELD['MAN_ID_HIGH'] = 0x4
        self._BITFIELD['RSVD_7_5_REG_UPDATE'] = 0x0
        self._BITFIELD['ADC_UPDATE'] = 0x0
        self._BITFIELD['RSVD_3_1_REG_UPDATE'] = 0x0
        self._BITFIELD['DAC_UPDATE'] = 0x0
        self._BITFIELD['CMODE'] = 0x0
        self._BITFIELD['ADC_CONV_RATE'] = 0x0
        self._BITFIELD['ADC_REF_BUFF'] = 0x0
        self._BITFIELD['RSVD_3_2_ADC_CFG'] = 0x0
        self._BITFIELD['RT_CONV_RATE'] = 0x0
        self._BITFIELD['CH_FALR_CT'] = 0x3
        self._BITFIELD['LT_FALR_CT'] = 0x2
        self._BITFIELD['RT_FALR_CT'] = 0x2
        self._BITFIELD['RSVD_0_FALSE_ALR_CFG'] = 0x0
        self._BITFIELD['RSVD_7_4_ADC_AVG'] = 0x0
        self._BITFIELD['ADC_AVG_ADC'] = 0x0
        self._BITFIELD['RSVD_7_6_ADC_MUX_CFG'] = 0x0
        self._BITFIELD['RT_CH'] = 0x0
        self._BITFIELD['LT_CH'] = 0x0
        self._BITFIELD['CS_B'] = 0x0
        self._BITFIELD['CS_A'] = 0x0
        self._BITFIELD['ADC_IN1'] = 0x0
        self._BITFIELD['ADC_IN0'] = 0x0
        self._BITFIELD['ASSERT'] = 0x0
        self._BITFIELD['TIMER'] = 0x1
        self._BITFIELD['CLREN_B7'] = 0x0
        self._BITFIELD['CLREN_B6'] = 0x0
        self._BITFIELD['CLREN_B5'] = 0x0
        self._BITFIELD['CLREN_B4'] = 0x0
        self._BITFIELD['CLREN_A3'] = 0x0
        self._BITFIELD['CLREN_A2'] = 0x0
        self._BITFIELD['CLREN_A1'] = 0x0
        self._BITFIELD['CLREN_A0'] = 0x0
        self._BITFIELD['RSVD_7_6_DAC_CLR_SRC_0'] = 0x0
        self._BITFIELD['RT_HIGH_ALR_CLR'] = 0x0
        self._BITFIELD['RT_LOW_ALR_CLR'] = 0x0
        self._BITFIELD['CS_B_ALR_CLR'] = 0x0
        self._BITFIELD['CS_A_ALR_CLR'] = 0x0
        self._BITFIELD['ADC_IN1_ALR_CLR'] = 0x0
        self._BITFIELD['ADC_IN0_ALR_CLR'] = 0x0
        self._BITFIELD['RSVD_7_3_DAC_CLR_SRC_1'] = 0x0
        self._BITFIELD['THERM_ALR_CLR'] = 0x0
        self._BITFIELD['LT_HIGH_ALR_CLR'] = 0x0
        self._BITFIELD['LT_LOW_ALR_CLR'] = 0x0
        self._BITFIELD['RSVD_7_6_ALR_CFG_0'] = 0x0
        self._BITFIELD['RT_HIGH_ALR_STAT'] = 0x0
        self._BITFIELD['RT_LOW_ALR_STAT'] = 0x0
        self._BITFIELD['CS_B_ALR_STAT'] = 0x0
        self._BITFIELD['CS_A_ALR_STAT'] = 0x0
        self._BITFIELD['ADC_IN1_ALR_STAT'] = 0x0
        self._BITFIELD['ADC_IN0_ALR_STAT'] = 0x0
        self._BITFIELD['ALR_LATCH_DIS'] = 0x0
        self._BITFIELD['RSVD_6_ALR_CFG_1'] = 0x0
        self._BITFIELD['S0S1_ERR_ALR'] = 0x0
        self._BITFIELD['PAR_ERR_ALR'] = 0x0
        self._BITFIELD['DAV_ALR'] = 0x0
        self._BITFIELD['THERM_ALR'] = 0x0
        self._BITFIELD['LT_HIGH_ALR'] = 0x0
        self._BITFIELD['LT_LOW_ALR'] = 0x0
        self._BITFIELD['RSVD_7_DAC_RANGE'] = 0x0
        self._BITFIELD['DAC_RANGEB'] = 0x0
        self._BITFIELD['RSVD_3_DAC_RANGE'] = 0x0
        self._BITFIELD['DAC_RANGEA'] = 0x0
        self._BITFIELD['ADC_IN0_DATA_L'] = 0x0
        self._BITFIELD['RSVD_7_4_ADC_IN0_DATA_H'] = 0x0
        self._BITFIELD['ADC_IN0_DATA_H'] = 0x0
        self._BITFIELD['ADC_IN1_DATA_L'] = 0x0
        self._BITFIELD['RSVD_7_4_ADC_IN1_DATA_H'] = 0x0
        self._BITFIELD['ADC_IN1_DATA_H'] = 0x0
        self._BITFIELD['CS_A_DATA_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_A_DATA_H'] = 0x0
        self._BITFIELD['CS_A_DATA_H_SIGN'] = 0x0
        self._BITFIELD['CS_A_DATA_H'] = 0x0
        self._BITFIELD['CS_B_DATA_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_B_DATA_H'] = 0x0
        self._BITFIELD['CS_B_DATA_H_SIGN'] = 0x0
        self._BITFIELD['CS_B_DATA_H'] = 0x0
        self._BITFIELD['LT_DATA_L'] = 0x0
        self._BITFIELD['RSVD_7_4_LT_DATA_H'] = 0x0
        self._BITFIELD['LT_DATA_H'] = 0x0
        self._BITFIELD['RT_DATA_L'] = 0x0
        self._BITFIELD['RSVD_7_4_RT_DATA_H'] = 0x0
        self._BITFIELD['RT_DATA_H'] = 0x0
        self._BITFIELD['DAC0_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC0_DATA_H'] = 0x0
        self._BITFIELD['DAC0_DATA_H'] = 0x6
        self._BITFIELD['DAC1_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC1_DATA_H'] = 0x0
        self._BITFIELD['DAC1_DATA_H'] = 0x6
        self._BITFIELD['DAC2_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC2_DATA_H'] = 0x0
        self._BITFIELD['DAC2_DATA_H'] = 0x6
        self._BITFIELD['DAC3_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC3_DATA_H'] = 0x0
        self._BITFIELD['DAC3_DATA_H'] = 0x6
        self._BITFIELD['DAC4_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC4_DATA_H'] = 0x0
        self._BITFIELD['DAC4_DATA_H'] = 0x6
        self._BITFIELD['DAC5_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC5_DATA_H'] = 0x0
        self._BITFIELD['DAC5_DATA_H'] = 0x6
        self._BITFIELD['DAC6_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC6_DATA_H'] = 0x0
        self._BITFIELD['DAC6_DATA_H'] = 0x6
        self._BITFIELD['DAC7_DATA_L'] = 0x66
        self._BITFIELD['RSVD_7_4_DAC7_DATA_H'] = 0x0
        self._BITFIELD['DAC7_DATA_H'] = 0x6
        self._BITFIELD['RSVD_7_4_ALR_STAT_0'] = 0x0
        self._BITFIELD['RT_HIGH_ALR'] = 0x0
        self._BITFIELD['RT_LOW_ALR'] = 0x0
        self._BITFIELD['CS_B_ALR'] = 0x0
        self._BITFIELD['CS_A_ALR'] = 0x0
        self._BITFIELD['ADC_IN1_ALR'] = 0x0
        self._BITFIELD['ADC_IN0_ALR'] = 0x0
        self._BITFIELD['RSVD_7_6_ALR_STAT_1'] = 0x0
        self._BITFIELD['S0S1_ERR_ALR_STAT'] = 0x0
        self._BITFIELD['PAR_ERR_ALR_STAT'] = 0x0
        self._BITFIELD['DAV_ALR_STAT'] = 0x0
        self._BITFIELD['THERM_ALR_STAT'] = 0x0
        self._BITFIELD['LT_HIGH_ALR_STAT'] = 0x0
        self._BITFIELD['LT_LOW_ALR_STAT'] = 0x0
        self._BITFIELD['IBI_PEND'] = 0x0
        self._BITFIELD['IBI_ENABLE'] = 0x1
        self._BITFIELD['AVSSB'] = 0x0
        self._BITFIELD['AVSSA'] = 0x0
        self._BITFIELD['ADC_IDLE'] = 0x1
        self._BITFIELD['I3C_MODE'] = 0x0
        self._BITFIELD['GALR'] = 0x0
        self._BITFIELD['DAVF'] = 0x0
        self._BITFIELD['RSVD_7_2_GEN_STAT_1'] = 0x0
        self._BITFIELD['AVCCB'] = 0x0
        self._BITFIELD['AVCCA'] = 0x0
        self._BITFIELD['DAC_OUT_OK'] = 0x0
        self._BITFIELD['RSVD_6_GEN_STAT_2'] = 0x0
        self._BITFIELD['DAC_POWER_OK'] = 0x1
        self._BITFIELD['AVSS_OK'] = 0x1
        self._BITFIELD['AVCC_OK'] = 0x1
        self._BITFIELD['IOVDD_OK'] = 0x1
        self._BITFIELD['RSVD_1_GEN_STAT_2'] = 0x0
        self._BITFIELD['AVDD_OK'] = 0x1
        self._BITFIELD['RSVD_7_4_DAC_SW_EN'] = 0x0
        self._BITFIELD['DAC_B2_SW_EN'] = 0x0
        self._BITFIELD['DAC_B0_SW_EN'] = 0x0
        self._BITFIELD['DAC_A2_SW_EN'] = 0x0
        self._BITFIELD['DAC_A0_SW_EN'] = 0x0
        self._BITFIELD['RSVD_7_OUT_AEN_GROUPA'] = 0x0
        self._BITFIELD['FETDRV_A2_AEN_GROUPA'] = 0x1
        self._BITFIELD['RSVD_5_OUT_AEN_GROUPA'] = 0x0
        self._BITFIELD['FETDRV_A0_AEN_GROUPA'] = 0x1
        self._BITFIELD['DAC_A3_AEN_GROUPA'] = 0x0
        self._BITFIELD['DAC_A2_AEN_GROUPA'] = 0x0
        self._BITFIELD['DAC_A1_AEN_GROUPA'] = 0x0
        self._BITFIELD['DAC_A0_AEN_GROUPA'] = 0x0
        self._BITFIELD['RSVD_7_OUT_AEN_GROUPB'] = 0x0
        self._BITFIELD['FETDRV_B2_AEN_GROUPB'] = 0x0
        self._BITFIELD['RSVD_5_OUT_AEN_GROUPB'] = 0x0
        self._BITFIELD['FETDRV_B0_AEN_GROUPB'] = 0x0
        self._BITFIELD['DAC_B3_AEN_GROUPB'] = 0x0
        self._BITFIELD['DAC_B2_AEN_GROUPB'] = 0x0
        self._BITFIELD['DAC_B1_AEN_GROUPB'] = 0x0
        self._BITFIELD['DAC_B0_AEN_GROUPB'] = 0x0
        self._BITFIELD['RSVD_7_OUT_BEN_GROUPA'] = 0x0
        self._BITFIELD['FETDRV_A2_BEN_GROUPA'] = 0x0
        self._BITFIELD['RSVD_5_OUT_BEN_GROUPA'] = 0x0
        self._BITFIELD['FETDRV_A0_BEN_GROUPA'] = 0x0
        self._BITFIELD['DAC_A3_BEN_GROUPA'] = 0x0
        self._BITFIELD['DAC_A2_BEN_GROUPA'] = 0x0
        self._BITFIELD['DAC_A1_BEN_GROUPA'] = 0x0
        self._BITFIELD['DAC_A0_BEN_GROUPA'] = 0x0
        self._BITFIELD['RSVD_7_OUT_BEN_GROUPB'] = 0x0
        self._BITFIELD['FETDRV_B2_BEN_GROUPB'] = 0x1
        self._BITFIELD['RSVD_5_OUT_BEN_GROUPB'] = 0x0
        self._BITFIELD['FETDRV_B0_BEN_GROUPB'] = 0x1
        self._BITFIELD['DAC_B3_BEN_GROUPB'] = 0x0
        self._BITFIELD['DAC_B2_BEN_GROUPB'] = 0x0
        self._BITFIELD['DAC_B1_BEN_GROUPB'] = 0x0
        self._BITFIELD['DAC_B0_BEN_GROUPB'] = 0x0
        self._BITFIELD['THRU_ADC_IN0_L'] = 0xFF
        self._BITFIELD['RSVD_7_4_ADC_IN0_UP_THR_H'] = 0x0
        self._BITFIELD['THRU_ADC_IN0_H'] = 0xF
        self._BITFIELD['THRL_ADC_IN0_L'] = 0x0
        self._BITFIELD['RSVD_7_4_ADC_IN0_LO_THR_H'] = 0x0
        self._BITFIELD['THRL_ADC_IN0_H'] = 0x0
        self._BITFIELD['THRU_ADC_IN1_L'] = 0xFF
        self._BITFIELD['RSVD_7_4_ADC_IN1_UP_THR_H'] = 0x0
        self._BITFIELD['THRU_ADC_IN1_H'] = 0xF
        self._BITFIELD['THRL_ADC_IN1_L'] = 0x0
        self._BITFIELD['RSVD_7_4_ADC_IN1_LO_THR_H'] = 0x0
        self._BITFIELD['THRL_ADC_IN1_H'] = 0x0
        self._BITFIELD['THRU_CS_A_L'] = 0xFF
        self._BITFIELD['RSVD_7_4_CS_A_UP_THR_H'] = 0x0
        self._BITFIELD['THRU_CS_A_H'] = 0xF
        self._BITFIELD['THRL_CS_A_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_A_LO_THR_H'] = 0x0
        self._BITFIELD['THRL_CS_A_H'] = 0x0
        self._BITFIELD['THRU_CS_B_L'] = 0xFF
        self._BITFIELD['RSVD_7_4_CS_B_UP_THR_H'] = 0x0
        self._BITFIELD['THRU_CS_B_H'] = 0xF
        self._BITFIELD['THRL_CS_B_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_B_LO_THR_H'] = 0x0
        self._BITFIELD['THRL_CS_B_H'] = 0x0
        self._BITFIELD['THRU_LT_L'] = 0xFF
        self._BITFIELD['RSVD_7_4_LT_UP_THR_H'] = 0x0
        self._BITFIELD['THRU_LT_H'] = 0x7
        self._BITFIELD['THRL_LT_L'] = 0x0
        self._BITFIELD['RSVD_7_4_LT_LO_THR_H'] = 0x0
        self._BITFIELD['THRL_LT_H'] = 0x8
        self._BITFIELD['THRU_RT_L'] = 0xFF
        self._BITFIELD['RSVD_7_4_RT_UP_THR_H'] = 0x0
        self._BITFIELD['THRU_RT_H'] = 0x7
        self._BITFIELD['THRL_RT_L'] = 0x0
        self._BITFIELD['RSVD_7_4_RT_LO_THR_H'] = 0x0
        self._BITFIELD['THRL_RT_H'] = 0x8
        self._BITFIELD['RSVD_7_ADC_IN0_HYST'] = 0x0
        self._BITFIELD['HYST_ADC_IN0'] = 0x8
        self._BITFIELD['RSVD_7_ADC_IN1_HYST'] = 0x0
        self._BITFIELD['HYST_ADC_IN1'] = 0x8
        self._BITFIELD['RSVD_7_CS_A_HYST'] = 0x0
        self._BITFIELD['HYST_CS_A'] = 0x8
        self._BITFIELD['RSVD_7_CS_B_HYST'] = 0x0
        self._BITFIELD['HYST_CS_B'] = 0x8
        self._BITFIELD['RSVD_7_5_LT_HYST'] = 0x0
        self._BITFIELD['HYST_LT'] = 0x8
        self._BITFIELD['RSVD_7_5_RT_HYST'] = 0x0
        self._BITFIELD['HYST_RT'] = 0x8
        self._BITFIELD['CLR_B7'] = 0x0
        self._BITFIELD['CLR_B6'] = 0x0
        self._BITFIELD['CLR_B5'] = 0x0
        self._BITFIELD['CLR_B4'] = 0x0
        self._BITFIELD['CLR_A3'] = 0x0
        self._BITFIELD['CLR_A2'] = 0x0
        self._BITFIELD['CLR_A1'] = 0x0
        self._BITFIELD['CLR_A0'] = 0x0
        self._BITFIELD['PDAC_B7'] = 0x0
        self._BITFIELD['PDAC_B6'] = 0x0
        self._BITFIELD['PDAC_B5'] = 0x0
        self._BITFIELD['PDAC_B4'] = 0x0
        self._BITFIELD['PDAC_A3'] = 0x0
        self._BITFIELD['PDAC_A2'] = 0x0
        self._BITFIELD['PDAC_A1'] = 0x0
        self._BITFIELD['PDAC_A0'] = 0x0
        self._BITFIELD['RSVD_7_1_PD_ADC'] = 0x0
        self._BITFIELD['PADC'] = 0x0
        self._BITFIELD['RSVD_7_2_PD_CS'] = 0x0
        self._BITFIELD['PCS_B'] = 0x0
        self._BITFIELD['PCS_A'] = 0x0
        self._BITFIELD['RSVD_7_1_ADC_TRIG'] = 0x0
        self._BITFIELD['ICONV'] = 0x0
        self._BITFIELD['DAC0_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC1_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC2_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC3_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC4_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC5_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC6_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC7_GAIN_CAL_R00'] = 0x40
        self._BITFIELD['DAC0_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC1_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC2_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC3_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC4_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC5_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC6_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC7_OFFSET_CAL_R00'] = 0x20
        self._BITFIELD['DAC0_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC1_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC2_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC3_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC4_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC5_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC6_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC7_GAIN_CAL_R11'] = 0x40
        self._BITFIELD['DAC0_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['DAC1_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['DAC2_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['DAC3_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['DAC4_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['DAC5_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['DAC6_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['DAC7_OFFSET_CAL_R11'] = 0x20
        self._BITFIELD['TRIM_OSC'] = 0x10
        self._BITFIELD['TRIM_BG'] = 0x24
        self._BITFIELD['SPIKE_FILTER_CAL_SCL'] = 0xC
        self._BITFIELD['SPIKE_FILTER_CAL_SDA'] = 0xC
        self._BITFIELD['ADC_TRIM_REFBUF'] = 0x0
        self._BITFIELD['ADC_TRIM_VCM'] = 0x0
        self._BITFIELD['ADC_TRIM_LDO'] = 0x0
        self._BITFIELD['PD_DAC'] = 0x0
        self._BITFIELD['RSVD_7_3_PD_DAC_CFG'] = 0x0
        self._BITFIELD['TIM_DAC_DEL_EN'] = 0x0
        self._BITFIELD['TIM_DAC_DEL'] = 0x0
        self._BITFIELD['CS_A_GAIN_ERROR_SIGN'] = 0x0
        self._BITFIELD['GAIN_ERROR_CS_A_GAIN_ERROR'] = 0x0
        self._BITFIELD['CS_B_GAIN_ERROR_SIGN'] = 0x0
        self._BITFIELD['GAIN_ERROR_CS_B_GAIN_ERROR'] = 0x0
        self._BITFIELD['RSVD_7_6_CS_A_LUT0_OFFSET'] = 0x0
        self._BITFIELD['CS_A_LUT0_OFFSET_LUT0_OFFSET'] = 0x0
        self._BITFIELD['RSVD_7_6_CS_A_LUT1_OFFSET'] = 0x0
        self._BITFIELD['CS_A_LUT1_OFFSET'] = 0x0
        self._BITFIELD['RSVD_7_6_CS_B_LUT0_OFFSET'] = 0x0
        self._BITFIELD['CS_B_LUT0_OFFSET_LUT0_OFFSET'] = 0x0
        self._BITFIELD['RSVD_7_6_CS_B_LUT1_OFFSET'] = 0x0
        self._BITFIELD['CS_B_LUT1_OFFSET'] = 0x0
        self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_SIGN'] = 0x0
        self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE'] = 0x0
        self._BITFIELD['ADC_OFFSET_CS_CAL_SIGN'] = 0x0
        self._BITFIELD['ADC_OFFSET_CS_CAL_OFFSET_VALUE'] = 0x0
        self._BITFIELD['ADC_OFFSET_LT_CAL_SIGN'] = 0x0
        self._BITFIELD['ADC_OFFSET_LT_CAL_OFFSET_VALUE'] = 0x0
        self._BITFIELD['ADC_OFFSET_RT_CAL_SIGN'] = 0x0
        self._BITFIELD['ADC_OFFSET_RT_CAL_OFFSET_VALUE'] = 0x0
        self._BITFIELD['RSVD_7_ADC_CAL_CNTL'] = 0x0
        self._BITFIELD['OFFSET_EN'] = 0x0
        self._BITFIELD['RSVD_5_3_ADC_CAL_CNTL'] = 0x0
        self._BITFIELD['CS_FAST_AVG_EN'] = 0x0
        self._BITFIELD['ADC_SAMPLE_DLY'] = 0x0
        self._BITFIELD['CS_A_VCM_BASE_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_A_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_A_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_A_ER_VCM_BASE_L'] = 0x0
        self._BITFIELD['CS_A_CAL_ALU_BYP'] = 0x0
        self._BITFIELD['RSVD_6_5_CS_A_ER_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_A_ER_VCM_BASE_H_SIGN'] = 0x0
        self._BITFIELD['CS_A_ER_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_A_VCM_SLOPE_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_A_VCM_SLOPE_H'] = 0x0
        self._BITFIELD['CS_A_VCM_SLOPE_H_SIGN'] = 0x0
        self._BITFIELD['CS_A_VCM_SLOPE_H'] = 0x0
        self._BITFIELD['CS_B_VCM_BASE_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_B_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_B_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_B_ER_VCM_BASE_L'] = 0x0
        self._BITFIELD['CS_B_CAL_ALU_BYP'] = 0x0
        self._BITFIELD['RSVD_6_5_CS_B_ER_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_B_ER_VCM_BASE_H_SIGN'] = 0x0
        self._BITFIELD['CS_B_ER_VCM_BASE_H'] = 0x0
        self._BITFIELD['CS_B_VCM_SLOPE_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_B_VCM_SLOPE_H'] = 0x0
        self._BITFIELD['CS_B_VCM_SLOPE_H_SIGN'] = 0x0
        self._BITFIELD['CS_B_VCM_SLOPE_H'] = 0x0
        self._BITFIELD['CS_DAC_MODE'] = 0x0
        self._BITFIELD['CS_DATA_CLAMP_EN'] = 0x0
        self._BITFIELD['CS_ADC_ACQ_DLY_EN'] = 0x0
        self._BITFIELD['CS_CFG_0_SIGN'] = 0x0
        self._BITFIELD['CS_A_DAC_OFFSET'] = 0x0
        self._BITFIELD['CS_CONV_RATE'] = 0x4
        self._BITFIELD['CS_CFG_1_SIGN'] = 0x0
        self._BITFIELD['CS_B_DAC_OFFSET'] = 0x0
        self._BITFIELD['DAC_CODE_BYPASS'] = 0x0
        self._BITFIELD['CS_CFG_2_DAC_CODE'] = 0x0
        self._BITFIELD['I3C_MAX_DS'] = 0x5
        self._BITFIELD['I2C_SPIKE_DIS'] = 0x1
        self._BITFIELD['DAC_CLAMP_EN'] = 0x2
        self._BITFIELD['DAC_ICALP'] = 0x1
        self._BITFIELD['DAC_ICALN'] = 0x1
        self._BITFIELD['LT_SENSE_GAIN_CAL_H'] = 0x3
        self._BITFIELD['LT_SENSE_GAIN_CAL_L'] = 0x7
        self._BITFIELD['RT_SENSE_GAIN_CAL_H'] = 0x0
        self._BITFIELD['RT_SENSE_GAIN_CAL_L'] = 0x0
        self._BITFIELD['THRT_LT_L'] = 0x58
        self._BITFIELD['RSVD_7_4_LT_THERM_THR_H'] = 0x0
        self._BITFIELD['THRT_LT_H'] = 0x2
        self._BITFIELD['CS_A_DEL_ER_VCM0_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM0'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM1_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM1'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM2_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM2'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM3_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM3'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM4_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM4'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM5_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM5'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM6_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM6'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM7_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM7'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM8_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM8'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM9_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM9'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM10_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM10'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM11_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM11'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM12_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM12'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM13_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM13'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM14_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM14'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM15_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM15'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM16_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM16'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM17_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM17'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM18_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM18'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM19_SIGN'] = 0x0
        self._BITFIELD['CS_A_DEL_ER_VCM19'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM0_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM0'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM1_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM1'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM2_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM2'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM3_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM3'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM4_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM4'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM5_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM5'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM6_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM6'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM7_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM7'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM8_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM8'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM9_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM9'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM10_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM10'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM11_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM11'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM12_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM12'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM13_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM13'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM14_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM14'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM15_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM15'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM16_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM16'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM17_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM17'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM18_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM18'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM19_SIGN'] = 0x0
        self._BITFIELD['CS_B_DEL_ER_VCM19'] = 0x0
        self._BITFIELD['CMD_STATUS'] = 0x0
        self._BITFIELD['RSVD_7_2_EEPROM_CFG'] = 0x0
        self._BITFIELD['E2P_FAST_MODE'] = 0x0
        self._BITFIELD['ECC_DIS'] = 0x0
        self._BITFIELD['KEY_STATUS'] = 0x0
        self._BITFIELD['TRIM_DIS'] = 0x0
        self._BITFIELD['OSC_CLK_DIS'] = 0x0
        self._BITFIELD['ADC_TEST'] = 0x0
        self._BITFIELD['OSC_TEST_ENABLE'] = 0x0
        self._BITFIELD['TRACE_PORT'] = 0x0
        self._BITFIELD['OSC_CLK_EXT'] = 0x0
        self._BITFIELD['IO_TEST'] = 0x0
        self._BITFIELD['SCAN_TEST'] = 0x0
        self._BITFIELD['RSVD_7_5_ADC_TEST_CNTL'] = 0x0
        self._BITFIELD['ADC_VCM_EN_SEL'] = 0x0
        self._BITFIELD['ADC_CAL_TM_EN'] = 0x0
        self._BITFIELD['ADC_CAL_OFFSET_EN'] = 0x0
        self._BITFIELD['ADC_LDO_EN'] = 0x1
        self._BITFIELD['ADC_VCM_EN'] = 0x0
        self._BITFIELD['ATEST_CNTL0'] = 0x0
        self._BITFIELD['RSVD_7_ANA_DFT_CTRL'] = 0x0
        self._BITFIELD['EN_BYPASS_ANA_DFT_BUF'] = 0x0
        self._BITFIELD['EN_RES_LADDER_CALIB'] = 0x0
        self._BITFIELD['RES_DIV_SEL'] = 0x0
        self._BITFIELD['EN_RES_DIV'] = 0x0
        self._BITFIELD['EN_DIRECT_PATH'] = 0x0
        self._BITFIELD['EN_ANA_DFT_BUFFER'] = 0x0
        self._BITFIELD['RSVD_7_4_ANA_DFT_MUX_CTRL'] = 0x0
        self._BITFIELD['ANA_DFT_MUX_SEL'] = 0x0
        self._BITFIELD['EN_ANA_DFT_MUX'] = 0x0
        self._BITFIELD['RSVD_7_5_LDO_TRIM_VDDD'] = 0x0
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_20MA'] = 0x0
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_10MA'] = 0x0
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_5MA'] = 0x0
        self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P9V'] = 0x0
        self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P85V'] = 0x0
        self._BITFIELD['RSVD_7_5_LDO_TRIM_IOVDD'] = 0x0
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_20MA'] = 0x0
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_10MA'] = 0x0
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_5MA'] = 0x0
        self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P9V'] = 0x0
        self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P85V'] = 0x0
        self._BITFIELD['ANATOP6'] = 0x0
        self._BITFIELD['ANATOP7'] = 0x0
        self._BITFIELD['ANATOP8'] = 0x0
        self._BITFIELD['ANATOP9'] = 0x0
        self._BITFIELD['RSVD_7_5_GPIO_TRACE'] = 0x0
        self._BITFIELD['GPIO_TRACE'] = 0x0
        self._BITFIELD['RSVD_7_1_ATEST_CNTL1'] = 0x0
        self._BITFIELD['SPIKE_FILTER_TEST_MODE'] = 0x0
        self._BITFIELD['POR_BYPASS_L'] = 0x34
        self._BITFIELD['POR_BYPASS_H'] = 0x12
        self._BITFIELD['CLK_CNT_CMP_L'] = 0x0
        self._BITFIELD['RSVD_7_4_OSC_CNT_CMP_H'] = 0x0
        self._BITFIELD['CLK_CNT_CMP_H'] = 0x0
        self._BITFIELD['CLK_COUNT_L'] = 0x0
        self._BITFIELD['RSVD_7_4_OSC_CNT_H'] = 0x0
        self._BITFIELD['CLK_COUNT_H'] = 0x0
        self._BITFIELD['OSC_TRIM_TEST'] = 0x10
        self._BITFIELD['RSVD_7_2_OSC_CMP_HYST'] = 0x0
        self._BITFIELD['CMP_HYST'] = 0x0
        self._BITFIELD['DAC_CLAMP_DIS'] = 0x0
        self._BITFIELD['RSVD_6_DAC_TEST_CNTL'] = 0x0
        self._BITFIELD['DAC_HIZ_GROUP_B'] = 0x0
        self._BITFIELD['DAC_HIZ_GROUP_A'] = 0x0
        self._BITFIELD['RSVD_3_0_DAC_TEST_CNTL'] = 0x0
        self._BITFIELD['RSVD_7_2_GPIO_IN'] = 0x0
        self._BITFIELD['OUT_BEN_IN'] = 0x0
        self._BITFIELD['OUT_AEN_IN'] = 0x0
        self._BITFIELD['RSVD_7_2_GPIO_OUT'] = 0x0
        self._BITFIELD['OUT_BEN_OUT'] = 0x0
        self._BITFIELD['RSVD_0_GPIO_OUT'] = 0x0
        self._BITFIELD['RSVD_7_3_GPIO_OEB'] = 0x0
        self._BITFIELD['DAC_OUT_OK_OEB'] = 0x0
        self._BITFIELD['OUT_BEN_OEB'] = 0x1
        self._BITFIELD['RSVD_0_GPIO_OEB'] = 0x0
        self._BITFIELD['RSVD_7_GPIO_IEB'] = 0x0
        self._BITFIELD['DAC_OUT_OK_IEB'] = 0x0
        self._BITFIELD['SDO_IEB'] = 0x0
        self._BITFIELD['SDI_IEB'] = 0x0
        self._BITFIELD['CSB_IEB'] = 0x0
        self._BITFIELD['SCLK_IEB'] = 0x0
        self._BITFIELD['OUT_BEN_IEB'] = 0x0
        self._BITFIELD['OUT_AEN_IEB'] = 0x0
        self._BITFIELD['I2C_SPIKE_OK'] = 0x0
        self._BITFIELD['RSVD_6_COMP_STATUS'] = 0x0
        self._BITFIELD['I3C_1P8V_MODE'] = 0x0
        self._BITFIELD['SPI_I3C_SEL'] = 0x0
        self._BITFIELD['A1_COMP2'] = 0x0
        self._BITFIELD['A1_COMP1'] = 0x0
        self._BITFIELD['A0_COMP2'] = 0x0
        self._BITFIELD['A0_COMP1'] = 0x0
        self._BITFIELD['DIFF10_OVRD_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_DIFF10_OVRD_H'] = 0x0
        self._BITFIELD['CS_DIFF10_OVRD_H_SIGN'] = 0x0
        self._BITFIELD['DIFF10_OVRD_H'] = 0x0
        self._BITFIELD['VCM_OVRD_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_VCM_OVRD_H'] = 0x0
        self._BITFIELD['VCM_OVRD_H'] = 0x0
        self._BITFIELD['CS_B_DTEST_EN'] = 0x0
        self._BITFIELD['CS_B_DTEST_CTRL'] = 0x0
        self._BITFIELD['CS_A_DTEST_EN'] = 0x0
        self._BITFIELD['CS_A_DTEST_CTRL'] = 0x0
        self._BITFIELD['RSVD_7_4_ADC_CTRL_SIG'] = 0x0
        self._BITFIELD['ADC_CAL_START'] = 0x0
        self._BITFIELD['ADC_SAMPLE'] = 0x0
        self._BITFIELD['ADC_SOC'] = 0x0
        self._BITFIELD['ADC_RESETB'] = 0x0
        self._BITFIELD['CS_VCM_OC'] = 0x0
        self._BITFIELD['CS_VCM_OCH'] = 0x0
        self._BITFIELD['CS_VCM_UPDATE'] = 0x0
        self._BITFIELD['CS_CAL_MODE'] = 0x0
        self._BITFIELD['CS_PHASE_CTRL'] = 0x0
        self._BITFIELD['CS_MUX_SEL'] = 0x0
        self._BITFIELD['ADC_DATA_L'] = 0x0
        self._BITFIELD['ADC_EOC'] = 0x0
        self._BITFIELD['RSVD_6_4_ADC_DATA_H'] = 0x0
        self._BITFIELD['ADC_DATA_H'] = 0x0
        self._BITFIELD['VCM_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_VCM_H'] = 0x0
        self._BITFIELD['VCM_H'] = 0x0
        self._BITFIELD['DAC_MID_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_DAC_MID_H'] = 0x0
        self._BITFIELD['DAC_MID_H'] = 0x0
        self._BITFIELD['SENSE_P_DAC_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_SENSE_P_DAC_H'] = 0x0
        self._BITFIELD['SENSE_P_DAC_H'] = 0x0
        self._BITFIELD['SENSE_N_DAC_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_SENSE_N_DAC_H'] = 0x0
        self._BITFIELD['SENSE_N_DAC_H'] = 0x0
        self._BITFIELD['DAC_SHIFT_L'] = 0x0
        self._BITFIELD['RSVD_7_2_CS_DAC_SHIFT_H'] = 0x0
        self._BITFIELD['CS_DAC_SHIFT_H_SIGN'] = 0x0
        self._BITFIELD['DAC_SHIFT_H'] = 0x0
        self._BITFIELD['DAC_SHIFT_COR_L'] = 0x0
        self._BITFIELD['RSVD_7_2_CS_DAC_SHIFT_COR_H'] = 0x0
        self._BITFIELD['CS_DAC_SHIFT_COR_H_SIGN'] = 0x0
        self._BITFIELD['DAC_SHIFT_COR_H'] = 0x0
        self._BITFIELD['RSVD_7_CS_DAC_CODE'] = 0x0
        self._BITFIELD['CS_DAC_CODE'] = 0x40
        self._BITFIELD['SENSE_P10_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_SENSE_P10_H'] = 0x0
        self._BITFIELD['SENSE_P10_H'] = 0x0
        self._BITFIELD['SENSE_N10_L'] = 0x0
        self._BITFIELD['RSVD_7_4_CS_SENSE_N10_H'] = 0x0
        self._BITFIELD['SENSE_N10_H'] = 0x0
        self._BITFIELD['DIFF10_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_DIFF10_H'] = 0x0
        self._BITFIELD['CS_DIFF10_H_SIGN'] = 0x0
        self._BITFIELD['DIFF10_H'] = 0x0
        self._BITFIELD['CAL_ER_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_CAL_ER_H'] = 0x0
        self._BITFIELD['CS_CAL_ER_H_SIGN'] = 0x0
        self._BITFIELD['CAL_ER_H'] = 0x0
        self._BITFIELD['CAL_DIFF10_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_CAL_DIFF10_H'] = 0x0
        self._BITFIELD['CS_CAL_DIFF10_H_SIGN'] = 0x0
        self._BITFIELD['CAL_DIFF10_H'] = 0x0
        self._BITFIELD['RSVD_7_6_CS_CAL_ER_LUTP'] = 0x0
        self._BITFIELD['CAL_ER_LUTP'] = 0x0
        self._BITFIELD['CAL_LUTS_L'] = 0x0
        self._BITFIELD['RSVD_7_5_CS_CAL_LUTS_H'] = 0x0
        self._BITFIELD['CS_CAL_LUTS_H_SIGN'] = 0x0
        self._BITFIELD['CAL_LUTS_H'] = 0x0
        self._BITFIELD['CS_CAL_ER_FRAC_SIGN'] = 0x0
        self._BITFIELD['CAL_ER_FRAC'] = 0x0
        self._BITFIELD['GAIN_ER_L'] = 0x0
        self._BITFIELD['RSVD_7_1_CS_GAIN_ER_H'] = 0x0
        self._BITFIELD['CS_GAIN_ER_H_SIGN'] = 0x0

    def __init__(self, readback: bool = False,
                 serial_number: str = None,
                 spi_clock_rate: int = 1e6,
                 settings_filename: str = None,
                 program_defaults: bool = False,
                 auto_open: bool = False):

        """
        Constructor for AMC7834 class.  You must pass the protocol argument to define SPI/I3C and hardware (FTDI/SCOUT).
        This class instantiates one of the following classes:
        AMC7834_ftdi_spi.py
        AMC7834_ftdi_i3c.py
        f159x_sc4420_spi.py
        f159x_sc4420_i3c.py
        f159x_xdimax_sub20_spi.py
         
        :param readback: Switch to select if every write is verified by reading back from hardware
        :type readback: bool
        
        :param serial_number: Serial number of the USB interface board. Useful if more than one FTDI interface board is present in the system. 
        :type serial_number: string
        
        :param spi_clock_rate: SPI clock rate (Hz) (Ignored in I3C or I2C Modes)
        :type spi_clock_rate: int
        
        :param i3c_clock_rate: I3C clock rate (Hz) - Used for the the SCOUT.  Must be passed even if using I2C. 
        :type i3c_clock_rate: sc4420_Enumerations.I3C_CLOCK_RATE
        
        :param i2c_clock_rate: I2C clock rate (Hz)- Used for the the SCOUT.  Must be passed even if using I3C. 
        :type i2c_clock_rate: sc4420_Enumerations.I2C_CLOCK_RATE
        
        :param settings_filename: Path and file name to use for defaults
        :type settings_filename: string
        
        :param program_defaults: Switch to program defaults to the device
        :type program_defaults: bool
        
        :param deviceType: Select the device type to use with the class 
        :type deviceType: F159X_DEVICE_TYPE
        
        :param auto_open: Switch to select if the USB board is opened in the constructor
        :type auto_open: bool
        
        :param protocol: Selects the communicaton protocol and hardware interface for this class to use
        :type protocol: AMC7834_Enumerations.F159X_PROTOCOL
        
        :param visa_address: Selects the communicaton protocol and hardware interface for this class to use
        :type visa_address: str
        
        :param static_address: Sets the static I2C / I3C address for the bus
        :type static_address: int
        
        :param device_index: Sets the DiMax Sub20 hardware board index
        :type device_index: int
                        
        """

        # Software settings
        self.register_addr_mode = ADDRESS_MODE.ONE_BYTE  # Assumes the part is reset
        self.isOpen = False
        self.settingsFile = settings_filename
        self.programDefaults = program_defaults
        self.hexList = []
        self.readbackValues = {}
        self.REGISTER_ADDRESSES = {}
        self.READ_COMP_MASK = {}
        self._BITFIELD = {}

        # This property ignores shadow registers and always reads back from the hardware
        self.readModifyWrite = False

        self.defineAMC7836Defaults()
        self._defineRegisterDictionaries()

        # Verify a minimum version
        MAJOR_MIN = 3
        MINOR_MIN = 7
        MICRO_MIN = 6
        # Mandate python version 3.7.6
        if (sys.version_info.major < MAJOR_MIN or
                (sys.version_info.major == MAJOR_MIN and sys.version_info.minor < MINOR_MIN) or
                (
                        sys.version_info.major == MAJOR_MIN and sys.version_info.minor == MINOR_MIN and sys.version_info.micro < MICRO_MIN)):
            raise Exception('AMC7834.py: Minimum Python version is %d.%d.%d' % (MAJOR_MIN, MINOR_MIN, MICRO_MIN))

        # Instantiate the proper class for hardware IO        

        self.io = Amc7836FtdiSpi(serial_number, readback)

        self.io.clockFrequencyMHz = spi_clock_rate / 1E6

        # If auto_open is passed as true, call open()
        if auto_open:
            self.open()

    def __del__(self):

        """
        Destructor - Private method to delete the class.  Called by the garbage collector, not manually.
        close the port gracefully if it's still open (Called by garbage collector)
        
        """

        self.close()

    def open(self) -> bool:
        """
        Open the handle to the boards and configure the IO that was defined in the constructor

        :return: Returns status of opening.  For I3C SCOUT returns if the bus arbitration was successful.
        :rtype: bool

        """

        # Open the board in the IO Class
        result = self.io.open()

        if result:
            self.isOpen = True

            # Program the settings files if you desire
            if self.programDefaults:
                if self.settingsFile is None:
                    self.program_settings_file_to_device(None, "Default")
                else:
                    self.program_settings_file_to_device(self.settingsFile, "Default")

        return result

    def close(self):
        """
        Closes the IO port. 
        """
        if self.isOpen:
            self.io.close()

    def program_device_defaults(self):
        """
        Program device defaults provided by the designers. These settings
        will be used if no settings file is provided.       
        """

        if self.isOpen:

            saved_addr_mode = self.register_addr_mode

            # Put in two byte mode
            self.io.write_register(0x01, 0x10)

            self.io.write_register(0x00, 0x30)
            self.io.write_register(0x0F, 0x00)
            self.io.write_register(0x10, 0x00)
            self.io.write_register(0x11, 0x74)
            self.io.write_register(0x12, 0x00)
            self.io.write_register(0x15, 0x00)
            self.io.write_register(0x17, 0x01)
            self.io.write_register(0x18, 0x00)
            self.io.write_register(0x1A, 0x00)
            self.io.write_register(0x1B, 0x00)
            self.io.write_register(0x1C, 0x00)
            self.io.write_register(0x1D, 0x00)
            self.io.write_register(0x1E, 0x00)
            self.io.write_register(0x30, 0x66)
            self.io.write_register(0x31, 0x06)
            self.io.write_register(0x32, 0x66)
            self.io.write_register(0x33, 0x06)
            self.io.write_register(0x34, 0x66)
            self.io.write_register(0x35, 0x06)
            self.io.write_register(0x36, 0x66)
            self.io.write_register(0x37, 0x06)
            self.io.write_register(0x38, 0x66)
            self.io.write_register(0x39, 0x06)
            self.io.write_register(0x3A, 0x66)
            self.io.write_register(0x3B, 0x06)
            self.io.write_register(0x3C, 0x66)
            self.io.write_register(0x3D, 0x06)
            self.io.write_register(0x3E, 0x66)
            self.io.write_register(0x3F, 0x06)
            self.io.write_register(0x46, 0x00)
            self.io.write_register(0x47, 0x50)
            self.io.write_register(0x48, 0x00)
            self.io.write_register(0x49, 0x00)
            self.io.write_register(0x4A, 0x50)
            self.io.write_register(0x50, 0xFF)
            self.io.write_register(0x51, 0x0F)
            self.io.write_register(0x52, 0x00)
            self.io.write_register(0x53, 0x00)
            self.io.write_register(0x54, 0xFF)
            self.io.write_register(0x55, 0x0F)
            self.io.write_register(0x56, 0x00)
            self.io.write_register(0x57, 0x00)
            self.io.write_register(0x58, 0xFF)
            self.io.write_register(0x59, 0x0F)
            self.io.write_register(0x5A, 0x00)
            self.io.write_register(0x5B, 0x00)
            self.io.write_register(0x5C, 0xFF)
            self.io.write_register(0x5D, 0x0F)
            self.io.write_register(0x5E, 0x00)
            self.io.write_register(0x5F, 0x00)
            self.io.write_register(0x60, 0xFF)
            self.io.write_register(0x61, 0x07)
            self.io.write_register(0x62, 0x00)
            self.io.write_register(0x63, 0x08)
            self.io.write_register(0x64, 0xFF)
            self.io.write_register(0x65, 0x07)
            self.io.write_register(0x66, 0x00)
            self.io.write_register(0x67, 0x08)
            self.io.write_register(0x68, 0x08)
            self.io.write_register(0x69, 0x08)
            self.io.write_register(0x6A, 0x08)
            self.io.write_register(0x6B, 0x08)
            self.io.write_register(0x6C, 0x08)
            self.io.write_register(0x6D, 0x08)
            self.io.write_register(0x70, 0x00)
            self.io.write_register(0x71, 0x00)
            self.io.write_register(0x72, 0x00)
            self.io.write_register(0x73, 0x00)
            self.io.write_register(0x7D, 0x00)
            self.io.write_register(0x1000, 0x40)
            self.io.write_register(0x1001, 0x40)
            self.io.write_register(0x1002, 0x40)
            self.io.write_register(0x1003, 0x40)
            self.io.write_register(0x1004, 0x40)
            self.io.write_register(0x1005, 0x40)
            self.io.write_register(0x1006, 0x40)
            self.io.write_register(0x1007, 0x40)
            self.io.write_register(0x1008, 0x20)
            self.io.write_register(0x1009, 0x20)
            self.io.write_register(0x100A, 0x20)
            self.io.write_register(0x100B, 0x20)
            self.io.write_register(0x100C, 0x20)
            self.io.write_register(0x100D, 0x20)
            self.io.write_register(0x100E, 0x20)
            self.io.write_register(0x100F, 0x20)
            self.io.write_register(0x1010, 0x40)
            self.io.write_register(0x1011, 0x40)
            self.io.write_register(0x1012, 0x40)
            self.io.write_register(0x1013, 0x40)
            self.io.write_register(0x1014, 0x40)
            self.io.write_register(0x1015, 0x40)
            self.io.write_register(0x1016, 0x40)
            self.io.write_register(0x1017, 0x40)
            self.io.write_register(0x1018, 0x20)
            self.io.write_register(0x1019, 0x20)
            self.io.write_register(0x101A, 0x20)
            self.io.write_register(0x101B, 0x20)
            self.io.write_register(0x101C, 0x20)
            self.io.write_register(0x101D, 0x20)
            self.io.write_register(0x101E, 0x20)
            self.io.write_register(0x101F, 0x20)
            self.io.write_register(0x1020, 0x10)
            self.io.write_register(0x1021, 0x24)
            self.io.write_register(0x1022, 0x0C)
            self.io.write_register(0x1023, 0x0C)
            self.io.write_register(0x1024, 0x00)
            self.io.write_register(0x1025, 0x00)
            self.io.write_register(0x1026, 0x00)
            self.io.write_register(0x1027, 0x00)
            self.io.write_register(0x1028, 0x00)
            self.io.write_register(0x1029, 0x00)
            self.io.write_register(0x102A, 0x00)
            self.io.write_register(0x102B, 0x00)
            self.io.write_register(0x102C, 0x00)
            self.io.write_register(0x102D, 0x00)
            self.io.write_register(0x102E, 0x00)
            self.io.write_register(0x102F, 0x00)
            self.io.write_register(0x1030, 0x00)
            self.io.write_register(0x1031, 0x00)
            self.io.write_register(0x1032, 0x00)
            self.io.write_register(0x1033, 0x00)
            self.io.write_register(0x1034, 0x00)
            self.io.write_register(0x1035, 0x00)
            self.io.write_register(0x1036, 0x00)
            self.io.write_register(0x1037, 0x00)
            self.io.write_register(0x1038, 0x00)
            self.io.write_register(0x1039, 0x00)
            self.io.write_register(0x103A, 0x00)
            self.io.write_register(0x103B, 0x00)
            self.io.write_register(0x103C, 0x00)
            self.io.write_register(0x103D, 0x00)
            self.io.write_register(0x103E, 0x00)
            self.io.write_register(0x103F, 0x00)
            self.io.write_register(0x1040, 0x00)
            self.io.write_register(0x1041, 0x80)
            self.io.write_register(0x1042, 0x00)
            self.io.write_register(0x1043, 0xBB)
            self.io.write_register(0x1044, 0x1F)
            self.io.write_register(0x1045, 0x00)
            self.io.write_register(0x1046, 0x58)
            self.io.write_register(0x1047, 0x02)
            self.io.write_register(0x1048, 0x00)
            self.io.write_register(0x1049, 0x00)
            self.io.write_register(0x104A, 0x00)
            self.io.write_register(0x104B, 0x00)
            self.io.write_register(0x104C, 0x00)
            self.io.write_register(0x104D, 0x00)
            self.io.write_register(0x104E, 0x00)
            self.io.write_register(0x104F, 0x00)
            self.io.write_register(0x1050, 0x00)
            self.io.write_register(0x1051, 0x00)
            self.io.write_register(0x1052, 0x00)
            self.io.write_register(0x1053, 0x00)
            self.io.write_register(0x1054, 0x00)
            self.io.write_register(0x1055, 0x00)
            self.io.write_register(0x1056, 0x00)
            self.io.write_register(0x1057, 0x00)
            self.io.write_register(0x1058, 0x00)
            self.io.write_register(0x1059, 0x00)
            self.io.write_register(0x105A, 0x00)
            self.io.write_register(0x105B, 0x00)
            self.io.write_register(0x105C, 0x00)
            self.io.write_register(0x105D, 0x00)
            self.io.write_register(0x105E, 0x00)
            self.io.write_register(0x105F, 0x00)
            self.io.write_register(0x1060, 0x00)
            self.io.write_register(0x1061, 0x00)
            self.io.write_register(0x1062, 0x00)
            self.io.write_register(0x1063, 0x00)
            self.io.write_register(0x1064, 0x00)
            self.io.write_register(0x1065, 0x00)
            self.io.write_register(0x1066, 0x00)
            self.io.write_register(0x1067, 0x00)
            self.io.write_register(0x1068, 0x00)
            self.io.write_register(0x1069, 0x00)
            self.io.write_register(0x106A, 0x00)
            self.io.write_register(0x106B, 0x00)
            self.io.write_register(0x106C, 0x00)
            self.io.write_register(0x106D, 0x00)
            self.io.write_register(0x106E, 0x00)
            self.io.write_register(0x106F, 0x00)
            self.io.write_register(0x1100, 0x00)
            self.io.write_register(0x1101, 0x00)
            self.io.write_register(0x1200, 0x00)
            self.io.write_register(0x1201, 0x00)
            self.io.write_register(0x1202, 0x02)
            self.io.write_register(0x1203, 0x00)
            self.io.write_register(0x1204, 0x00)
            self.io.write_register(0x1205, 0x00)
            self.io.write_register(0x1208, 0x00)
            self.io.write_register(0x1209, 0x00)
            self.io.write_register(0x120A, 0x00)
            self.io.write_register(0x120B, 0x00)
            self.io.write_register(0x120C, 0x00)
            self.io.write_register(0x120D, 0x00)
            self.io.write_register(0x120E, 0x00)
            self.io.write_register(0x120F, 0x00)
            self.io.write_register(0x1210, 0x34)
            self.io.write_register(0x1211, 0x12)
            self.io.write_register(0x1212, 0x00)
            self.io.write_register(0x1213, 0x00)
            self.io.write_register(0x1217, 0x00)
            self.io.write_register(0x1218, 0x00)
            self.io.write_register(0x121A, 0x00)
            self.io.write_register(0x121C, 0x02)
            self.io.write_register(0x121D, 0x00)
            self.io.write_register(0x1307, 0x00)
            self.io.write_register(0x1308, 0x00)
            self.io.write_register(0x1309, 0x00)
            self.io.write_register(0x130A, 0x00)
            self.io.write_register(0x130B, 0x00)
            self.io.write_register(0x130C, 0x00)
            self.io.write_register(0x130D, 0x00)

            if saved_addr_mode == ADDRESS_MODE.ONE_BYTE:
                # Put back into one byte addr mode
                self.io.write_register(0x0001, 0x00)

    def read_all_registers(self) -> dict:

        """
        Reads all registers from the DUT and stores the values in the dictionary at the variable readbackValues.
        Returns the dictionary for convenience.
        
        :return:  Dictionary containing current values in DUT
        :rtype:  Dict
                
        """
        self.readbackValues = {}
        self.readbackValues['IF_CFG_0'] = self.io.read_register(0x00)
        self.readbackValues['IF_CFG_1'] = self.io.read_register(0x01)
        self.readbackValues['CHIP_TYPE'] = self.io.read_register(0x03)
        self.readbackValues['CHIP_ID_L'] = self.io.read_register(0x04)
        self.readbackValues['CHIP_ID_H'] = self.io.read_register(0x05)
        self.readbackValues['CHIP_VERSION'] = self.io.read_register(0x06)
        self.readbackValues['CHIP_VARIANT'] = self.io.read_register(0x07)
        self.readbackValues['MIPI_MAN_ID_L'] = self.io.read_register(0x0C)
        self.readbackValues['MIPI_MAN_ID_H'] = self.io.read_register(0x0D)
        self.readbackValues['REG_UPDATE'] = self.io.read_register(0x0F)
        self.readbackValues['ADC_CFG'] = self.io.read_register(0x10)
        self.readbackValues['FALSE_ALR_CFG'] = self.io.read_register(0x11)
        self.readbackValues['ADC_AVG'] = self.io.read_register(0x12)
        self.readbackValues['ADC_MUX_CFG'] = self.io.read_register(0x15)
        self.readbackValues['DAC_OUT_OK_CFG'] = self.io.read_register(0x17)
        self.readbackValues['DAC_CLR_EN'] = self.io.read_register(0x18)
        self.readbackValues['DAC_CLR_SRC_0'] = self.io.read_register(0x1A)
        self.readbackValues['DAC_CLR_SRC_1'] = self.io.read_register(0x1B)
        self.readbackValues['ALR_CFG_0'] = self.io.read_register(0x1C)
        self.readbackValues['ALR_CFG_1'] = self.io.read_register(0x1D)
        self.readbackValues['DAC_RANGE'] = self.io.read_register(0x1E)
        self.readbackValues['ADC_IN0_DATA_L'] = self.io.read_register(0x20)
        self.readbackValues['ADC_IN0_DATA_H'] = self.io.read_register(0x21)
        self.readbackValues['ADC_IN1_DATA_L'] = self.io.read_register(0x22)
        self.readbackValues['ADC_IN1_DATA_H'] = self.io.read_register(0x23)
        self.readbackValues['CS_A_DATA_L'] = self.io.read_register(0x24)
        self.readbackValues['CS_A_DATA_H'] = self.io.read_register(0x25)
        self.readbackValues['CS_B_DATA_L'] = self.io.read_register(0x26)
        self.readbackValues['CS_B_DATA_H'] = self.io.read_register(0x27)
        self.readbackValues['LT_DATA_L'] = self.io.read_register(0x28)
        self.readbackValues['LT_DATA_H'] = self.io.read_register(0x29)
        self.readbackValues['RT_DATA_L'] = self.io.read_register(0x2A)
        self.readbackValues['RT_DATA_H'] = self.io.read_register(0x2B)
        self.readbackValues['DAC0_DATA_L'] = self.io.read_register(0x30)
        self.readbackValues['DAC0_DATA_H'] = self.io.read_register(0x31)
        self.readbackValues['DAC1_DATA_L'] = self.io.read_register(0x32)
        self.readbackValues['DAC1_DATA_H'] = self.io.read_register(0x33)
        self.readbackValues['DAC2_DATA_L'] = self.io.read_register(0x34)
        self.readbackValues['DAC2_DATA_H'] = self.io.read_register(0x35)
        self.readbackValues['DAC3_DATA_L'] = self.io.read_register(0x36)
        self.readbackValues['DAC3_DATA_H'] = self.io.read_register(0x37)
        self.readbackValues['DAC4_DATA_L'] = self.io.read_register(0x38)
        self.readbackValues['DAC4_DATA_H'] = self.io.read_register(0x39)
        self.readbackValues['DAC5_DATA_L'] = self.io.read_register(0x3A)
        self.readbackValues['DAC5_DATA_H'] = self.io.read_register(0x3B)
        self.readbackValues['DAC6_DATA_L'] = self.io.read_register(0x3C)
        self.readbackValues['DAC6_DATA_H'] = self.io.read_register(0x3D)
        self.readbackValues['DAC7_DATA_L'] = self.io.read_register(0x3E)
        self.readbackValues['DAC7_DATA_H'] = self.io.read_register(0x3F)
        self.readbackValues['ALR_STAT_0'] = self.io.read_register(0x40)
        self.readbackValues['ALR_STAT_1'] = self.io.read_register(0x41)
        self.readbackValues['GEN_STAT'] = self.io.read_register(0x42)
        self.readbackValues['GEN_STAT_1'] = self.io.read_register(0x43)
        self.readbackValues['GEN_STAT_2'] = self.io.read_register(0x44)
        self.readbackValues['DAC_SW_EN'] = self.io.read_register(0x46)
        self.readbackValues['OUT_AEN_GROUPA'] = self.io.read_register(0x47)
        self.readbackValues['OUT_AEN_GROUPB'] = self.io.read_register(0x48)
        self.readbackValues['OUT_BEN_GROUPA'] = self.io.read_register(0x49)
        self.readbackValues['OUT_BEN_GROUPB'] = self.io.read_register(0x4A)
        self.readbackValues['ADC_IN0_UP_THR_L'] = self.io.read_register(0x50)
        self.readbackValues['ADC_IN0_UP_THR_H'] = self.io.read_register(0x51)
        self.readbackValues['ADC_IN0_LO_THR_L'] = self.io.read_register(0x52)
        self.readbackValues['ADC_IN0_LO_THR_H'] = self.io.read_register(0x53)
        self.readbackValues['ADC_IN1_UP_THR_L'] = self.io.read_register(0x54)
        self.readbackValues['ADC_IN1_UP_THR_H'] = self.io.read_register(0x55)
        self.readbackValues['ADC_IN1_LO_THR_L'] = self.io.read_register(0x56)
        self.readbackValues['ADC_IN1_LO_THR_H'] = self.io.read_register(0x57)
        self.readbackValues['CS_A_UP_THR_L'] = self.io.read_register(0x58)
        self.readbackValues['CS_A_UP_THR_H'] = self.io.read_register(0x59)
        self.readbackValues['CS_A_LO_THR_L'] = self.io.read_register(0x5A)
        self.readbackValues['CS_A_LO_THR_H'] = self.io.read_register(0x5B)
        self.readbackValues['CS_B_UP_THR_L'] = self.io.read_register(0x5C)
        self.readbackValues['CS_B_UP_THR_H'] = self.io.read_register(0x5D)
        self.readbackValues['CS_B_LO_THR_L'] = self.io.read_register(0x5E)
        self.readbackValues['CS_B_LO_THR_H'] = self.io.read_register(0x5F)
        self.readbackValues['LT_UP_THR_L'] = self.io.read_register(0x60)
        self.readbackValues['LT_UP_THR_H'] = self.io.read_register(0x61)
        self.readbackValues['LT_LO_THR_L'] = self.io.read_register(0x62)
        self.readbackValues['LT_LO_THR_H'] = self.io.read_register(0x63)
        self.readbackValues['RT_UP_THR_L'] = self.io.read_register(0x64)
        self.readbackValues['RT_UP_THR_H'] = self.io.read_register(0x65)
        self.readbackValues['RT_LO_THR_L'] = self.io.read_register(0x66)
        self.readbackValues['RT_LO_THR_H'] = self.io.read_register(0x67)
        self.readbackValues['ADC_IN0_HYST'] = self.io.read_register(0x68)
        self.readbackValues['ADC_IN1_HYST'] = self.io.read_register(0x69)
        self.readbackValues['CS_A_HYST'] = self.io.read_register(0x6A)
        self.readbackValues['CS_B_HYST'] = self.io.read_register(0x6B)
        self.readbackValues['LT_HYST'] = self.io.read_register(0x6C)
        self.readbackValues['RT_HYST'] = self.io.read_register(0x6D)
        self.readbackValues['DAC_CLR'] = self.io.read_register(0x70)
        self.readbackValues['PD_DAC'] = self.io.read_register(0x71)
        self.readbackValues['PD_ADC'] = self.io.read_register(0x72)
        self.readbackValues['PD_CS'] = self.io.read_register(0x73)
        self.readbackValues['ADC_TRIG'] = self.io.read_register(0x7D)
        self.readbackValues['DAC0_GAIN_CAL_R00'] = self.io.read_register(0x1000)
        self.readbackValues['DAC1_GAIN_CAL_R00'] = self.io.read_register(0x1001)
        self.readbackValues['DAC2_GAIN_CAL_R00'] = self.io.read_register(0x1002)
        self.readbackValues['DAC3_GAIN_CAL_R00'] = self.io.read_register(0x1003)
        self.readbackValues['DAC4_GAIN_CAL_R00'] = self.io.read_register(0x1004)
        self.readbackValues['DAC5_GAIN_CAL_R00'] = self.io.read_register(0x1005)
        self.readbackValues['DAC6_GAIN_CAL_R00'] = self.io.read_register(0x1006)
        self.readbackValues['DAC7_GAIN_CAL_R00'] = self.io.read_register(0x1007)
        self.readbackValues['DAC0_OFFSET_CAL_R00'] = self.io.read_register(0x1008)
        self.readbackValues['DAC1_OFFSET_CAL_R00'] = self.io.read_register(0x1009)
        self.readbackValues['DAC2_OFFSET_CAL_R00'] = self.io.read_register(0x100A)
        self.readbackValues['DAC3_OFFSET_CAL_R00'] = self.io.read_register(0x100B)
        self.readbackValues['DAC4_OFFSET_CAL_R00'] = self.io.read_register(0x100C)
        self.readbackValues['DAC5_OFFSET_CAL_R00'] = self.io.read_register(0x100D)
        self.readbackValues['DAC6_OFFSET_CAL_R00'] = self.io.read_register(0x100E)
        self.readbackValues['DAC7_OFFSET_CAL_R00'] = self.io.read_register(0x100F)
        self.readbackValues['DAC0_GAIN_CAL_R11'] = self.io.read_register(0x1010)
        self.readbackValues['DAC1_GAIN_CAL_R11'] = self.io.read_register(0x1011)
        self.readbackValues['DAC2_GAIN_CAL_R11'] = self.io.read_register(0x1012)
        self.readbackValues['DAC3_GAIN_CAL_R11'] = self.io.read_register(0x1013)
        self.readbackValues['DAC4_GAIN_CAL_R11'] = self.io.read_register(0x1014)
        self.readbackValues['DAC5_GAIN_CAL_R11'] = self.io.read_register(0x1015)
        self.readbackValues['DAC6_GAIN_CAL_R11'] = self.io.read_register(0x1016)
        self.readbackValues['DAC7_GAIN_CAL_R11'] = self.io.read_register(0x1017)
        self.readbackValues['DAC0_OFFSET_CAL_R11'] = self.io.read_register(0x1018)
        self.readbackValues['DAC1_OFFSET_CAL_R11'] = self.io.read_register(0x1019)
        self.readbackValues['DAC2_OFFSET_CAL_R11'] = self.io.read_register(0x101A)
        self.readbackValues['DAC3_OFFSET_CAL_R11'] = self.io.read_register(0x101B)
        self.readbackValues['DAC4_OFFSET_CAL_R11'] = self.io.read_register(0x101C)
        self.readbackValues['DAC5_OFFSET_CAL_R11'] = self.io.read_register(0x101D)
        self.readbackValues['DAC6_OFFSET_CAL_R11'] = self.io.read_register(0x101E)
        self.readbackValues['DAC7_OFFSET_CAL_R11'] = self.io.read_register(0x101F)
        self.readbackValues['TRIM_OSC'] = self.io.read_register(0x1020)
        self.readbackValues['TRIM_BG'] = self.io.read_register(0x1021)
        self.readbackValues['SPIKE_FILTER_CAL_SCL'] = self.io.read_register(0x1022)
        self.readbackValues['SPIKE_FILTER_CAL_SDA'] = self.io.read_register(0x1023)
        self.readbackValues['ADC_TRIM_REFBUF'] = self.io.read_register(0x1024)
        self.readbackValues['ADC_TRIM_VCM'] = self.io.read_register(0x1025)
        self.readbackValues['ADC_TRIM_LDO'] = self.io.read_register(0x1026)
        self.readbackValues['E2P_PD_DAC'] = self.io.read_register(0x1027)
        self.readbackValues['PD_DAC_CFG'] = self.io.read_register(0x1028)
        self.readbackValues['CS_A_GAIN_ERROR'] = self.io.read_register(0x1029)
        self.readbackValues['CS_B_GAIN_ERROR'] = self.io.read_register(0x102A)
        self.readbackValues['CS_A_LUT0_OFFSET'] = self.io.read_register(0x102B)
        self.readbackValues['CS_A_LUT1_OFFSET'] = self.io.read_register(0x102C)
        self.readbackValues['CS_B_LUT0_OFFSET'] = self.io.read_register(0x102D)
        self.readbackValues['CS_B_LUT1_OFFSET'] = self.io.read_register(0x102E)
        self.readbackValues['ADC_OFFSET_ADC_IN_CAL'] = self.io.read_register(0x102F)
        self.readbackValues['ADC_OFFSET_CS_CAL'] = self.io.read_register(0x1030)
        self.readbackValues['ADC_OFFSET_LT_CAL'] = self.io.read_register(0x1031)
        self.readbackValues['ADC_OFFSET_RT_CAL'] = self.io.read_register(0x1032)
        self.readbackValues['ADC_CAL_CNTL'] = self.io.read_register(0x1033)
        self.readbackValues['CS_A_VCM_BASE_L'] = self.io.read_register(0x1034)
        self.readbackValues['CS_A_VCM_BASE_H'] = self.io.read_register(0x1035)
        self.readbackValues['CS_A_ER_VCM_BASE_L'] = self.io.read_register(0x1036)
        self.readbackValues['CS_A_ER_VCM_BASE_H'] = self.io.read_register(0x1037)
        self.readbackValues['CS_A_VCM_SLOPE_L'] = self.io.read_register(0x1038)
        self.readbackValues['CS_A_VCM_SLOPE_H'] = self.io.read_register(0x1039)
        self.readbackValues['CS_B_VCM_BASE_L'] = self.io.read_register(0x103A)
        self.readbackValues['CS_B_VCM_BASE_H'] = self.io.read_register(0x103B)
        self.readbackValues['CS_B_ER_VCM_BASE_L'] = self.io.read_register(0x103C)
        self.readbackValues['CS_B_ER_VCM_BASE_H'] = self.io.read_register(0x103D)
        self.readbackValues['CS_B_VCM_SLOPE_L'] = self.io.read_register(0x103E)
        self.readbackValues['CS_B_VCM_SLOPE_H'] = self.io.read_register(0x103F)
        self.readbackValues['CS_CFG_0'] = self.io.read_register(0x1040)
        self.readbackValues['CS_CFG_1'] = self.io.read_register(0x1041)
        self.readbackValues['CS_CFG_2'] = self.io.read_register(0x1042)
        self.readbackValues['MISC_CNTL'] = self.io.read_register(0x1043)
        self.readbackValues['ADC_LT_CAL'] = self.io.read_register(0x1044)
        self.readbackValues['ADC_RT_CAL'] = self.io.read_register(0x1045)
        self.readbackValues['LT_THERM_THR_L'] = self.io.read_register(0x1046)
        self.readbackValues['LT_THERM_THR_H'] = self.io.read_register(0x1047)
        self.readbackValues['CS_A_DEL_ER_VCM0'] = self.io.read_register(0x1048)
        self.readbackValues['CS_A_DEL_ER_VCM1'] = self.io.read_register(0x1049)
        self.readbackValues['CS_A_DEL_ER_VCM2'] = self.io.read_register(0x104A)
        self.readbackValues['CS_A_DEL_ER_VCM3'] = self.io.read_register(0x104B)
        self.readbackValues['CS_A_DEL_ER_VCM4'] = self.io.read_register(0x104C)
        self.readbackValues['CS_A_DEL_ER_VCM5'] = self.io.read_register(0x104D)
        self.readbackValues['CS_A_DEL_ER_VCM6'] = self.io.read_register(0x104E)
        self.readbackValues['CS_A_DEL_ER_VCM7'] = self.io.read_register(0x104F)
        self.readbackValues['CS_A_DEL_ER_VCM8'] = self.io.read_register(0x1050)
        self.readbackValues['CS_A_DEL_ER_VCM9'] = self.io.read_register(0x1051)
        self.readbackValues['CS_A_DEL_ER_VCM10'] = self.io.read_register(0x1052)
        self.readbackValues['CS_A_DEL_ER_VCM11'] = self.io.read_register(0x1053)
        self.readbackValues['CS_A_DEL_ER_VCM12'] = self.io.read_register(0x1054)
        self.readbackValues['CS_A_DEL_ER_VCM13'] = self.io.read_register(0x1055)
        self.readbackValues['CS_A_DEL_ER_VCM14'] = self.io.read_register(0x1056)
        self.readbackValues['CS_A_DEL_ER_VCM15'] = self.io.read_register(0x1057)
        self.readbackValues['CS_A_DEL_ER_VCM16'] = self.io.read_register(0x1058)
        self.readbackValues['CS_A_DEL_ER_VCM17'] = self.io.read_register(0x1059)
        self.readbackValues['CS_A_DEL_ER_VCM18'] = self.io.read_register(0x105A)
        self.readbackValues['CS_A_DEL_ER_VCM19'] = self.io.read_register(0x105B)
        self.readbackValues['CS_B_DEL_ER_VCM0'] = self.io.read_register(0x105C)
        self.readbackValues['CS_B_DEL_ER_VCM1'] = self.io.read_register(0x105D)
        self.readbackValues['CS_B_DEL_ER_VCM2'] = self.io.read_register(0x105E)
        self.readbackValues['CS_B_DEL_ER_VCM3'] = self.io.read_register(0x105F)
        self.readbackValues['CS_B_DEL_ER_VCM4'] = self.io.read_register(0x1060)
        self.readbackValues['CS_B_DEL_ER_VCM5'] = self.io.read_register(0x1061)
        self.readbackValues['CS_B_DEL_ER_VCM6'] = self.io.read_register(0x1062)
        self.readbackValues['CS_B_DEL_ER_VCM7'] = self.io.read_register(0x1063)
        self.readbackValues['CS_B_DEL_ER_VCM8'] = self.io.read_register(0x1064)
        self.readbackValues['CS_B_DEL_ER_VCM9'] = self.io.read_register(0x1065)
        self.readbackValues['CS_B_DEL_ER_VCM10'] = self.io.read_register(0x1066)
        self.readbackValues['CS_B_DEL_ER_VCM11'] = self.io.read_register(0x1067)
        self.readbackValues['CS_B_DEL_ER_VCM12'] = self.io.read_register(0x1068)
        self.readbackValues['CS_B_DEL_ER_VCM13'] = self.io.read_register(0x1069)
        self.readbackValues['CS_B_DEL_ER_VCM14'] = self.io.read_register(0x106A)
        self.readbackValues['CS_B_DEL_ER_VCM15'] = self.io.read_register(0x106B)
        self.readbackValues['CS_B_DEL_ER_VCM16'] = self.io.read_register(0x106C)
        self.readbackValues['CS_B_DEL_ER_VCM17'] = self.io.read_register(0x106D)
        self.readbackValues['CS_B_DEL_ER_VCM18'] = self.io.read_register(0x106E)
        self.readbackValues['CS_B_DEL_ER_VCM19'] = self.io.read_register(0x106F)
        self.readbackValues['EEPROM_CNTL'] = self.io.read_register(0x1100)
        self.readbackValues['EEPROM_CFG'] = self.io.read_register(0x1101)
        self.readbackValues['TEST_KEY'] = self.io.read_register(0x1200)
        self.readbackValues['DTEST_CNTL0'] = self.io.read_register(0x1201)
        self.readbackValues['ADC_TEST_CNTL'] = self.io.read_register(0x1202)
        self.readbackValues['ATEST_CNTL0'] = self.io.read_register(0x1203)
        self.readbackValues['ANA_DFT_CTRL'] = self.io.read_register(0x1204)
        self.readbackValues['ANA_DFT_MUX_CTRL'] = self.io.read_register(0x1205)
        self.readbackValues['LDO_TRIM_VDDD'] = self.io.read_register(0x1208)
        self.readbackValues['LDO_TRIM_IOVDD'] = self.io.read_register(0x1209)
        self.readbackValues['ANATOP6'] = self.io.read_register(0x120A)
        self.readbackValues['ANATOP7'] = self.io.read_register(0x120B)
        self.readbackValues['ANATOP8'] = self.io.read_register(0x120C)
        self.readbackValues['ANATOP9'] = self.io.read_register(0x120D)
        self.readbackValues['GPIO_TRACE'] = self.io.read_register(0x120E)
        self.readbackValues['ATEST_CNTL1'] = self.io.read_register(0x120F)
        self.readbackValues['POR_BYPASS_L'] = self.io.read_register(0x1210)
        self.readbackValues['POR_BYPASS_H'] = self.io.read_register(0x1211)
        self.readbackValues['OSC_CNT_CMP_L'] = self.io.read_register(0x1212)
        self.readbackValues['OSC_CNT_CMP_H'] = self.io.read_register(0x1213)
        self.readbackValues['OSC_CNT_L'] = self.io.read_register(0x1214)
        self.readbackValues['OSC_CNT_H'] = self.io.read_register(0x1215)
        self.readbackValues['OSC_TRIM_TEST'] = self.io.read_register(0x1216)
        self.readbackValues['OSC_CMP_HYST'] = self.io.read_register(0x1217)
        self.readbackValues['DAC_TEST_CNTL'] = self.io.read_register(0x1218)
        self.readbackValues['GPIO_IN'] = self.io.read_register(0x1219)
        self.readbackValues['GPIO_OUT'] = self.io.read_register(0x121A)
        self.readbackValues['GPIO_OEB'] = self.io.read_register(0x121C)
        self.readbackValues['GPIO_IEB'] = self.io.read_register(0x121D)
        self.readbackValues['COMP_STATUS'] = self.io.read_register(0x121E)
        self.readbackValues['CS_DIFF10_OVRD_L'] = self.io.read_register(0x1307)
        self.readbackValues['CS_DIFF10_OVRD_H'] = self.io.read_register(0x1308)
        self.readbackValues['CS_VCM_OVRD_L'] = self.io.read_register(0x1309)
        self.readbackValues['CS_VCM_OVRD_H'] = self.io.read_register(0x130A)
        self.readbackValues['CS_DTEST_CTRL'] = self.io.read_register(0x130B)
        self.readbackValues['ADC_CTRL_SIG'] = self.io.read_register(0x130C)
        self.readbackValues['CS_TEST_CTRL'] = self.io.read_register(0x130D)
        self.readbackValues['ADC_DATA_L'] = self.io.read_register(0x130E)
        self.readbackValues['ADC_DATA_H'] = self.io.read_register(0x130F)
        self.readbackValues['CS_VCM_L'] = self.io.read_register(0x1310)
        self.readbackValues['CS_VCM_H'] = self.io.read_register(0x1311)
        self.readbackValues['CS_DAC_MID_L'] = self.io.read_register(0x1312)
        self.readbackValues['CS_DAC_MID_H'] = self.io.read_register(0x1313)
        self.readbackValues['CS_SENSE_P_DAC_L'] = self.io.read_register(0x1314)
        self.readbackValues['CS_SENSE_P_DAC_H'] = self.io.read_register(0x1315)
        self.readbackValues['CS_SENSE_N_DAC_L'] = self.io.read_register(0x1316)
        self.readbackValues['CS_SENSE_N_DAC_H'] = self.io.read_register(0x1317)
        self.readbackValues['CS_DAC_SHIFT_L'] = self.io.read_register(0x1318)
        self.readbackValues['CS_DAC_SHIFT_H'] = self.io.read_register(0x1319)
        self.readbackValues['CS_DAC_SHIFT_COR_L'] = self.io.read_register(0x131A)
        self.readbackValues['CS_DAC_SHIFT_COR_H'] = self.io.read_register(0x131B)
        self.readbackValues['CS_DAC_CODE'] = self.io.read_register(0x131C)
        self.readbackValues['CS_SENSE_P10_L'] = self.io.read_register(0x131D)
        self.readbackValues['CS_SENSE_P10_H'] = self.io.read_register(0x131E)
        self.readbackValues['CS_SENSE_N10_L'] = self.io.read_register(0x131F)
        self.readbackValues['CS_SENSE_N10_H'] = self.io.read_register(0x1320)
        self.readbackValues['CS_DIFF10_L'] = self.io.read_register(0x1321)
        self.readbackValues['CS_DIFF10_H'] = self.io.read_register(0x1322)
        self.readbackValues['CS_CAL_ER_L'] = self.io.read_register(0x1323)
        self.readbackValues['CS_CAL_ER_H'] = self.io.read_register(0x1324)
        self.readbackValues['CS_CAL_DIFF10_L'] = self.io.read_register(0x1325)
        self.readbackValues['CS_CAL_DIFF10_H'] = self.io.read_register(0x1326)
        self.readbackValues['CS_CAL_ER_LUTP'] = self.io.read_register(0x1327)
        self.readbackValues['CS_CAL_LUTS_L'] = self.io.read_register(0x1328)
        self.readbackValues['CS_CAL_LUTS_H'] = self.io.read_register(0x1329)
        self.readbackValues['CS_CAL_ER_FRAC'] = self.io.read_register(0x132A)
        self.readbackValues['CS_GAIN_ER_L'] = self.io.read_register(0x132B)
        self.readbackValues['CS_GAIN_ER_H'] = self.io.read_register(0x132C)

        return self.readbackValues

    def program_settings_file_to_device(self, filename: str = None, sheet_name: str = None):
        """
        Programs the settings indicated by the xlsx file. If there is no 
        designated xlsx file, programs hard-coded, device specific default
        values. 
        
        :param filename: Path and file name to use for defaults
        :type filename: str
        
        :param sheet_name: Name of sheet in excel file to parse for defaults
        :type sheet_name: str
                
        
        """
        if self.isOpen:

            if filename is None:
                self.program_device_defaults()

            else:
                settings = pandas.read_excel(filename, sheet_name=sheet_name)
                hexList = []

                for index, row in settings.iterrows():  # @UnusedVariable
                    address = int(str(row[self.ADDRESS_HEADER]), 16)
                    value = int(str(row[self.VALUE_HEADER]), 16)

                    hexWord = hex((address << 16) | (value))
                    hexList.append(hexWord)

                    self.io.write_register(address, value)

            self.read_all_registers()

    #################################################################
    # GPIO Functions
    #################################################################    

    def set_i2c_pullup_line(self, state: bool):
        """
        Sets the F159x i2c pullup en pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_i2c_pullup_line(state)

    def set_out_ben_line(self, state: bool):
        """
        Sets the F159x set out_ben line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_out_ben_line(state)

    def set_a0_ftdi_line(self, state: bool):
        """
        Sets the F159x set_A0_FTDI_line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_a0_ftdi_line(state)

    def set_out_aen_line(self, state: bool):
        """
        Sets the F159x set_out_aen_line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_out_aen_line(state)

    def set_i3c_sda_en_line(self, state: bool):
        """
        Sets the F159x set_i3c_sda_en_line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_i3c_sda_en_line(state)

    def set_nreset_line(self, state: bool):
        """
        Sets the F159x nRESET pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_nreset_line(state)

    def toggle_nreset_line(self):
        """
        Toggle the reset line LOW -> HIGH. 
        """
        if self.isOpen:
            self.io.toggle_nreset_line()

    def toggle_out_aen_line(self, count: int = 8):
        """
        Toggles the F159x set_out_aen_line pin to the specified state.
        
        :param count: Number of times to toggle the pin.
        :type count: int
        
        """
        if self.isOpen:
            self.io.toggle_out_aen_line(count)

    def set_spi_mosi_en_line(self, state):
        """
        Sets the F159x set_spi_mosi_en pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_spi_mosi_en_line(state)

    def set_cm_a2_line(self, state):
        """
        Sets the F159x CM/A2 pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_cm_a2_line(state)

    def set_a0_line(self, state):
        """
        Sets the F159x A0 pin to the specified state (SCOUT)

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_a0_line(state)

    def set_a1_line(self, state):
        """
        Sets the F159x A1 pin to the specified state (SCOUT)

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self.isOpen:
            self.io.set_a1_line(state)

    def get_dac_out_ok_state(self):
        """
        Gets the F1590 DAC_OUT_OK state 

        :return: Value of GPIO - True for high (1), False for low (0).
        :rtype: bool
        
        """
        if self.isOpen:
            return self.io.get_dac_out_ok_state()
        else:
            raise Exception('AMC7834.py:get_dac_out_ok_state:Port not open.')

    #################################################################
    # IO Protocol
    #################################################################

    def set_i3c_one_byte_address_mode(self):
        # Put the DUT into single byte address mode if I3C mode

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            one_byte_readback = self.read_register(0x4, 0x1, ADDRESS_MODE.ONE_BYTE)
        if one_byte_readback == 0x37:
            print('AMC7834 already in ONE_BYTE ADDR MODE.')
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                two_byte_readback = self.read_register(0x4, 0x1, ADDRESS_MODE.TWO_BYTE)
                if two_byte_readback == 0x37:
                    # put the device back into one byte mode
                    print('AMC7834 detected in TWO_BYTE mode.  Setting to ONE_BYTE mode.')
                    ifcfg1_value = self.read_register(0x1, 0x1, ADDRESS_MODE.TWO_BYTE)
                    new_ifCfg1_value = ifcfg1_value & ~ 0x10
                    self.write_register(0x1, new_ifCfg1_value, ADDRESS_MODE.TWO_BYTE)

                    one_byte_readback = self.read_register(0x4, 0x1, ADDRESS_MODE.ONE_BYTE)
                    if one_byte_readback == 0x37:
                        print('AMC7834 successfully changed to ONE_BYTE ADDR MODE.')
                    else:
                        warnings.warn('AMC7834 did not respond to ONE BYTE ADDR MODE command.')
                else:
                    warnings.warn('Cannot determine which ADDR MODE AMC7834 is in. Is the power supply enabled?')

    def set_i3c_two_byte_address_mode(self):
        # Put the DUT into single byte address mode if I3C mode

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            one_byte_readback = self.io.read_register(0x4, 0x1, ADDRESS_MODE.ONE_BYTE)
        if one_byte_readback == 0x37:
            with warnings.catch_warnings():
                # put the device into two byte mode
                print('AMC7834 detected in ONE_BYTE mode.  Setting to TWO_BYTE mode.')
                warnings.simplefilter("ignore")
                ifcfg1_value = self.read_register(0x1, 0x1, ADDRESS_MODE.ONE_BYTE)
                new_ifCfg1_value = ifcfg1_value | 0x10
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    self.write_register(0x1, new_ifCfg1_value, ADDRESS_MODE.ONE_BYTE)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    two_byte_readback = self.io.read_register(0x4, 0x1, ADDRESS_MODE.TWO_BYTE)
                if two_byte_readback == 0x37:
                    print('AMC7834 successfully changed to TWO_BYTE ADDR MODE.')
                else:
                    warnings.warn('AMC7834 did not respond to TWO BYTE ADDR MODE command.')
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                two_byte_readback = self.io.read_register(0x4, 0x1, ADDRESS_MODE.TWO_BYTE)
                if two_byte_readback == 0x37:
                    print('AMC7834 already in TWO_BYTE ADDR MODE.  Nothing to set.')
                else:
                    warnings.warn('Cannot determine which ADDR MODE AMC7834 is in. Is the power supply enabled?')

    def set_clock_frequency_mhz(self, clock_frequency_mhz: float):

        if self.isOpen:
            self.io.set_clock_frequency_mhz(clock_frequency_mhz)

    def read_register(self, register_address: int, read_length: int = 1, addr_mode: ADDRESS_MODE = None):
        """
        Perform a Local SPI Read:
       
        :param register_address: 8 or 15-bit address of the register to read from.
        :type register_address: int
        :param read_length: Number of registers to read.
        :type read_length: int
        :param addr_mode: Write mode (1 byte or 2 byte addressing) used for I2C/I3C messaging.
        :type addr_mode: ADDRESS_MODE
        
        """

        if addr_mode is None:
            addr_mode = self.register_addr_mode

        return self.io.read_register(register_address, read_length, addr_mode)

    def write_register(self, register_address: int, value, addr_mode: ADDRESS_MODE = None):

        """        
        Perform a Local SPI Write:

        :param register_address: 8 or 16 bit address of the register to write to.
        :type register_address: int
        :param value: 8-bit data value to program.
        :type value: int or list
        :param addr_mode: Write mode (1 byte or 2 byte addressing) used for I2C/I3C messaging.
        :type addr_mode: ADDR_MODE
        
        """

        # Attempt to keep the class in sync with ADDR_MODE in the device 
        reg1Val = None
        if register_address == 0:
            if (type(value) is list) and (len(value) > 1):
                reg1Val = value[1]
        elif register_address == 1:
            if type(value) is int:
                reg1Val = value
            elif type(value) is list:
                reg1Val = value[0]

        self.io.write_register(register_address, value, addr_mode)

        # Change the class variable value after the write so future defaults match hardware expectation
        if reg1Val is not None:
            if ((reg1Val >> 4) & 1) == 0:
                self.register_addr_mode = ADDRESS_MODE.ONE_BYTE
            else:
                self.register_addr_mode = ADDRESS_MODE.TWO_BYTE

    def set_SOFT_RESET(self, value):
        """
        Writes the SOFT_RESET bitfield in the IF_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_IF_CFG_0()
        self._BITFIELD['SOFT_RESET'] = value
        self.write_IF_CFG_0()
        self._BITFIELD['SOFT_RESET'] = 0

    def get_SOFT_RESET(self):
        """
        Reads the IF_CFG_0 register
        
        :return: the shadow register SOFT_RESET.
        :rtype: int
        """
        self.read_IF_CFG_0()
        return self._BITFIELD['SOFT_RESET']

    def set_RSVD_6_IF_CFG_0(self, value):
        """
         Read Only bit field RSVD_6_IF_CFG_0 in the IF_CFG_0 register. Skip the write.
        """

    def get_RSVD_6_IF_CFG_0(self):
        """
        Reads the IF_CFG_0 register
        
        :return: the shadow register RSVD_6_IF_CFG_0.
        :rtype: int
        """
        self.read_IF_CFG_0()
        return self._BITFIELD['RSVD_6_IF_CFG_0']

    def set_ADDR_ASCEND(self, value):
        """
        Writes the ADDR_ASCEND bitfield in the IF_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_IF_CFG_0()
        self._BITFIELD['ADDR_ASCEND'] = value
        self.write_IF_CFG_0()

    def get_ADDR_ASCEND(self):
        """
        Reads the IF_CFG_0 register
        
        :return: the shadow register ADDR_ASCEND.
        :rtype: int
        """
        self.read_IF_CFG_0()
        return self._BITFIELD['ADDR_ASCEND']

    def set_RSVD_4_0_IF_CFG_0(self, value):
        """
         Read Only bit field RSVD_4_0_IF_CFG_0 in the IF_CFG_0 register. Skip the write.
        """

    def get_RSVD_4_0_IF_CFG_0(self):
        """
        Reads the IF_CFG_0 register
        
        :return: the shadow register RSVD_4_0_IF_CFG_0.
        :rtype: int
        """
        self.read_IF_CFG_0()
        return self._BITFIELD['RSVD_4_0_IF_CFG_0']

    def set_SINGLE_INSTR(self, value):
        """
        Writes the SINGLE_INSTR bitfield in the IF_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_IF_CFG_1()
        self._BITFIELD['SINGLE_INSTR'] = value
        self.write_IF_CFG_1()

    def get_SINGLE_INSTR(self):
        """
        Reads the IF_CFG_1 register
        
        :return: the shadow register SINGLE_INSTR.
        :rtype: int
        """
        self.read_IF_CFG_1()
        return self._BITFIELD['SINGLE_INSTR']

    def set_RSVD_6_IF_CFG_1(self, value):
        """
         Read Only bit field RSVD_6_IF_CFG_1 in the IF_CFG_1 register. Skip the write.
        """

    def get_RSVD_6_IF_CFG_1(self):
        """
        Reads the IF_CFG_1 register
        
        :return: the shadow register RSVD_6_IF_CFG_1.
        :rtype: int
        """
        self.read_IF_CFG_1()
        return self._BITFIELD['RSVD_6_IF_CFG_1']

    def set_READBACK(self, value):
        """
        Writes the READBACK bitfield in the IF_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_IF_CFG_1()
        self._BITFIELD['READBACK'] = value
        self.write_IF_CFG_1()

    def get_READBACK(self):
        """
        Reads the IF_CFG_1 register
        
        :return: the shadow register READBACK.
        :rtype: int
        """
        self.read_IF_CFG_1()
        return self._BITFIELD['READBACK']

    def set_ADDR_MODE(self, value):
        """
        Writes the ADDR_MODE bitfield in the IF_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_IF_CFG_1()
        self._BITFIELD['ADDR_MODE'] = value
        self.write_IF_CFG_1()

    def get_ADDR_MODE(self):
        """
        Reads the IF_CFG_1 register
        
        :return: the shadow register ADDR_MODE.
        :rtype: int
        """
        self.read_IF_CFG_1()
        return self._BITFIELD['ADDR_MODE']

    def set_RSVD_3_0_IF_CFG_1(self, value):
        """
         Read Only bit field RSVD_3_0_IF_CFG_1 in the IF_CFG_1 register. Skip the write.
        """

    def get_RSVD_3_0_IF_CFG_1(self):
        """
        Reads the IF_CFG_1 register
        
        :return: the shadow register RSVD_3_0_IF_CFG_1.
        :rtype: int
        """
        self.read_IF_CFG_1()
        return self._BITFIELD['RSVD_3_0_IF_CFG_1']

    def set_RSVD_7_4_CHIP_TYPE(self, value):
        """
         Read Only bit field RSVD_7_4_CHIP_TYPE in the CHIP_TYPE register. Skip the write.
        """

    def get_RSVD_7_4_CHIP_TYPE(self):
        """
        Reads the CHIP_TYPE register
        
        :return: the shadow register RSVD_7_4_CHIP_TYPE.
        :rtype: int
        """
        self.read_CHIP_TYPE()
        return self._BITFIELD['RSVD_7_4_CHIP_TYPE']

    def set_CHIP_TYPE(self, value):
        """
         Read Only bit field CHIP_TYPE in the CHIP_TYPE register. Skip the write.
        """

    def get_CHIP_TYPE(self):
        """
        Reads the CHIP_TYPE register
        
        :return: the shadow register CHIP_TYPE.
        :rtype: int
        """
        self.read_CHIP_TYPE()
        return self._BITFIELD['CHIP_TYPE']

    def set_CHIPDID_LOW(self, value):
        """
         Read Only bit field CHIPDID_LOW in the CHIP_ID_L register. Skip the write.
        """

    def get_CHIPDID_LOW(self):
        """
        Reads the CHIP_ID_L register
        
        :return: the shadow register CHIPDID_LOW.
        :rtype: int
        """
        self.read_CHIP_ID_L()
        return self._BITFIELD['CHIPDID_LOW']

    def set_CHIPDID_HIGH(self, value):
        """
         Read Only bit field CHIPDID_HIGH in the CHIP_ID_H register. Skip the write.
        """

    def get_CHIPDID_HIGH(self):
        """
        Reads the CHIP_ID_H register
        
        :return: the shadow register CHIPDID_HIGH.
        :rtype: int
        """
        self.read_CHIP_ID_H()
        return self._BITFIELD['CHIPDID_HIGH']

    def set_VERSIONID(self, value):
        """
         Read Only bit field VERSIONID in the CHIP_VERSION register. Skip the write.
        """

    def get_VERSIONID(self):
        """
        Reads the CHIP_VERSION register
        
        :return: the shadow register VERSIONID.
        :rtype: int
        """
        self.read_CHIP_VERSION()
        return self._BITFIELD['VERSIONID']

    def set_RSVD_7_4_CHIP_VARIANT(self, value):
        """
         Read Only bit field RSVD_7_4_CHIP_VARIANT in the CHIP_VARIANT register. Skip the write.
        """

    def get_RSVD_7_4_CHIP_VARIANT(self):
        """
        Reads the CHIP_VARIANT register
        
        :return: the shadow register RSVD_7_4_CHIP_VARIANT.
        :rtype: int
        """
        self.read_CHIP_VARIANT()
        return self._BITFIELD['RSVD_7_4_CHIP_VARIANT']

    def set_CHIP_VARIANT(self, value):
        """
         Read Only bit field CHIP_VARIANT in the CHIP_VARIANT register. Skip the write.
        """

    def get_CHIP_VARIANT(self):
        """
        Reads the CHIP_VARIANT register
        
        :return: the shadow register CHIP_VARIANT.
        :rtype: int
        """
        self.read_CHIP_VARIANT()
        return self._BITFIELD['CHIP_VARIANT']

    def set_MAN_ID_LOW(self, value):
        """
         Read Only bit field MAN_ID_LOW in the MIPI_MAN_ID_L register. Skip the write.
        """

    def get_MAN_ID_LOW(self):
        """
        Reads the MIPI_MAN_ID_L register
        
        :return: the shadow register MAN_ID_LOW.
        :rtype: int
        """
        self.read_MIPI_MAN_ID_L()
        return self._BITFIELD['MAN_ID_LOW']

    def set_RSVD_0_MIPI_MAN_ID_L(self, value):
        """
         Read Only bit field RSVD_0_MIPI_MAN_ID_L in the MIPI_MAN_ID_L register. Skip the write.
        """

    def get_RSVD_0_MIPI_MAN_ID_L(self):
        """
        Reads the MIPI_MAN_ID_L register
        
        :return: the shadow register RSVD_0_MIPI_MAN_ID_L.
        :rtype: int
        """
        self.read_MIPI_MAN_ID_L()
        return self._BITFIELD['RSVD_0_MIPI_MAN_ID_L']

    def set_MAN_ID_HIGH(self, value):
        """
         Read Only bit field MAN_ID_HIGH in the MIPI_MAN_ID_H register. Skip the write.
        """

    def get_MAN_ID_HIGH(self):
        """
        Reads the MIPI_MAN_ID_H register
        
        :return: the shadow register MAN_ID_HIGH.
        :rtype: int
        """
        self.read_MIPI_MAN_ID_H()
        return self._BITFIELD['MAN_ID_HIGH']

    def set_RSVD_7_5_REG_UPDATE(self, value):
        """
         Read Only bit field RSVD_7_5_REG_UPDATE in the REG_UPDATE register. Skip the write.
        """

    def get_RSVD_7_5_REG_UPDATE(self):
        """
        Reads the REG_UPDATE register
        
        :return: the shadow register RSVD_7_5_REG_UPDATE.
        :rtype: int
        """
        self.read_REG_UPDATE()
        return self._BITFIELD['RSVD_7_5_REG_UPDATE']

    def set_ADC_UPDATE(self, value):
        """
        Writes the ADC_UPDATE bitfield in the REG_UPDATE register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_REG_UPDATE()
        self._BITFIELD['ADC_UPDATE'] = value
        self.write_REG_UPDATE()

    def get_ADC_UPDATE(self):
        """
        Reads the REG_UPDATE register
        
        :return: the shadow register ADC_UPDATE.
        :rtype: int
        """
        self.read_REG_UPDATE()
        return self._BITFIELD['ADC_UPDATE']

    def set_RSVD_3_1_REG_UPDATE(self, value):
        """
         Read Only bit field RSVD_3_1_REG_UPDATE in the REG_UPDATE register. Skip the write.
        """

    def get_RSVD_3_1_REG_UPDATE(self):
        """
        Reads the REG_UPDATE register
        
        :return: the shadow register RSVD_3_1_REG_UPDATE.
        :rtype: int
        """
        self.read_REG_UPDATE()
        return self._BITFIELD['RSVD_3_1_REG_UPDATE']

    def set_DAC_UPDATE(self, value):
        """
        Writes the DAC_UPDATE bitfield in the REG_UPDATE register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_REG_UPDATE()
        self._BITFIELD['DAC_UPDATE'] = value
        self.write_REG_UPDATE()

    def get_DAC_UPDATE(self):
        """
        Reads the REG_UPDATE register
        
        :return: the shadow register DAC_UPDATE.
        :rtype: int
        """
        self.read_REG_UPDATE()
        return self._BITFIELD['DAC_UPDATE']

    def set_CMODE(self, value):
        """
        Writes the CMODE bitfield in the ADC_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CFG()
        self._BITFIELD['CMODE'] = value
        self.write_ADC_CFG()

    def get_CMODE(self):
        """
        Reads the ADC_CFG register
        
        :return: the shadow register CMODE.
        :rtype: int
        """
        self.read_ADC_CFG()
        return self._BITFIELD['CMODE']

    def set_ADC_CONV_RATE(self, value):
        """
        Writes the ADC_CONV_RATE bitfield in the ADC_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CFG()
        self._BITFIELD['ADC_CONV_RATE'] = value
        self.write_ADC_CFG()

    def get_ADC_CONV_RATE(self):
        """
        Reads the ADC_CFG register
        
        :return: the shadow register ADC_CONV_RATE.
        :rtype: int
        """
        self.read_ADC_CFG()
        return self._BITFIELD['ADC_CONV_RATE']

    def set_ADC_REF_BUFF(self, value):
        """
        Writes the ADC_REF_BUFF bitfield in the ADC_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CFG()
        self._BITFIELD['ADC_REF_BUFF'] = value
        self.write_ADC_CFG()

    def get_ADC_REF_BUFF(self):
        """
        Reads the ADC_CFG register
        
        :return: the shadow register ADC_REF_BUFF.
        :rtype: int
        """
        self.read_ADC_CFG()
        return self._BITFIELD['ADC_REF_BUFF']

    def set_RSVD_3_2_ADC_CFG(self, value):
        """
         Read Only bit field RSVD_3_2_ADC_CFG in the ADC_CFG register. Skip the write.
        """

    def get_RSVD_3_2_ADC_CFG(self):
        """
        Reads the ADC_CFG register
        
        :return: the shadow register RSVD_3_2_ADC_CFG.
        :rtype: int
        """
        self.read_ADC_CFG()
        return self._BITFIELD['RSVD_3_2_ADC_CFG']

    def set_RT_CONV_RATE(self, value):
        """
        Writes the RT_CONV_RATE bitfield in the ADC_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CFG()
        self._BITFIELD['RT_CONV_RATE'] = value
        self.write_ADC_CFG()

    def get_RT_CONV_RATE(self):
        """
        Reads the ADC_CFG register
        
        :return: the shadow register RT_CONV_RATE.
        :rtype: int
        """
        self.read_ADC_CFG()
        return self._BITFIELD['RT_CONV_RATE']

    def set_CH_FALR_CT(self, value):
        """
        Writes the CH_FALR_CT bitfield in the FALSE_ALR_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_FALSE_ALR_CFG()
        self._BITFIELD['CH_FALR_CT'] = value
        self.write_FALSE_ALR_CFG()

    def get_CH_FALR_CT(self):
        """
        Reads the FALSE_ALR_CFG register
        
        :return: the shadow register CH_FALR_CT.
        :rtype: int
        """
        self.read_FALSE_ALR_CFG()
        return self._BITFIELD['CH_FALR_CT']

    def set_LT_FALR_CT(self, value):
        """
        Writes the LT_FALR_CT bitfield in the FALSE_ALR_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_FALSE_ALR_CFG()
        self._BITFIELD['LT_FALR_CT'] = value
        self.write_FALSE_ALR_CFG()

    def get_LT_FALR_CT(self):
        """
        Reads the FALSE_ALR_CFG register
        
        :return: the shadow register LT_FALR_CT.
        :rtype: int
        """
        self.read_FALSE_ALR_CFG()
        return self._BITFIELD['LT_FALR_CT']

    def set_RT_FALR_CT(self, value):
        """
        Writes the RT_FALR_CT bitfield in the FALSE_ALR_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_FALSE_ALR_CFG()
        self._BITFIELD['RT_FALR_CT'] = value
        self.write_FALSE_ALR_CFG()

    def get_RT_FALR_CT(self):
        """
        Reads the FALSE_ALR_CFG register
        
        :return: the shadow register RT_FALR_CT.
        :rtype: int
        """
        self.read_FALSE_ALR_CFG()
        return self._BITFIELD['RT_FALR_CT']

    def set_RSVD_0_FALSE_ALR_CFG(self, value):
        """
         Read Only bit field RSVD_0_FALSE_ALR_CFG in the FALSE_ALR_CFG register. Skip the write.
        """

    def get_RSVD_0_FALSE_ALR_CFG(self):
        """
        Reads the FALSE_ALR_CFG register
        
        :return: the shadow register RSVD_0_FALSE_ALR_CFG.
        :rtype: int
        """
        self.read_FALSE_ALR_CFG()
        return self._BITFIELD['RSVD_0_FALSE_ALR_CFG']

    def set_RSVD_7_4_ADC_AVG(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_AVG in the ADC_AVG register. Skip the write.
        """

    def get_RSVD_7_4_ADC_AVG(self):
        """
        Reads the ADC_AVG register
        
        :return: the shadow register RSVD_7_4_ADC_AVG.
        :rtype: int
        """
        self.read_ADC_AVG()
        return self._BITFIELD['RSVD_7_4_ADC_AVG']

    def set_ADC_AVG_ADC(self, value):
        """
        Writes the ADC_AVG_ADC bitfield in the ADC_AVG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_AVG()
        self._BITFIELD['ADC_AVG_ADC'] = value
        self.write_ADC_AVG()

    def get_ADC_AVG_ADC(self):
        """
        Reads the ADC_AVG register
        
        :return: the shadow register ADC_AVG_ADC.
        :rtype: int
        """
        self.read_ADC_AVG()
        return self._BITFIELD['ADC_AVG_ADC']

    def set_RSVD_7_6_ADC_MUX_CFG(self, value):
        """
        Writes the RSVD_7_6_ADC_MUX_CFG bitfield in the ADC_MUX_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_MUX_CFG()
        self._BITFIELD['RSVD_7_6_ADC_MUX_CFG'] = value
        self.write_ADC_MUX_CFG()

    def get_RSVD_7_6_ADC_MUX_CFG(self):
        """
        Reads the ADC_MUX_CFG register
        
        :return: the shadow register RSVD_7_6_ADC_MUX_CFG.
        :rtype: int
        """
        self.read_ADC_MUX_CFG()
        return self._BITFIELD['RSVD_7_6_ADC_MUX_CFG']

    def set_RT_CH(self, value):
        """
        Writes the RT_CH bitfield in the ADC_MUX_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_MUX_CFG()
        self._BITFIELD['RT_CH'] = value
        self.write_ADC_MUX_CFG()

    def get_RT_CH(self):
        """
        Reads the ADC_MUX_CFG register
        
        :return: the shadow register RT_CH.
        :rtype: int
        """
        self.read_ADC_MUX_CFG()
        return self._BITFIELD['RT_CH']

    def set_LT_CH(self, value):
        """
        Writes the LT_CH bitfield in the ADC_MUX_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_MUX_CFG()
        self._BITFIELD['LT_CH'] = value
        self.write_ADC_MUX_CFG()

    def get_LT_CH(self):
        """
        Reads the ADC_MUX_CFG register
        
        :return: the shadow register LT_CH.
        :rtype: int
        """
        self.read_ADC_MUX_CFG()
        return self._BITFIELD['LT_CH']

    def set_CS_B(self, value):
        """
        Writes the CS_B bitfield in the ADC_MUX_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_MUX_CFG()
        self._BITFIELD['CS_B'] = value
        self.write_ADC_MUX_CFG()

    def get_CS_B(self):
        """
        Reads the ADC_MUX_CFG register
        
        :return: the shadow register CS_B.
        :rtype: int
        """
        self.read_ADC_MUX_CFG()
        return self._BITFIELD['CS_B']

    def set_CS_A(self, value):
        """
        Writes the CS_A bitfield in the ADC_MUX_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_MUX_CFG()
        self._BITFIELD['CS_A'] = value
        self.write_ADC_MUX_CFG()

    def get_CS_A(self):
        """
        Reads the ADC_MUX_CFG register
        
        :return: the shadow register CS_A.
        :rtype: int
        """
        self.read_ADC_MUX_CFG()
        return self._BITFIELD['CS_A']

    def set_ADC_IN1(self, value):
        """
        Writes the ADC_IN1 bitfield in the ADC_MUX_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_MUX_CFG()
        self._BITFIELD['ADC_IN1'] = value
        self.write_ADC_MUX_CFG()

    def get_ADC_IN1(self):
        """
        Reads the ADC_MUX_CFG register
        
        :return: the shadow register ADC_IN1.
        :rtype: int
        """
        self.read_ADC_MUX_CFG()
        return self._BITFIELD['ADC_IN1']

    def set_ADC_IN0(self, value):
        """
        Writes the ADC_IN0 bitfield in the ADC_MUX_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_MUX_CFG()
        self._BITFIELD['ADC_IN0'] = value
        self.write_ADC_MUX_CFG()

    def get_ADC_IN0(self):
        """
        Reads the ADC_MUX_CFG register
        
        :return: the shadow register ADC_IN0.
        :rtype: int
        """
        self.read_ADC_MUX_CFG()
        return self._BITFIELD['ADC_IN0']

    def set_ASSERT(self, value):
        """
        Writes the ASSERT bitfield in the DAC_OUT_OK_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_OUT_OK_CFG()
        self._BITFIELD['ASSERT'] = value
        self.write_DAC_OUT_OK_CFG()

    def get_ASSERT(self):
        """
        Reads the DAC_OUT_OK_CFG register
        
        :return: the shadow register ASSERT.
        :rtype: int
        """
        self.read_DAC_OUT_OK_CFG()
        return self._BITFIELD['ASSERT']

    def set_TIMER(self, value):
        """
        Writes the TIMER bitfield in the DAC_OUT_OK_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_OUT_OK_CFG()
        self._BITFIELD['TIMER'] = value
        self.write_DAC_OUT_OK_CFG()

    def get_TIMER(self):
        """
        Reads the DAC_OUT_OK_CFG register
        
        :return: the shadow register TIMER.
        :rtype: int
        """
        self.read_DAC_OUT_OK_CFG()
        return self._BITFIELD['TIMER']

    def set_CLREN_B7(self, value):
        """
        Writes the CLREN_B7 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_B7'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_B7(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_B7.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_B7']

    def set_CLREN_B6(self, value):
        """
        Writes the CLREN_B6 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_B6'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_B6(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_B6.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_B6']

    def set_CLREN_B5(self, value):
        """
        Writes the CLREN_B5 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_B5'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_B5(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_B5.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_B5']

    def set_CLREN_B4(self, value):
        """
        Writes the CLREN_B4 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_B4'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_B4(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_B4.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_B4']

    def set_CLREN_A3(self, value):
        """
        Writes the CLREN_A3 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_A3'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_A3(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_A3.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_A3']

    def set_CLREN_A2(self, value):
        """
        Writes the CLREN_A2 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_A2'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_A2(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_A2.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_A2']

    def set_CLREN_A1(self, value):
        """
        Writes the CLREN_A1 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_A1'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_A1(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_A1.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_A1']

    def set_CLREN_A0(self, value):
        """
        Writes the CLREN_A0 bitfield in the DAC_CLR_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_EN()
        self._BITFIELD['CLREN_A0'] = value
        self.write_DAC_CLR_EN()

    def get_CLREN_A0(self):
        """
        Reads the DAC_CLR_EN register
        
        :return: the shadow register CLREN_A0.
        :rtype: int
        """
        self.read_DAC_CLR_EN()
        return self._BITFIELD['CLREN_A0']

    def set_RSVD_7_6_DAC_CLR_SRC_0(self, value):
        """
         Read Only bit field RSVD_7_6_DAC_CLR_SRC_0 in the DAC_CLR_SRC_0 register. Skip the write.
        """

    def get_RSVD_7_6_DAC_CLR_SRC_0(self):
        """
        Reads the DAC_CLR_SRC_0 register
        
        :return: the shadow register RSVD_7_6_DAC_CLR_SRC_0.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_0()
        return self._BITFIELD['RSVD_7_6_DAC_CLR_SRC_0']

    def set_RT_HIGH_ALR_CLR(self, value):
        """
        Writes the RT_HIGH_ALR_CLR bitfield in the DAC_CLR_SRC_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_0()
        self._BITFIELD['RT_HIGH_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_0()

    def get_RT_HIGH_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_0 register
        
        :return: the shadow register RT_HIGH_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_0()
        return self._BITFIELD['RT_HIGH_ALR_CLR']

    def set_RT_LOW_ALR_CLR(self, value):
        """
        Writes the RT_LOW_ALR_CLR bitfield in the DAC_CLR_SRC_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_0()
        self._BITFIELD['RT_LOW_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_0()

    def get_RT_LOW_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_0 register
        
        :return: the shadow register RT_LOW_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_0()
        return self._BITFIELD['RT_LOW_ALR_CLR']

    def set_CS_B_ALR_CLR(self, value):
        """
        Writes the CS_B_ALR_CLR bitfield in the DAC_CLR_SRC_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_0()
        self._BITFIELD['CS_B_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_0()

    def get_CS_B_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_0 register
        
        :return: the shadow register CS_B_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_0()
        return self._BITFIELD['CS_B_ALR_CLR']

    def set_CS_A_ALR_CLR(self, value):
        """
        Writes the CS_A_ALR_CLR bitfield in the DAC_CLR_SRC_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_0()
        self._BITFIELD['CS_A_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_0()

    def get_CS_A_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_0 register
        
        :return: the shadow register CS_A_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_0()
        return self._BITFIELD['CS_A_ALR_CLR']

    def set_ADC_IN1_ALR_CLR(self, value):
        """
        Writes the ADC_IN1_ALR_CLR bitfield in the DAC_CLR_SRC_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_0()
        self._BITFIELD['ADC_IN1_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_0()

    def get_ADC_IN1_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_0 register
        
        :return: the shadow register ADC_IN1_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_0()
        return self._BITFIELD['ADC_IN1_ALR_CLR']

    def set_ADC_IN0_ALR_CLR(self, value):
        """
        Writes the ADC_IN0_ALR_CLR bitfield in the DAC_CLR_SRC_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_0()
        self._BITFIELD['ADC_IN0_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_0()

    def get_ADC_IN0_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_0 register
        
        :return: the shadow register ADC_IN0_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_0()
        return self._BITFIELD['ADC_IN0_ALR_CLR']

    def set_RSVD_7_3_DAC_CLR_SRC_1(self, value):
        """
         Read Only bit field RSVD_7_3_DAC_CLR_SRC_1 in the DAC_CLR_SRC_1 register. Skip the write.
        """

    def get_RSVD_7_3_DAC_CLR_SRC_1(self):
        """
        Reads the DAC_CLR_SRC_1 register
        
        :return: the shadow register RSVD_7_3_DAC_CLR_SRC_1.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_1()
        return self._BITFIELD['RSVD_7_3_DAC_CLR_SRC_1']

    def set_THERM_ALR_CLR(self, value):
        """
        Writes the THERM_ALR_CLR bitfield in the DAC_CLR_SRC_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_1()
        self._BITFIELD['THERM_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_1()

    def get_THERM_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_1 register
        
        :return: the shadow register THERM_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_1()
        return self._BITFIELD['THERM_ALR_CLR']

    def set_LT_HIGH_ALR_CLR(self, value):
        """
        Writes the LT_HIGH_ALR_CLR bitfield in the DAC_CLR_SRC_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_1()
        self._BITFIELD['LT_HIGH_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_1()

    def get_LT_HIGH_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_1 register
        
        :return: the shadow register LT_HIGH_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_1()
        return self._BITFIELD['LT_HIGH_ALR_CLR']

    def set_LT_LOW_ALR_CLR(self, value):
        """
        Writes the LT_LOW_ALR_CLR bitfield in the DAC_CLR_SRC_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR_SRC_1()
        self._BITFIELD['LT_LOW_ALR_CLR'] = value
        self.write_DAC_CLR_SRC_1()

    def get_LT_LOW_ALR_CLR(self):
        """
        Reads the DAC_CLR_SRC_1 register
        
        :return: the shadow register LT_LOW_ALR_CLR.
        :rtype: int
        """
        self.read_DAC_CLR_SRC_1()
        return self._BITFIELD['LT_LOW_ALR_CLR']

    def set_RSVD_7_6_ALR_CFG_0(self, value):
        """
         Read Only bit field RSVD_7_6_ALR_CFG_0 in the ALR_CFG_0 register. Skip the write.
        """

    def get_RSVD_7_6_ALR_CFG_0(self):
        """
        Reads the ALR_CFG_0 register
        
        :return: the shadow register RSVD_7_6_ALR_CFG_0.
        :rtype: int
        """
        self.read_ALR_CFG_0()
        return self._BITFIELD['RSVD_7_6_ALR_CFG_0']

    def set_RT_HIGH_ALR_STAT(self, value):
        """
        Writes the RT_HIGH_ALR_STAT bitfield in the ALR_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_0()
        self._BITFIELD['RT_HIGH_ALR_STAT'] = value
        self.write_ALR_CFG_0()

    def get_RT_HIGH_ALR_STAT(self):
        """
        Reads the ALR_CFG_0 register
        
        :return: the shadow register RT_HIGH_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_CFG_0()
        return self._BITFIELD['RT_HIGH_ALR_STAT']

    def set_RT_LOW_ALR_STAT(self, value):
        """
        Writes the RT_LOW_ALR_STAT bitfield in the ALR_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_0()
        self._BITFIELD['RT_LOW_ALR_STAT'] = value
        self.write_ALR_CFG_0()

    def get_RT_LOW_ALR_STAT(self):
        """
        Reads the ALR_CFG_0 register
        
        :return: the shadow register RT_LOW_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_CFG_0()
        return self._BITFIELD['RT_LOW_ALR_STAT']

    def set_CS_B_ALR_STAT(self, value):
        """
        Writes the CS_B_ALR_STAT bitfield in the ALR_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_0()
        self._BITFIELD['CS_B_ALR_STAT'] = value
        self.write_ALR_CFG_0()

    def get_CS_B_ALR_STAT(self):
        """
        Reads the ALR_CFG_0 register
        
        :return: the shadow register CS_B_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_CFG_0()
        return self._BITFIELD['CS_B_ALR_STAT']

    def set_CS_A_ALR_STAT(self, value):
        """
        Writes the CS_A_ALR_STAT bitfield in the ALR_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_0()
        self._BITFIELD['CS_A_ALR_STAT'] = value
        self.write_ALR_CFG_0()

    def get_CS_A_ALR_STAT(self):
        """
        Reads the ALR_CFG_0 register
        
        :return: the shadow register CS_A_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_CFG_0()
        return self._BITFIELD['CS_A_ALR_STAT']

    def set_ADC_IN1_ALR_STAT(self, value):
        """
        Writes the ADC_IN1_ALR_STAT bitfield in the ALR_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_0()
        self._BITFIELD['ADC_IN1_ALR_STAT'] = value
        self.write_ALR_CFG_0()

    def get_ADC_IN1_ALR_STAT(self):
        """
        Reads the ALR_CFG_0 register
        
        :return: the shadow register ADC_IN1_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_CFG_0()
        return self._BITFIELD['ADC_IN1_ALR_STAT']

    def set_ADC_IN0_ALR_STAT(self, value):
        """
        Writes the ADC_IN0_ALR_STAT bitfield in the ALR_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_0()
        self._BITFIELD['ADC_IN0_ALR_STAT'] = value
        self.write_ALR_CFG_0()

    def get_ADC_IN0_ALR_STAT(self):
        """
        Reads the ALR_CFG_0 register
        
        :return: the shadow register ADC_IN0_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_CFG_0()
        return self._BITFIELD['ADC_IN0_ALR_STAT']

    def set_ALR_LATCH_DIS(self, value):
        """
        Writes the ALR_LATCH_DIS bitfield in the ALR_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_1()
        self._BITFIELD['ALR_LATCH_DIS'] = value
        self.write_ALR_CFG_1()

    def get_ALR_LATCH_DIS(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register ALR_LATCH_DIS.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['ALR_LATCH_DIS']

    def set_RSVD_6_ALR_CFG_1(self, value):
        """
         Read Only bit field RSVD_6_ALR_CFG_1 in the ALR_CFG_1 register. Skip the write.
        """

    def get_RSVD_6_ALR_CFG_1(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register RSVD_6_ALR_CFG_1.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['RSVD_6_ALR_CFG_1']

    def set_S0S1_ERR_ALR(self, value):
        """
        Writes the S0S1_ERR_ALR bitfield in the ALR_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_1()
        self._BITFIELD['S0S1_ERR_ALR'] = value
        self.write_ALR_CFG_1()

    def get_S0S1_ERR_ALR(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register S0S1_ERR_ALR.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['S0S1_ERR_ALR']

    def set_PAR_ERR_ALR(self, value):
        """
        Writes the PAR_ERR_ALR bitfield in the ALR_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_1()
        self._BITFIELD['PAR_ERR_ALR'] = value
        self.write_ALR_CFG_1()

    def get_PAR_ERR_ALR(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register PAR_ERR_ALR.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['PAR_ERR_ALR']

    def set_DAV_ALR(self, value):
        """
        Writes the DAV_ALR bitfield in the ALR_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_1()
        self._BITFIELD['DAV_ALR'] = value
        self.write_ALR_CFG_1()

    def get_DAV_ALR(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register DAV_ALR.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['DAV_ALR']

    def set_THERM_ALR(self, value):
        """
        Writes the THERM_ALR bitfield in the ALR_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_1()
        self._BITFIELD['THERM_ALR'] = value
        self.write_ALR_CFG_1()

    def get_THERM_ALR(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register THERM_ALR.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['THERM_ALR']

    def set_LT_HIGH_ALR(self, value):
        """
        Writes the LT_HIGH_ALR bitfield in the ALR_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_1()
        self._BITFIELD['LT_HIGH_ALR'] = value
        self.write_ALR_CFG_1()

    def get_LT_HIGH_ALR(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register LT_HIGH_ALR.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['LT_HIGH_ALR']

    def set_LT_LOW_ALR(self, value):
        """
        Writes the LT_LOW_ALR bitfield in the ALR_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ALR_CFG_1()
        self._BITFIELD['LT_LOW_ALR'] = value
        self.write_ALR_CFG_1()

    def get_LT_LOW_ALR(self):
        """
        Reads the ALR_CFG_1 register
        
        :return: the shadow register LT_LOW_ALR.
        :rtype: int
        """
        self.read_ALR_CFG_1()
        return self._BITFIELD['LT_LOW_ALR']

    def set_RSVD_7_DAC_RANGE(self, value):
        """
         Read Only bit field RSVD_7_DAC_RANGE in the DAC_RANGE register. Skip the write.
        """

    def get_RSVD_7_DAC_RANGE(self):
        """
        Reads the DAC_RANGE register
        
        :return: the shadow register RSVD_7_DAC_RANGE.
        :rtype: int
        """
        self.read_DAC_RANGE()
        return self._BITFIELD['RSVD_7_DAC_RANGE']

    def set_DAC_RANGEB(self, value):
        """
        Writes the DAC_RANGEB bitfield in the DAC_RANGE register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_RANGE()
        self._BITFIELD['DAC_RANGEB'] = value
        self.write_DAC_RANGE()

    def get_DAC_RANGEB(self):
        """
        Reads the DAC_RANGE register
        
        :return: the shadow register DAC_RANGEB.
        :rtype: int
        """
        self.read_DAC_RANGE()
        return self._BITFIELD['DAC_RANGEB']

    def set_RSVD_3_DAC_RANGE(self, value):
        """
         Read Only bit field RSVD_3_DAC_RANGE in the DAC_RANGE register. Skip the write.
        """

    def get_RSVD_3_DAC_RANGE(self):
        """
        Reads the DAC_RANGE register
        
        :return: the shadow register RSVD_3_DAC_RANGE.
        :rtype: int
        """
        self.read_DAC_RANGE()
        return self._BITFIELD['RSVD_3_DAC_RANGE']

    def set_DAC_RANGEA(self, value):
        """
        Writes the DAC_RANGEA bitfield in the DAC_RANGE register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_RANGE()
        self._BITFIELD['DAC_RANGEA'] = value
        self.write_DAC_RANGE()

    def get_DAC_RANGEA(self):
        """
        Reads the DAC_RANGE register
        
        :return: the shadow register DAC_RANGEA.
        :rtype: int
        """
        self.read_DAC_RANGE()
        return self._BITFIELD['DAC_RANGEA']

    def set_ADC_IN0_DATA_L(self, value):
        """
         Read Only bit field ADC_IN0_DATA_L in the ADC_IN0_DATA_L register. Skip the write.
        """

    def get_ADC_IN0_DATA_L(self):
        """
        Reads the ADC_IN0_DATA_L register
        
        :return: the shadow register ADC_IN0_DATA_L.
        :rtype: int
        """
        self.read_ADC_IN0_DATA_L()
        return self._BITFIELD['ADC_IN0_DATA_L']

    def set_RSVD_7_4_ADC_IN0_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_IN0_DATA_H in the ADC_IN0_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_ADC_IN0_DATA_H(self):
        """
        Reads the ADC_IN0_DATA_H register
        
        :return: the shadow register RSVD_7_4_ADC_IN0_DATA_H.
        :rtype: int
        """
        self.read_ADC_IN0_DATA_H()
        return self._BITFIELD['RSVD_7_4_ADC_IN0_DATA_H']

    def set_ADC_IN0_DATA_H(self, value):
        """
         Read Only bit field ADC_IN0_DATA_H in the ADC_IN0_DATA_H register. Skip the write.
        """

    def get_ADC_IN0_DATA_H(self):
        """
        Reads the ADC_IN0_DATA_H register
        
        :return: the shadow register ADC_IN0_DATA_H.
        :rtype: int
        """
        self.read_ADC_IN0_DATA_H()
        return self._BITFIELD['ADC_IN0_DATA_H']

    def set_ADC_IN1_DATA_L(self, value):
        """
         Read Only bit field ADC_IN1_DATA_L in the ADC_IN1_DATA_L register. Skip the write.
        """

    def get_ADC_IN1_DATA_L(self):
        """
        Reads the ADC_IN1_DATA_L register
        
        :return: the shadow register ADC_IN1_DATA_L.
        :rtype: int
        """
        self.read_ADC_IN1_DATA_L()
        return self._BITFIELD['ADC_IN1_DATA_L']

    def set_RSVD_7_4_ADC_IN1_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_IN1_DATA_H in the ADC_IN1_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_ADC_IN1_DATA_H(self):
        """
        Reads the ADC_IN1_DATA_H register
        
        :return: the shadow register RSVD_7_4_ADC_IN1_DATA_H.
        :rtype: int
        """
        self.read_ADC_IN1_DATA_H()
        return self._BITFIELD['RSVD_7_4_ADC_IN1_DATA_H']

    def set_ADC_IN1_DATA_H(self, value):
        """
         Read Only bit field ADC_IN1_DATA_H in the ADC_IN1_DATA_H register. Skip the write.
        """

    def get_ADC_IN1_DATA_H(self):
        """
        Reads the ADC_IN1_DATA_H register
        
        :return: the shadow register ADC_IN1_DATA_H.
        :rtype: int
        """
        self.read_ADC_IN1_DATA_H()
        return self._BITFIELD['ADC_IN1_DATA_H']

    def set_CS_A_DATA_L(self, value):
        """
         Read Only bit field CS_A_DATA_L in the CS_A_DATA_L register. Skip the write.
        """

    def get_CS_A_DATA_L(self):
        """
        Reads the CS_A_DATA_L register
        
        :return: the shadow register CS_A_DATA_L.
        :rtype: int
        """
        self.read_CS_A_DATA_L()
        return self._BITFIELD['CS_A_DATA_L']

    def set_RSVD_7_5_CS_A_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_5_CS_A_DATA_H in the CS_A_DATA_H register. Skip the write.
        """

    def get_RSVD_7_5_CS_A_DATA_H(self):
        """
        Reads the CS_A_DATA_H register
        
        :return: the shadow register RSVD_7_5_CS_A_DATA_H.
        :rtype: int
        """
        self.read_CS_A_DATA_H()
        return self._BITFIELD['RSVD_7_5_CS_A_DATA_H']

    def set_CS_A_DATA_H_SIGN(self, value):
        """
         Read Only bit field CS_A_DATA_H_SIGN in the CS_A_DATA_H register. Skip the write.
        """

    def get_CS_A_DATA_H_SIGN(self):
        """
        Reads the CS_A_DATA_H register
        
        :return: the shadow register CS_A_DATA_H_SIGN.
        :rtype: int
        """
        self.read_CS_A_DATA_H()
        return self._BITFIELD['CS_A_DATA_H_SIGN']

    def set_CS_A_DATA_H(self, value):
        """
         Read Only bit field CS_A_DATA_H in the CS_A_DATA_H register. Skip the write.
        """

    def get_CS_A_DATA_H(self):
        """
        Reads the CS_A_DATA_H register
        
        :return: the shadow register CS_A_DATA_H.
        :rtype: int
        """
        self.read_CS_A_DATA_H()
        return self._BITFIELD['CS_A_DATA_H']

    def set_CS_B_DATA_L(self, value):
        """
         Read Only bit field CS_B_DATA_L in the CS_B_DATA_L register. Skip the write.
        """

    def get_CS_B_DATA_L(self):
        """
        Reads the CS_B_DATA_L register
        
        :return: the shadow register CS_B_DATA_L.
        :rtype: int
        """
        self.read_CS_B_DATA_L()
        return self._BITFIELD['CS_B_DATA_L']

    def set_RSVD_7_5_CS_B_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_5_CS_B_DATA_H in the CS_B_DATA_H register. Skip the write.
        """

    def get_RSVD_7_5_CS_B_DATA_H(self):
        """
        Reads the CS_B_DATA_H register
        
        :return: the shadow register RSVD_7_5_CS_B_DATA_H.
        :rtype: int
        """
        self.read_CS_B_DATA_H()
        return self._BITFIELD['RSVD_7_5_CS_B_DATA_H']

    def set_CS_B_DATA_H_SIGN(self, value):
        """
         Read Only bit field CS_B_DATA_H_SIGN in the CS_B_DATA_H register. Skip the write.
        """

    def get_CS_B_DATA_H_SIGN(self):
        """
        Reads the CS_B_DATA_H register
        
        :return: the shadow register CS_B_DATA_H_SIGN.
        :rtype: int
        """
        self.read_CS_B_DATA_H()
        return self._BITFIELD['CS_B_DATA_H_SIGN']

    def set_CS_B_DATA_H(self, value):
        """
         Read Only bit field CS_B_DATA_H in the CS_B_DATA_H register. Skip the write.
        """

    def get_CS_B_DATA_H(self):
        """
        Reads the CS_B_DATA_H register
        
        :return: the shadow register CS_B_DATA_H.
        :rtype: int
        """
        self.read_CS_B_DATA_H()
        return self._BITFIELD['CS_B_DATA_H']

    def set_LT_DATA_L(self, value):
        """
         Read Only bit field LT_DATA_L in the LT_DATA_L register. Skip the write.
        """

    def get_LT_DATA_L(self):
        """
        Reads the LT_DATA_L register
        
        :return: the shadow register LT_DATA_L.
        :rtype: int
        """
        self.read_LT_DATA_L()
        return self._BITFIELD['LT_DATA_L']

    def set_RSVD_7_4_LT_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_LT_DATA_H in the LT_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_LT_DATA_H(self):
        """
        Reads the LT_DATA_H register
        
        :return: the shadow register RSVD_7_4_LT_DATA_H.
        :rtype: int
        """
        self.read_LT_DATA_H()
        return self._BITFIELD['RSVD_7_4_LT_DATA_H']

    def set_LT_DATA_H(self, value):
        """
         Read Only bit field LT_DATA_H in the LT_DATA_H register. Skip the write.
        """

    def get_LT_DATA_H(self):
        """
        Reads the LT_DATA_H register
        
        :return: the shadow register LT_DATA_H.
        :rtype: int
        """
        self.read_LT_DATA_H()
        return self._BITFIELD['LT_DATA_H']

    def set_RT_DATA_L(self, value):
        """
         Read Only bit field RT_DATA_L in the RT_DATA_L register. Skip the write.
        """

    def get_RT_DATA_L(self):
        """
        Reads the RT_DATA_L register
        
        :return: the shadow register RT_DATA_L.
        :rtype: int
        """
        self.read_RT_DATA_L()
        return self._BITFIELD['RT_DATA_L']

    def set_RSVD_7_4_RT_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_RT_DATA_H in the RT_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_RT_DATA_H(self):
        """
        Reads the RT_DATA_H register
        
        :return: the shadow register RSVD_7_4_RT_DATA_H.
        :rtype: int
        """
        self.read_RT_DATA_H()
        return self._BITFIELD['RSVD_7_4_RT_DATA_H']

    def set_RT_DATA_H(self, value):
        """
         Read Only bit field RT_DATA_H in the RT_DATA_H register. Skip the write.
        """

    def get_RT_DATA_H(self):
        """
        Reads the RT_DATA_H register
        
        :return: the shadow register RT_DATA_H.
        :rtype: int
        """
        self.read_RT_DATA_H()
        return self._BITFIELD['RT_DATA_H']

    def set_DAC0_DATA_L(self, value):
        """
        Writes the DAC0_DATA_L bitfield in the DAC0_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC0_DATA_L()
        self._BITFIELD['DAC0_DATA_L'] = value
        self.write_DAC0_DATA_L()

    def get_DAC0_DATA_L(self):
        """
        Reads the DAC0_DATA_L register
        
        :return: the shadow register DAC0_DATA_L.
        :rtype: int
        """
        self.read_DAC0_DATA_L()
        return self._BITFIELD['DAC0_DATA_L']

    def set_RSVD_7_4_DAC0_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC0_DATA_H in the DAC0_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC0_DATA_H(self):
        """
        Reads the DAC0_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC0_DATA_H.
        :rtype: int
        """
        self.read_DAC0_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC0_DATA_H']

    def set_DAC0_DATA_H(self, value):
        """
        Writes the DAC0_DATA_H bitfield in the DAC0_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC0_DATA_H()
        self._BITFIELD['DAC0_DATA_H'] = value
        self.write_DAC0_DATA_H()

    def get_DAC0_DATA_H(self):
        """
        Reads the DAC0_DATA_H register
        
        :return: the shadow register DAC0_DATA_H.
        :rtype: int
        """
        self.read_DAC0_DATA_H()
        return self._BITFIELD['DAC0_DATA_H']

    def set_DAC1_DATA_L(self, value):
        """
        Writes the DAC1_DATA_L bitfield in the DAC1_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC1_DATA_L()
        self._BITFIELD['DAC1_DATA_L'] = value
        self.write_DAC1_DATA_L()

    def get_DAC1_DATA_L(self):
        """
        Reads the DAC1_DATA_L register
        
        :return: the shadow register DAC1_DATA_L.
        :rtype: int
        """
        self.read_DAC1_DATA_L()
        return self._BITFIELD['DAC1_DATA_L']

    def set_RSVD_7_4_DAC1_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC1_DATA_H in the DAC1_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC1_DATA_H(self):
        """
        Reads the DAC1_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC1_DATA_H.
        :rtype: int
        """
        self.read_DAC1_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC1_DATA_H']

    def set_DAC1_DATA_H(self, value):
        """
        Writes the DAC1_DATA_H bitfield in the DAC1_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC1_DATA_H()
        self._BITFIELD['DAC1_DATA_H'] = value
        self.write_DAC1_DATA_H()

    def get_DAC1_DATA_H(self):
        """
        Reads the DAC1_DATA_H register
        
        :return: the shadow register DAC1_DATA_H.
        :rtype: int
        """
        self.read_DAC1_DATA_H()
        return self._BITFIELD['DAC1_DATA_H']

    def set_DAC2_DATA_L(self, value):
        """
        Writes the DAC2_DATA_L bitfield in the DAC2_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC2_DATA_L()
        self._BITFIELD['DAC2_DATA_L'] = value
        self.write_DAC2_DATA_L()

    def get_DAC2_DATA_L(self):
        """
        Reads the DAC2_DATA_L register
        
        :return: the shadow register DAC2_DATA_L.
        :rtype: int
        """
        self.read_DAC2_DATA_L()
        return self._BITFIELD['DAC2_DATA_L']

    def set_RSVD_7_4_DAC2_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC2_DATA_H in the DAC2_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC2_DATA_H(self):
        """
        Reads the DAC2_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC2_DATA_H.
        :rtype: int
        """
        self.read_DAC2_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC2_DATA_H']

    def set_DAC2_DATA_H(self, value):
        """
        Writes the DAC2_DATA_H bitfield in the DAC2_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC2_DATA_H()
        self._BITFIELD['DAC2_DATA_H'] = value
        self.write_DAC2_DATA_H()

    def get_DAC2_DATA_H(self):
        """
        Reads the DAC2_DATA_H register
        
        :return: the shadow register DAC2_DATA_H.
        :rtype: int
        """
        self.read_DAC2_DATA_H()
        return self._BITFIELD['DAC2_DATA_H']

    def set_DAC3_DATA_L(self, value):
        """
        Writes the DAC3_DATA_L bitfield in the DAC3_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC3_DATA_L()
        self._BITFIELD['DAC3_DATA_L'] = value
        self.write_DAC3_DATA_L()

    def get_DAC3_DATA_L(self):
        """
        Reads the DAC3_DATA_L register
        
        :return: the shadow register DAC3_DATA_L.
        :rtype: int
        """
        self.read_DAC3_DATA_L()
        return self._BITFIELD['DAC3_DATA_L']

    def set_RSVD_7_4_DAC3_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC3_DATA_H in the DAC3_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC3_DATA_H(self):
        """
        Reads the DAC3_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC3_DATA_H.
        :rtype: int
        """
        self.read_DAC3_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC3_DATA_H']

    def set_DAC3_DATA_H(self, value):
        """
        Writes the DAC3_DATA_H bitfield in the DAC3_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC3_DATA_H()
        self._BITFIELD['DAC3_DATA_H'] = value
        self.write_DAC3_DATA_H()

    def get_DAC3_DATA_H(self):
        """
        Reads the DAC3_DATA_H register
        
        :return: the shadow register DAC3_DATA_H.
        :rtype: int
        """
        self.read_DAC3_DATA_H()
        return self._BITFIELD['DAC3_DATA_H']

    def set_DAC4_DATA_L(self, value):
        """
        Writes the DAC4_DATA_L bitfield in the DAC4_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC4_DATA_L()
        self._BITFIELD['DAC4_DATA_L'] = value
        self.write_DAC4_DATA_L()

    def get_DAC4_DATA_L(self):
        """
        Reads the DAC4_DATA_L register
        
        :return: the shadow register DAC4_DATA_L.
        :rtype: int
        """
        self.read_DAC4_DATA_L()
        return self._BITFIELD['DAC4_DATA_L']

    def set_RSVD_7_4_DAC4_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC4_DATA_H in the DAC4_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC4_DATA_H(self):
        """
        Reads the DAC4_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC4_DATA_H.
        :rtype: int
        """
        self.read_DAC4_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC4_DATA_H']

    def set_DAC4_DATA_H(self, value):
        """
        Writes the DAC4_DATA_H bitfield in the DAC4_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC4_DATA_H()
        self._BITFIELD['DAC4_DATA_H'] = value
        self.write_DAC4_DATA_H()

    def get_DAC4_DATA_H(self):
        """
        Reads the DAC4_DATA_H register
        
        :return: the shadow register DAC4_DATA_H.
        :rtype: int
        """
        self.read_DAC4_DATA_H()
        return self._BITFIELD['DAC4_DATA_H']

    def set_DAC5_DATA_L(self, value):
        """
        Writes the DAC5_DATA_L bitfield in the DAC5_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC5_DATA_L()
        self._BITFIELD['DAC5_DATA_L'] = value
        self.write_DAC5_DATA_L()

    def get_DAC5_DATA_L(self):
        """
        Reads the DAC5_DATA_L register
        
        :return: the shadow register DAC5_DATA_L.
        :rtype: int
        """
        self.read_DAC5_DATA_L()
        return self._BITFIELD['DAC5_DATA_L']

    def set_RSVD_7_4_DAC5_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC5_DATA_H in the DAC5_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC5_DATA_H(self):
        """
        Reads the DAC5_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC5_DATA_H.
        :rtype: int
        """
        self.read_DAC5_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC5_DATA_H']

    def set_DAC5_DATA_H(self, value):
        """
        Writes the DAC5_DATA_H bitfield in the DAC5_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC5_DATA_H()
        self._BITFIELD['DAC5_DATA_H'] = value
        self.write_DAC5_DATA_H()

    def get_DAC5_DATA_H(self):
        """
        Reads the DAC5_DATA_H register
        
        :return: the shadow register DAC5_DATA_H.
        :rtype: int
        """
        self.read_DAC5_DATA_H()
        return self._BITFIELD['DAC5_DATA_H']

    def set_DAC6_DATA_L(self, value):
        """
        Writes the DAC6_DATA_L bitfield in the DAC6_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC6_DATA_L()
        self._BITFIELD['DAC6_DATA_L'] = value
        self.write_DAC6_DATA_L()

    def get_DAC6_DATA_L(self):
        """
        Reads the DAC6_DATA_L register
        
        :return: the shadow register DAC6_DATA_L.
        :rtype: int
        """
        self.read_DAC6_DATA_L()
        return self._BITFIELD['DAC6_DATA_L']

    def set_RSVD_7_4_DAC6_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC6_DATA_H in the DAC6_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC6_DATA_H(self):
        """
        Reads the DAC6_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC6_DATA_H.
        :rtype: int
        """
        self.read_DAC6_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC6_DATA_H']

    def set_DAC6_DATA_H(self, value):
        """
        Writes the DAC6_DATA_H bitfield in the DAC6_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC6_DATA_H()
        self._BITFIELD['DAC6_DATA_H'] = value
        self.write_DAC6_DATA_H()

    def get_DAC6_DATA_H(self):
        """
        Reads the DAC6_DATA_H register
        
        :return: the shadow register DAC6_DATA_H.
        :rtype: int
        """
        self.read_DAC6_DATA_H()
        return self._BITFIELD['DAC6_DATA_H']

    def set_DAC7_DATA_L(self, value):
        """
        Writes the DAC7_DATA_L bitfield in the DAC7_DATA_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC7_DATA_L()
        self._BITFIELD['DAC7_DATA_L'] = value
        self.write_DAC7_DATA_L()

    def get_DAC7_DATA_L(self):
        """
        Reads the DAC7_DATA_L register
        
        :return: the shadow register DAC7_DATA_L.
        :rtype: int
        """
        self.read_DAC7_DATA_L()
        return self._BITFIELD['DAC7_DATA_L']

    def set_RSVD_7_4_DAC7_DATA_H(self, value):
        """
         Read Only bit field RSVD_7_4_DAC7_DATA_H in the DAC7_DATA_H register. Skip the write.
        """

    def get_RSVD_7_4_DAC7_DATA_H(self):
        """
        Reads the DAC7_DATA_H register
        
        :return: the shadow register RSVD_7_4_DAC7_DATA_H.
        :rtype: int
        """
        self.read_DAC7_DATA_H()
        return self._BITFIELD['RSVD_7_4_DAC7_DATA_H']

    def set_DAC7_DATA_H(self, value):
        """
        Writes the DAC7_DATA_H bitfield in the DAC7_DATA_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC7_DATA_H()
        self._BITFIELD['DAC7_DATA_H'] = value
        self.write_DAC7_DATA_H()

    def get_DAC7_DATA_H(self):
        """
        Reads the DAC7_DATA_H register
        
        :return: the shadow register DAC7_DATA_H.
        :rtype: int
        """
        self.read_DAC7_DATA_H()
        return self._BITFIELD['DAC7_DATA_H']

    def set_RSVD_7_4_ALR_STAT_0(self, value):
        """
         Read Only bit field RSVD_7_4_ALR_STAT_0 in the ALR_STAT_0 register. Skip the write.
        """

    def get_RSVD_7_4_ALR_STAT_0(self):
        """
        Reads the ALR_STAT_0 register
        
        :return: the shadow register RSVD_7_4_ALR_STAT_0.
        :rtype: int
        """
        self.read_ALR_STAT_0()
        return self._BITFIELD['RSVD_7_4_ALR_STAT_0']

    def set_RT_HIGH_ALR(self, value):
        """
         Read Only bit field RT_HIGH_ALR in the ALR_STAT_0 register. Skip the write.
        """

    def get_RT_HIGH_ALR(self):
        """
        Reads the ALR_STAT_0 register
        
        :return: the shadow register RT_HIGH_ALR.
        :rtype: int
        """
        self.read_ALR_STAT_0()
        return self._BITFIELD['RT_HIGH_ALR']

    def set_RT_LOW_ALR(self, value):
        """
         Read Only bit field RT_LOW_ALR in the ALR_STAT_0 register. Skip the write.
        """

    def get_RT_LOW_ALR(self):
        """
        Reads the ALR_STAT_0 register
        
        :return: the shadow register RT_LOW_ALR.
        :rtype: int
        """
        self.read_ALR_STAT_0()
        return self._BITFIELD['RT_LOW_ALR']

    def set_CS_B_ALR(self, value):
        """
         Read Only bit field CS_B_ALR in the ALR_STAT_0 register. Skip the write.
        """

    def get_CS_B_ALR(self):
        """
        Reads the ALR_STAT_0 register
        
        :return: the shadow register CS_B_ALR.
        :rtype: int
        """
        self.read_ALR_STAT_0()
        return self._BITFIELD['CS_B_ALR']

    def set_CS_A_ALR(self, value):
        """
         Read Only bit field CS_A_ALR in the ALR_STAT_0 register. Skip the write.
        """

    def get_CS_A_ALR(self):
        """
        Reads the ALR_STAT_0 register
        
        :return: the shadow register CS_A_ALR.
        :rtype: int
        """
        self.read_ALR_STAT_0()
        return self._BITFIELD['CS_A_ALR']

    def set_ADC_IN1_ALR(self, value):
        """
         Read Only bit field ADC_IN1_ALR in the ALR_STAT_0 register. Skip the write.
        """

    def get_ADC_IN1_ALR(self):
        """
        Reads the ALR_STAT_0 register
        
        :return: the shadow register ADC_IN1_ALR.
        :rtype: int
        """
        self.read_ALR_STAT_0()
        return self._BITFIELD['ADC_IN1_ALR']

    def set_ADC_IN0_ALR(self, value):
        """
         Read Only bit field ADC_IN0_ALR in the ALR_STAT_0 register. Skip the write.
        """

    def get_ADC_IN0_ALR(self):
        """
        Reads the ALR_STAT_0 register
        
        :return: the shadow register ADC_IN0_ALR.
        :rtype: int
        """
        self.read_ALR_STAT_0()
        return self._BITFIELD['ADC_IN0_ALR']

    def set_RSVD_7_6_ALR_STAT_1(self, value):
        """
         Read Only bit field RSVD_7_6_ALR_STAT_1 in the ALR_STAT_1 register. Skip the write.
        """

    def get_RSVD_7_6_ALR_STAT_1(self):
        """
        Reads the ALR_STAT_1 register
        
        :return: the shadow register RSVD_7_6_ALR_STAT_1.
        :rtype: int
        """
        self.read_ALR_STAT_1()
        return self._BITFIELD['RSVD_7_6_ALR_STAT_1']

    def set_S0S1_ERR_ALR_STAT(self, value):
        """
         Read Only bit field S0S1_ERR_ALR_STAT in the ALR_STAT_1 register. Skip the write.
        """

    def get_S0S1_ERR_ALR_STAT(self):
        """
        Reads the ALR_STAT_1 register
        
        :return: the shadow register S0S1_ERR_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_STAT_1()
        return self._BITFIELD['S0S1_ERR_ALR_STAT']

    def set_PAR_ERR_ALR_STAT(self, value):
        """
         Read Only bit field PAR_ERR_ALR_STAT in the ALR_STAT_1 register. Skip the write.
        """

    def get_PAR_ERR_ALR_STAT(self):
        """
        Reads the ALR_STAT_1 register
        
        :return: the shadow register PAR_ERR_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_STAT_1()
        return self._BITFIELD['PAR_ERR_ALR_STAT']

    def set_DAV_ALR_STAT(self, value):
        """
         Read Only bit field DAV_ALR_STAT in the ALR_STAT_1 register. Skip the write.
        """

    def get_DAV_ALR_STAT(self):
        """
        Reads the ALR_STAT_1 register
        
        :return: the shadow register DAV_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_STAT_1()
        return self._BITFIELD['DAV_ALR_STAT']

    def set_THERM_ALR_STAT(self, value):
        """
         Read Only bit field THERM_ALR_STAT in the ALR_STAT_1 register. Skip the write.
        """

    def get_THERM_ALR_STAT(self):
        """
        Reads the ALR_STAT_1 register
        
        :return: the shadow register THERM_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_STAT_1()
        return self._BITFIELD['THERM_ALR_STAT']

    def set_LT_HIGH_ALR_STAT(self, value):
        """
         Read Only bit field LT_HIGH_ALR_STAT in the ALR_STAT_1 register. Skip the write.
        """

    def get_LT_HIGH_ALR_STAT(self):
        """
        Reads the ALR_STAT_1 register
        
        :return: the shadow register LT_HIGH_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_STAT_1()
        return self._BITFIELD['LT_HIGH_ALR_STAT']

    def set_LT_LOW_ALR_STAT(self, value):
        """
         Read Only bit field LT_LOW_ALR_STAT in the ALR_STAT_1 register. Skip the write.
        """

    def get_LT_LOW_ALR_STAT(self):
        """
        Reads the ALR_STAT_1 register
        
        :return: the shadow register LT_LOW_ALR_STAT.
        :rtype: int
        """
        self.read_ALR_STAT_1()
        return self._BITFIELD['LT_LOW_ALR_STAT']

    def set_IBI_PEND(self, value):
        """
         Read Only bit field IBI_PEND in the GEN_STAT register. Skip the write.
        """

    def get_IBI_PEND(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register IBI_PEND.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['IBI_PEND']

    def set_IBI_ENABLE(self, value):
        """
         Read Only bit field IBI_ENABLE in the GEN_STAT register. Skip the write.
        """

    def get_IBI_ENABLE(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register IBI_ENABLE.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['IBI_ENABLE']

    def set_AVSSB(self, value):
        """
         Read Only bit field AVSSB in the GEN_STAT register. Skip the write.
        """

    def get_AVSSB(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register AVSSB.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['AVSSB']

    def set_AVSSA(self, value):
        """
         Read Only bit field AVSSA in the GEN_STAT register. Skip the write.
        """

    def get_AVSSA(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register AVSSA.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['AVSSA']

    def set_ADC_IDLE(self, value):
        """
         Read Only bit field ADC_IDLE in the GEN_STAT register. Skip the write.
        """

    def get_ADC_IDLE(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register ADC_IDLE.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['ADC_IDLE']

    def set_I3C_MODE(self, value):
        """
         Read Only bit field I3C_MODE in the GEN_STAT register. Skip the write.
        """

    def get_I3C_MODE(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register I3C_MODE.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['I3C_MODE']

    def set_GALR(self, value):
        """
         Read Only bit field GALR in the GEN_STAT register. Skip the write.
        """

    def get_GALR(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register GALR.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['GALR']

    def set_DAVF(self, value):
        """
         Read Only bit field DAVF in the GEN_STAT register. Skip the write.
        """

    def get_DAVF(self):
        """
        Reads the GEN_STAT register
        
        :return: the shadow register DAVF.
        :rtype: int
        """
        self.read_GEN_STAT()
        return self._BITFIELD['DAVF']

    def set_RSVD_7_2_GEN_STAT_1(self, value):
        """
         Read Only bit field RSVD_7_2_GEN_STAT_1 in the GEN_STAT_1 register. Skip the write.
        """

    def get_RSVD_7_2_GEN_STAT_1(self):
        """
        Reads the GEN_STAT_1 register
        
        :return: the shadow register RSVD_7_2_GEN_STAT_1.
        :rtype: int
        """
        self.read_GEN_STAT_1()
        return self._BITFIELD['RSVD_7_2_GEN_STAT_1']

    def set_AVCCB(self, value):
        """
         Read Only bit field AVCCB in the GEN_STAT_1 register. Skip the write.
        """

    def get_AVCCB(self):
        """
        Reads the GEN_STAT_1 register
        
        :return: the shadow register AVCCB.
        :rtype: int
        """
        self.read_GEN_STAT_1()
        return self._BITFIELD['AVCCB']

    def set_AVCCA(self, value):
        """
         Read Only bit field AVCCA in the GEN_STAT_1 register. Skip the write.
        """

    def get_AVCCA(self):
        """
        Reads the GEN_STAT_1 register
        
        :return: the shadow register AVCCA.
        :rtype: int
        """
        self.read_GEN_STAT_1()
        return self._BITFIELD['AVCCA']

    def set_DAC_OUT_OK(self, value):
        """
         Read Only bit field DAC_OUT_OK in the GEN_STAT_2 register. Skip the write.
        """

    def get_DAC_OUT_OK(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register DAC_OUT_OK.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['DAC_OUT_OK']

    def set_RSVD_6_GEN_STAT_2(self, value):
        """
         Read Only bit field RSVD_6_GEN_STAT_2 in the GEN_STAT_2 register. Skip the write.
        """

    def get_RSVD_6_GEN_STAT_2(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register RSVD_6_GEN_STAT_2.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['RSVD_6_GEN_STAT_2']

    def set_DAC_POWER_OK(self, value):
        """
         Read Only bit field DAC_POWER_OK in the GEN_STAT_2 register. Skip the write.
        """

    def get_DAC_POWER_OK(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register DAC_POWER_OK.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['DAC_POWER_OK']

    def set_AVSS_OK(self, value):
        """
         Read Only bit field AVSS_OK in the GEN_STAT_2 register. Skip the write.
        """

    def get_AVSS_OK(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register AVSS_OK.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['AVSS_OK']

    def set_AVCC_OK(self, value):
        """
         Read Only bit field AVCC_OK in the GEN_STAT_2 register. Skip the write.
        """

    def get_AVCC_OK(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register AVCC_OK.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['AVCC_OK']

    def set_IOVDD_OK(self, value):
        """
         Read Only bit field IOVDD_OK in the GEN_STAT_2 register. Skip the write.
        """

    def get_IOVDD_OK(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register IOVDD_OK.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['IOVDD_OK']

    def set_RSVD_1_GEN_STAT_2(self, value):
        """
         Read Only bit field RSVD_1_GEN_STAT_2 in the GEN_STAT_2 register. Skip the write.
        """

    def get_RSVD_1_GEN_STAT_2(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register RSVD_1_GEN_STAT_2.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['RSVD_1_GEN_STAT_2']

    def set_AVDD_OK(self, value):
        """
         Read Only bit field AVDD_OK in the GEN_STAT_2 register. Skip the write.
        """

    def get_AVDD_OK(self):
        """
        Reads the GEN_STAT_2 register
        
        :return: the shadow register AVDD_OK.
        :rtype: int
        """
        self.read_GEN_STAT_2()
        return self._BITFIELD['AVDD_OK']

    def set_RSVD_7_4_DAC_SW_EN(self, value):
        """
         Read Only bit field RSVD_7_4_DAC_SW_EN in the DAC_SW_EN register. Skip the write.
        """

    def get_RSVD_7_4_DAC_SW_EN(self):
        """
        Reads the DAC_SW_EN register
        
        :return: the shadow register RSVD_7_4_DAC_SW_EN.
        :rtype: int
        """
        self.read_DAC_SW_EN()
        return self._BITFIELD['RSVD_7_4_DAC_SW_EN']

    def set_DAC_B2_SW_EN(self, value):
        """
        Writes the DAC_B2_SW_EN bitfield in the DAC_SW_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_SW_EN()
        self._BITFIELD['DAC_B2_SW_EN'] = value
        self.write_DAC_SW_EN()

    def get_DAC_B2_SW_EN(self):
        """
        Reads the DAC_SW_EN register
        
        :return: the shadow register DAC_B2_SW_EN.
        :rtype: int
        """
        self.read_DAC_SW_EN()
        return self._BITFIELD['DAC_B2_SW_EN']

    def set_DAC_B0_SW_EN(self, value):
        """
        Writes the DAC_B0_SW_EN bitfield in the DAC_SW_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_SW_EN()
        self._BITFIELD['DAC_B0_SW_EN'] = value
        self.write_DAC_SW_EN()

    def get_DAC_B0_SW_EN(self):
        """
        Reads the DAC_SW_EN register
        
        :return: the shadow register DAC_B0_SW_EN.
        :rtype: int
        """
        self.read_DAC_SW_EN()
        return self._BITFIELD['DAC_B0_SW_EN']

    def set_DAC_A2_SW_EN(self, value):
        """
        Writes the DAC_A2_SW_EN bitfield in the DAC_SW_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_SW_EN()
        self._BITFIELD['DAC_A2_SW_EN'] = value
        self.write_DAC_SW_EN()

    def get_DAC_A2_SW_EN(self):
        """
        Reads the DAC_SW_EN register
        
        :return: the shadow register DAC_A2_SW_EN.
        :rtype: int
        """
        self.read_DAC_SW_EN()
        return self._BITFIELD['DAC_A2_SW_EN']

    def set_DAC_A0_SW_EN(self, value):
        """
        Writes the DAC_A0_SW_EN bitfield in the DAC_SW_EN register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_SW_EN()
        self._BITFIELD['DAC_A0_SW_EN'] = value
        self.write_DAC_SW_EN()

    def get_DAC_A0_SW_EN(self):
        """
        Reads the DAC_SW_EN register
        
        :return: the shadow register DAC_A0_SW_EN.
        :rtype: int
        """
        self.read_DAC_SW_EN()
        return self._BITFIELD['DAC_A0_SW_EN']

    def set_RSVD_7_OUT_AEN_GROUPA(self, value):
        """
         Read Only bit field RSVD_7_OUT_AEN_GROUPA in the OUT_AEN_GROUPA register. Skip the write.
        """

    def get_RSVD_7_OUT_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register RSVD_7_OUT_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['RSVD_7_OUT_AEN_GROUPA']

    def set_FETDRV_A2_AEN_GROUPA(self, value):
        """
        Writes the FETDRV_A2_AEN_GROUPA bitfield in the OUT_AEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPA()
        self._BITFIELD['FETDRV_A2_AEN_GROUPA'] = value
        self.write_OUT_AEN_GROUPA()

    def get_FETDRV_A2_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register FETDRV_A2_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['FETDRV_A2_AEN_GROUPA']

    def set_RSVD_5_OUT_AEN_GROUPA(self, value):
        """
         Read Only bit field RSVD_5_OUT_AEN_GROUPA in the OUT_AEN_GROUPA register. Skip the write.
        """

    def get_RSVD_5_OUT_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register RSVD_5_OUT_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['RSVD_5_OUT_AEN_GROUPA']

    def set_FETDRV_A0_AEN_GROUPA(self, value):
        """
        Writes the FETDRV_A0_AEN_GROUPA bitfield in the OUT_AEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPA()
        self._BITFIELD['FETDRV_A0_AEN_GROUPA'] = value
        self.write_OUT_AEN_GROUPA()

    def get_FETDRV_A0_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register FETDRV_A0_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['FETDRV_A0_AEN_GROUPA']

    def set_DAC_A3_AEN_GROUPA(self, value):
        """
        Writes the DAC_A3_AEN_GROUPA bitfield in the OUT_AEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPA()
        self._BITFIELD['DAC_A3_AEN_GROUPA'] = value
        self.write_OUT_AEN_GROUPA()

    def get_DAC_A3_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register DAC_A3_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['DAC_A3_AEN_GROUPA']

    def set_DAC_A2_AEN_GROUPA(self, value):
        """
        Writes the DAC_A2_AEN_GROUPA bitfield in the OUT_AEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPA()
        self._BITFIELD['DAC_A2_AEN_GROUPA'] = value
        self.write_OUT_AEN_GROUPA()

    def get_DAC_A2_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register DAC_A2_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['DAC_A2_AEN_GROUPA']

    def set_DAC_A1_AEN_GROUPA(self, value):
        """
        Writes the DAC_A1_AEN_GROUPA bitfield in the OUT_AEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPA()
        self._BITFIELD['DAC_A1_AEN_GROUPA'] = value
        self.write_OUT_AEN_GROUPA()

    def get_DAC_A1_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register DAC_A1_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['DAC_A1_AEN_GROUPA']

    def set_DAC_A0_AEN_GROUPA(self, value):
        """
        Writes the DAC_A0_AEN_GROUPA bitfield in the OUT_AEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPA()
        self._BITFIELD['DAC_A0_AEN_GROUPA'] = value
        self.write_OUT_AEN_GROUPA()

    def get_DAC_A0_AEN_GROUPA(self):
        """
        Reads the OUT_AEN_GROUPA register
        
        :return: the shadow register DAC_A0_AEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPA()
        return self._BITFIELD['DAC_A0_AEN_GROUPA']

    def set_RSVD_7_OUT_AEN_GROUPB(self, value):
        """
         Read Only bit field RSVD_7_OUT_AEN_GROUPB in the OUT_AEN_GROUPB register. Skip the write.
        """

    def get_RSVD_7_OUT_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register RSVD_7_OUT_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['RSVD_7_OUT_AEN_GROUPB']

    def set_FETDRV_B2_AEN_GROUPB(self, value):
        """
        Writes the FETDRV_B2_AEN_GROUPB bitfield in the OUT_AEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPB()
        self._BITFIELD['FETDRV_B2_AEN_GROUPB'] = value
        self.write_OUT_AEN_GROUPB()

    def get_FETDRV_B2_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register FETDRV_B2_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['FETDRV_B2_AEN_GROUPB']

    def set_RSVD_5_OUT_AEN_GROUPB(self, value):
        """
         Read Only bit field RSVD_5_OUT_AEN_GROUPB in the OUT_AEN_GROUPB register. Skip the write.
        """

    def get_RSVD_5_OUT_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register RSVD_5_OUT_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['RSVD_5_OUT_AEN_GROUPB']

    def set_FETDRV_B0_AEN_GROUPB(self, value):
        """
        Writes the FETDRV_B0_AEN_GROUPB bitfield in the OUT_AEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPB()
        self._BITFIELD['FETDRV_B0_AEN_GROUPB'] = value
        self.write_OUT_AEN_GROUPB()

    def get_FETDRV_B0_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register FETDRV_B0_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['FETDRV_B0_AEN_GROUPB']

    def set_DAC_B3_AEN_GROUPB(self, value):
        """
        Writes the DAC_B3_AEN_GROUPB bitfield in the OUT_AEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPB()
        self._BITFIELD['DAC_B3_AEN_GROUPB'] = value
        self.write_OUT_AEN_GROUPB()

    def get_DAC_B3_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register DAC_B3_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['DAC_B3_AEN_GROUPB']

    def set_DAC_B2_AEN_GROUPB(self, value):
        """
        Writes the DAC_B2_AEN_GROUPB bitfield in the OUT_AEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPB()
        self._BITFIELD['DAC_B2_AEN_GROUPB'] = value
        self.write_OUT_AEN_GROUPB()

    def get_DAC_B2_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register DAC_B2_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['DAC_B2_AEN_GROUPB']

    def set_DAC_B1_AEN_GROUPB(self, value):
        """
        Writes the DAC_B1_AEN_GROUPB bitfield in the OUT_AEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPB()
        self._BITFIELD['DAC_B1_AEN_GROUPB'] = value
        self.write_OUT_AEN_GROUPB()

    def get_DAC_B1_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register DAC_B1_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['DAC_B1_AEN_GROUPB']

    def set_DAC_B0_AEN_GROUPB(self, value):
        """
        Writes the DAC_B0_AEN_GROUPB bitfield in the OUT_AEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_AEN_GROUPB()
        self._BITFIELD['DAC_B0_AEN_GROUPB'] = value
        self.write_OUT_AEN_GROUPB()

    def get_DAC_B0_AEN_GROUPB(self):
        """
        Reads the OUT_AEN_GROUPB register
        
        :return: the shadow register DAC_B0_AEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_AEN_GROUPB()
        return self._BITFIELD['DAC_B0_AEN_GROUPB']

    def set_RSVD_7_OUT_BEN_GROUPA(self, value):
        """
         Read Only bit field RSVD_7_OUT_BEN_GROUPA in the OUT_BEN_GROUPA register. Skip the write.
        """

    def get_RSVD_7_OUT_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register RSVD_7_OUT_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['RSVD_7_OUT_BEN_GROUPA']

    def set_FETDRV_A2_BEN_GROUPA(self, value):
        """
        Writes the FETDRV_A2_BEN_GROUPA bitfield in the OUT_BEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPA()
        self._BITFIELD['FETDRV_A2_BEN_GROUPA'] = value
        self.write_OUT_BEN_GROUPA()

    def get_FETDRV_A2_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register FETDRV_A2_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['FETDRV_A2_BEN_GROUPA']

    def set_RSVD_5_OUT_BEN_GROUPA(self, value):
        """
         Read Only bit field RSVD_5_OUT_BEN_GROUPA in the OUT_BEN_GROUPA register. Skip the write.
        """

    def get_RSVD_5_OUT_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register RSVD_5_OUT_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['RSVD_5_OUT_BEN_GROUPA']

    def set_FETDRV_A0_BEN_GROUPA(self, value):
        """
        Writes the FETDRV_A0_BEN_GROUPA bitfield in the OUT_BEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPA()
        self._BITFIELD['FETDRV_A0_BEN_GROUPA'] = value
        self.write_OUT_BEN_GROUPA()

    def get_FETDRV_A0_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register FETDRV_A0_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['FETDRV_A0_BEN_GROUPA']

    def set_DAC_A3_BEN_GROUPA(self, value):
        """
        Writes the DAC_A3_BEN_GROUPA bitfield in the OUT_BEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPA()
        self._BITFIELD['DAC_A3_BEN_GROUPA'] = value
        self.write_OUT_BEN_GROUPA()

    def get_DAC_A3_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register DAC_A3_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['DAC_A3_BEN_GROUPA']

    def set_DAC_A2_BEN_GROUPA(self, value):
        """
        Writes the DAC_A2_BEN_GROUPA bitfield in the OUT_BEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPA()
        self._BITFIELD['DAC_A2_BEN_GROUPA'] = value
        self.write_OUT_BEN_GROUPA()

    def get_DAC_A2_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register DAC_A2_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['DAC_A2_BEN_GROUPA']

    def set_DAC_A1_BEN_GROUPA(self, value):
        """
        Writes the DAC_A1_BEN_GROUPA bitfield in the OUT_BEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPA()
        self._BITFIELD['DAC_A1_BEN_GROUPA'] = value
        self.write_OUT_BEN_GROUPA()

    def get_DAC_A1_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register DAC_A1_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['DAC_A1_BEN_GROUPA']

    def set_DAC_A0_BEN_GROUPA(self, value):
        """
        Writes the DAC_A0_BEN_GROUPA bitfield in the OUT_BEN_GROUPA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPA()
        self._BITFIELD['DAC_A0_BEN_GROUPA'] = value
        self.write_OUT_BEN_GROUPA()

    def get_DAC_A0_BEN_GROUPA(self):
        """
        Reads the OUT_BEN_GROUPA register
        
        :return: the shadow register DAC_A0_BEN_GROUPA.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPA()
        return self._BITFIELD['DAC_A0_BEN_GROUPA']

    def set_RSVD_7_OUT_BEN_GROUPB(self, value):
        """
         Read Only bit field RSVD_7_OUT_BEN_GROUPB in the OUT_BEN_GROUPB register. Skip the write.
        """

    def get_RSVD_7_OUT_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register RSVD_7_OUT_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['RSVD_7_OUT_BEN_GROUPB']

    def set_FETDRV_B2_BEN_GROUPB(self, value):
        """
        Writes the FETDRV_B2_BEN_GROUPB bitfield in the OUT_BEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPB()
        self._BITFIELD['FETDRV_B2_BEN_GROUPB'] = value
        self.write_OUT_BEN_GROUPB()

    def get_FETDRV_B2_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register FETDRV_B2_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['FETDRV_B2_BEN_GROUPB']

    def set_RSVD_5_OUT_BEN_GROUPB(self, value):
        """
         Read Only bit field RSVD_5_OUT_BEN_GROUPB in the OUT_BEN_GROUPB register. Skip the write.
        """

    def get_RSVD_5_OUT_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register RSVD_5_OUT_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['RSVD_5_OUT_BEN_GROUPB']

    def set_FETDRV_B0_BEN_GROUPB(self, value):
        """
        Writes the FETDRV_B0_BEN_GROUPB bitfield in the OUT_BEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPB()
        self._BITFIELD['FETDRV_B0_BEN_GROUPB'] = value
        self.write_OUT_BEN_GROUPB()

    def get_FETDRV_B0_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register FETDRV_B0_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['FETDRV_B0_BEN_GROUPB']

    def set_DAC_B3_BEN_GROUPB(self, value):
        """
        Writes the DAC_B3_BEN_GROUPB bitfield in the OUT_BEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPB()
        self._BITFIELD['DAC_B3_BEN_GROUPB'] = value
        self.write_OUT_BEN_GROUPB()

    def get_DAC_B3_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register DAC_B3_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['DAC_B3_BEN_GROUPB']

    def set_DAC_B2_BEN_GROUPB(self, value):
        """
        Writes the DAC_B2_BEN_GROUPB bitfield in the OUT_BEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPB()
        self._BITFIELD['DAC_B2_BEN_GROUPB'] = value
        self.write_OUT_BEN_GROUPB()

    def get_DAC_B2_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register DAC_B2_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['DAC_B2_BEN_GROUPB']

    def set_DAC_B1_BEN_GROUPB(self, value):
        """
        Writes the DAC_B1_BEN_GROUPB bitfield in the OUT_BEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPB()
        self._BITFIELD['DAC_B1_BEN_GROUPB'] = value
        self.write_OUT_BEN_GROUPB()

    def get_DAC_B1_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register DAC_B1_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['DAC_B1_BEN_GROUPB']

    def set_DAC_B0_BEN_GROUPB(self, value):
        """
        Writes the DAC_B0_BEN_GROUPB bitfield in the OUT_BEN_GROUPB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OUT_BEN_GROUPB()
        self._BITFIELD['DAC_B0_BEN_GROUPB'] = value
        self.write_OUT_BEN_GROUPB()

    def get_DAC_B0_BEN_GROUPB(self):
        """
        Reads the OUT_BEN_GROUPB register
        
        :return: the shadow register DAC_B0_BEN_GROUPB.
        :rtype: int
        """
        self.read_OUT_BEN_GROUPB()
        return self._BITFIELD['DAC_B0_BEN_GROUPB']

    def set_THRU_ADC_IN0_L(self, value):
        """
        Writes the THRU_ADC_IN0_L bitfield in the ADC_IN0_UP_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN0_UP_THR_L()
        self._BITFIELD['THRU_ADC_IN0_L'] = value
        self.write_ADC_IN0_UP_THR_L()

    def get_THRU_ADC_IN0_L(self):
        """
        Reads the ADC_IN0_UP_THR_L register
        
        :return: the shadow register THRU_ADC_IN0_L.
        :rtype: int
        """
        self.read_ADC_IN0_UP_THR_L()
        return self._BITFIELD['THRU_ADC_IN0_L']

    def set_RSVD_7_4_ADC_IN0_UP_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_IN0_UP_THR_H in the ADC_IN0_UP_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_ADC_IN0_UP_THR_H(self):
        """
        Reads the ADC_IN0_UP_THR_H register
        
        :return: the shadow register RSVD_7_4_ADC_IN0_UP_THR_H.
        :rtype: int
        """
        self.read_ADC_IN0_UP_THR_H()
        return self._BITFIELD['RSVD_7_4_ADC_IN0_UP_THR_H']

    def set_THRU_ADC_IN0_H(self, value):
        """
        Writes the THRU_ADC_IN0_H bitfield in the ADC_IN0_UP_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN0_UP_THR_H()
        self._BITFIELD['THRU_ADC_IN0_H'] = value
        self.write_ADC_IN0_UP_THR_H()

    def get_THRU_ADC_IN0_H(self):
        """
        Reads the ADC_IN0_UP_THR_H register
        
        :return: the shadow register THRU_ADC_IN0_H.
        :rtype: int
        """
        self.read_ADC_IN0_UP_THR_H()
        return self._BITFIELD['THRU_ADC_IN0_H']

    def set_THRL_ADC_IN0_L(self, value):
        """
        Writes the THRL_ADC_IN0_L bitfield in the ADC_IN0_LO_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN0_LO_THR_L()
        self._BITFIELD['THRL_ADC_IN0_L'] = value
        self.write_ADC_IN0_LO_THR_L()

    def get_THRL_ADC_IN0_L(self):
        """
        Reads the ADC_IN0_LO_THR_L register
        
        :return: the shadow register THRL_ADC_IN0_L.
        :rtype: int
        """
        self.read_ADC_IN0_LO_THR_L()
        return self._BITFIELD['THRL_ADC_IN0_L']

    def set_RSVD_7_4_ADC_IN0_LO_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_IN0_LO_THR_H in the ADC_IN0_LO_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_ADC_IN0_LO_THR_H(self):
        """
        Reads the ADC_IN0_LO_THR_H register
        
        :return: the shadow register RSVD_7_4_ADC_IN0_LO_THR_H.
        :rtype: int
        """
        self.read_ADC_IN0_LO_THR_H()
        return self._BITFIELD['RSVD_7_4_ADC_IN0_LO_THR_H']

    def set_THRL_ADC_IN0_H(self, value):
        """
        Writes the THRL_ADC_IN0_H bitfield in the ADC_IN0_LO_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN0_LO_THR_H()
        self._BITFIELD['THRL_ADC_IN0_H'] = value
        self.write_ADC_IN0_LO_THR_H()

    def get_THRL_ADC_IN0_H(self):
        """
        Reads the ADC_IN0_LO_THR_H register
        
        :return: the shadow register THRL_ADC_IN0_H.
        :rtype: int
        """
        self.read_ADC_IN0_LO_THR_H()
        return self._BITFIELD['THRL_ADC_IN0_H']

    def set_THRU_ADC_IN1_L(self, value):
        """
        Writes the THRU_ADC_IN1_L bitfield in the ADC_IN1_UP_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN1_UP_THR_L()
        self._BITFIELD['THRU_ADC_IN1_L'] = value
        self.write_ADC_IN1_UP_THR_L()

    def get_THRU_ADC_IN1_L(self):
        """
        Reads the ADC_IN1_UP_THR_L register
        
        :return: the shadow register THRU_ADC_IN1_L.
        :rtype: int
        """
        self.read_ADC_IN1_UP_THR_L()
        return self._BITFIELD['THRU_ADC_IN1_L']

    def set_RSVD_7_4_ADC_IN1_UP_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_IN1_UP_THR_H in the ADC_IN1_UP_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_ADC_IN1_UP_THR_H(self):
        """
        Reads the ADC_IN1_UP_THR_H register
        
        :return: the shadow register RSVD_7_4_ADC_IN1_UP_THR_H.
        :rtype: int
        """
        self.read_ADC_IN1_UP_THR_H()
        return self._BITFIELD['RSVD_7_4_ADC_IN1_UP_THR_H']

    def set_THRU_ADC_IN1_H(self, value):
        """
        Writes the THRU_ADC_IN1_H bitfield in the ADC_IN1_UP_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN1_UP_THR_H()
        self._BITFIELD['THRU_ADC_IN1_H'] = value
        self.write_ADC_IN1_UP_THR_H()

    def get_THRU_ADC_IN1_H(self):
        """
        Reads the ADC_IN1_UP_THR_H register
        
        :return: the shadow register THRU_ADC_IN1_H.
        :rtype: int
        """
        self.read_ADC_IN1_UP_THR_H()
        return self._BITFIELD['THRU_ADC_IN1_H']

    def set_THRL_ADC_IN1_L(self, value):
        """
        Writes the THRL_ADC_IN1_L bitfield in the ADC_IN1_LO_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN1_LO_THR_L()
        self._BITFIELD['THRL_ADC_IN1_L'] = value
        self.write_ADC_IN1_LO_THR_L()

    def get_THRL_ADC_IN1_L(self):
        """
        Reads the ADC_IN1_LO_THR_L register
        
        :return: the shadow register THRL_ADC_IN1_L.
        :rtype: int
        """
        self.read_ADC_IN1_LO_THR_L()
        return self._BITFIELD['THRL_ADC_IN1_L']

    def set_RSVD_7_4_ADC_IN1_LO_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_IN1_LO_THR_H in the ADC_IN1_LO_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_ADC_IN1_LO_THR_H(self):
        """
        Reads the ADC_IN1_LO_THR_H register
        
        :return: the shadow register RSVD_7_4_ADC_IN1_LO_THR_H.
        :rtype: int
        """
        self.read_ADC_IN1_LO_THR_H()
        return self._BITFIELD['RSVD_7_4_ADC_IN1_LO_THR_H']

    def set_THRL_ADC_IN1_H(self, value):
        """
        Writes the THRL_ADC_IN1_H bitfield in the ADC_IN1_LO_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN1_LO_THR_H()
        self._BITFIELD['THRL_ADC_IN1_H'] = value
        self.write_ADC_IN1_LO_THR_H()

    def get_THRL_ADC_IN1_H(self):
        """
        Reads the ADC_IN1_LO_THR_H register
        
        :return: the shadow register THRL_ADC_IN1_H.
        :rtype: int
        """
        self.read_ADC_IN1_LO_THR_H()
        return self._BITFIELD['THRL_ADC_IN1_H']

    def set_THRU_CS_A_L(self, value):
        """
        Writes the THRU_CS_A_L bitfield in the CS_A_UP_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_UP_THR_L()
        self._BITFIELD['THRU_CS_A_L'] = value
        self.write_CS_A_UP_THR_L()

    def get_THRU_CS_A_L(self):
        """
        Reads the CS_A_UP_THR_L register
        
        :return: the shadow register THRU_CS_A_L.
        :rtype: int
        """
        self.read_CS_A_UP_THR_L()
        return self._BITFIELD['THRU_CS_A_L']

    def set_RSVD_7_4_CS_A_UP_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_A_UP_THR_H in the CS_A_UP_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_A_UP_THR_H(self):
        """
        Reads the CS_A_UP_THR_H register
        
        :return: the shadow register RSVD_7_4_CS_A_UP_THR_H.
        :rtype: int
        """
        self.read_CS_A_UP_THR_H()
        return self._BITFIELD['RSVD_7_4_CS_A_UP_THR_H']

    def set_THRU_CS_A_H(self, value):
        """
        Writes the THRU_CS_A_H bitfield in the CS_A_UP_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_UP_THR_H()
        self._BITFIELD['THRU_CS_A_H'] = value
        self.write_CS_A_UP_THR_H()

    def get_THRU_CS_A_H(self):
        """
        Reads the CS_A_UP_THR_H register
        
        :return: the shadow register THRU_CS_A_H.
        :rtype: int
        """
        self.read_CS_A_UP_THR_H()
        return self._BITFIELD['THRU_CS_A_H']

    def set_THRL_CS_A_L(self, value):
        """
        Writes the THRL_CS_A_L bitfield in the CS_A_LO_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_LO_THR_L()
        self._BITFIELD['THRL_CS_A_L'] = value
        self.write_CS_A_LO_THR_L()

    def get_THRL_CS_A_L(self):
        """
        Reads the CS_A_LO_THR_L register
        
        :return: the shadow register THRL_CS_A_L.
        :rtype: int
        """
        self.read_CS_A_LO_THR_L()
        return self._BITFIELD['THRL_CS_A_L']

    def set_RSVD_7_4_CS_A_LO_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_A_LO_THR_H in the CS_A_LO_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_A_LO_THR_H(self):
        """
        Reads the CS_A_LO_THR_H register
        
        :return: the shadow register RSVD_7_4_CS_A_LO_THR_H.
        :rtype: int
        """
        self.read_CS_A_LO_THR_H()
        return self._BITFIELD['RSVD_7_4_CS_A_LO_THR_H']

    def set_THRL_CS_A_H(self, value):
        """
        Writes the THRL_CS_A_H bitfield in the CS_A_LO_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_LO_THR_H()
        self._BITFIELD['THRL_CS_A_H'] = value
        self.write_CS_A_LO_THR_H()

    def get_THRL_CS_A_H(self):
        """
        Reads the CS_A_LO_THR_H register
        
        :return: the shadow register THRL_CS_A_H.
        :rtype: int
        """
        self.read_CS_A_LO_THR_H()
        return self._BITFIELD['THRL_CS_A_H']

    def set_THRU_CS_B_L(self, value):
        """
        Writes the THRU_CS_B_L bitfield in the CS_B_UP_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_UP_THR_L()
        self._BITFIELD['THRU_CS_B_L'] = value
        self.write_CS_B_UP_THR_L()

    def get_THRU_CS_B_L(self):
        """
        Reads the CS_B_UP_THR_L register
        
        :return: the shadow register THRU_CS_B_L.
        :rtype: int
        """
        self.read_CS_B_UP_THR_L()
        return self._BITFIELD['THRU_CS_B_L']

    def set_RSVD_7_4_CS_B_UP_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_B_UP_THR_H in the CS_B_UP_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_B_UP_THR_H(self):
        """
        Reads the CS_B_UP_THR_H register
        
        :return: the shadow register RSVD_7_4_CS_B_UP_THR_H.
        :rtype: int
        """
        self.read_CS_B_UP_THR_H()
        return self._BITFIELD['RSVD_7_4_CS_B_UP_THR_H']

    def set_THRU_CS_B_H(self, value):
        """
        Writes the THRU_CS_B_H bitfield in the CS_B_UP_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_UP_THR_H()
        self._BITFIELD['THRU_CS_B_H'] = value
        self.write_CS_B_UP_THR_H()

    def get_THRU_CS_B_H(self):
        """
        Reads the CS_B_UP_THR_H register
        
        :return: the shadow register THRU_CS_B_H.
        :rtype: int
        """
        self.read_CS_B_UP_THR_H()
        return self._BITFIELD['THRU_CS_B_H']

    def set_THRL_CS_B_L(self, value):
        """
        Writes the THRL_CS_B_L bitfield in the CS_B_LO_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_LO_THR_L()
        self._BITFIELD['THRL_CS_B_L'] = value
        self.write_CS_B_LO_THR_L()

    def get_THRL_CS_B_L(self):
        """
        Reads the CS_B_LO_THR_L register
        
        :return: the shadow register THRL_CS_B_L.
        :rtype: int
        """
        self.read_CS_B_LO_THR_L()
        return self._BITFIELD['THRL_CS_B_L']

    def set_RSVD_7_4_CS_B_LO_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_B_LO_THR_H in the CS_B_LO_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_B_LO_THR_H(self):
        """
        Reads the CS_B_LO_THR_H register
        
        :return: the shadow register RSVD_7_4_CS_B_LO_THR_H.
        :rtype: int
        """
        self.read_CS_B_LO_THR_H()
        return self._BITFIELD['RSVD_7_4_CS_B_LO_THR_H']

    def set_THRL_CS_B_H(self, value):
        """
        Writes the THRL_CS_B_H bitfield in the CS_B_LO_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_LO_THR_H()
        self._BITFIELD['THRL_CS_B_H'] = value
        self.write_CS_B_LO_THR_H()

    def get_THRL_CS_B_H(self):
        """
        Reads the CS_B_LO_THR_H register
        
        :return: the shadow register THRL_CS_B_H.
        :rtype: int
        """
        self.read_CS_B_LO_THR_H()
        return self._BITFIELD['THRL_CS_B_H']

    def set_THRU_LT_L(self, value):
        """
        Writes the THRU_LT_L bitfield in the LT_UP_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_UP_THR_L()
        self._BITFIELD['THRU_LT_L'] = value
        self.write_LT_UP_THR_L()

    def get_THRU_LT_L(self):
        """
        Reads the LT_UP_THR_L register
        
        :return: the shadow register THRU_LT_L.
        :rtype: int
        """
        self.read_LT_UP_THR_L()
        return self._BITFIELD['THRU_LT_L']

    def set_RSVD_7_4_LT_UP_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_LT_UP_THR_H in the LT_UP_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_LT_UP_THR_H(self):
        """
        Reads the LT_UP_THR_H register
        
        :return: the shadow register RSVD_7_4_LT_UP_THR_H.
        :rtype: int
        """
        self.read_LT_UP_THR_H()
        return self._BITFIELD['RSVD_7_4_LT_UP_THR_H']

    def set_THRU_LT_H(self, value):
        """
        Writes the THRU_LT_H bitfield in the LT_UP_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_UP_THR_H()
        self._BITFIELD['THRU_LT_H'] = value
        self.write_LT_UP_THR_H()

    def get_THRU_LT_H(self):
        """
        Reads the LT_UP_THR_H register
        
        :return: the shadow register THRU_LT_H.
        :rtype: int
        """
        self.read_LT_UP_THR_H()
        return self._BITFIELD['THRU_LT_H']

    def set_THRL_LT_L(self, value):
        """
        Writes the THRL_LT_L bitfield in the LT_LO_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_LO_THR_L()
        self._BITFIELD['THRL_LT_L'] = value
        self.write_LT_LO_THR_L()

    def get_THRL_LT_L(self):
        """
        Reads the LT_LO_THR_L register
        
        :return: the shadow register THRL_LT_L.
        :rtype: int
        """
        self.read_LT_LO_THR_L()
        return self._BITFIELD['THRL_LT_L']

    def set_RSVD_7_4_LT_LO_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_LT_LO_THR_H in the LT_LO_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_LT_LO_THR_H(self):
        """
        Reads the LT_LO_THR_H register
        
        :return: the shadow register RSVD_7_4_LT_LO_THR_H.
        :rtype: int
        """
        self.read_LT_LO_THR_H()
        return self._BITFIELD['RSVD_7_4_LT_LO_THR_H']

    def set_THRL_LT_H(self, value):
        """
        Writes the THRL_LT_H bitfield in the LT_LO_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_LO_THR_H()
        self._BITFIELD['THRL_LT_H'] = value
        self.write_LT_LO_THR_H()

    def get_THRL_LT_H(self):
        """
        Reads the LT_LO_THR_H register
        
        :return: the shadow register THRL_LT_H.
        :rtype: int
        """
        self.read_LT_LO_THR_H()
        return self._BITFIELD['THRL_LT_H']

    def set_THRU_RT_L(self, value):
        """
        Writes the THRU_RT_L bitfield in the RT_UP_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_RT_UP_THR_L()
        self._BITFIELD['THRU_RT_L'] = value
        self.write_RT_UP_THR_L()

    def get_THRU_RT_L(self):
        """
        Reads the RT_UP_THR_L register
        
        :return: the shadow register THRU_RT_L.
        :rtype: int
        """
        self.read_RT_UP_THR_L()
        return self._BITFIELD['THRU_RT_L']

    def set_RSVD_7_4_RT_UP_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_RT_UP_THR_H in the RT_UP_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_RT_UP_THR_H(self):
        """
        Reads the RT_UP_THR_H register
        
        :return: the shadow register RSVD_7_4_RT_UP_THR_H.
        :rtype: int
        """
        self.read_RT_UP_THR_H()
        return self._BITFIELD['RSVD_7_4_RT_UP_THR_H']

    def set_THRU_RT_H(self, value):
        """
        Writes the THRU_RT_H bitfield in the RT_UP_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_RT_UP_THR_H()
        self._BITFIELD['THRU_RT_H'] = value
        self.write_RT_UP_THR_H()

    def get_THRU_RT_H(self):
        """
        Reads the RT_UP_THR_H register
        
        :return: the shadow register THRU_RT_H.
        :rtype: int
        """
        self.read_RT_UP_THR_H()
        return self._BITFIELD['THRU_RT_H']

    def set_THRL_RT_L(self, value):
        """
        Writes the THRL_RT_L bitfield in the RT_LO_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_RT_LO_THR_L()
        self._BITFIELD['THRL_RT_L'] = value
        self.write_RT_LO_THR_L()

    def get_THRL_RT_L(self):
        """
        Reads the RT_LO_THR_L register
        
        :return: the shadow register THRL_RT_L.
        :rtype: int
        """
        self.read_RT_LO_THR_L()
        return self._BITFIELD['THRL_RT_L']

    def set_RSVD_7_4_RT_LO_THR_H(self, value):
        """
         Read Only bit field RSVD_7_4_RT_LO_THR_H in the RT_LO_THR_H register. Skip the write.
        """

    def get_RSVD_7_4_RT_LO_THR_H(self):
        """
        Reads the RT_LO_THR_H register
        
        :return: the shadow register RSVD_7_4_RT_LO_THR_H.
        :rtype: int
        """
        self.read_RT_LO_THR_H()
        return self._BITFIELD['RSVD_7_4_RT_LO_THR_H']

    def set_THRL_RT_H(self, value):
        """
        Writes the THRL_RT_H bitfield in the RT_LO_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_RT_LO_THR_H()
        self._BITFIELD['THRL_RT_H'] = value
        self.write_RT_LO_THR_H()

    def get_THRL_RT_H(self):
        """
        Reads the RT_LO_THR_H register
        
        :return: the shadow register THRL_RT_H.
        :rtype: int
        """
        self.read_RT_LO_THR_H()
        return self._BITFIELD['THRL_RT_H']

    def set_RSVD_7_ADC_IN0_HYST(self, value):
        """
         Read Only bit field RSVD_7_ADC_IN0_HYST in the ADC_IN0_HYST register. Skip the write.
        """

    def get_RSVD_7_ADC_IN0_HYST(self):
        """
        Reads the ADC_IN0_HYST register
        
        :return: the shadow register RSVD_7_ADC_IN0_HYST.
        :rtype: int
        """
        self.read_ADC_IN0_HYST()
        return self._BITFIELD['RSVD_7_ADC_IN0_HYST']

    def set_HYST_ADC_IN0(self, value):
        """
        Writes the HYST_ADC_IN0 bitfield in the ADC_IN0_HYST register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN0_HYST()
        self._BITFIELD['HYST_ADC_IN0'] = value
        self.write_ADC_IN0_HYST()

    def get_HYST_ADC_IN0(self):
        """
        Reads the ADC_IN0_HYST register
        
        :return: the shadow register HYST_ADC_IN0.
        :rtype: int
        """
        self.read_ADC_IN0_HYST()
        return self._BITFIELD['HYST_ADC_IN0']

    def set_RSVD_7_ADC_IN1_HYST(self, value):
        """
         Read Only bit field RSVD_7_ADC_IN1_HYST in the ADC_IN1_HYST register. Skip the write.
        """

    def get_RSVD_7_ADC_IN1_HYST(self):
        """
        Reads the ADC_IN1_HYST register
        
        :return: the shadow register RSVD_7_ADC_IN1_HYST.
        :rtype: int
        """
        self.read_ADC_IN1_HYST()
        return self._BITFIELD['RSVD_7_ADC_IN1_HYST']

    def set_HYST_ADC_IN1(self, value):
        """
        Writes the HYST_ADC_IN1 bitfield in the ADC_IN1_HYST register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_IN1_HYST()
        self._BITFIELD['HYST_ADC_IN1'] = value
        self.write_ADC_IN1_HYST()

    def get_HYST_ADC_IN1(self):
        """
        Reads the ADC_IN1_HYST register
        
        :return: the shadow register HYST_ADC_IN1.
        :rtype: int
        """
        self.read_ADC_IN1_HYST()
        return self._BITFIELD['HYST_ADC_IN1']

    def set_RSVD_7_CS_A_HYST(self, value):
        """
         Read Only bit field RSVD_7_CS_A_HYST in the CS_A_HYST register. Skip the write.
        """

    def get_RSVD_7_CS_A_HYST(self):
        """
        Reads the CS_A_HYST register
        
        :return: the shadow register RSVD_7_CS_A_HYST.
        :rtype: int
        """
        self.read_CS_A_HYST()
        return self._BITFIELD['RSVD_7_CS_A_HYST']

    def set_HYST_CS_A(self, value):
        """
        Writes the HYST_CS_A bitfield in the CS_A_HYST register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_HYST()
        self._BITFIELD['HYST_CS_A'] = value
        self.write_CS_A_HYST()

    def get_HYST_CS_A(self):
        """
        Reads the CS_A_HYST register
        
        :return: the shadow register HYST_CS_A.
        :rtype: int
        """
        self.read_CS_A_HYST()
        return self._BITFIELD['HYST_CS_A']

    def set_RSVD_7_CS_B_HYST(self, value):
        """
         Read Only bit field RSVD_7_CS_B_HYST in the CS_B_HYST register. Skip the write.
        """

    def get_RSVD_7_CS_B_HYST(self):
        """
        Reads the CS_B_HYST register
        
        :return: the shadow register RSVD_7_CS_B_HYST.
        :rtype: int
        """
        self.read_CS_B_HYST()
        return self._BITFIELD['RSVD_7_CS_B_HYST']

    def set_HYST_CS_B(self, value):
        """
        Writes the HYST_CS_B bitfield in the CS_B_HYST register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_HYST()
        self._BITFIELD['HYST_CS_B'] = value
        self.write_CS_B_HYST()

    def get_HYST_CS_B(self):
        """
        Reads the CS_B_HYST register
        
        :return: the shadow register HYST_CS_B.
        :rtype: int
        """
        self.read_CS_B_HYST()
        return self._BITFIELD['HYST_CS_B']

    def set_RSVD_7_5_LT_HYST(self, value):
        """
         Read Only bit field RSVD_7_5_LT_HYST in the LT_HYST register. Skip the write.
        """

    def get_RSVD_7_5_LT_HYST(self):
        """
        Reads the LT_HYST register
        
        :return: the shadow register RSVD_7_5_LT_HYST.
        :rtype: int
        """
        self.read_LT_HYST()
        return self._BITFIELD['RSVD_7_5_LT_HYST']

    def set_HYST_LT(self, value):
        """
        Writes the HYST_LT bitfield in the LT_HYST register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_HYST()
        self._BITFIELD['HYST_LT'] = value
        self.write_LT_HYST()

    def get_HYST_LT(self):
        """
        Reads the LT_HYST register
        
        :return: the shadow register HYST_LT.
        :rtype: int
        """
        self.read_LT_HYST()
        return self._BITFIELD['HYST_LT']

    def set_RSVD_7_5_RT_HYST(self, value):
        """
         Read Only bit field RSVD_7_5_RT_HYST in the RT_HYST register. Skip the write.
        """

    def get_RSVD_7_5_RT_HYST(self):
        """
        Reads the RT_HYST register
        
        :return: the shadow register RSVD_7_5_RT_HYST.
        :rtype: int
        """
        self.read_RT_HYST()
        return self._BITFIELD['RSVD_7_5_RT_HYST']

    def set_HYST_RT(self, value):
        """
        Writes the HYST_RT bitfield in the RT_HYST register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_RT_HYST()
        self._BITFIELD['HYST_RT'] = value
        self.write_RT_HYST()

    def get_HYST_RT(self):
        """
        Reads the RT_HYST register
        
        :return: the shadow register HYST_RT.
        :rtype: int
        """
        self.read_RT_HYST()
        return self._BITFIELD['HYST_RT']

    def set_CLR_B7(self, value):
        """
        Writes the CLR_B7 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_B7'] = value
        self.write_DAC_CLR()

    def get_CLR_B7(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_B7.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_B7']

    def set_CLR_B6(self, value):
        """
        Writes the CLR_B6 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_B6'] = value
        self.write_DAC_CLR()

    def get_CLR_B6(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_B6.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_B6']

    def set_CLR_B5(self, value):
        """
        Writes the CLR_B5 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_B5'] = value
        self.write_DAC_CLR()

    def get_CLR_B5(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_B5.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_B5']

    def set_CLR_B4(self, value):
        """
        Writes the CLR_B4 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_B4'] = value
        self.write_DAC_CLR()

    def get_CLR_B4(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_B4.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_B4']

    def set_CLR_A3(self, value):
        """
        Writes the CLR_A3 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_A3'] = value
        self.write_DAC_CLR()

    def get_CLR_A3(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_A3.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_A3']

    def set_CLR_A2(self, value):
        """
        Writes the CLR_A2 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_A2'] = value
        self.write_DAC_CLR()

    def get_CLR_A2(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_A2.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_A2']

    def set_CLR_A1(self, value):
        """
        Writes the CLR_A1 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_A1'] = value
        self.write_DAC_CLR()

    def get_CLR_A1(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_A1.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_A1']

    def set_CLR_A0(self, value):
        """
        Writes the CLR_A0 bitfield in the DAC_CLR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_CLR()
        self._BITFIELD['CLR_A0'] = value
        self.write_DAC_CLR()

    def get_CLR_A0(self):
        """
        Reads the DAC_CLR register
        
        :return: the shadow register CLR_A0.
        :rtype: int
        """
        self.read_DAC_CLR()
        return self._BITFIELD['CLR_A0']

    def set_PDAC_B7(self, value):
        """
        Writes the PDAC_B7 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_B7'] = value
        self.write_PD_DAC()

    def get_PDAC_B7(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_B7.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_B7']

    def set_PDAC_B6(self, value):
        """
        Writes the PDAC_B6 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_B6'] = value
        self.write_PD_DAC()

    def get_PDAC_B6(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_B6.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_B6']

    def set_PDAC_B5(self, value):
        """
        Writes the PDAC_B5 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_B5'] = value
        self.write_PD_DAC()

    def get_PDAC_B5(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_B5.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_B5']

    def set_PDAC_B4(self, value):
        """
        Writes the PDAC_B4 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_B4'] = value
        self.write_PD_DAC()

    def get_PDAC_B4(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_B4.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_B4']

    def set_PDAC_A3(self, value):
        """
        Writes the PDAC_A3 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_A3'] = value
        self.write_PD_DAC()

    def get_PDAC_A3(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_A3.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_A3']

    def set_PDAC_A2(self, value):
        """
        Writes the PDAC_A2 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_A2'] = value
        self.write_PD_DAC()

    def get_PDAC_A2(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_A2.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_A2']

    def set_PDAC_A1(self, value):
        """
        Writes the PDAC_A1 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_A1'] = value
        self.write_PD_DAC()

    def get_PDAC_A1(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_A1.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_A1']

    def set_PDAC_A0(self, value):
        """
        Writes the PDAC_A0 bitfield in the PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC()
        self._BITFIELD['PDAC_A0'] = value
        self.write_PD_DAC()

    def get_PDAC_A0(self):
        """
        Reads the PD_DAC register
        
        :return: the shadow register PDAC_A0.
        :rtype: int
        """
        self.read_PD_DAC()
        return self._BITFIELD['PDAC_A0']

    def set_RSVD_7_1_PD_ADC(self, value):
        """
         Read Only bit field RSVD_7_1_PD_ADC in the PD_ADC register. Skip the write.
        """

    def get_RSVD_7_1_PD_ADC(self):
        """
        Reads the PD_ADC register
        
        :return: the shadow register RSVD_7_1_PD_ADC.
        :rtype: int
        """
        self.read_PD_ADC()
        return self._BITFIELD['RSVD_7_1_PD_ADC']

    def set_PADC(self, value):
        """
        Writes the PADC bitfield in the PD_ADC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_ADC()
        self._BITFIELD['PADC'] = value
        self.write_PD_ADC()

    def get_PADC(self):
        """
        Reads the PD_ADC register
        
        :return: the shadow register PADC.
        :rtype: int
        """
        self.read_PD_ADC()
        return self._BITFIELD['PADC']

    def set_RSVD_7_2_PD_CS(self, value):
        """
         Read Only bit field RSVD_7_2_PD_CS in the PD_CS register. Skip the write.
        """

    def get_RSVD_7_2_PD_CS(self):
        """
        Reads the PD_CS register
        
        :return: the shadow register RSVD_7_2_PD_CS.
        :rtype: int
        """
        self.read_PD_CS()
        return self._BITFIELD['RSVD_7_2_PD_CS']

    def set_PCS_B(self, value):
        """
        Writes the PCS_B bitfield in the PD_CS register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_CS()
        self._BITFIELD['PCS_B'] = value
        self.write_PD_CS()

    def get_PCS_B(self):
        """
        Reads the PD_CS register
        
        :return: the shadow register PCS_B.
        :rtype: int
        """
        self.read_PD_CS()
        return self._BITFIELD['PCS_B']

    def set_PCS_A(self, value):
        """
        Writes the PCS_A bitfield in the PD_CS register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_CS()
        self._BITFIELD['PCS_A'] = value
        self.write_PD_CS()

    def get_PCS_A(self):
        """
        Reads the PD_CS register
        
        :return: the shadow register PCS_A.
        :rtype: int
        """
        self.read_PD_CS()
        return self._BITFIELD['PCS_A']

    def set_RSVD_7_1_ADC_TRIG(self, value):
        """
         Read Only bit field RSVD_7_1_ADC_TRIG in the ADC_TRIG register. Skip the write.
        """

    def get_RSVD_7_1_ADC_TRIG(self):
        """
        Reads the ADC_TRIG register
        
        :return: the shadow register RSVD_7_1_ADC_TRIG.
        :rtype: int
        """
        self.read_ADC_TRIG()
        return self._BITFIELD['RSVD_7_1_ADC_TRIG']

    def set_ICONV(self, value):
        """
        Writes the ICONV bitfield in the ADC_TRIG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TRIG()
        self._BITFIELD['ICONV'] = value
        self.write_ADC_TRIG()

    def get_ICONV(self):
        """
        Reads the ADC_TRIG register
        
        :return: the shadow register ICONV.
        :rtype: int
        """
        self.read_ADC_TRIG()
        return self._BITFIELD['ICONV']

    def set_DAC0_GAIN_CAL_R00(self, value):
        """
        Writes the DAC0_GAIN_CAL_R00 bitfield in the DAC0_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC0_GAIN_CAL_R00()
        self._BITFIELD['DAC0_GAIN_CAL_R00'] = value
        self.write_DAC0_GAIN_CAL_R00()

    def get_DAC0_GAIN_CAL_R00(self):
        """
        Reads the DAC0_GAIN_CAL_R00 register
        
        :return: the shadow register DAC0_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC0_GAIN_CAL_R00()
        return self._BITFIELD['DAC0_GAIN_CAL_R00']

    def set_DAC1_GAIN_CAL_R00(self, value):
        """
        Writes the DAC1_GAIN_CAL_R00 bitfield in the DAC1_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC1_GAIN_CAL_R00()
        self._BITFIELD['DAC1_GAIN_CAL_R00'] = value
        self.write_DAC1_GAIN_CAL_R00()

    def get_DAC1_GAIN_CAL_R00(self):
        """
        Reads the DAC1_GAIN_CAL_R00 register
        
        :return: the shadow register DAC1_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC1_GAIN_CAL_R00()
        return self._BITFIELD['DAC1_GAIN_CAL_R00']

    def set_DAC2_GAIN_CAL_R00(self, value):
        """
        Writes the DAC2_GAIN_CAL_R00 bitfield in the DAC2_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC2_GAIN_CAL_R00()
        self._BITFIELD['DAC2_GAIN_CAL_R00'] = value
        self.write_DAC2_GAIN_CAL_R00()

    def get_DAC2_GAIN_CAL_R00(self):
        """
        Reads the DAC2_GAIN_CAL_R00 register
        
        :return: the shadow register DAC2_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC2_GAIN_CAL_R00()
        return self._BITFIELD['DAC2_GAIN_CAL_R00']

    def set_DAC3_GAIN_CAL_R00(self, value):
        """
        Writes the DAC3_GAIN_CAL_R00 bitfield in the DAC3_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC3_GAIN_CAL_R00()
        self._BITFIELD['DAC3_GAIN_CAL_R00'] = value
        self.write_DAC3_GAIN_CAL_R00()

    def get_DAC3_GAIN_CAL_R00(self):
        """
        Reads the DAC3_GAIN_CAL_R00 register
        
        :return: the shadow register DAC3_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC3_GAIN_CAL_R00()
        return self._BITFIELD['DAC3_GAIN_CAL_R00']

    def set_DAC4_GAIN_CAL_R00(self, value):
        """
        Writes the DAC4_GAIN_CAL_R00 bitfield in the DAC4_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC4_GAIN_CAL_R00()
        self._BITFIELD['DAC4_GAIN_CAL_R00'] = value
        self.write_DAC4_GAIN_CAL_R00()

    def get_DAC4_GAIN_CAL_R00(self):
        """
        Reads the DAC4_GAIN_CAL_R00 register
        
        :return: the shadow register DAC4_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC4_GAIN_CAL_R00()
        return self._BITFIELD['DAC4_GAIN_CAL_R00']

    def set_DAC5_GAIN_CAL_R00(self, value):
        """
        Writes the DAC5_GAIN_CAL_R00 bitfield in the DAC5_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC5_GAIN_CAL_R00()
        self._BITFIELD['DAC5_GAIN_CAL_R00'] = value
        self.write_DAC5_GAIN_CAL_R00()

    def get_DAC5_GAIN_CAL_R00(self):
        """
        Reads the DAC5_GAIN_CAL_R00 register
        
        :return: the shadow register DAC5_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC5_GAIN_CAL_R00()
        return self._BITFIELD['DAC5_GAIN_CAL_R00']

    def set_DAC6_GAIN_CAL_R00(self, value):
        """
        Writes the DAC6_GAIN_CAL_R00 bitfield in the DAC6_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC6_GAIN_CAL_R00()
        self._BITFIELD['DAC6_GAIN_CAL_R00'] = value
        self.write_DAC6_GAIN_CAL_R00()

    def get_DAC6_GAIN_CAL_R00(self):
        """
        Reads the DAC6_GAIN_CAL_R00 register
        
        :return: the shadow register DAC6_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC6_GAIN_CAL_R00()
        return self._BITFIELD['DAC6_GAIN_CAL_R00']

    def set_DAC7_GAIN_CAL_R00(self, value):
        """
        Writes the DAC7_GAIN_CAL_R00 bitfield in the DAC7_GAIN_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC7_GAIN_CAL_R00()
        self._BITFIELD['DAC7_GAIN_CAL_R00'] = value
        self.write_DAC7_GAIN_CAL_R00()

    def get_DAC7_GAIN_CAL_R00(self):
        """
        Reads the DAC7_GAIN_CAL_R00 register
        
        :return: the shadow register DAC7_GAIN_CAL_R00.
        :rtype: int
        """
        self.read_DAC7_GAIN_CAL_R00()
        return self._BITFIELD['DAC7_GAIN_CAL_R00']

    def set_DAC0_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC0_OFFSET_CAL_R00 bitfield in the DAC0_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC0_OFFSET_CAL_R00()
        self._BITFIELD['DAC0_OFFSET_CAL_R00'] = value
        self.write_DAC0_OFFSET_CAL_R00()

    def get_DAC0_OFFSET_CAL_R00(self):
        """
        Reads the DAC0_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC0_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC0_OFFSET_CAL_R00()
        return self._BITFIELD['DAC0_OFFSET_CAL_R00']

    def set_DAC1_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC1_OFFSET_CAL_R00 bitfield in the DAC1_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC1_OFFSET_CAL_R00()
        self._BITFIELD['DAC1_OFFSET_CAL_R00'] = value
        self.write_DAC1_OFFSET_CAL_R00()

    def get_DAC1_OFFSET_CAL_R00(self):
        """
        Reads the DAC1_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC1_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC1_OFFSET_CAL_R00()
        return self._BITFIELD['DAC1_OFFSET_CAL_R00']

    def set_DAC2_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC2_OFFSET_CAL_R00 bitfield in the DAC2_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC2_OFFSET_CAL_R00()
        self._BITFIELD['DAC2_OFFSET_CAL_R00'] = value
        self.write_DAC2_OFFSET_CAL_R00()

    def get_DAC2_OFFSET_CAL_R00(self):
        """
        Reads the DAC2_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC2_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC2_OFFSET_CAL_R00()
        return self._BITFIELD['DAC2_OFFSET_CAL_R00']

    def set_DAC3_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC3_OFFSET_CAL_R00 bitfield in the DAC3_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC3_OFFSET_CAL_R00()
        self._BITFIELD['DAC3_OFFSET_CAL_R00'] = value
        self.write_DAC3_OFFSET_CAL_R00()

    def get_DAC3_OFFSET_CAL_R00(self):
        """
        Reads the DAC3_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC3_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC3_OFFSET_CAL_R00()
        return self._BITFIELD['DAC3_OFFSET_CAL_R00']

    def set_DAC4_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC4_OFFSET_CAL_R00 bitfield in the DAC4_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC4_OFFSET_CAL_R00()
        self._BITFIELD['DAC4_OFFSET_CAL_R00'] = value
        self.write_DAC4_OFFSET_CAL_R00()

    def get_DAC4_OFFSET_CAL_R00(self):
        """
        Reads the DAC4_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC4_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC4_OFFSET_CAL_R00()
        return self._BITFIELD['DAC4_OFFSET_CAL_R00']

    def set_DAC5_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC5_OFFSET_CAL_R00 bitfield in the DAC5_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC5_OFFSET_CAL_R00()
        self._BITFIELD['DAC5_OFFSET_CAL_R00'] = value
        self.write_DAC5_OFFSET_CAL_R00()

    def get_DAC5_OFFSET_CAL_R00(self):
        """
        Reads the DAC5_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC5_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC5_OFFSET_CAL_R00()
        return self._BITFIELD['DAC5_OFFSET_CAL_R00']

    def set_DAC6_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC6_OFFSET_CAL_R00 bitfield in the DAC6_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC6_OFFSET_CAL_R00()
        self._BITFIELD['DAC6_OFFSET_CAL_R00'] = value
        self.write_DAC6_OFFSET_CAL_R00()

    def get_DAC6_OFFSET_CAL_R00(self):
        """
        Reads the DAC6_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC6_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC6_OFFSET_CAL_R00()
        return self._BITFIELD['DAC6_OFFSET_CAL_R00']

    def set_DAC7_OFFSET_CAL_R00(self, value):
        """
        Writes the DAC7_OFFSET_CAL_R00 bitfield in the DAC7_OFFSET_CAL_R00 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC7_OFFSET_CAL_R00()
        self._BITFIELD['DAC7_OFFSET_CAL_R00'] = value
        self.write_DAC7_OFFSET_CAL_R00()

    def get_DAC7_OFFSET_CAL_R00(self):
        """
        Reads the DAC7_OFFSET_CAL_R00 register
        
        :return: the shadow register DAC7_OFFSET_CAL_R00.
        :rtype: int
        """
        self.read_DAC7_OFFSET_CAL_R00()
        return self._BITFIELD['DAC7_OFFSET_CAL_R00']

    def set_DAC0_GAIN_CAL_R11(self, value):
        """
        Writes the DAC0_GAIN_CAL_R11 bitfield in the DAC0_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC0_GAIN_CAL_R11()
        self._BITFIELD['DAC0_GAIN_CAL_R11'] = value
        self.write_DAC0_GAIN_CAL_R11()

    def get_DAC0_GAIN_CAL_R11(self):
        """
        Reads the DAC0_GAIN_CAL_R11 register
        
        :return: the shadow register DAC0_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC0_GAIN_CAL_R11()
        return self._BITFIELD['DAC0_GAIN_CAL_R11']

    def set_DAC1_GAIN_CAL_R11(self, value):
        """
        Writes the DAC1_GAIN_CAL_R11 bitfield in the DAC1_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC1_GAIN_CAL_R11()
        self._BITFIELD['DAC1_GAIN_CAL_R11'] = value
        self.write_DAC1_GAIN_CAL_R11()

    def get_DAC1_GAIN_CAL_R11(self):
        """
        Reads the DAC1_GAIN_CAL_R11 register
        
        :return: the shadow register DAC1_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC1_GAIN_CAL_R11()
        return self._BITFIELD['DAC1_GAIN_CAL_R11']

    def set_DAC2_GAIN_CAL_R11(self, value):
        """
        Writes the DAC2_GAIN_CAL_R11 bitfield in the DAC2_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC2_GAIN_CAL_R11()
        self._BITFIELD['DAC2_GAIN_CAL_R11'] = value
        self.write_DAC2_GAIN_CAL_R11()

    def get_DAC2_GAIN_CAL_R11(self):
        """
        Reads the DAC2_GAIN_CAL_R11 register
        
        :return: the shadow register DAC2_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC2_GAIN_CAL_R11()
        return self._BITFIELD['DAC2_GAIN_CAL_R11']

    def set_DAC3_GAIN_CAL_R11(self, value):
        """
        Writes the DAC3_GAIN_CAL_R11 bitfield in the DAC3_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC3_GAIN_CAL_R11()
        self._BITFIELD['DAC3_GAIN_CAL_R11'] = value
        self.write_DAC3_GAIN_CAL_R11()

    def get_DAC3_GAIN_CAL_R11(self):
        """
        Reads the DAC3_GAIN_CAL_R11 register
        
        :return: the shadow register DAC3_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC3_GAIN_CAL_R11()
        return self._BITFIELD['DAC3_GAIN_CAL_R11']

    def set_DAC4_GAIN_CAL_R11(self, value):
        """
        Writes the DAC4_GAIN_CAL_R11 bitfield in the DAC4_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC4_GAIN_CAL_R11()
        self._BITFIELD['DAC4_GAIN_CAL_R11'] = value
        self.write_DAC4_GAIN_CAL_R11()

    def get_DAC4_GAIN_CAL_R11(self):
        """
        Reads the DAC4_GAIN_CAL_R11 register
        
        :return: the shadow register DAC4_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC4_GAIN_CAL_R11()
        return self._BITFIELD['DAC4_GAIN_CAL_R11']

    def set_DAC5_GAIN_CAL_R11(self, value):
        """
        Writes the DAC5_GAIN_CAL_R11 bitfield in the DAC5_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC5_GAIN_CAL_R11()
        self._BITFIELD['DAC5_GAIN_CAL_R11'] = value
        self.write_DAC5_GAIN_CAL_R11()

    def get_DAC5_GAIN_CAL_R11(self):
        """
        Reads the DAC5_GAIN_CAL_R11 register
        
        :return: the shadow register DAC5_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC5_GAIN_CAL_R11()
        return self._BITFIELD['DAC5_GAIN_CAL_R11']

    def set_DAC6_GAIN_CAL_R11(self, value):
        """
        Writes the DAC6_GAIN_CAL_R11 bitfield in the DAC6_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC6_GAIN_CAL_R11()
        self._BITFIELD['DAC6_GAIN_CAL_R11'] = value
        self.write_DAC6_GAIN_CAL_R11()

    def get_DAC6_GAIN_CAL_R11(self):
        """
        Reads the DAC6_GAIN_CAL_R11 register
        
        :return: the shadow register DAC6_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC6_GAIN_CAL_R11()
        return self._BITFIELD['DAC6_GAIN_CAL_R11']

    def set_DAC7_GAIN_CAL_R11(self, value):
        """
        Writes the DAC7_GAIN_CAL_R11 bitfield in the DAC7_GAIN_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC7_GAIN_CAL_R11()
        self._BITFIELD['DAC7_GAIN_CAL_R11'] = value
        self.write_DAC7_GAIN_CAL_R11()

    def get_DAC7_GAIN_CAL_R11(self):
        """
        Reads the DAC7_GAIN_CAL_R11 register
        
        :return: the shadow register DAC7_GAIN_CAL_R11.
        :rtype: int
        """
        self.read_DAC7_GAIN_CAL_R11()
        return self._BITFIELD['DAC7_GAIN_CAL_R11']

    def set_DAC0_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC0_OFFSET_CAL_R11 bitfield in the DAC0_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC0_OFFSET_CAL_R11()
        self._BITFIELD['DAC0_OFFSET_CAL_R11'] = value
        self.write_DAC0_OFFSET_CAL_R11()

    def get_DAC0_OFFSET_CAL_R11(self):
        """
        Reads the DAC0_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC0_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC0_OFFSET_CAL_R11()
        return self._BITFIELD['DAC0_OFFSET_CAL_R11']

    def set_DAC1_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC1_OFFSET_CAL_R11 bitfield in the DAC1_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC1_OFFSET_CAL_R11()
        self._BITFIELD['DAC1_OFFSET_CAL_R11'] = value
        self.write_DAC1_OFFSET_CAL_R11()

    def get_DAC1_OFFSET_CAL_R11(self):
        """
        Reads the DAC1_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC1_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC1_OFFSET_CAL_R11()
        return self._BITFIELD['DAC1_OFFSET_CAL_R11']

    def set_DAC2_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC2_OFFSET_CAL_R11 bitfield in the DAC2_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC2_OFFSET_CAL_R11()
        self._BITFIELD['DAC2_OFFSET_CAL_R11'] = value
        self.write_DAC2_OFFSET_CAL_R11()

    def get_DAC2_OFFSET_CAL_R11(self):
        """
        Reads the DAC2_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC2_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC2_OFFSET_CAL_R11()
        return self._BITFIELD['DAC2_OFFSET_CAL_R11']

    def set_DAC3_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC3_OFFSET_CAL_R11 bitfield in the DAC3_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC3_OFFSET_CAL_R11()
        self._BITFIELD['DAC3_OFFSET_CAL_R11'] = value
        self.write_DAC3_OFFSET_CAL_R11()

    def get_DAC3_OFFSET_CAL_R11(self):
        """
        Reads the DAC3_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC3_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC3_OFFSET_CAL_R11()
        return self._BITFIELD['DAC3_OFFSET_CAL_R11']

    def set_DAC4_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC4_OFFSET_CAL_R11 bitfield in the DAC4_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC4_OFFSET_CAL_R11()
        self._BITFIELD['DAC4_OFFSET_CAL_R11'] = value
        self.write_DAC4_OFFSET_CAL_R11()

    def get_DAC4_OFFSET_CAL_R11(self):
        """
        Reads the DAC4_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC4_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC4_OFFSET_CAL_R11()
        return self._BITFIELD['DAC4_OFFSET_CAL_R11']

    def set_DAC5_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC5_OFFSET_CAL_R11 bitfield in the DAC5_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC5_OFFSET_CAL_R11()
        self._BITFIELD['DAC5_OFFSET_CAL_R11'] = value
        self.write_DAC5_OFFSET_CAL_R11()

    def get_DAC5_OFFSET_CAL_R11(self):
        """
        Reads the DAC5_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC5_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC5_OFFSET_CAL_R11()
        return self._BITFIELD['DAC5_OFFSET_CAL_R11']

    def set_DAC6_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC6_OFFSET_CAL_R11 bitfield in the DAC6_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC6_OFFSET_CAL_R11()
        self._BITFIELD['DAC6_OFFSET_CAL_R11'] = value
        self.write_DAC6_OFFSET_CAL_R11()

    def get_DAC6_OFFSET_CAL_R11(self):
        """
        Reads the DAC6_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC6_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC6_OFFSET_CAL_R11()
        return self._BITFIELD['DAC6_OFFSET_CAL_R11']

    def set_DAC7_OFFSET_CAL_R11(self, value):
        """
        Writes the DAC7_OFFSET_CAL_R11 bitfield in the DAC7_OFFSET_CAL_R11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC7_OFFSET_CAL_R11()
        self._BITFIELD['DAC7_OFFSET_CAL_R11'] = value
        self.write_DAC7_OFFSET_CAL_R11()

    def get_DAC7_OFFSET_CAL_R11(self):
        """
        Reads the DAC7_OFFSET_CAL_R11 register
        
        :return: the shadow register DAC7_OFFSET_CAL_R11.
        :rtype: int
        """
        self.read_DAC7_OFFSET_CAL_R11()
        return self._BITFIELD['DAC7_OFFSET_CAL_R11']

    def set_TRIM_OSC(self, value):
        """
        Writes the TRIM_OSC bitfield in the TRIM_OSC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_TRIM_OSC()
        self._BITFIELD['TRIM_OSC'] = value
        self.write_TRIM_OSC()

    def get_TRIM_OSC(self):
        """
        Reads the TRIM_OSC register
        
        :return: the shadow register TRIM_OSC.
        :rtype: int
        """
        self.read_TRIM_OSC()
        return self._BITFIELD['TRIM_OSC']

    def set_TRIM_BG(self, value):
        """
        Writes the TRIM_BG bitfield in the TRIM_BG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_TRIM_BG()
        self._BITFIELD['TRIM_BG'] = value
        self.write_TRIM_BG()

    def get_TRIM_BG(self):
        """
        Reads the TRIM_BG register
        
        :return: the shadow register TRIM_BG.
        :rtype: int
        """
        self.read_TRIM_BG()
        return self._BITFIELD['TRIM_BG']

    def set_SPIKE_FILTER_CAL_SCL(self, value):
        """
        Writes the SPIKE_FILTER_CAL_SCL bitfield in the SPIKE_FILTER_CAL_SCL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_SPIKE_FILTER_CAL_SCL()
        self._BITFIELD['SPIKE_FILTER_CAL_SCL'] = value
        self.write_SPIKE_FILTER_CAL_SCL()

    def get_SPIKE_FILTER_CAL_SCL(self):
        """
        Reads the SPIKE_FILTER_CAL_SCL register
        
        :return: the shadow register SPIKE_FILTER_CAL_SCL.
        :rtype: int
        """
        self.read_SPIKE_FILTER_CAL_SCL()
        return self._BITFIELD['SPIKE_FILTER_CAL_SCL']

    def set_SPIKE_FILTER_CAL_SDA(self, value):
        """
        Writes the SPIKE_FILTER_CAL_SDA bitfield in the SPIKE_FILTER_CAL_SDA register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_SPIKE_FILTER_CAL_SDA()
        self._BITFIELD['SPIKE_FILTER_CAL_SDA'] = value
        self.write_SPIKE_FILTER_CAL_SDA()

    def get_SPIKE_FILTER_CAL_SDA(self):
        """
        Reads the SPIKE_FILTER_CAL_SDA register
        
        :return: the shadow register SPIKE_FILTER_CAL_SDA.
        :rtype: int
        """
        self.read_SPIKE_FILTER_CAL_SDA()
        return self._BITFIELD['SPIKE_FILTER_CAL_SDA']

    def set_ADC_TRIM_REFBUF(self, value):
        """
        Writes the ADC_TRIM_REFBUF bitfield in the ADC_TRIM_REFBUF register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TRIM_REFBUF()
        self._BITFIELD['ADC_TRIM_REFBUF'] = value
        self.write_ADC_TRIM_REFBUF()

    def get_ADC_TRIM_REFBUF(self):
        """
        Reads the ADC_TRIM_REFBUF register
        
        :return: the shadow register ADC_TRIM_REFBUF.
        :rtype: int
        """
        self.read_ADC_TRIM_REFBUF()
        return self._BITFIELD['ADC_TRIM_REFBUF']

    def set_ADC_TRIM_VCM(self, value):
        """
        Writes the ADC_TRIM_VCM bitfield in the ADC_TRIM_VCM register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TRIM_VCM()
        self._BITFIELD['ADC_TRIM_VCM'] = value
        self.write_ADC_TRIM_VCM()

    def get_ADC_TRIM_VCM(self):
        """
        Reads the ADC_TRIM_VCM register
        
        :return: the shadow register ADC_TRIM_VCM.
        :rtype: int
        """
        self.read_ADC_TRIM_VCM()
        return self._BITFIELD['ADC_TRIM_VCM']

    def set_ADC_TRIM_LDO(self, value):
        """
        Writes the ADC_TRIM_LDO bitfield in the ADC_TRIM_LDO register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TRIM_LDO()
        self._BITFIELD['ADC_TRIM_LDO'] = value
        self.write_ADC_TRIM_LDO()

    def get_ADC_TRIM_LDO(self):
        """
        Reads the ADC_TRIM_LDO register
        
        :return: the shadow register ADC_TRIM_LDO.
        :rtype: int
        """
        self.read_ADC_TRIM_LDO()
        return self._BITFIELD['ADC_TRIM_LDO']

    def set_PD_DAC(self, value):
        """
        Writes the PD_DAC bitfield in the E2P_PD_DAC register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_E2P_PD_DAC()
        self._BITFIELD['PD_DAC'] = value
        self.write_E2P_PD_DAC()

    def get_PD_DAC(self):
        """
        Reads the E2P_PD_DAC register
        
        :return: the shadow register PD_DAC.
        :rtype: int
        """
        self.read_E2P_PD_DAC()
        return self._BITFIELD['PD_DAC']

    def set_RSVD_7_3_PD_DAC_CFG(self, value):
        """
        Writes the RSVD_7_3_PD_DAC_CFG bitfield in the PD_DAC_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC_CFG()
        self._BITFIELD['RSVD_7_3_PD_DAC_CFG'] = value
        self.write_PD_DAC_CFG()

    def get_RSVD_7_3_PD_DAC_CFG(self):
        """
        Reads the PD_DAC_CFG register
        
        :return: the shadow register RSVD_7_3_PD_DAC_CFG.
        :rtype: int
        """
        self.read_PD_DAC_CFG()
        return self._BITFIELD['RSVD_7_3_PD_DAC_CFG']

    def set_TIM_DAC_DEL_EN(self, value):
        """
        Writes the TIM_DAC_DEL_EN bitfield in the PD_DAC_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC_CFG()
        self._BITFIELD['TIM_DAC_DEL_EN'] = value
        self.write_PD_DAC_CFG()

    def get_TIM_DAC_DEL_EN(self):
        """
        Reads the PD_DAC_CFG register
        
        :return: the shadow register TIM_DAC_DEL_EN.
        :rtype: int
        """
        self.read_PD_DAC_CFG()
        return self._BITFIELD['TIM_DAC_DEL_EN']

    def set_TIM_DAC_DEL(self, value):
        """
        Writes the TIM_DAC_DEL bitfield in the PD_DAC_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_PD_DAC_CFG()
        self._BITFIELD['TIM_DAC_DEL'] = value
        self.write_PD_DAC_CFG()

    def get_TIM_DAC_DEL(self):
        """
        Reads the PD_DAC_CFG register
        
        :return: the shadow register TIM_DAC_DEL.
        :rtype: int
        """
        self.read_PD_DAC_CFG()
        return self._BITFIELD['TIM_DAC_DEL']

    def set_CS_A_GAIN_ERROR_SIGN(self, value):
        """
        Writes the CS_A_GAIN_ERROR_SIGN bitfield in the CS_A_GAIN_ERROR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_GAIN_ERROR()
        self._BITFIELD['CS_A_GAIN_ERROR_SIGN'] = value
        self.write_CS_A_GAIN_ERROR()

    def get_CS_A_GAIN_ERROR_SIGN(self):
        """
        Reads the CS_A_GAIN_ERROR register
        
        :return: the shadow register CS_A_GAIN_ERROR_SIGN.
        :rtype: int
        """
        self.read_CS_A_GAIN_ERROR()
        return self._BITFIELD['CS_A_GAIN_ERROR_SIGN']

    def set_GAIN_ERROR_CS_A_GAIN_ERROR(self, value):
        """
        Writes the GAIN_ERROR_CS_A_GAIN_ERROR bitfield in the CS_A_GAIN_ERROR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_GAIN_ERROR()
        self._BITFIELD['GAIN_ERROR_CS_A_GAIN_ERROR'] = value
        self.write_CS_A_GAIN_ERROR()

    def get_GAIN_ERROR_CS_A_GAIN_ERROR(self):
        """
        Reads the CS_A_GAIN_ERROR register
        
        :return: the shadow register GAIN_ERROR_CS_A_GAIN_ERROR.
        :rtype: int
        """
        self.read_CS_A_GAIN_ERROR()
        return self._BITFIELD['GAIN_ERROR_CS_A_GAIN_ERROR']

    def set_CS_B_GAIN_ERROR_SIGN(self, value):
        """
        Writes the CS_B_GAIN_ERROR_SIGN bitfield in the CS_B_GAIN_ERROR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_GAIN_ERROR()
        self._BITFIELD['CS_B_GAIN_ERROR_SIGN'] = value
        self.write_CS_B_GAIN_ERROR()

    def get_CS_B_GAIN_ERROR_SIGN(self):
        """
        Reads the CS_B_GAIN_ERROR register
        
        :return: the shadow register CS_B_GAIN_ERROR_SIGN.
        :rtype: int
        """
        self.read_CS_B_GAIN_ERROR()
        return self._BITFIELD['CS_B_GAIN_ERROR_SIGN']

    def set_GAIN_ERROR_CS_B_GAIN_ERROR(self, value):
        """
        Writes the GAIN_ERROR_CS_B_GAIN_ERROR bitfield in the CS_B_GAIN_ERROR register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_GAIN_ERROR()
        self._BITFIELD['GAIN_ERROR_CS_B_GAIN_ERROR'] = value
        self.write_CS_B_GAIN_ERROR()

    def get_GAIN_ERROR_CS_B_GAIN_ERROR(self):
        """
        Reads the CS_B_GAIN_ERROR register
        
        :return: the shadow register GAIN_ERROR_CS_B_GAIN_ERROR.
        :rtype: int
        """
        self.read_CS_B_GAIN_ERROR()
        return self._BITFIELD['GAIN_ERROR_CS_B_GAIN_ERROR']

    def set_RSVD_7_6_CS_A_LUT0_OFFSET(self, value):
        """
        Writes the RSVD_7_6_CS_A_LUT0_OFFSET bitfield in the CS_A_LUT0_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_LUT0_OFFSET()
        self._BITFIELD['RSVD_7_6_CS_A_LUT0_OFFSET'] = value
        self.write_CS_A_LUT0_OFFSET()

    def get_RSVD_7_6_CS_A_LUT0_OFFSET(self):
        """
        Reads the CS_A_LUT0_OFFSET register
        
        :return: the shadow register RSVD_7_6_CS_A_LUT0_OFFSET.
        :rtype: int
        """
        self.read_CS_A_LUT0_OFFSET()
        return self._BITFIELD['RSVD_7_6_CS_A_LUT0_OFFSET']

    def set_CS_A_LUT0_OFFSET_LUT0_OFFSET(self, value):
        """
        Writes the CS_A_LUT0_OFFSET_LUT0_OFFSET bitfield in the CS_A_LUT0_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_LUT0_OFFSET()
        self._BITFIELD['CS_A_LUT0_OFFSET_LUT0_OFFSET'] = value
        self.write_CS_A_LUT0_OFFSET()

    def get_CS_A_LUT0_OFFSET_LUT0_OFFSET(self):
        """
        Reads the CS_A_LUT0_OFFSET register
        
        :return: the shadow register CS_A_LUT0_OFFSET_LUT0_OFFSET.
        :rtype: int
        """
        self.read_CS_A_LUT0_OFFSET()
        return self._BITFIELD['CS_A_LUT0_OFFSET_LUT0_OFFSET']

    def set_RSVD_7_6_CS_A_LUT1_OFFSET(self, value):
        """
        Writes the RSVD_7_6_CS_A_LUT1_OFFSET bitfield in the CS_A_LUT1_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_LUT1_OFFSET()
        self._BITFIELD['RSVD_7_6_CS_A_LUT1_OFFSET'] = value
        self.write_CS_A_LUT1_OFFSET()

    def get_RSVD_7_6_CS_A_LUT1_OFFSET(self):
        """
        Reads the CS_A_LUT1_OFFSET register
        
        :return: the shadow register RSVD_7_6_CS_A_LUT1_OFFSET.
        :rtype: int
        """
        self.read_CS_A_LUT1_OFFSET()
        return self._BITFIELD['RSVD_7_6_CS_A_LUT1_OFFSET']

    def set_CS_A_LUT1_OFFSET(self, value):
        """
        Writes the CS_A_LUT1_OFFSET bitfield in the CS_A_LUT1_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_LUT1_OFFSET()
        self._BITFIELD['CS_A_LUT1_OFFSET'] = value
        self.write_CS_A_LUT1_OFFSET()

    def get_CS_A_LUT1_OFFSET(self):
        """
        Reads the CS_A_LUT1_OFFSET register
        
        :return: the shadow register CS_A_LUT1_OFFSET.
        :rtype: int
        """
        self.read_CS_A_LUT1_OFFSET()
        return self._BITFIELD['CS_A_LUT1_OFFSET']

    def set_RSVD_7_6_CS_B_LUT0_OFFSET(self, value):
        """
        Writes the RSVD_7_6_CS_B_LUT0_OFFSET bitfield in the CS_B_LUT0_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_LUT0_OFFSET()
        self._BITFIELD['RSVD_7_6_CS_B_LUT0_OFFSET'] = value
        self.write_CS_B_LUT0_OFFSET()

    def get_RSVD_7_6_CS_B_LUT0_OFFSET(self):
        """
        Reads the CS_B_LUT0_OFFSET register
        
        :return: the shadow register RSVD_7_6_CS_B_LUT0_OFFSET.
        :rtype: int
        """
        self.read_CS_B_LUT0_OFFSET()
        return self._BITFIELD['RSVD_7_6_CS_B_LUT0_OFFSET']

    def set_CS_B_LUT0_OFFSET_LUT0_OFFSET(self, value):
        """
        Writes the CS_B_LUT0_OFFSET_LUT0_OFFSET bitfield in the CS_B_LUT0_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_LUT0_OFFSET()
        self._BITFIELD['CS_B_LUT0_OFFSET_LUT0_OFFSET'] = value
        self.write_CS_B_LUT0_OFFSET()

    def get_CS_B_LUT0_OFFSET_LUT0_OFFSET(self):
        """
        Reads the CS_B_LUT0_OFFSET register
        
        :return: the shadow register CS_B_LUT0_OFFSET_LUT0_OFFSET.
        :rtype: int
        """
        self.read_CS_B_LUT0_OFFSET()
        return self._BITFIELD['CS_B_LUT0_OFFSET_LUT0_OFFSET']

    def set_RSVD_7_6_CS_B_LUT1_OFFSET(self, value):
        """
        Writes the RSVD_7_6_CS_B_LUT1_OFFSET bitfield in the CS_B_LUT1_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_LUT1_OFFSET()
        self._BITFIELD['RSVD_7_6_CS_B_LUT1_OFFSET'] = value
        self.write_CS_B_LUT1_OFFSET()

    def get_RSVD_7_6_CS_B_LUT1_OFFSET(self):
        """
        Reads the CS_B_LUT1_OFFSET register
        
        :return: the shadow register RSVD_7_6_CS_B_LUT1_OFFSET.
        :rtype: int
        """
        self.read_CS_B_LUT1_OFFSET()
        return self._BITFIELD['RSVD_7_6_CS_B_LUT1_OFFSET']

    def set_CS_B_LUT1_OFFSET(self, value):
        """
        Writes the CS_B_LUT1_OFFSET bitfield in the CS_B_LUT1_OFFSET register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_LUT1_OFFSET()
        self._BITFIELD['CS_B_LUT1_OFFSET'] = value
        self.write_CS_B_LUT1_OFFSET()

    def get_CS_B_LUT1_OFFSET(self):
        """
        Reads the CS_B_LUT1_OFFSET register
        
        :return: the shadow register CS_B_LUT1_OFFSET.
        :rtype: int
        """
        self.read_CS_B_LUT1_OFFSET()
        return self._BITFIELD['CS_B_LUT1_OFFSET']

    def set_ADC_OFFSET_ADC_IN_CAL_SIGN(self, value):
        """
        Writes the ADC_OFFSET_ADC_IN_CAL_SIGN bitfield in the ADC_OFFSET_ADC_IN_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_ADC_IN_CAL()
        self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_SIGN'] = value
        self.write_ADC_OFFSET_ADC_IN_CAL()

    def get_ADC_OFFSET_ADC_IN_CAL_SIGN(self):
        """
        Reads the ADC_OFFSET_ADC_IN_CAL register
        
        :return: the shadow register ADC_OFFSET_ADC_IN_CAL_SIGN.
        :rtype: int
        """
        self.read_ADC_OFFSET_ADC_IN_CAL()
        return self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_SIGN']

    def set_ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE(self, value):
        """
        Writes the ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE bitfield in the ADC_OFFSET_ADC_IN_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_ADC_IN_CAL()
        self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE'] = value
        self.write_ADC_OFFSET_ADC_IN_CAL()

    def get_ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE(self):
        """
        Reads the ADC_OFFSET_ADC_IN_CAL register
        
        :return: the shadow register ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE.
        :rtype: int
        """
        self.read_ADC_OFFSET_ADC_IN_CAL()
        return self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE']

    def set_ADC_OFFSET_CS_CAL_SIGN(self, value):
        """
        Writes the ADC_OFFSET_CS_CAL_SIGN bitfield in the ADC_OFFSET_CS_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_CS_CAL()
        self._BITFIELD['ADC_OFFSET_CS_CAL_SIGN'] = value
        self.write_ADC_OFFSET_CS_CAL()

    def get_ADC_OFFSET_CS_CAL_SIGN(self):
        """
        Reads the ADC_OFFSET_CS_CAL register
        
        :return: the shadow register ADC_OFFSET_CS_CAL_SIGN.
        :rtype: int
        """
        self.read_ADC_OFFSET_CS_CAL()
        return self._BITFIELD['ADC_OFFSET_CS_CAL_SIGN']

    def set_ADC_OFFSET_CS_CAL_OFFSET_VALUE(self, value):
        """
        Writes the ADC_OFFSET_CS_CAL_OFFSET_VALUE bitfield in the ADC_OFFSET_CS_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_CS_CAL()
        self._BITFIELD['ADC_OFFSET_CS_CAL_OFFSET_VALUE'] = value
        self.write_ADC_OFFSET_CS_CAL()

    def get_ADC_OFFSET_CS_CAL_OFFSET_VALUE(self):
        """
        Reads the ADC_OFFSET_CS_CAL register
        
        :return: the shadow register ADC_OFFSET_CS_CAL_OFFSET_VALUE.
        :rtype: int
        """
        self.read_ADC_OFFSET_CS_CAL()
        return self._BITFIELD['ADC_OFFSET_CS_CAL_OFFSET_VALUE']

    def set_ADC_OFFSET_LT_CAL_SIGN(self, value):
        """
        Writes the ADC_OFFSET_LT_CAL_SIGN bitfield in the ADC_OFFSET_LT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_LT_CAL()
        self._BITFIELD['ADC_OFFSET_LT_CAL_SIGN'] = value
        self.write_ADC_OFFSET_LT_CAL()

    def get_ADC_OFFSET_LT_CAL_SIGN(self):
        """
        Reads the ADC_OFFSET_LT_CAL register
        
        :return: the shadow register ADC_OFFSET_LT_CAL_SIGN.
        :rtype: int
        """
        self.read_ADC_OFFSET_LT_CAL()
        return self._BITFIELD['ADC_OFFSET_LT_CAL_SIGN']

    def set_ADC_OFFSET_LT_CAL_OFFSET_VALUE(self, value):
        """
        Writes the ADC_OFFSET_LT_CAL_OFFSET_VALUE bitfield in the ADC_OFFSET_LT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_LT_CAL()
        self._BITFIELD['ADC_OFFSET_LT_CAL_OFFSET_VALUE'] = value
        self.write_ADC_OFFSET_LT_CAL()

    def get_ADC_OFFSET_LT_CAL_OFFSET_VALUE(self):
        """
        Reads the ADC_OFFSET_LT_CAL register
        
        :return: the shadow register ADC_OFFSET_LT_CAL_OFFSET_VALUE.
        :rtype: int
        """
        self.read_ADC_OFFSET_LT_CAL()
        return self._BITFIELD['ADC_OFFSET_LT_CAL_OFFSET_VALUE']

    def set_ADC_OFFSET_RT_CAL_SIGN(self, value):
        """
        Writes the ADC_OFFSET_RT_CAL_SIGN bitfield in the ADC_OFFSET_RT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_RT_CAL()
        self._BITFIELD['ADC_OFFSET_RT_CAL_SIGN'] = value
        self.write_ADC_OFFSET_RT_CAL()

    def get_ADC_OFFSET_RT_CAL_SIGN(self):
        """
        Reads the ADC_OFFSET_RT_CAL register
        
        :return: the shadow register ADC_OFFSET_RT_CAL_SIGN.
        :rtype: int
        """
        self.read_ADC_OFFSET_RT_CAL()
        return self._BITFIELD['ADC_OFFSET_RT_CAL_SIGN']

    def set_ADC_OFFSET_RT_CAL_OFFSET_VALUE(self, value):
        """
        Writes the ADC_OFFSET_RT_CAL_OFFSET_VALUE bitfield in the ADC_OFFSET_RT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_OFFSET_RT_CAL()
        self._BITFIELD['ADC_OFFSET_RT_CAL_OFFSET_VALUE'] = value
        self.write_ADC_OFFSET_RT_CAL()

    def get_ADC_OFFSET_RT_CAL_OFFSET_VALUE(self):
        """
        Reads the ADC_OFFSET_RT_CAL register
        
        :return: the shadow register ADC_OFFSET_RT_CAL_OFFSET_VALUE.
        :rtype: int
        """
        self.read_ADC_OFFSET_RT_CAL()
        return self._BITFIELD['ADC_OFFSET_RT_CAL_OFFSET_VALUE']

    def set_RSVD_7_ADC_CAL_CNTL(self, value):
        """
        Writes the RSVD_7_ADC_CAL_CNTL bitfield in the ADC_CAL_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CAL_CNTL()
        self._BITFIELD['RSVD_7_ADC_CAL_CNTL'] = value
        self.write_ADC_CAL_CNTL()

    def get_RSVD_7_ADC_CAL_CNTL(self):
        """
        Reads the ADC_CAL_CNTL register
        
        :return: the shadow register RSVD_7_ADC_CAL_CNTL.
        :rtype: int
        """
        self.read_ADC_CAL_CNTL()
        return self._BITFIELD['RSVD_7_ADC_CAL_CNTL']

    def set_OFFSET_EN(self, value):
        """
        Writes the OFFSET_EN bitfield in the ADC_CAL_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CAL_CNTL()
        self._BITFIELD['OFFSET_EN'] = value
        self.write_ADC_CAL_CNTL()

    def get_OFFSET_EN(self):
        """
        Reads the ADC_CAL_CNTL register
        
        :return: the shadow register OFFSET_EN.
        :rtype: int
        """
        self.read_ADC_CAL_CNTL()
        return self._BITFIELD['OFFSET_EN']

    def set_RSVD_5_3_ADC_CAL_CNTL(self, value):
        """
        Writes the RSVD_5_3_ADC_CAL_CNTL bitfield in the ADC_CAL_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CAL_CNTL()
        self._BITFIELD['RSVD_5_3_ADC_CAL_CNTL'] = value
        self.write_ADC_CAL_CNTL()

    def get_RSVD_5_3_ADC_CAL_CNTL(self):
        """
        Reads the ADC_CAL_CNTL register
        
        :return: the shadow register RSVD_5_3_ADC_CAL_CNTL.
        :rtype: int
        """
        self.read_ADC_CAL_CNTL()
        return self._BITFIELD['RSVD_5_3_ADC_CAL_CNTL']

    def set_CS_FAST_AVG_EN(self, value):
        """
        Writes the CS_FAST_AVG_EN bitfield in the ADC_CAL_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CAL_CNTL()
        self._BITFIELD['CS_FAST_AVG_EN'] = value
        self.write_ADC_CAL_CNTL()

    def get_CS_FAST_AVG_EN(self):
        """
        Reads the ADC_CAL_CNTL register
        
        :return: the shadow register CS_FAST_AVG_EN.
        :rtype: int
        """
        self.read_ADC_CAL_CNTL()
        return self._BITFIELD['CS_FAST_AVG_EN']

    def set_ADC_SAMPLE_DLY(self, value):
        """
        Writes the ADC_SAMPLE_DLY bitfield in the ADC_CAL_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CAL_CNTL()
        self._BITFIELD['ADC_SAMPLE_DLY'] = value
        self.write_ADC_CAL_CNTL()

    def get_ADC_SAMPLE_DLY(self):
        """
        Reads the ADC_CAL_CNTL register
        
        :return: the shadow register ADC_SAMPLE_DLY.
        :rtype: int
        """
        self.read_ADC_CAL_CNTL()
        return self._BITFIELD['ADC_SAMPLE_DLY']

    def set_CS_A_VCM_BASE_L(self, value):
        """
        Writes the CS_A_VCM_BASE_L bitfield in the CS_A_VCM_BASE_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_VCM_BASE_L()
        self._BITFIELD['CS_A_VCM_BASE_L'] = value
        self.write_CS_A_VCM_BASE_L()

    def get_CS_A_VCM_BASE_L(self):
        """
        Reads the CS_A_VCM_BASE_L register
        
        :return: the shadow register CS_A_VCM_BASE_L.
        :rtype: int
        """
        self.read_CS_A_VCM_BASE_L()
        return self._BITFIELD['CS_A_VCM_BASE_L']

    def set_RSVD_7_4_CS_A_VCM_BASE_H(self, value):
        """
        Writes the RSVD_7_4_CS_A_VCM_BASE_H bitfield in the CS_A_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_VCM_BASE_H()
        self._BITFIELD['RSVD_7_4_CS_A_VCM_BASE_H'] = value
        self.write_CS_A_VCM_BASE_H()

    def get_RSVD_7_4_CS_A_VCM_BASE_H(self):
        """
        Reads the CS_A_VCM_BASE_H register
        
        :return: the shadow register RSVD_7_4_CS_A_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_A_VCM_BASE_H()
        return self._BITFIELD['RSVD_7_4_CS_A_VCM_BASE_H']

    def set_CS_A_VCM_BASE_H(self, value):
        """
        Writes the CS_A_VCM_BASE_H bitfield in the CS_A_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_VCM_BASE_H()
        self._BITFIELD['CS_A_VCM_BASE_H'] = value
        self.write_CS_A_VCM_BASE_H()

    def get_CS_A_VCM_BASE_H(self):
        """
        Reads the CS_A_VCM_BASE_H register
        
        :return: the shadow register CS_A_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_A_VCM_BASE_H()
        return self._BITFIELD['CS_A_VCM_BASE_H']

    def set_CS_A_ER_VCM_BASE_L(self, value):
        """
        Writes the CS_A_ER_VCM_BASE_L bitfield in the CS_A_ER_VCM_BASE_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_ER_VCM_BASE_L()
        self._BITFIELD['CS_A_ER_VCM_BASE_L'] = value
        self.write_CS_A_ER_VCM_BASE_L()

    def get_CS_A_ER_VCM_BASE_L(self):
        """
        Reads the CS_A_ER_VCM_BASE_L register
        
        :return: the shadow register CS_A_ER_VCM_BASE_L.
        :rtype: int
        """
        self.read_CS_A_ER_VCM_BASE_L()
        return self._BITFIELD['CS_A_ER_VCM_BASE_L']

    def set_CS_A_CAL_ALU_BYP(self, value):
        """
        Writes the CS_A_CAL_ALU_BYP bitfield in the CS_A_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_ER_VCM_BASE_H()
        self._BITFIELD['CS_A_CAL_ALU_BYP'] = value
        self.write_CS_A_ER_VCM_BASE_H()

    def get_CS_A_CAL_ALU_BYP(self):
        """
        Reads the CS_A_ER_VCM_BASE_H register
        
        :return: the shadow register CS_A_CAL_ALU_BYP.
        :rtype: int
        """
        self.read_CS_A_ER_VCM_BASE_H()
        return self._BITFIELD['CS_A_CAL_ALU_BYP']

    def set_RSVD_6_5_CS_A_ER_VCM_BASE_H(self, value):
        """
        Writes the RSVD_6_5_CS_A_ER_VCM_BASE_H bitfield in the CS_A_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_ER_VCM_BASE_H()
        self._BITFIELD['RSVD_6_5_CS_A_ER_VCM_BASE_H'] = value
        self.write_CS_A_ER_VCM_BASE_H()

    def get_RSVD_6_5_CS_A_ER_VCM_BASE_H(self):
        """
        Reads the CS_A_ER_VCM_BASE_H register
        
        :return: the shadow register RSVD_6_5_CS_A_ER_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_A_ER_VCM_BASE_H()
        return self._BITFIELD['RSVD_6_5_CS_A_ER_VCM_BASE_H']

    def set_CS_A_ER_VCM_BASE_H_SIGN(self, value):
        """
        Writes the CS_A_ER_VCM_BASE_H_SIGN bitfield in the CS_A_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_ER_VCM_BASE_H()
        self._BITFIELD['CS_A_ER_VCM_BASE_H_SIGN'] = value
        self.write_CS_A_ER_VCM_BASE_H()

    def get_CS_A_ER_VCM_BASE_H_SIGN(self):
        """
        Reads the CS_A_ER_VCM_BASE_H register
        
        :return: the shadow register CS_A_ER_VCM_BASE_H_SIGN.
        :rtype: int
        """
        self.read_CS_A_ER_VCM_BASE_H()
        return self._BITFIELD['CS_A_ER_VCM_BASE_H_SIGN']

    def set_CS_A_ER_VCM_BASE_H(self, value):
        """
        Writes the CS_A_ER_VCM_BASE_H bitfield in the CS_A_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_ER_VCM_BASE_H()
        self._BITFIELD['CS_A_ER_VCM_BASE_H'] = value
        self.write_CS_A_ER_VCM_BASE_H()

    def get_CS_A_ER_VCM_BASE_H(self):
        """
        Reads the CS_A_ER_VCM_BASE_H register
        
        :return: the shadow register CS_A_ER_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_A_ER_VCM_BASE_H()
        return self._BITFIELD['CS_A_ER_VCM_BASE_H']

    def set_CS_A_VCM_SLOPE_L(self, value):
        """
        Writes the CS_A_VCM_SLOPE_L bitfield in the CS_A_VCM_SLOPE_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_VCM_SLOPE_L()
        self._BITFIELD['CS_A_VCM_SLOPE_L'] = value
        self.write_CS_A_VCM_SLOPE_L()

    def get_CS_A_VCM_SLOPE_L(self):
        """
        Reads the CS_A_VCM_SLOPE_L register
        
        :return: the shadow register CS_A_VCM_SLOPE_L.
        :rtype: int
        """
        self.read_CS_A_VCM_SLOPE_L()
        return self._BITFIELD['CS_A_VCM_SLOPE_L']

    def set_RSVD_7_5_CS_A_VCM_SLOPE_H(self, value):
        """
        Writes the RSVD_7_5_CS_A_VCM_SLOPE_H bitfield in the CS_A_VCM_SLOPE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_VCM_SLOPE_H()
        self._BITFIELD['RSVD_7_5_CS_A_VCM_SLOPE_H'] = value
        self.write_CS_A_VCM_SLOPE_H()

    def get_RSVD_7_5_CS_A_VCM_SLOPE_H(self):
        """
        Reads the CS_A_VCM_SLOPE_H register
        
        :return: the shadow register RSVD_7_5_CS_A_VCM_SLOPE_H.
        :rtype: int
        """
        self.read_CS_A_VCM_SLOPE_H()
        return self._BITFIELD['RSVD_7_5_CS_A_VCM_SLOPE_H']

    def set_CS_A_VCM_SLOPE_H_SIGN(self, value):
        """
        Writes the CS_A_VCM_SLOPE_H_SIGN bitfield in the CS_A_VCM_SLOPE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_VCM_SLOPE_H()
        self._BITFIELD['CS_A_VCM_SLOPE_H_SIGN'] = value
        self.write_CS_A_VCM_SLOPE_H()

    def get_CS_A_VCM_SLOPE_H_SIGN(self):
        """
        Reads the CS_A_VCM_SLOPE_H register
        
        :return: the shadow register CS_A_VCM_SLOPE_H_SIGN.
        :rtype: int
        """
        self.read_CS_A_VCM_SLOPE_H()
        return self._BITFIELD['CS_A_VCM_SLOPE_H_SIGN']

    def set_CS_A_VCM_SLOPE_H(self, value):
        """
        Writes the CS_A_VCM_SLOPE_H bitfield in the CS_A_VCM_SLOPE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_VCM_SLOPE_H()
        self._BITFIELD['CS_A_VCM_SLOPE_H'] = value
        self.write_CS_A_VCM_SLOPE_H()

    def get_CS_A_VCM_SLOPE_H(self):
        """
        Reads the CS_A_VCM_SLOPE_H register
        
        :return: the shadow register CS_A_VCM_SLOPE_H.
        :rtype: int
        """
        self.read_CS_A_VCM_SLOPE_H()
        return self._BITFIELD['CS_A_VCM_SLOPE_H']

    def set_CS_B_VCM_BASE_L(self, value):
        """
        Writes the CS_B_VCM_BASE_L bitfield in the CS_B_VCM_BASE_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_VCM_BASE_L()
        self._BITFIELD['CS_B_VCM_BASE_L'] = value
        self.write_CS_B_VCM_BASE_L()

    def get_CS_B_VCM_BASE_L(self):
        """
        Reads the CS_B_VCM_BASE_L register
        
        :return: the shadow register CS_B_VCM_BASE_L.
        :rtype: int
        """
        self.read_CS_B_VCM_BASE_L()
        return self._BITFIELD['CS_B_VCM_BASE_L']

    def set_RSVD_7_4_CS_B_VCM_BASE_H(self, value):
        """
        Writes the RSVD_7_4_CS_B_VCM_BASE_H bitfield in the CS_B_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_VCM_BASE_H()
        self._BITFIELD['RSVD_7_4_CS_B_VCM_BASE_H'] = value
        self.write_CS_B_VCM_BASE_H()

    def get_RSVD_7_4_CS_B_VCM_BASE_H(self):
        """
        Reads the CS_B_VCM_BASE_H register
        
        :return: the shadow register RSVD_7_4_CS_B_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_B_VCM_BASE_H()
        return self._BITFIELD['RSVD_7_4_CS_B_VCM_BASE_H']

    def set_CS_B_VCM_BASE_H(self, value):
        """
        Writes the CS_B_VCM_BASE_H bitfield in the CS_B_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_VCM_BASE_H()
        self._BITFIELD['CS_B_VCM_BASE_H'] = value
        self.write_CS_B_VCM_BASE_H()

    def get_CS_B_VCM_BASE_H(self):
        """
        Reads the CS_B_VCM_BASE_H register
        
        :return: the shadow register CS_B_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_B_VCM_BASE_H()
        return self._BITFIELD['CS_B_VCM_BASE_H']

    def set_CS_B_ER_VCM_BASE_L(self, value):
        """
        Writes the CS_B_ER_VCM_BASE_L bitfield in the CS_B_ER_VCM_BASE_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_ER_VCM_BASE_L()
        self._BITFIELD['CS_B_ER_VCM_BASE_L'] = value
        self.write_CS_B_ER_VCM_BASE_L()

    def get_CS_B_ER_VCM_BASE_L(self):
        """
        Reads the CS_B_ER_VCM_BASE_L register
        
        :return: the shadow register CS_B_ER_VCM_BASE_L.
        :rtype: int
        """
        self.read_CS_B_ER_VCM_BASE_L()
        return self._BITFIELD['CS_B_ER_VCM_BASE_L']

    def set_CS_B_CAL_ALU_BYP(self, value):
        """
        Writes the CS_B_CAL_ALU_BYP bitfield in the CS_B_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_ER_VCM_BASE_H()
        self._BITFIELD['CS_B_CAL_ALU_BYP'] = value
        self.write_CS_B_ER_VCM_BASE_H()

    def get_CS_B_CAL_ALU_BYP(self):
        """
        Reads the CS_B_ER_VCM_BASE_H register
        
        :return: the shadow register CS_B_CAL_ALU_BYP.
        :rtype: int
        """
        self.read_CS_B_ER_VCM_BASE_H()
        return self._BITFIELD['CS_B_CAL_ALU_BYP']

    def set_RSVD_6_5_CS_B_ER_VCM_BASE_H(self, value):
        """
        Writes the RSVD_6_5_CS_B_ER_VCM_BASE_H bitfield in the CS_B_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_ER_VCM_BASE_H()
        self._BITFIELD['RSVD_6_5_CS_B_ER_VCM_BASE_H'] = value
        self.write_CS_B_ER_VCM_BASE_H()

    def get_RSVD_6_5_CS_B_ER_VCM_BASE_H(self):
        """
        Reads the CS_B_ER_VCM_BASE_H register
        
        :return: the shadow register RSVD_6_5_CS_B_ER_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_B_ER_VCM_BASE_H()
        return self._BITFIELD['RSVD_6_5_CS_B_ER_VCM_BASE_H']

    def set_CS_B_ER_VCM_BASE_H_SIGN(self, value):
        """
        Writes the CS_B_ER_VCM_BASE_H_SIGN bitfield in the CS_B_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_ER_VCM_BASE_H()
        self._BITFIELD['CS_B_ER_VCM_BASE_H_SIGN'] = value
        self.write_CS_B_ER_VCM_BASE_H()

    def get_CS_B_ER_VCM_BASE_H_SIGN(self):
        """
        Reads the CS_B_ER_VCM_BASE_H register
        
        :return: the shadow register CS_B_ER_VCM_BASE_H_SIGN.
        :rtype: int
        """
        self.read_CS_B_ER_VCM_BASE_H()
        return self._BITFIELD['CS_B_ER_VCM_BASE_H_SIGN']

    def set_CS_B_ER_VCM_BASE_H(self, value):
        """
        Writes the CS_B_ER_VCM_BASE_H bitfield in the CS_B_ER_VCM_BASE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_ER_VCM_BASE_H()
        self._BITFIELD['CS_B_ER_VCM_BASE_H'] = value
        self.write_CS_B_ER_VCM_BASE_H()

    def get_CS_B_ER_VCM_BASE_H(self):
        """
        Reads the CS_B_ER_VCM_BASE_H register
        
        :return: the shadow register CS_B_ER_VCM_BASE_H.
        :rtype: int
        """
        self.read_CS_B_ER_VCM_BASE_H()
        return self._BITFIELD['CS_B_ER_VCM_BASE_H']

    def set_CS_B_VCM_SLOPE_L(self, value):
        """
        Writes the CS_B_VCM_SLOPE_L bitfield in the CS_B_VCM_SLOPE_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_VCM_SLOPE_L()
        self._BITFIELD['CS_B_VCM_SLOPE_L'] = value
        self.write_CS_B_VCM_SLOPE_L()

    def get_CS_B_VCM_SLOPE_L(self):
        """
        Reads the CS_B_VCM_SLOPE_L register
        
        :return: the shadow register CS_B_VCM_SLOPE_L.
        :rtype: int
        """
        self.read_CS_B_VCM_SLOPE_L()
        return self._BITFIELD['CS_B_VCM_SLOPE_L']

    def set_RSVD_7_5_CS_B_VCM_SLOPE_H(self, value):
        """
        Writes the RSVD_7_5_CS_B_VCM_SLOPE_H bitfield in the CS_B_VCM_SLOPE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_VCM_SLOPE_H()
        self._BITFIELD['RSVD_7_5_CS_B_VCM_SLOPE_H'] = value
        self.write_CS_B_VCM_SLOPE_H()

    def get_RSVD_7_5_CS_B_VCM_SLOPE_H(self):
        """
        Reads the CS_B_VCM_SLOPE_H register
        
        :return: the shadow register RSVD_7_5_CS_B_VCM_SLOPE_H.
        :rtype: int
        """
        self.read_CS_B_VCM_SLOPE_H()
        return self._BITFIELD['RSVD_7_5_CS_B_VCM_SLOPE_H']

    def set_CS_B_VCM_SLOPE_H_SIGN(self, value):
        """
        Writes the CS_B_VCM_SLOPE_H_SIGN bitfield in the CS_B_VCM_SLOPE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_VCM_SLOPE_H()
        self._BITFIELD['CS_B_VCM_SLOPE_H_SIGN'] = value
        self.write_CS_B_VCM_SLOPE_H()

    def get_CS_B_VCM_SLOPE_H_SIGN(self):
        """
        Reads the CS_B_VCM_SLOPE_H register
        
        :return: the shadow register CS_B_VCM_SLOPE_H_SIGN.
        :rtype: int
        """
        self.read_CS_B_VCM_SLOPE_H()
        return self._BITFIELD['CS_B_VCM_SLOPE_H_SIGN']

    def set_CS_B_VCM_SLOPE_H(self, value):
        """
        Writes the CS_B_VCM_SLOPE_H bitfield in the CS_B_VCM_SLOPE_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_VCM_SLOPE_H()
        self._BITFIELD['CS_B_VCM_SLOPE_H'] = value
        self.write_CS_B_VCM_SLOPE_H()

    def get_CS_B_VCM_SLOPE_H(self):
        """
        Reads the CS_B_VCM_SLOPE_H register
        
        :return: the shadow register CS_B_VCM_SLOPE_H.
        :rtype: int
        """
        self.read_CS_B_VCM_SLOPE_H()
        return self._BITFIELD['CS_B_VCM_SLOPE_H']

    def set_CS_DAC_MODE(self, value):
        """
        Writes the CS_DAC_MODE bitfield in the CS_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_0()
        self._BITFIELD['CS_DAC_MODE'] = value
        self.write_CS_CFG_0()

    def get_CS_DAC_MODE(self):
        """
        Reads the CS_CFG_0 register
        
        :return: the shadow register CS_DAC_MODE.
        :rtype: int
        """
        self.read_CS_CFG_0()
        return self._BITFIELD['CS_DAC_MODE']

    def set_CS_DATA_CLAMP_EN(self, value):
        """
        Writes the CS_DATA_CLAMP_EN bitfield in the CS_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_0()
        self._BITFIELD['CS_DATA_CLAMP_EN'] = value
        self.write_CS_CFG_0()

    def get_CS_DATA_CLAMP_EN(self):
        """
        Reads the CS_CFG_0 register
        
        :return: the shadow register CS_DATA_CLAMP_EN.
        :rtype: int
        """
        self.read_CS_CFG_0()
        return self._BITFIELD['CS_DATA_CLAMP_EN']

    def set_CS_ADC_ACQ_DLY_EN(self, value):
        """
        Writes the CS_ADC_ACQ_DLY_EN bitfield in the CS_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_0()
        self._BITFIELD['CS_ADC_ACQ_DLY_EN'] = value
        self.write_CS_CFG_0()

    def get_CS_ADC_ACQ_DLY_EN(self):
        """
        Reads the CS_CFG_0 register
        
        :return: the shadow register CS_ADC_ACQ_DLY_EN.
        :rtype: int
        """
        self.read_CS_CFG_0()
        return self._BITFIELD['CS_ADC_ACQ_DLY_EN']

    def set_CS_CFG_0_SIGN(self, value):
        """
        Writes the CS_CFG_0_SIGN bitfield in the CS_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_0()
        self._BITFIELD['CS_CFG_0_SIGN'] = value
        self.write_CS_CFG_0()

    def get_CS_CFG_0_SIGN(self):
        """
        Reads the CS_CFG_0 register
        
        :return: the shadow register CS_CFG_0_SIGN.
        :rtype: int
        """
        self.read_CS_CFG_0()
        return self._BITFIELD['CS_CFG_0_SIGN']

    def set_CS_A_DAC_OFFSET(self, value):
        """
        Writes the CS_A_DAC_OFFSET bitfield in the CS_CFG_0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_0()
        self._BITFIELD['CS_A_DAC_OFFSET'] = value
        self.write_CS_CFG_0()

    def get_CS_A_DAC_OFFSET(self):
        """
        Reads the CS_CFG_0 register
        
        :return: the shadow register CS_A_DAC_OFFSET.
        :rtype: int
        """
        self.read_CS_CFG_0()
        return self._BITFIELD['CS_A_DAC_OFFSET']

    def set_CS_CONV_RATE(self, value):
        """
        Writes the CS_CONV_RATE bitfield in the CS_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_1()
        self._BITFIELD['CS_CONV_RATE'] = value
        self.write_CS_CFG_1()

    def get_CS_CONV_RATE(self):
        """
        Reads the CS_CFG_1 register
        
        :return: the shadow register CS_CONV_RATE.
        :rtype: int
        """
        self.read_CS_CFG_1()
        return self._BITFIELD['CS_CONV_RATE']

    def set_CS_CFG_1_SIGN(self, value):
        """
        Writes the CS_CFG_1_SIGN bitfield in the CS_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_1()
        self._BITFIELD['CS_CFG_1_SIGN'] = value
        self.write_CS_CFG_1()

    def get_CS_CFG_1_SIGN(self):
        """
        Reads the CS_CFG_1 register
        
        :return: the shadow register CS_CFG_1_SIGN.
        :rtype: int
        """
        self.read_CS_CFG_1()
        return self._BITFIELD['CS_CFG_1_SIGN']

    def set_CS_B_DAC_OFFSET(self, value):
        """
        Writes the CS_B_DAC_OFFSET bitfield in the CS_CFG_1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_1()
        self._BITFIELD['CS_B_DAC_OFFSET'] = value
        self.write_CS_CFG_1()

    def get_CS_B_DAC_OFFSET(self):
        """
        Reads the CS_CFG_1 register
        
        :return: the shadow register CS_B_DAC_OFFSET.
        :rtype: int
        """
        self.read_CS_CFG_1()
        return self._BITFIELD['CS_B_DAC_OFFSET']

    def set_DAC_CODE_BYPASS(self, value):
        """
        Writes the DAC_CODE_BYPASS bitfield in the CS_CFG_2 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_2()
        self._BITFIELD['DAC_CODE_BYPASS'] = value
        self.write_CS_CFG_2()

    def get_DAC_CODE_BYPASS(self):
        """
        Reads the CS_CFG_2 register
        
        :return: the shadow register DAC_CODE_BYPASS.
        :rtype: int
        """
        self.read_CS_CFG_2()
        return self._BITFIELD['DAC_CODE_BYPASS']

    def set_CS_CFG_2_DAC_CODE(self, value):
        """
        Writes the CS_CFG_2_DAC_CODE bitfield in the CS_CFG_2 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_CFG_2()
        self._BITFIELD['CS_CFG_2_DAC_CODE'] = value
        self.write_CS_CFG_2()

    def get_CS_CFG_2_DAC_CODE(self):
        """
        Reads the CS_CFG_2 register
        
        :return: the shadow register CS_CFG_2_DAC_CODE.
        :rtype: int
        """
        self.read_CS_CFG_2()
        return self._BITFIELD['CS_CFG_2_DAC_CODE']

    def set_I3C_MAX_DS(self, value):
        """
        Writes the I3C_MAX_DS bitfield in the MISC_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_MISC_CNTL()
        self._BITFIELD['I3C_MAX_DS'] = value
        self.write_MISC_CNTL()

    def get_I3C_MAX_DS(self):
        """
        Reads the MISC_CNTL register
        
        :return: the shadow register I3C_MAX_DS.
        :rtype: int
        """
        self.read_MISC_CNTL()
        return self._BITFIELD['I3C_MAX_DS']

    def set_I2C_SPIKE_DIS(self, value):
        """
        Writes the I2C_SPIKE_DIS bitfield in the MISC_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_MISC_CNTL()
        self._BITFIELD['I2C_SPIKE_DIS'] = value
        self.write_MISC_CNTL()

    def get_I2C_SPIKE_DIS(self):
        """
        Reads the MISC_CNTL register
        
        :return: the shadow register I2C_SPIKE_DIS.
        :rtype: int
        """
        self.read_MISC_CNTL()
        return self._BITFIELD['I2C_SPIKE_DIS']

    def set_DAC_CLAMP_EN(self, value):
        """
        Writes the DAC_CLAMP_EN bitfield in the MISC_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_MISC_CNTL()
        self._BITFIELD['DAC_CLAMP_EN'] = value
        self.write_MISC_CNTL()

    def get_DAC_CLAMP_EN(self):
        """
        Reads the MISC_CNTL register
        
        :return: the shadow register DAC_CLAMP_EN.
        :rtype: int
        """
        self.read_MISC_CNTL()
        return self._BITFIELD['DAC_CLAMP_EN']

    def set_DAC_ICALP(self, value):
        """
        Writes the DAC_ICALP bitfield in the MISC_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_MISC_CNTL()
        self._BITFIELD['DAC_ICALP'] = value
        self.write_MISC_CNTL()

    def get_DAC_ICALP(self):
        """
        Reads the MISC_CNTL register
        
        :return: the shadow register DAC_ICALP.
        :rtype: int
        """
        self.read_MISC_CNTL()
        return self._BITFIELD['DAC_ICALP']

    def set_DAC_ICALN(self, value):
        """
        Writes the DAC_ICALN bitfield in the MISC_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_MISC_CNTL()
        self._BITFIELD['DAC_ICALN'] = value
        self.write_MISC_CNTL()

    def get_DAC_ICALN(self):
        """
        Reads the MISC_CNTL register
        
        :return: the shadow register DAC_ICALN.
        :rtype: int
        """
        self.read_MISC_CNTL()
        return self._BITFIELD['DAC_ICALN']

    def set_LT_SENSE_GAIN_CAL_H(self, value):
        """
        Writes the LT_SENSE_GAIN_CAL_H bitfield in the ADC_LT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_LT_CAL()
        self._BITFIELD['LT_SENSE_GAIN_CAL_H'] = value
        self.write_ADC_LT_CAL()

    def get_LT_SENSE_GAIN_CAL_H(self):
        """
        Reads the ADC_LT_CAL register
        
        :return: the shadow register LT_SENSE_GAIN_CAL_H.
        :rtype: int
        """
        self.read_ADC_LT_CAL()
        return self._BITFIELD['LT_SENSE_GAIN_CAL_H']

    def set_LT_SENSE_GAIN_CAL_L(self, value):
        """
        Writes the LT_SENSE_GAIN_CAL_L bitfield in the ADC_LT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_LT_CAL()
        self._BITFIELD['LT_SENSE_GAIN_CAL_L'] = value
        self.write_ADC_LT_CAL()

    def get_LT_SENSE_GAIN_CAL_L(self):
        """
        Reads the ADC_LT_CAL register
        
        :return: the shadow register LT_SENSE_GAIN_CAL_L.
        :rtype: int
        """
        self.read_ADC_LT_CAL()
        return self._BITFIELD['LT_SENSE_GAIN_CAL_L']

    def set_RT_SENSE_GAIN_CAL_H(self, value):
        """
        Writes the RT_SENSE_GAIN_CAL_H bitfield in the ADC_RT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_RT_CAL()
        self._BITFIELD['RT_SENSE_GAIN_CAL_H'] = value
        self.write_ADC_RT_CAL()

    def get_RT_SENSE_GAIN_CAL_H(self):
        """
        Reads the ADC_RT_CAL register
        
        :return: the shadow register RT_SENSE_GAIN_CAL_H.
        :rtype: int
        """
        self.read_ADC_RT_CAL()
        return self._BITFIELD['RT_SENSE_GAIN_CAL_H']

    def set_RT_SENSE_GAIN_CAL_L(self, value):
        """
        Writes the RT_SENSE_GAIN_CAL_L bitfield in the ADC_RT_CAL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_RT_CAL()
        self._BITFIELD['RT_SENSE_GAIN_CAL_L'] = value
        self.write_ADC_RT_CAL()

    def get_RT_SENSE_GAIN_CAL_L(self):
        """
        Reads the ADC_RT_CAL register
        
        :return: the shadow register RT_SENSE_GAIN_CAL_L.
        :rtype: int
        """
        self.read_ADC_RT_CAL()
        return self._BITFIELD['RT_SENSE_GAIN_CAL_L']

    def set_THRT_LT_L(self, value):
        """
        Writes the THRT_LT_L bitfield in the LT_THERM_THR_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_THERM_THR_L()
        self._BITFIELD['THRT_LT_L'] = value
        self.write_LT_THERM_THR_L()

    def get_THRT_LT_L(self):
        """
        Reads the LT_THERM_THR_L register
        
        :return: the shadow register THRT_LT_L.
        :rtype: int
        """
        self.read_LT_THERM_THR_L()
        return self._BITFIELD['THRT_LT_L']

    def set_RSVD_7_4_LT_THERM_THR_H(self, value):
        """
        Writes the RSVD_7_4_LT_THERM_THR_H bitfield in the LT_THERM_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_THERM_THR_H()
        self._BITFIELD['RSVD_7_4_LT_THERM_THR_H'] = value
        self.write_LT_THERM_THR_H()

    def get_RSVD_7_4_LT_THERM_THR_H(self):
        """
        Reads the LT_THERM_THR_H register
        
        :return: the shadow register RSVD_7_4_LT_THERM_THR_H.
        :rtype: int
        """
        self.read_LT_THERM_THR_H()
        return self._BITFIELD['RSVD_7_4_LT_THERM_THR_H']

    def set_THRT_LT_H(self, value):
        """
        Writes the THRT_LT_H bitfield in the LT_THERM_THR_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LT_THERM_THR_H()
        self._BITFIELD['THRT_LT_H'] = value
        self.write_LT_THERM_THR_H()

    def get_THRT_LT_H(self):
        """
        Reads the LT_THERM_THR_H register
        
        :return: the shadow register THRT_LT_H.
        :rtype: int
        """
        self.read_LT_THERM_THR_H()
        return self._BITFIELD['THRT_LT_H']

    def set_CS_A_DEL_ER_VCM0_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM0_SIGN bitfield in the CS_A_DEL_ER_VCM0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM0()
        self._BITFIELD['CS_A_DEL_ER_VCM0_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM0()

    def get_CS_A_DEL_ER_VCM0_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM0 register
        
        :return: the shadow register CS_A_DEL_ER_VCM0_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM0()
        return self._BITFIELD['CS_A_DEL_ER_VCM0_SIGN']

    def set_CS_A_DEL_ER_VCM0(self, value):
        """
        Writes the CS_A_DEL_ER_VCM0 bitfield in the CS_A_DEL_ER_VCM0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM0()
        self._BITFIELD['CS_A_DEL_ER_VCM0'] = value
        self.write_CS_A_DEL_ER_VCM0()

    def get_CS_A_DEL_ER_VCM0(self):
        """
        Reads the CS_A_DEL_ER_VCM0 register
        
        :return: the shadow register CS_A_DEL_ER_VCM0.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM0()
        return self._BITFIELD['CS_A_DEL_ER_VCM0']

    def set_CS_A_DEL_ER_VCM1_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM1_SIGN bitfield in the CS_A_DEL_ER_VCM1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM1()
        self._BITFIELD['CS_A_DEL_ER_VCM1_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM1()

    def get_CS_A_DEL_ER_VCM1_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM1 register
        
        :return: the shadow register CS_A_DEL_ER_VCM1_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM1()
        return self._BITFIELD['CS_A_DEL_ER_VCM1_SIGN']

    def set_CS_A_DEL_ER_VCM1(self, value):
        """
        Writes the CS_A_DEL_ER_VCM1 bitfield in the CS_A_DEL_ER_VCM1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM1()
        self._BITFIELD['CS_A_DEL_ER_VCM1'] = value
        self.write_CS_A_DEL_ER_VCM1()

    def get_CS_A_DEL_ER_VCM1(self):
        """
        Reads the CS_A_DEL_ER_VCM1 register
        
        :return: the shadow register CS_A_DEL_ER_VCM1.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM1()
        return self._BITFIELD['CS_A_DEL_ER_VCM1']

    def set_CS_A_DEL_ER_VCM2_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM2_SIGN bitfield in the CS_A_DEL_ER_VCM2 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM2()
        self._BITFIELD['CS_A_DEL_ER_VCM2_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM2()

    def get_CS_A_DEL_ER_VCM2_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM2 register
        
        :return: the shadow register CS_A_DEL_ER_VCM2_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM2()
        return self._BITFIELD['CS_A_DEL_ER_VCM2_SIGN']

    def set_CS_A_DEL_ER_VCM2(self, value):
        """
        Writes the CS_A_DEL_ER_VCM2 bitfield in the CS_A_DEL_ER_VCM2 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM2()
        self._BITFIELD['CS_A_DEL_ER_VCM2'] = value
        self.write_CS_A_DEL_ER_VCM2()

    def get_CS_A_DEL_ER_VCM2(self):
        """
        Reads the CS_A_DEL_ER_VCM2 register
        
        :return: the shadow register CS_A_DEL_ER_VCM2.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM2()
        return self._BITFIELD['CS_A_DEL_ER_VCM2']

    def set_CS_A_DEL_ER_VCM3_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM3_SIGN bitfield in the CS_A_DEL_ER_VCM3 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM3()
        self._BITFIELD['CS_A_DEL_ER_VCM3_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM3()

    def get_CS_A_DEL_ER_VCM3_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM3 register
        
        :return: the shadow register CS_A_DEL_ER_VCM3_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM3()
        return self._BITFIELD['CS_A_DEL_ER_VCM3_SIGN']

    def set_CS_A_DEL_ER_VCM3(self, value):
        """
        Writes the CS_A_DEL_ER_VCM3 bitfield in the CS_A_DEL_ER_VCM3 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM3()
        self._BITFIELD['CS_A_DEL_ER_VCM3'] = value
        self.write_CS_A_DEL_ER_VCM3()

    def get_CS_A_DEL_ER_VCM3(self):
        """
        Reads the CS_A_DEL_ER_VCM3 register
        
        :return: the shadow register CS_A_DEL_ER_VCM3.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM3()
        return self._BITFIELD['CS_A_DEL_ER_VCM3']

    def set_CS_A_DEL_ER_VCM4_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM4_SIGN bitfield in the CS_A_DEL_ER_VCM4 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM4()
        self._BITFIELD['CS_A_DEL_ER_VCM4_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM4()

    def get_CS_A_DEL_ER_VCM4_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM4 register
        
        :return: the shadow register CS_A_DEL_ER_VCM4_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM4()
        return self._BITFIELD['CS_A_DEL_ER_VCM4_SIGN']

    def set_CS_A_DEL_ER_VCM4(self, value):
        """
        Writes the CS_A_DEL_ER_VCM4 bitfield in the CS_A_DEL_ER_VCM4 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM4()
        self._BITFIELD['CS_A_DEL_ER_VCM4'] = value
        self.write_CS_A_DEL_ER_VCM4()

    def get_CS_A_DEL_ER_VCM4(self):
        """
        Reads the CS_A_DEL_ER_VCM4 register
        
        :return: the shadow register CS_A_DEL_ER_VCM4.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM4()
        return self._BITFIELD['CS_A_DEL_ER_VCM4']

    def set_CS_A_DEL_ER_VCM5_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM5_SIGN bitfield in the CS_A_DEL_ER_VCM5 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM5()
        self._BITFIELD['CS_A_DEL_ER_VCM5_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM5()

    def get_CS_A_DEL_ER_VCM5_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM5 register
        
        :return: the shadow register CS_A_DEL_ER_VCM5_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM5()
        return self._BITFIELD['CS_A_DEL_ER_VCM5_SIGN']

    def set_CS_A_DEL_ER_VCM5(self, value):
        """
        Writes the CS_A_DEL_ER_VCM5 bitfield in the CS_A_DEL_ER_VCM5 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM5()
        self._BITFIELD['CS_A_DEL_ER_VCM5'] = value
        self.write_CS_A_DEL_ER_VCM5()

    def get_CS_A_DEL_ER_VCM5(self):
        """
        Reads the CS_A_DEL_ER_VCM5 register
        
        :return: the shadow register CS_A_DEL_ER_VCM5.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM5()
        return self._BITFIELD['CS_A_DEL_ER_VCM5']

    def set_CS_A_DEL_ER_VCM6_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM6_SIGN bitfield in the CS_A_DEL_ER_VCM6 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM6()
        self._BITFIELD['CS_A_DEL_ER_VCM6_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM6()

    def get_CS_A_DEL_ER_VCM6_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM6 register
        
        :return: the shadow register CS_A_DEL_ER_VCM6_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM6()
        return self._BITFIELD['CS_A_DEL_ER_VCM6_SIGN']

    def set_CS_A_DEL_ER_VCM6(self, value):
        """
        Writes the CS_A_DEL_ER_VCM6 bitfield in the CS_A_DEL_ER_VCM6 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM6()
        self._BITFIELD['CS_A_DEL_ER_VCM6'] = value
        self.write_CS_A_DEL_ER_VCM6()

    def get_CS_A_DEL_ER_VCM6(self):
        """
        Reads the CS_A_DEL_ER_VCM6 register
        
        :return: the shadow register CS_A_DEL_ER_VCM6.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM6()
        return self._BITFIELD['CS_A_DEL_ER_VCM6']

    def set_CS_A_DEL_ER_VCM7_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM7_SIGN bitfield in the CS_A_DEL_ER_VCM7 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM7()
        self._BITFIELD['CS_A_DEL_ER_VCM7_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM7()

    def get_CS_A_DEL_ER_VCM7_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM7 register
        
        :return: the shadow register CS_A_DEL_ER_VCM7_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM7()
        return self._BITFIELD['CS_A_DEL_ER_VCM7_SIGN']

    def set_CS_A_DEL_ER_VCM7(self, value):
        """
        Writes the CS_A_DEL_ER_VCM7 bitfield in the CS_A_DEL_ER_VCM7 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM7()
        self._BITFIELD['CS_A_DEL_ER_VCM7'] = value
        self.write_CS_A_DEL_ER_VCM7()

    def get_CS_A_DEL_ER_VCM7(self):
        """
        Reads the CS_A_DEL_ER_VCM7 register
        
        :return: the shadow register CS_A_DEL_ER_VCM7.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM7()
        return self._BITFIELD['CS_A_DEL_ER_VCM7']

    def set_CS_A_DEL_ER_VCM8_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM8_SIGN bitfield in the CS_A_DEL_ER_VCM8 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM8()
        self._BITFIELD['CS_A_DEL_ER_VCM8_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM8()

    def get_CS_A_DEL_ER_VCM8_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM8 register
        
        :return: the shadow register CS_A_DEL_ER_VCM8_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM8()
        return self._BITFIELD['CS_A_DEL_ER_VCM8_SIGN']

    def set_CS_A_DEL_ER_VCM8(self, value):
        """
        Writes the CS_A_DEL_ER_VCM8 bitfield in the CS_A_DEL_ER_VCM8 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM8()
        self._BITFIELD['CS_A_DEL_ER_VCM8'] = value
        self.write_CS_A_DEL_ER_VCM8()

    def get_CS_A_DEL_ER_VCM8(self):
        """
        Reads the CS_A_DEL_ER_VCM8 register
        
        :return: the shadow register CS_A_DEL_ER_VCM8.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM8()
        return self._BITFIELD['CS_A_DEL_ER_VCM8']

    def set_CS_A_DEL_ER_VCM9_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM9_SIGN bitfield in the CS_A_DEL_ER_VCM9 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM9()
        self._BITFIELD['CS_A_DEL_ER_VCM9_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM9()

    def get_CS_A_DEL_ER_VCM9_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM9 register
        
        :return: the shadow register CS_A_DEL_ER_VCM9_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM9()
        return self._BITFIELD['CS_A_DEL_ER_VCM9_SIGN']

    def set_CS_A_DEL_ER_VCM9(self, value):
        """
        Writes the CS_A_DEL_ER_VCM9 bitfield in the CS_A_DEL_ER_VCM9 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM9()
        self._BITFIELD['CS_A_DEL_ER_VCM9'] = value
        self.write_CS_A_DEL_ER_VCM9()

    def get_CS_A_DEL_ER_VCM9(self):
        """
        Reads the CS_A_DEL_ER_VCM9 register
        
        :return: the shadow register CS_A_DEL_ER_VCM9.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM9()
        return self._BITFIELD['CS_A_DEL_ER_VCM9']

    def set_CS_A_DEL_ER_VCM10_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM10_SIGN bitfield in the CS_A_DEL_ER_VCM10 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM10()
        self._BITFIELD['CS_A_DEL_ER_VCM10_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM10()

    def get_CS_A_DEL_ER_VCM10_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM10 register
        
        :return: the shadow register CS_A_DEL_ER_VCM10_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM10()
        return self._BITFIELD['CS_A_DEL_ER_VCM10_SIGN']

    def set_CS_A_DEL_ER_VCM10(self, value):
        """
        Writes the CS_A_DEL_ER_VCM10 bitfield in the CS_A_DEL_ER_VCM10 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM10()
        self._BITFIELD['CS_A_DEL_ER_VCM10'] = value
        self.write_CS_A_DEL_ER_VCM10()

    def get_CS_A_DEL_ER_VCM10(self):
        """
        Reads the CS_A_DEL_ER_VCM10 register
        
        :return: the shadow register CS_A_DEL_ER_VCM10.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM10()
        return self._BITFIELD['CS_A_DEL_ER_VCM10']

    def set_CS_A_DEL_ER_VCM11_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM11_SIGN bitfield in the CS_A_DEL_ER_VCM11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM11()
        self._BITFIELD['CS_A_DEL_ER_VCM11_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM11()

    def get_CS_A_DEL_ER_VCM11_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM11 register
        
        :return: the shadow register CS_A_DEL_ER_VCM11_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM11()
        return self._BITFIELD['CS_A_DEL_ER_VCM11_SIGN']

    def set_CS_A_DEL_ER_VCM11(self, value):
        """
        Writes the CS_A_DEL_ER_VCM11 bitfield in the CS_A_DEL_ER_VCM11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM11()
        self._BITFIELD['CS_A_DEL_ER_VCM11'] = value
        self.write_CS_A_DEL_ER_VCM11()

    def get_CS_A_DEL_ER_VCM11(self):
        """
        Reads the CS_A_DEL_ER_VCM11 register
        
        :return: the shadow register CS_A_DEL_ER_VCM11.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM11()
        return self._BITFIELD['CS_A_DEL_ER_VCM11']

    def set_CS_A_DEL_ER_VCM12_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM12_SIGN bitfield in the CS_A_DEL_ER_VCM12 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM12()
        self._BITFIELD['CS_A_DEL_ER_VCM12_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM12()

    def get_CS_A_DEL_ER_VCM12_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM12 register
        
        :return: the shadow register CS_A_DEL_ER_VCM12_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM12()
        return self._BITFIELD['CS_A_DEL_ER_VCM12_SIGN']

    def set_CS_A_DEL_ER_VCM12(self, value):
        """
        Writes the CS_A_DEL_ER_VCM12 bitfield in the CS_A_DEL_ER_VCM12 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM12()
        self._BITFIELD['CS_A_DEL_ER_VCM12'] = value
        self.write_CS_A_DEL_ER_VCM12()

    def get_CS_A_DEL_ER_VCM12(self):
        """
        Reads the CS_A_DEL_ER_VCM12 register
        
        :return: the shadow register CS_A_DEL_ER_VCM12.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM12()
        return self._BITFIELD['CS_A_DEL_ER_VCM12']

    def set_CS_A_DEL_ER_VCM13_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM13_SIGN bitfield in the CS_A_DEL_ER_VCM13 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM13()
        self._BITFIELD['CS_A_DEL_ER_VCM13_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM13()

    def get_CS_A_DEL_ER_VCM13_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM13 register
        
        :return: the shadow register CS_A_DEL_ER_VCM13_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM13()
        return self._BITFIELD['CS_A_DEL_ER_VCM13_SIGN']

    def set_CS_A_DEL_ER_VCM13(self, value):
        """
        Writes the CS_A_DEL_ER_VCM13 bitfield in the CS_A_DEL_ER_VCM13 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM13()
        self._BITFIELD['CS_A_DEL_ER_VCM13'] = value
        self.write_CS_A_DEL_ER_VCM13()

    def get_CS_A_DEL_ER_VCM13(self):
        """
        Reads the CS_A_DEL_ER_VCM13 register
        
        :return: the shadow register CS_A_DEL_ER_VCM13.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM13()
        return self._BITFIELD['CS_A_DEL_ER_VCM13']

    def set_CS_A_DEL_ER_VCM14_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM14_SIGN bitfield in the CS_A_DEL_ER_VCM14 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM14()
        self._BITFIELD['CS_A_DEL_ER_VCM14_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM14()

    def get_CS_A_DEL_ER_VCM14_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM14 register
        
        :return: the shadow register CS_A_DEL_ER_VCM14_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM14()
        return self._BITFIELD['CS_A_DEL_ER_VCM14_SIGN']

    def set_CS_A_DEL_ER_VCM14(self, value):
        """
        Writes the CS_A_DEL_ER_VCM14 bitfield in the CS_A_DEL_ER_VCM14 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM14()
        self._BITFIELD['CS_A_DEL_ER_VCM14'] = value
        self.write_CS_A_DEL_ER_VCM14()

    def get_CS_A_DEL_ER_VCM14(self):
        """
        Reads the CS_A_DEL_ER_VCM14 register
        
        :return: the shadow register CS_A_DEL_ER_VCM14.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM14()
        return self._BITFIELD['CS_A_DEL_ER_VCM14']

    def set_CS_A_DEL_ER_VCM15_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM15_SIGN bitfield in the CS_A_DEL_ER_VCM15 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM15()
        self._BITFIELD['CS_A_DEL_ER_VCM15_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM15()

    def get_CS_A_DEL_ER_VCM15_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM15 register
        
        :return: the shadow register CS_A_DEL_ER_VCM15_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM15()
        return self._BITFIELD['CS_A_DEL_ER_VCM15_SIGN']

    def set_CS_A_DEL_ER_VCM15(self, value):
        """
        Writes the CS_A_DEL_ER_VCM15 bitfield in the CS_A_DEL_ER_VCM15 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM15()
        self._BITFIELD['CS_A_DEL_ER_VCM15'] = value
        self.write_CS_A_DEL_ER_VCM15()

    def get_CS_A_DEL_ER_VCM15(self):
        """
        Reads the CS_A_DEL_ER_VCM15 register
        
        :return: the shadow register CS_A_DEL_ER_VCM15.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM15()
        return self._BITFIELD['CS_A_DEL_ER_VCM15']

    def set_CS_A_DEL_ER_VCM16_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM16_SIGN bitfield in the CS_A_DEL_ER_VCM16 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM16()
        self._BITFIELD['CS_A_DEL_ER_VCM16_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM16()

    def get_CS_A_DEL_ER_VCM16_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM16 register
        
        :return: the shadow register CS_A_DEL_ER_VCM16_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM16()
        return self._BITFIELD['CS_A_DEL_ER_VCM16_SIGN']

    def set_CS_A_DEL_ER_VCM16(self, value):
        """
        Writes the CS_A_DEL_ER_VCM16 bitfield in the CS_A_DEL_ER_VCM16 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM16()
        self._BITFIELD['CS_A_DEL_ER_VCM16'] = value
        self.write_CS_A_DEL_ER_VCM16()

    def get_CS_A_DEL_ER_VCM16(self):
        """
        Reads the CS_A_DEL_ER_VCM16 register
        
        :return: the shadow register CS_A_DEL_ER_VCM16.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM16()
        return self._BITFIELD['CS_A_DEL_ER_VCM16']

    def set_CS_A_DEL_ER_VCM17_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM17_SIGN bitfield in the CS_A_DEL_ER_VCM17 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM17()
        self._BITFIELD['CS_A_DEL_ER_VCM17_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM17()

    def get_CS_A_DEL_ER_VCM17_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM17 register
        
        :return: the shadow register CS_A_DEL_ER_VCM17_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM17()
        return self._BITFIELD['CS_A_DEL_ER_VCM17_SIGN']

    def set_CS_A_DEL_ER_VCM17(self, value):
        """
        Writes the CS_A_DEL_ER_VCM17 bitfield in the CS_A_DEL_ER_VCM17 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM17()
        self._BITFIELD['CS_A_DEL_ER_VCM17'] = value
        self.write_CS_A_DEL_ER_VCM17()

    def get_CS_A_DEL_ER_VCM17(self):
        """
        Reads the CS_A_DEL_ER_VCM17 register
        
        :return: the shadow register CS_A_DEL_ER_VCM17.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM17()
        return self._BITFIELD['CS_A_DEL_ER_VCM17']

    def set_CS_A_DEL_ER_VCM18_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM18_SIGN bitfield in the CS_A_DEL_ER_VCM18 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM18()
        self._BITFIELD['CS_A_DEL_ER_VCM18_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM18()

    def get_CS_A_DEL_ER_VCM18_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM18 register
        
        :return: the shadow register CS_A_DEL_ER_VCM18_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM18()
        return self._BITFIELD['CS_A_DEL_ER_VCM18_SIGN']

    def set_CS_A_DEL_ER_VCM18(self, value):
        """
        Writes the CS_A_DEL_ER_VCM18 bitfield in the CS_A_DEL_ER_VCM18 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM18()
        self._BITFIELD['CS_A_DEL_ER_VCM18'] = value
        self.write_CS_A_DEL_ER_VCM18()

    def get_CS_A_DEL_ER_VCM18(self):
        """
        Reads the CS_A_DEL_ER_VCM18 register
        
        :return: the shadow register CS_A_DEL_ER_VCM18.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM18()
        return self._BITFIELD['CS_A_DEL_ER_VCM18']

    def set_CS_A_DEL_ER_VCM19_SIGN(self, value):
        """
        Writes the CS_A_DEL_ER_VCM19_SIGN bitfield in the CS_A_DEL_ER_VCM19 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM19()
        self._BITFIELD['CS_A_DEL_ER_VCM19_SIGN'] = value
        self.write_CS_A_DEL_ER_VCM19()

    def get_CS_A_DEL_ER_VCM19_SIGN(self):
        """
        Reads the CS_A_DEL_ER_VCM19 register
        
        :return: the shadow register CS_A_DEL_ER_VCM19_SIGN.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM19()
        return self._BITFIELD['CS_A_DEL_ER_VCM19_SIGN']

    def set_CS_A_DEL_ER_VCM19(self, value):
        """
        Writes the CS_A_DEL_ER_VCM19 bitfield in the CS_A_DEL_ER_VCM19 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_A_DEL_ER_VCM19()
        self._BITFIELD['CS_A_DEL_ER_VCM19'] = value
        self.write_CS_A_DEL_ER_VCM19()

    def get_CS_A_DEL_ER_VCM19(self):
        """
        Reads the CS_A_DEL_ER_VCM19 register
        
        :return: the shadow register CS_A_DEL_ER_VCM19.
        :rtype: int
        """
        self.read_CS_A_DEL_ER_VCM19()
        return self._BITFIELD['CS_A_DEL_ER_VCM19']

    def set_CS_B_DEL_ER_VCM0_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM0_SIGN bitfield in the CS_B_DEL_ER_VCM0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM0()
        self._BITFIELD['CS_B_DEL_ER_VCM0_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM0()

    def get_CS_B_DEL_ER_VCM0_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM0 register
        
        :return: the shadow register CS_B_DEL_ER_VCM0_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM0()
        return self._BITFIELD['CS_B_DEL_ER_VCM0_SIGN']

    def set_CS_B_DEL_ER_VCM0(self, value):
        """
        Writes the CS_B_DEL_ER_VCM0 bitfield in the CS_B_DEL_ER_VCM0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM0()
        self._BITFIELD['CS_B_DEL_ER_VCM0'] = value
        self.write_CS_B_DEL_ER_VCM0()

    def get_CS_B_DEL_ER_VCM0(self):
        """
        Reads the CS_B_DEL_ER_VCM0 register
        
        :return: the shadow register CS_B_DEL_ER_VCM0.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM0()
        return self._BITFIELD['CS_B_DEL_ER_VCM0']

    def set_CS_B_DEL_ER_VCM1_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM1_SIGN bitfield in the CS_B_DEL_ER_VCM1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM1()
        self._BITFIELD['CS_B_DEL_ER_VCM1_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM1()

    def get_CS_B_DEL_ER_VCM1_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM1 register
        
        :return: the shadow register CS_B_DEL_ER_VCM1_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM1()
        return self._BITFIELD['CS_B_DEL_ER_VCM1_SIGN']

    def set_CS_B_DEL_ER_VCM1(self, value):
        """
        Writes the CS_B_DEL_ER_VCM1 bitfield in the CS_B_DEL_ER_VCM1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM1()
        self._BITFIELD['CS_B_DEL_ER_VCM1'] = value
        self.write_CS_B_DEL_ER_VCM1()

    def get_CS_B_DEL_ER_VCM1(self):
        """
        Reads the CS_B_DEL_ER_VCM1 register
        
        :return: the shadow register CS_B_DEL_ER_VCM1.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM1()
        return self._BITFIELD['CS_B_DEL_ER_VCM1']

    def set_CS_B_DEL_ER_VCM2_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM2_SIGN bitfield in the CS_B_DEL_ER_VCM2 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM2()
        self._BITFIELD['CS_B_DEL_ER_VCM2_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM2()

    def get_CS_B_DEL_ER_VCM2_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM2 register
        
        :return: the shadow register CS_B_DEL_ER_VCM2_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM2()
        return self._BITFIELD['CS_B_DEL_ER_VCM2_SIGN']

    def set_CS_B_DEL_ER_VCM2(self, value):
        """
        Writes the CS_B_DEL_ER_VCM2 bitfield in the CS_B_DEL_ER_VCM2 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM2()
        self._BITFIELD['CS_B_DEL_ER_VCM2'] = value
        self.write_CS_B_DEL_ER_VCM2()

    def get_CS_B_DEL_ER_VCM2(self):
        """
        Reads the CS_B_DEL_ER_VCM2 register
        
        :return: the shadow register CS_B_DEL_ER_VCM2.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM2()
        return self._BITFIELD['CS_B_DEL_ER_VCM2']

    def set_CS_B_DEL_ER_VCM3_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM3_SIGN bitfield in the CS_B_DEL_ER_VCM3 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM3()
        self._BITFIELD['CS_B_DEL_ER_VCM3_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM3()

    def get_CS_B_DEL_ER_VCM3_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM3 register
        
        :return: the shadow register CS_B_DEL_ER_VCM3_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM3()
        return self._BITFIELD['CS_B_DEL_ER_VCM3_SIGN']

    def set_CS_B_DEL_ER_VCM3(self, value):
        """
        Writes the CS_B_DEL_ER_VCM3 bitfield in the CS_B_DEL_ER_VCM3 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM3()
        self._BITFIELD['CS_B_DEL_ER_VCM3'] = value
        self.write_CS_B_DEL_ER_VCM3()

    def get_CS_B_DEL_ER_VCM3(self):
        """
        Reads the CS_B_DEL_ER_VCM3 register
        
        :return: the shadow register CS_B_DEL_ER_VCM3.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM3()
        return self._BITFIELD['CS_B_DEL_ER_VCM3']

    def set_CS_B_DEL_ER_VCM4_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM4_SIGN bitfield in the CS_B_DEL_ER_VCM4 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM4()
        self._BITFIELD['CS_B_DEL_ER_VCM4_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM4()

    def get_CS_B_DEL_ER_VCM4_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM4 register
        
        :return: the shadow register CS_B_DEL_ER_VCM4_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM4()
        return self._BITFIELD['CS_B_DEL_ER_VCM4_SIGN']

    def set_CS_B_DEL_ER_VCM4(self, value):
        """
        Writes the CS_B_DEL_ER_VCM4 bitfield in the CS_B_DEL_ER_VCM4 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM4()
        self._BITFIELD['CS_B_DEL_ER_VCM4'] = value
        self.write_CS_B_DEL_ER_VCM4()

    def get_CS_B_DEL_ER_VCM4(self):
        """
        Reads the CS_B_DEL_ER_VCM4 register
        
        :return: the shadow register CS_B_DEL_ER_VCM4.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM4()
        return self._BITFIELD['CS_B_DEL_ER_VCM4']

    def set_CS_B_DEL_ER_VCM5_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM5_SIGN bitfield in the CS_B_DEL_ER_VCM5 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM5()
        self._BITFIELD['CS_B_DEL_ER_VCM5_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM5()

    def get_CS_B_DEL_ER_VCM5_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM5 register
        
        :return: the shadow register CS_B_DEL_ER_VCM5_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM5()
        return self._BITFIELD['CS_B_DEL_ER_VCM5_SIGN']

    def set_CS_B_DEL_ER_VCM5(self, value):
        """
        Writes the CS_B_DEL_ER_VCM5 bitfield in the CS_B_DEL_ER_VCM5 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM5()
        self._BITFIELD['CS_B_DEL_ER_VCM5'] = value
        self.write_CS_B_DEL_ER_VCM5()

    def get_CS_B_DEL_ER_VCM5(self):
        """
        Reads the CS_B_DEL_ER_VCM5 register
        
        :return: the shadow register CS_B_DEL_ER_VCM5.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM5()
        return self._BITFIELD['CS_B_DEL_ER_VCM5']

    def set_CS_B_DEL_ER_VCM6_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM6_SIGN bitfield in the CS_B_DEL_ER_VCM6 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM6()
        self._BITFIELD['CS_B_DEL_ER_VCM6_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM6()

    def get_CS_B_DEL_ER_VCM6_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM6 register
        
        :return: the shadow register CS_B_DEL_ER_VCM6_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM6()
        return self._BITFIELD['CS_B_DEL_ER_VCM6_SIGN']

    def set_CS_B_DEL_ER_VCM6(self, value):
        """
        Writes the CS_B_DEL_ER_VCM6 bitfield in the CS_B_DEL_ER_VCM6 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM6()
        self._BITFIELD['CS_B_DEL_ER_VCM6'] = value
        self.write_CS_B_DEL_ER_VCM6()

    def get_CS_B_DEL_ER_VCM6(self):
        """
        Reads the CS_B_DEL_ER_VCM6 register
        
        :return: the shadow register CS_B_DEL_ER_VCM6.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM6()
        return self._BITFIELD['CS_B_DEL_ER_VCM6']

    def set_CS_B_DEL_ER_VCM7_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM7_SIGN bitfield in the CS_B_DEL_ER_VCM7 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM7()
        self._BITFIELD['CS_B_DEL_ER_VCM7_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM7()

    def get_CS_B_DEL_ER_VCM7_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM7 register
        
        :return: the shadow register CS_B_DEL_ER_VCM7_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM7()
        return self._BITFIELD['CS_B_DEL_ER_VCM7_SIGN']

    def set_CS_B_DEL_ER_VCM7(self, value):
        """
        Writes the CS_B_DEL_ER_VCM7 bitfield in the CS_B_DEL_ER_VCM7 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM7()
        self._BITFIELD['CS_B_DEL_ER_VCM7'] = value
        self.write_CS_B_DEL_ER_VCM7()

    def get_CS_B_DEL_ER_VCM7(self):
        """
        Reads the CS_B_DEL_ER_VCM7 register
        
        :return: the shadow register CS_B_DEL_ER_VCM7.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM7()
        return self._BITFIELD['CS_B_DEL_ER_VCM7']

    def set_CS_B_DEL_ER_VCM8_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM8_SIGN bitfield in the CS_B_DEL_ER_VCM8 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM8()
        self._BITFIELD['CS_B_DEL_ER_VCM8_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM8()

    def get_CS_B_DEL_ER_VCM8_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM8 register
        
        :return: the shadow register CS_B_DEL_ER_VCM8_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM8()
        return self._BITFIELD['CS_B_DEL_ER_VCM8_SIGN']

    def set_CS_B_DEL_ER_VCM8(self, value):
        """
        Writes the CS_B_DEL_ER_VCM8 bitfield in the CS_B_DEL_ER_VCM8 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM8()
        self._BITFIELD['CS_B_DEL_ER_VCM8'] = value
        self.write_CS_B_DEL_ER_VCM8()

    def get_CS_B_DEL_ER_VCM8(self):
        """
        Reads the CS_B_DEL_ER_VCM8 register
        
        :return: the shadow register CS_B_DEL_ER_VCM8.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM8()
        return self._BITFIELD['CS_B_DEL_ER_VCM8']

    def set_CS_B_DEL_ER_VCM9_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM9_SIGN bitfield in the CS_B_DEL_ER_VCM9 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM9()
        self._BITFIELD['CS_B_DEL_ER_VCM9_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM9()

    def get_CS_B_DEL_ER_VCM9_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM9 register
        
        :return: the shadow register CS_B_DEL_ER_VCM9_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM9()
        return self._BITFIELD['CS_B_DEL_ER_VCM9_SIGN']

    def set_CS_B_DEL_ER_VCM9(self, value):
        """
        Writes the CS_B_DEL_ER_VCM9 bitfield in the CS_B_DEL_ER_VCM9 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM9()
        self._BITFIELD['CS_B_DEL_ER_VCM9'] = value
        self.write_CS_B_DEL_ER_VCM9()

    def get_CS_B_DEL_ER_VCM9(self):
        """
        Reads the CS_B_DEL_ER_VCM9 register
        
        :return: the shadow register CS_B_DEL_ER_VCM9.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM9()
        return self._BITFIELD['CS_B_DEL_ER_VCM9']

    def set_CS_B_DEL_ER_VCM10_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM10_SIGN bitfield in the CS_B_DEL_ER_VCM10 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM10()
        self._BITFIELD['CS_B_DEL_ER_VCM10_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM10()

    def get_CS_B_DEL_ER_VCM10_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM10 register
        
        :return: the shadow register CS_B_DEL_ER_VCM10_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM10()
        return self._BITFIELD['CS_B_DEL_ER_VCM10_SIGN']

    def set_CS_B_DEL_ER_VCM10(self, value):
        """
        Writes the CS_B_DEL_ER_VCM10 bitfield in the CS_B_DEL_ER_VCM10 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM10()
        self._BITFIELD['CS_B_DEL_ER_VCM10'] = value
        self.write_CS_B_DEL_ER_VCM10()

    def get_CS_B_DEL_ER_VCM10(self):
        """
        Reads the CS_B_DEL_ER_VCM10 register
        
        :return: the shadow register CS_B_DEL_ER_VCM10.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM10()
        return self._BITFIELD['CS_B_DEL_ER_VCM10']

    def set_CS_B_DEL_ER_VCM11_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM11_SIGN bitfield in the CS_B_DEL_ER_VCM11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM11()
        self._BITFIELD['CS_B_DEL_ER_VCM11_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM11()

    def get_CS_B_DEL_ER_VCM11_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM11 register
        
        :return: the shadow register CS_B_DEL_ER_VCM11_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM11()
        return self._BITFIELD['CS_B_DEL_ER_VCM11_SIGN']

    def set_CS_B_DEL_ER_VCM11(self, value):
        """
        Writes the CS_B_DEL_ER_VCM11 bitfield in the CS_B_DEL_ER_VCM11 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM11()
        self._BITFIELD['CS_B_DEL_ER_VCM11'] = value
        self.write_CS_B_DEL_ER_VCM11()

    def get_CS_B_DEL_ER_VCM11(self):
        """
        Reads the CS_B_DEL_ER_VCM11 register
        
        :return: the shadow register CS_B_DEL_ER_VCM11.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM11()
        return self._BITFIELD['CS_B_DEL_ER_VCM11']

    def set_CS_B_DEL_ER_VCM12_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM12_SIGN bitfield in the CS_B_DEL_ER_VCM12 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM12()
        self._BITFIELD['CS_B_DEL_ER_VCM12_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM12()

    def get_CS_B_DEL_ER_VCM12_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM12 register
        
        :return: the shadow register CS_B_DEL_ER_VCM12_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM12()
        return self._BITFIELD['CS_B_DEL_ER_VCM12_SIGN']

    def set_CS_B_DEL_ER_VCM12(self, value):
        """
        Writes the CS_B_DEL_ER_VCM12 bitfield in the CS_B_DEL_ER_VCM12 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM12()
        self._BITFIELD['CS_B_DEL_ER_VCM12'] = value
        self.write_CS_B_DEL_ER_VCM12()

    def get_CS_B_DEL_ER_VCM12(self):
        """
        Reads the CS_B_DEL_ER_VCM12 register
        
        :return: the shadow register CS_B_DEL_ER_VCM12.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM12()
        return self._BITFIELD['CS_B_DEL_ER_VCM12']

    def set_CS_B_DEL_ER_VCM13_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM13_SIGN bitfield in the CS_B_DEL_ER_VCM13 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM13()
        self._BITFIELD['CS_B_DEL_ER_VCM13_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM13()

    def get_CS_B_DEL_ER_VCM13_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM13 register
        
        :return: the shadow register CS_B_DEL_ER_VCM13_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM13()
        return self._BITFIELD['CS_B_DEL_ER_VCM13_SIGN']

    def set_CS_B_DEL_ER_VCM13(self, value):
        """
        Writes the CS_B_DEL_ER_VCM13 bitfield in the CS_B_DEL_ER_VCM13 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM13()
        self._BITFIELD['CS_B_DEL_ER_VCM13'] = value
        self.write_CS_B_DEL_ER_VCM13()

    def get_CS_B_DEL_ER_VCM13(self):
        """
        Reads the CS_B_DEL_ER_VCM13 register
        
        :return: the shadow register CS_B_DEL_ER_VCM13.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM13()
        return self._BITFIELD['CS_B_DEL_ER_VCM13']

    def set_CS_B_DEL_ER_VCM14_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM14_SIGN bitfield in the CS_B_DEL_ER_VCM14 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM14()
        self._BITFIELD['CS_B_DEL_ER_VCM14_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM14()

    def get_CS_B_DEL_ER_VCM14_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM14 register
        
        :return: the shadow register CS_B_DEL_ER_VCM14_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM14()
        return self._BITFIELD['CS_B_DEL_ER_VCM14_SIGN']

    def set_CS_B_DEL_ER_VCM14(self, value):
        """
        Writes the CS_B_DEL_ER_VCM14 bitfield in the CS_B_DEL_ER_VCM14 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM14()
        self._BITFIELD['CS_B_DEL_ER_VCM14'] = value
        self.write_CS_B_DEL_ER_VCM14()

    def get_CS_B_DEL_ER_VCM14(self):
        """
        Reads the CS_B_DEL_ER_VCM14 register
        
        :return: the shadow register CS_B_DEL_ER_VCM14.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM14()
        return self._BITFIELD['CS_B_DEL_ER_VCM14']

    def set_CS_B_DEL_ER_VCM15_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM15_SIGN bitfield in the CS_B_DEL_ER_VCM15 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM15()
        self._BITFIELD['CS_B_DEL_ER_VCM15_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM15()

    def get_CS_B_DEL_ER_VCM15_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM15 register
        
        :return: the shadow register CS_B_DEL_ER_VCM15_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM15()
        return self._BITFIELD['CS_B_DEL_ER_VCM15_SIGN']

    def set_CS_B_DEL_ER_VCM15(self, value):
        """
        Writes the CS_B_DEL_ER_VCM15 bitfield in the CS_B_DEL_ER_VCM15 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM15()
        self._BITFIELD['CS_B_DEL_ER_VCM15'] = value
        self.write_CS_B_DEL_ER_VCM15()

    def get_CS_B_DEL_ER_VCM15(self):
        """
        Reads the CS_B_DEL_ER_VCM15 register
        
        :return: the shadow register CS_B_DEL_ER_VCM15.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM15()
        return self._BITFIELD['CS_B_DEL_ER_VCM15']

    def set_CS_B_DEL_ER_VCM16_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM16_SIGN bitfield in the CS_B_DEL_ER_VCM16 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM16()
        self._BITFIELD['CS_B_DEL_ER_VCM16_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM16()

    def get_CS_B_DEL_ER_VCM16_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM16 register
        
        :return: the shadow register CS_B_DEL_ER_VCM16_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM16()
        return self._BITFIELD['CS_B_DEL_ER_VCM16_SIGN']

    def set_CS_B_DEL_ER_VCM16(self, value):
        """
        Writes the CS_B_DEL_ER_VCM16 bitfield in the CS_B_DEL_ER_VCM16 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM16()
        self._BITFIELD['CS_B_DEL_ER_VCM16'] = value
        self.write_CS_B_DEL_ER_VCM16()

    def get_CS_B_DEL_ER_VCM16(self):
        """
        Reads the CS_B_DEL_ER_VCM16 register
        
        :return: the shadow register CS_B_DEL_ER_VCM16.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM16()
        return self._BITFIELD['CS_B_DEL_ER_VCM16']

    def set_CS_B_DEL_ER_VCM17_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM17_SIGN bitfield in the CS_B_DEL_ER_VCM17 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM17()
        self._BITFIELD['CS_B_DEL_ER_VCM17_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM17()

    def get_CS_B_DEL_ER_VCM17_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM17 register
        
        :return: the shadow register CS_B_DEL_ER_VCM17_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM17()
        return self._BITFIELD['CS_B_DEL_ER_VCM17_SIGN']

    def set_CS_B_DEL_ER_VCM17(self, value):
        """
        Writes the CS_B_DEL_ER_VCM17 bitfield in the CS_B_DEL_ER_VCM17 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM17()
        self._BITFIELD['CS_B_DEL_ER_VCM17'] = value
        self.write_CS_B_DEL_ER_VCM17()

    def get_CS_B_DEL_ER_VCM17(self):
        """
        Reads the CS_B_DEL_ER_VCM17 register
        
        :return: the shadow register CS_B_DEL_ER_VCM17.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM17()
        return self._BITFIELD['CS_B_DEL_ER_VCM17']

    def set_CS_B_DEL_ER_VCM18_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM18_SIGN bitfield in the CS_B_DEL_ER_VCM18 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM18()
        self._BITFIELD['CS_B_DEL_ER_VCM18_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM18()

    def get_CS_B_DEL_ER_VCM18_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM18 register
        
        :return: the shadow register CS_B_DEL_ER_VCM18_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM18()
        return self._BITFIELD['CS_B_DEL_ER_VCM18_SIGN']

    def set_CS_B_DEL_ER_VCM18(self, value):
        """
        Writes the CS_B_DEL_ER_VCM18 bitfield in the CS_B_DEL_ER_VCM18 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM18()
        self._BITFIELD['CS_B_DEL_ER_VCM18'] = value
        self.write_CS_B_DEL_ER_VCM18()

    def get_CS_B_DEL_ER_VCM18(self):
        """
        Reads the CS_B_DEL_ER_VCM18 register
        
        :return: the shadow register CS_B_DEL_ER_VCM18.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM18()
        return self._BITFIELD['CS_B_DEL_ER_VCM18']

    def set_CS_B_DEL_ER_VCM19_SIGN(self, value):
        """
        Writes the CS_B_DEL_ER_VCM19_SIGN bitfield in the CS_B_DEL_ER_VCM19 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM19()
        self._BITFIELD['CS_B_DEL_ER_VCM19_SIGN'] = value
        self.write_CS_B_DEL_ER_VCM19()

    def get_CS_B_DEL_ER_VCM19_SIGN(self):
        """
        Reads the CS_B_DEL_ER_VCM19 register
        
        :return: the shadow register CS_B_DEL_ER_VCM19_SIGN.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM19()
        return self._BITFIELD['CS_B_DEL_ER_VCM19_SIGN']

    def set_CS_B_DEL_ER_VCM19(self, value):
        """
        Writes the CS_B_DEL_ER_VCM19 bitfield in the CS_B_DEL_ER_VCM19 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_B_DEL_ER_VCM19()
        self._BITFIELD['CS_B_DEL_ER_VCM19'] = value
        self.write_CS_B_DEL_ER_VCM19()

    def get_CS_B_DEL_ER_VCM19(self):
        """
        Reads the CS_B_DEL_ER_VCM19 register
        
        :return: the shadow register CS_B_DEL_ER_VCM19.
        :rtype: int
        """
        self.read_CS_B_DEL_ER_VCM19()
        return self._BITFIELD['CS_B_DEL_ER_VCM19']

    def set_CMD_STATUS(self, value):
        """
        Writes the CMD_STATUS bitfield in the EEPROM_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_EEPROM_CNTL()
        self._BITFIELD['CMD_STATUS'] = value
        self.write_EEPROM_CNTL()

    def get_CMD_STATUS(self):
        """
        Reads the EEPROM_CNTL register
        
        :return: the shadow register CMD_STATUS.
        :rtype: int
        """
        self.read_EEPROM_CNTL()
        return self._BITFIELD['CMD_STATUS']

    def set_RSVD_7_2_EEPROM_CFG(self, value):
        """
         Read Only bit field RSVD_7_2_EEPROM_CFG in the EEPROM_CFG register. Skip the write.
        """

    def get_RSVD_7_2_EEPROM_CFG(self):
        """
        Reads the EEPROM_CFG register
        
        :return: the shadow register RSVD_7_2_EEPROM_CFG.
        :rtype: int
        """
        self.read_EEPROM_CFG()
        return self._BITFIELD['RSVD_7_2_EEPROM_CFG']

    def set_E2P_FAST_MODE(self, value):
        """
        Writes the E2P_FAST_MODE bitfield in the EEPROM_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_EEPROM_CFG()
        self._BITFIELD['E2P_FAST_MODE'] = value
        self.write_EEPROM_CFG()

    def get_E2P_FAST_MODE(self):
        """
        Reads the EEPROM_CFG register
        
        :return: the shadow register E2P_FAST_MODE.
        :rtype: int
        """
        self.read_EEPROM_CFG()
        return self._BITFIELD['E2P_FAST_MODE']

    def set_ECC_DIS(self, value):
        """
        Writes the ECC_DIS bitfield in the EEPROM_CFG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_EEPROM_CFG()
        self._BITFIELD['ECC_DIS'] = value
        self.write_EEPROM_CFG()

    def get_ECC_DIS(self):
        """
        Reads the EEPROM_CFG register
        
        :return: the shadow register ECC_DIS.
        :rtype: int
        """
        self.read_EEPROM_CFG()
        return self._BITFIELD['ECC_DIS']

    def set_KEY_STATUS(self, value):
        """
        Writes the KEY_STATUS bitfield in the TEST_KEY register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_TEST_KEY()
        self._BITFIELD['KEY_STATUS'] = value
        self.write_TEST_KEY()

    def get_KEY_STATUS(self):
        """
        Reads the TEST_KEY register
        
        :return: the shadow register KEY_STATUS.
        :rtype: int
        """
        self.read_TEST_KEY()
        return self._BITFIELD['KEY_STATUS']

    def set_TRIM_DIS(self, value):
        """
        Writes the TRIM_DIS bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['TRIM_DIS'] = value
        self.write_DTEST_CNTL0()

    def get_TRIM_DIS(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register TRIM_DIS.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['TRIM_DIS']

    def set_OSC_CLK_DIS(self, value):
        """
        Writes the OSC_CLK_DIS bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['OSC_CLK_DIS'] = value
        self.write_DTEST_CNTL0()

    def get_OSC_CLK_DIS(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register OSC_CLK_DIS.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['OSC_CLK_DIS']

    def set_ADC_TEST(self, value):
        """
        Writes the ADC_TEST bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['ADC_TEST'] = value
        self.write_DTEST_CNTL0()

    def get_ADC_TEST(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register ADC_TEST.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['ADC_TEST']

    def set_OSC_TEST_ENABLE(self, value):
        """
        Writes the OSC_TEST_ENABLE bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['OSC_TEST_ENABLE'] = value
        self.write_DTEST_CNTL0()

    def get_OSC_TEST_ENABLE(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register OSC_TEST_ENABLE.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['OSC_TEST_ENABLE']

    def set_TRACE_PORT(self, value):
        """
        Writes the TRACE_PORT bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['TRACE_PORT'] = value
        self.write_DTEST_CNTL0()

    def get_TRACE_PORT(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register TRACE_PORT.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['TRACE_PORT']

    def set_OSC_CLK_EXT(self, value):
        """
        Writes the OSC_CLK_EXT bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['OSC_CLK_EXT'] = value
        self.write_DTEST_CNTL0()

    def get_OSC_CLK_EXT(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register OSC_CLK_EXT.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['OSC_CLK_EXT']

    def set_IO_TEST(self, value):
        """
        Writes the IO_TEST bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['IO_TEST'] = value
        self.write_DTEST_CNTL0()

    def get_IO_TEST(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register IO_TEST.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['IO_TEST']

    def set_SCAN_TEST(self, value):
        """
        Writes the SCAN_TEST bitfield in the DTEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DTEST_CNTL0()
        self._BITFIELD['SCAN_TEST'] = value
        self.write_DTEST_CNTL0()

    def get_SCAN_TEST(self):
        """
        Reads the DTEST_CNTL0 register
        
        :return: the shadow register SCAN_TEST.
        :rtype: int
        """
        self.read_DTEST_CNTL0()
        return self._BITFIELD['SCAN_TEST']

    def set_RSVD_7_5_ADC_TEST_CNTL(self, value):
        """
         Read Only bit field RSVD_7_5_ADC_TEST_CNTL in the ADC_TEST_CNTL register. Skip the write.
        """

    def get_RSVD_7_5_ADC_TEST_CNTL(self):
        """
        Reads the ADC_TEST_CNTL register
        
        :return: the shadow register RSVD_7_5_ADC_TEST_CNTL.
        :rtype: int
        """
        self.read_ADC_TEST_CNTL()
        return self._BITFIELD['RSVD_7_5_ADC_TEST_CNTL']

    def set_ADC_VCM_EN_SEL(self, value):
        """
        Writes the ADC_VCM_EN_SEL bitfield in the ADC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TEST_CNTL()
        self._BITFIELD['ADC_VCM_EN_SEL'] = value
        self.write_ADC_TEST_CNTL()

    def get_ADC_VCM_EN_SEL(self):
        """
        Reads the ADC_TEST_CNTL register
        
        :return: the shadow register ADC_VCM_EN_SEL.
        :rtype: int
        """
        self.read_ADC_TEST_CNTL()
        return self._BITFIELD['ADC_VCM_EN_SEL']

    def set_ADC_CAL_TM_EN(self, value):
        """
        Writes the ADC_CAL_TM_EN bitfield in the ADC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TEST_CNTL()
        self._BITFIELD['ADC_CAL_TM_EN'] = value
        self.write_ADC_TEST_CNTL()

    def get_ADC_CAL_TM_EN(self):
        """
        Reads the ADC_TEST_CNTL register
        
        :return: the shadow register ADC_CAL_TM_EN.
        :rtype: int
        """
        self.read_ADC_TEST_CNTL()
        return self._BITFIELD['ADC_CAL_TM_EN']

    def set_ADC_CAL_OFFSET_EN(self, value):
        """
        Writes the ADC_CAL_OFFSET_EN bitfield in the ADC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TEST_CNTL()
        self._BITFIELD['ADC_CAL_OFFSET_EN'] = value
        self.write_ADC_TEST_CNTL()

    def get_ADC_CAL_OFFSET_EN(self):
        """
        Reads the ADC_TEST_CNTL register
        
        :return: the shadow register ADC_CAL_OFFSET_EN.
        :rtype: int
        """
        self.read_ADC_TEST_CNTL()
        return self._BITFIELD['ADC_CAL_OFFSET_EN']

    def set_ADC_LDO_EN(self, value):
        """
        Writes the ADC_LDO_EN bitfield in the ADC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TEST_CNTL()
        self._BITFIELD['ADC_LDO_EN'] = value
        self.write_ADC_TEST_CNTL()

    def get_ADC_LDO_EN(self):
        """
        Reads the ADC_TEST_CNTL register
        
        :return: the shadow register ADC_LDO_EN.
        :rtype: int
        """
        self.read_ADC_TEST_CNTL()
        return self._BITFIELD['ADC_LDO_EN']

    def set_ADC_VCM_EN(self, value):
        """
        Writes the ADC_VCM_EN bitfield in the ADC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_TEST_CNTL()
        self._BITFIELD['ADC_VCM_EN'] = value
        self.write_ADC_TEST_CNTL()

    def get_ADC_VCM_EN(self):
        """
        Reads the ADC_TEST_CNTL register
        
        :return: the shadow register ADC_VCM_EN.
        :rtype: int
        """
        self.read_ADC_TEST_CNTL()
        return self._BITFIELD['ADC_VCM_EN']

    def set_ATEST_CNTL0(self, value):
        """
        Writes the ATEST_CNTL0 bitfield in the ATEST_CNTL0 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ATEST_CNTL0()
        self._BITFIELD['ATEST_CNTL0'] = value
        self.write_ATEST_CNTL0()

    def get_ATEST_CNTL0(self):
        """
        Reads the ATEST_CNTL0 register
        
        :return: the shadow register ATEST_CNTL0.
        :rtype: int
        """
        self.read_ATEST_CNTL0()
        return self._BITFIELD['ATEST_CNTL0']

    def set_RSVD_7_ANA_DFT_CTRL(self, value):
        """
        Writes the RSVD_7_ANA_DFT_CTRL bitfield in the ANA_DFT_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_CTRL()
        self._BITFIELD['RSVD_7_ANA_DFT_CTRL'] = value
        self.write_ANA_DFT_CTRL()

    def get_RSVD_7_ANA_DFT_CTRL(self):
        """
        Reads the ANA_DFT_CTRL register
        
        :return: the shadow register RSVD_7_ANA_DFT_CTRL.
        :rtype: int
        """
        self.read_ANA_DFT_CTRL()
        return self._BITFIELD['RSVD_7_ANA_DFT_CTRL']

    def set_EN_BYPASS_ANA_DFT_BUF(self, value):
        """
        Writes the EN_BYPASS_ANA_DFT_BUF bitfield in the ANA_DFT_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_CTRL()
        self._BITFIELD['EN_BYPASS_ANA_DFT_BUF'] = value
        self.write_ANA_DFT_CTRL()

    def get_EN_BYPASS_ANA_DFT_BUF(self):
        """
        Reads the ANA_DFT_CTRL register
        
        :return: the shadow register EN_BYPASS_ANA_DFT_BUF.
        :rtype: int
        """
        self.read_ANA_DFT_CTRL()
        return self._BITFIELD['EN_BYPASS_ANA_DFT_BUF']

    def set_EN_RES_LADDER_CALIB(self, value):
        """
        Writes the EN_RES_LADDER_CALIB bitfield in the ANA_DFT_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_CTRL()
        self._BITFIELD['EN_RES_LADDER_CALIB'] = value
        self.write_ANA_DFT_CTRL()

    def get_EN_RES_LADDER_CALIB(self):
        """
        Reads the ANA_DFT_CTRL register
        
        :return: the shadow register EN_RES_LADDER_CALIB.
        :rtype: int
        """
        self.read_ANA_DFT_CTRL()
        return self._BITFIELD['EN_RES_LADDER_CALIB']

    def set_RES_DIV_SEL(self, value):
        """
        Writes the RES_DIV_SEL bitfield in the ANA_DFT_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_CTRL()
        self._BITFIELD['RES_DIV_SEL'] = value
        self.write_ANA_DFT_CTRL()

    def get_RES_DIV_SEL(self):
        """
        Reads the ANA_DFT_CTRL register
        
        :return: the shadow register RES_DIV_SEL.
        :rtype: int
        """
        self.read_ANA_DFT_CTRL()
        return self._BITFIELD['RES_DIV_SEL']

    def set_EN_RES_DIV(self, value):
        """
        Writes the EN_RES_DIV bitfield in the ANA_DFT_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_CTRL()
        self._BITFIELD['EN_RES_DIV'] = value
        self.write_ANA_DFT_CTRL()

    def get_EN_RES_DIV(self):
        """
        Reads the ANA_DFT_CTRL register
        
        :return: the shadow register EN_RES_DIV.
        :rtype: int
        """
        self.read_ANA_DFT_CTRL()
        return self._BITFIELD['EN_RES_DIV']

    def set_EN_DIRECT_PATH(self, value):
        """
        Writes the EN_DIRECT_PATH bitfield in the ANA_DFT_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_CTRL()
        self._BITFIELD['EN_DIRECT_PATH'] = value
        self.write_ANA_DFT_CTRL()

    def get_EN_DIRECT_PATH(self):
        """
        Reads the ANA_DFT_CTRL register
        
        :return: the shadow register EN_DIRECT_PATH.
        :rtype: int
        """
        self.read_ANA_DFT_CTRL()
        return self._BITFIELD['EN_DIRECT_PATH']

    def set_EN_ANA_DFT_BUFFER(self, value):
        """
        Writes the EN_ANA_DFT_BUFFER bitfield in the ANA_DFT_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_CTRL()
        self._BITFIELD['EN_ANA_DFT_BUFFER'] = value
        self.write_ANA_DFT_CTRL()

    def get_EN_ANA_DFT_BUFFER(self):
        """
        Reads the ANA_DFT_CTRL register
        
        :return: the shadow register EN_ANA_DFT_BUFFER.
        :rtype: int
        """
        self.read_ANA_DFT_CTRL()
        return self._BITFIELD['EN_ANA_DFT_BUFFER']

    def set_RSVD_7_4_ANA_DFT_MUX_CTRL(self, value):
        """
        Writes the RSVD_7_4_ANA_DFT_MUX_CTRL bitfield in the ANA_DFT_MUX_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_MUX_CTRL()
        self._BITFIELD['RSVD_7_4_ANA_DFT_MUX_CTRL'] = value
        self.write_ANA_DFT_MUX_CTRL()

    def get_RSVD_7_4_ANA_DFT_MUX_CTRL(self):
        """
        Reads the ANA_DFT_MUX_CTRL register
        
        :return: the shadow register RSVD_7_4_ANA_DFT_MUX_CTRL.
        :rtype: int
        """
        self.read_ANA_DFT_MUX_CTRL()
        return self._BITFIELD['RSVD_7_4_ANA_DFT_MUX_CTRL']

    def set_ANA_DFT_MUX_SEL(self, value):
        """
        Writes the ANA_DFT_MUX_SEL bitfield in the ANA_DFT_MUX_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_MUX_CTRL()
        self._BITFIELD['ANA_DFT_MUX_SEL'] = value
        self.write_ANA_DFT_MUX_CTRL()

    def get_ANA_DFT_MUX_SEL(self):
        """
        Reads the ANA_DFT_MUX_CTRL register
        
        :return: the shadow register ANA_DFT_MUX_SEL.
        :rtype: int
        """
        self.read_ANA_DFT_MUX_CTRL()
        return self._BITFIELD['ANA_DFT_MUX_SEL']

    def set_EN_ANA_DFT_MUX(self, value):
        """
        Writes the EN_ANA_DFT_MUX bitfield in the ANA_DFT_MUX_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANA_DFT_MUX_CTRL()
        self._BITFIELD['EN_ANA_DFT_MUX'] = value
        self.write_ANA_DFT_MUX_CTRL()

    def get_EN_ANA_DFT_MUX(self):
        """
        Reads the ANA_DFT_MUX_CTRL register
        
        :return: the shadow register EN_ANA_DFT_MUX.
        :rtype: int
        """
        self.read_ANA_DFT_MUX_CTRL()
        return self._BITFIELD['EN_ANA_DFT_MUX']

    def set_RSVD_7_5_LDO_TRIM_VDDD(self, value):
        """
        Writes the RSVD_7_5_LDO_TRIM_VDDD bitfield in the LDO_TRIM_VDDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_VDDD()
        self._BITFIELD['RSVD_7_5_LDO_TRIM_VDDD'] = value
        self.write_LDO_TRIM_VDDD()

    def get_RSVD_7_5_LDO_TRIM_VDDD(self):
        """
        Reads the LDO_TRIM_VDDD register
        
        :return: the shadow register RSVD_7_5_LDO_TRIM_VDDD.
        :rtype: int
        """
        self.read_LDO_TRIM_VDDD()
        return self._BITFIELD['RSVD_7_5_LDO_TRIM_VDDD']

    def set_LDO_TRIM_VDDD_CURRENT_20MA(self, value):
        """
        Writes the LDO_TRIM_VDDD_CURRENT_20MA bitfield in the LDO_TRIM_VDDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_VDDD()
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_20MA'] = value
        self.write_LDO_TRIM_VDDD()

    def get_LDO_TRIM_VDDD_CURRENT_20MA(self):
        """
        Reads the LDO_TRIM_VDDD register
        
        :return: the shadow register LDO_TRIM_VDDD_CURRENT_20MA.
        :rtype: int
        """
        self.read_LDO_TRIM_VDDD()
        return self._BITFIELD['LDO_TRIM_VDDD_CURRENT_20MA']

    def set_LDO_TRIM_VDDD_CURRENT_10MA(self, value):
        """
        Writes the LDO_TRIM_VDDD_CURRENT_10MA bitfield in the LDO_TRIM_VDDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_VDDD()
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_10MA'] = value
        self.write_LDO_TRIM_VDDD()

    def get_LDO_TRIM_VDDD_CURRENT_10MA(self):
        """
        Reads the LDO_TRIM_VDDD register
        
        :return: the shadow register LDO_TRIM_VDDD_CURRENT_10MA.
        :rtype: int
        """
        self.read_LDO_TRIM_VDDD()
        return self._BITFIELD['LDO_TRIM_VDDD_CURRENT_10MA']

    def set_LDO_TRIM_VDDD_CURRENT_5MA(self, value):
        """
        Writes the LDO_TRIM_VDDD_CURRENT_5MA bitfield in the LDO_TRIM_VDDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_VDDD()
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_5MA'] = value
        self.write_LDO_TRIM_VDDD()

    def get_LDO_TRIM_VDDD_CURRENT_5MA(self):
        """
        Reads the LDO_TRIM_VDDD register
        
        :return: the shadow register LDO_TRIM_VDDD_CURRENT_5MA.
        :rtype: int
        """
        self.read_LDO_TRIM_VDDD()
        return self._BITFIELD['LDO_TRIM_VDDD_CURRENT_5MA']

    def set_LDO_TRIM_VDDD_BOOST_1P9V(self, value):
        """
        Writes the LDO_TRIM_VDDD_BOOST_1P9V bitfield in the LDO_TRIM_VDDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_VDDD()
        self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P9V'] = value
        self.write_LDO_TRIM_VDDD()

    def get_LDO_TRIM_VDDD_BOOST_1P9V(self):
        """
        Reads the LDO_TRIM_VDDD register
        
        :return: the shadow register LDO_TRIM_VDDD_BOOST_1P9V.
        :rtype: int
        """
        self.read_LDO_TRIM_VDDD()
        return self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P9V']

    def set_LDO_TRIM_VDDD_BOOST_1P85V(self, value):
        """
        Writes the LDO_TRIM_VDDD_BOOST_1P85V bitfield in the LDO_TRIM_VDDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_VDDD()
        self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P85V'] = value
        self.write_LDO_TRIM_VDDD()

    def get_LDO_TRIM_VDDD_BOOST_1P85V(self):
        """
        Reads the LDO_TRIM_VDDD register
        
        :return: the shadow register LDO_TRIM_VDDD_BOOST_1P85V.
        :rtype: int
        """
        self.read_LDO_TRIM_VDDD()
        return self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P85V']

    def set_RSVD_7_5_LDO_TRIM_IOVDD(self, value):
        """
        Writes the RSVD_7_5_LDO_TRIM_IOVDD bitfield in the LDO_TRIM_IOVDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_IOVDD()
        self._BITFIELD['RSVD_7_5_LDO_TRIM_IOVDD'] = value
        self.write_LDO_TRIM_IOVDD()

    def get_RSVD_7_5_LDO_TRIM_IOVDD(self):
        """
        Reads the LDO_TRIM_IOVDD register
        
        :return: the shadow register RSVD_7_5_LDO_TRIM_IOVDD.
        :rtype: int
        """
        self.read_LDO_TRIM_IOVDD()
        return self._BITFIELD['RSVD_7_5_LDO_TRIM_IOVDD']

    def set_LDO_TRIM_IOVDD_CURRENT_20MA(self, value):
        """
        Writes the LDO_TRIM_IOVDD_CURRENT_20MA bitfield in the LDO_TRIM_IOVDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_IOVDD()
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_20MA'] = value
        self.write_LDO_TRIM_IOVDD()

    def get_LDO_TRIM_IOVDD_CURRENT_20MA(self):
        """
        Reads the LDO_TRIM_IOVDD register
        
        :return: the shadow register LDO_TRIM_IOVDD_CURRENT_20MA.
        :rtype: int
        """
        self.read_LDO_TRIM_IOVDD()
        return self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_20MA']

    def set_LDO_TRIM_IOVDD_CURRENT_10MA(self, value):
        """
        Writes the LDO_TRIM_IOVDD_CURRENT_10MA bitfield in the LDO_TRIM_IOVDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_IOVDD()
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_10MA'] = value
        self.write_LDO_TRIM_IOVDD()

    def get_LDO_TRIM_IOVDD_CURRENT_10MA(self):
        """
        Reads the LDO_TRIM_IOVDD register
        
        :return: the shadow register LDO_TRIM_IOVDD_CURRENT_10MA.
        :rtype: int
        """
        self.read_LDO_TRIM_IOVDD()
        return self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_10MA']

    def set_LDO_TRIM_IOVDD_CURRENT_5MA(self, value):
        """
        Writes the LDO_TRIM_IOVDD_CURRENT_5MA bitfield in the LDO_TRIM_IOVDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_IOVDD()
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_5MA'] = value
        self.write_LDO_TRIM_IOVDD()

    def get_LDO_TRIM_IOVDD_CURRENT_5MA(self):
        """
        Reads the LDO_TRIM_IOVDD register
        
        :return: the shadow register LDO_TRIM_IOVDD_CURRENT_5MA.
        :rtype: int
        """
        self.read_LDO_TRIM_IOVDD()
        return self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_5MA']

    def set_LDO_TRIM_IOVDD_BOOST_1P9V(self, value):
        """
        Writes the LDO_TRIM_IOVDD_BOOST_1P9V bitfield in the LDO_TRIM_IOVDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_IOVDD()
        self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P9V'] = value
        self.write_LDO_TRIM_IOVDD()

    def get_LDO_TRIM_IOVDD_BOOST_1P9V(self):
        """
        Reads the LDO_TRIM_IOVDD register
        
        :return: the shadow register LDO_TRIM_IOVDD_BOOST_1P9V.
        :rtype: int
        """
        self.read_LDO_TRIM_IOVDD()
        return self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P9V']

    def set_LDO_TRIM_IOVDD_BOOST_1P85V(self, value):
        """
        Writes the LDO_TRIM_IOVDD_BOOST_1P85V bitfield in the LDO_TRIM_IOVDD register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_LDO_TRIM_IOVDD()
        self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P85V'] = value
        self.write_LDO_TRIM_IOVDD()

    def get_LDO_TRIM_IOVDD_BOOST_1P85V(self):
        """
        Reads the LDO_TRIM_IOVDD register
        
        :return: the shadow register LDO_TRIM_IOVDD_BOOST_1P85V.
        :rtype: int
        """
        self.read_LDO_TRIM_IOVDD()
        return self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P85V']

    def set_ANATOP6(self, value):
        """
        Writes the ANATOP6 bitfield in the ANATOP6 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANATOP6()
        self._BITFIELD['ANATOP6'] = value
        self.write_ANATOP6()

    def get_ANATOP6(self):
        """
        Reads the ANATOP6 register
        
        :return: the shadow register ANATOP6.
        :rtype: int
        """
        self.read_ANATOP6()
        return self._BITFIELD['ANATOP6']

    def set_ANATOP7(self, value):
        """
        Writes the ANATOP7 bitfield in the ANATOP7 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANATOP7()
        self._BITFIELD['ANATOP7'] = value
        self.write_ANATOP7()

    def get_ANATOP7(self):
        """
        Reads the ANATOP7 register
        
        :return: the shadow register ANATOP7.
        :rtype: int
        """
        self.read_ANATOP7()
        return self._BITFIELD['ANATOP7']

    def set_ANATOP8(self, value):
        """
        Writes the ANATOP8 bitfield in the ANATOP8 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANATOP8()
        self._BITFIELD['ANATOP8'] = value
        self.write_ANATOP8()

    def get_ANATOP8(self):
        """
        Reads the ANATOP8 register
        
        :return: the shadow register ANATOP8.
        :rtype: int
        """
        self.read_ANATOP8()
        return self._BITFIELD['ANATOP8']

    def set_ANATOP9(self, value):
        """
        Writes the ANATOP9 bitfield in the ANATOP9 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ANATOP9()
        self._BITFIELD['ANATOP9'] = value
        self.write_ANATOP9()

    def get_ANATOP9(self):
        """
        Reads the ANATOP9 register
        
        :return: the shadow register ANATOP9.
        :rtype: int
        """
        self.read_ANATOP9()
        return self._BITFIELD['ANATOP9']

    def set_RSVD_7_5_GPIO_TRACE(self, value):
        """
         Read Only bit field RSVD_7_5_GPIO_TRACE in the GPIO_TRACE register. Skip the write.
        """

    def get_RSVD_7_5_GPIO_TRACE(self):
        """
        Reads the GPIO_TRACE register
        
        :return: the shadow register RSVD_7_5_GPIO_TRACE.
        :rtype: int
        """
        self.read_GPIO_TRACE()
        return self._BITFIELD['RSVD_7_5_GPIO_TRACE']

    def set_GPIO_TRACE(self, value):
        """
        Writes the GPIO_TRACE bitfield in the GPIO_TRACE register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_TRACE()
        self._BITFIELD['GPIO_TRACE'] = value
        self.write_GPIO_TRACE()

    def get_GPIO_TRACE(self):
        """
        Reads the GPIO_TRACE register
        
        :return: the shadow register GPIO_TRACE.
        :rtype: int
        """
        self.read_GPIO_TRACE()
        return self._BITFIELD['GPIO_TRACE']

    def set_RSVD_7_1_ATEST_CNTL1(self, value):
        """
         Read Only bit field RSVD_7_1_ATEST_CNTL1 in the ATEST_CNTL1 register. Skip the write.
        """

    def get_RSVD_7_1_ATEST_CNTL1(self):
        """
        Reads the ATEST_CNTL1 register
        
        :return: the shadow register RSVD_7_1_ATEST_CNTL1.
        :rtype: int
        """
        self.read_ATEST_CNTL1()
        return self._BITFIELD['RSVD_7_1_ATEST_CNTL1']

    def set_SPIKE_FILTER_TEST_MODE(self, value):
        """
        Writes the SPIKE_FILTER_TEST_MODE bitfield in the ATEST_CNTL1 register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ATEST_CNTL1()
        self._BITFIELD['SPIKE_FILTER_TEST_MODE'] = value
        self.write_ATEST_CNTL1()

    def get_SPIKE_FILTER_TEST_MODE(self):
        """
        Reads the ATEST_CNTL1 register
        
        :return: the shadow register SPIKE_FILTER_TEST_MODE.
        :rtype: int
        """
        self.read_ATEST_CNTL1()
        return self._BITFIELD['SPIKE_FILTER_TEST_MODE']

    def set_POR_BYPASS_L(self, value):
        """
        Writes the POR_BYPASS_L bitfield in the POR_BYPASS_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_POR_BYPASS_L()
        self._BITFIELD['POR_BYPASS_L'] = value
        self.write_POR_BYPASS_L()

    def get_POR_BYPASS_L(self):
        """
        Reads the POR_BYPASS_L register
        
        :return: the shadow register POR_BYPASS_L.
        :rtype: int
        """
        self.read_POR_BYPASS_L()
        return self._BITFIELD['POR_BYPASS_L']

    def set_POR_BYPASS_H(self, value):
        """
        Writes the POR_BYPASS_H bitfield in the POR_BYPASS_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_POR_BYPASS_H()
        self._BITFIELD['POR_BYPASS_H'] = value
        self.write_POR_BYPASS_H()

    def get_POR_BYPASS_H(self):
        """
        Reads the POR_BYPASS_H register
        
        :return: the shadow register POR_BYPASS_H.
        :rtype: int
        """
        self.read_POR_BYPASS_H()
        return self._BITFIELD['POR_BYPASS_H']

    def set_CLK_CNT_CMP_L(self, value):
        """
        Writes the CLK_CNT_CMP_L bitfield in the OSC_CNT_CMP_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OSC_CNT_CMP_L()
        self._BITFIELD['CLK_CNT_CMP_L'] = value
        self.write_OSC_CNT_CMP_L()

    def get_CLK_CNT_CMP_L(self):
        """
        Reads the OSC_CNT_CMP_L register
        
        :return: the shadow register CLK_CNT_CMP_L.
        :rtype: int
        """
        self.read_OSC_CNT_CMP_L()
        return self._BITFIELD['CLK_CNT_CMP_L']

    def set_RSVD_7_4_OSC_CNT_CMP_H(self, value):
        """
         Read Only bit field RSVD_7_4_OSC_CNT_CMP_H in the OSC_CNT_CMP_H register. Skip the write.
        """

    def get_RSVD_7_4_OSC_CNT_CMP_H(self):
        """
        Reads the OSC_CNT_CMP_H register
        
        :return: the shadow register RSVD_7_4_OSC_CNT_CMP_H.
        :rtype: int
        """
        self.read_OSC_CNT_CMP_H()
        return self._BITFIELD['RSVD_7_4_OSC_CNT_CMP_H']

    def set_CLK_CNT_CMP_H(self, value):
        """
        Writes the CLK_CNT_CMP_H bitfield in the OSC_CNT_CMP_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OSC_CNT_CMP_H()
        self._BITFIELD['CLK_CNT_CMP_H'] = value
        self.write_OSC_CNT_CMP_H()

    def get_CLK_CNT_CMP_H(self):
        """
        Reads the OSC_CNT_CMP_H register
        
        :return: the shadow register CLK_CNT_CMP_H.
        :rtype: int
        """
        self.read_OSC_CNT_CMP_H()
        return self._BITFIELD['CLK_CNT_CMP_H']

    def set_CLK_COUNT_L(self, value):
        """
         Read Only bit field CLK_COUNT_L in the OSC_CNT_L register. Skip the write.
        """

    def get_CLK_COUNT_L(self):
        """
        Reads the OSC_CNT_L register
        
        :return: the shadow register CLK_COUNT_L.
        :rtype: int
        """
        self.read_OSC_CNT_L()
        return self._BITFIELD['CLK_COUNT_L']

    def set_RSVD_7_4_OSC_CNT_H(self, value):
        """
         Read Only bit field RSVD_7_4_OSC_CNT_H in the OSC_CNT_H register. Skip the write.
        """

    def get_RSVD_7_4_OSC_CNT_H(self):
        """
        Reads the OSC_CNT_H register
        
        :return: the shadow register RSVD_7_4_OSC_CNT_H.
        :rtype: int
        """
        self.read_OSC_CNT_H()
        return self._BITFIELD['RSVD_7_4_OSC_CNT_H']

    def set_CLK_COUNT_H(self, value):
        """
         Read Only bit field CLK_COUNT_H in the OSC_CNT_H register. Skip the write.
        """

    def get_CLK_COUNT_H(self):
        """
        Reads the OSC_CNT_H register
        
        :return: the shadow register CLK_COUNT_H.
        :rtype: int
        """
        self.read_OSC_CNT_H()
        return self._BITFIELD['CLK_COUNT_H']

    def set_OSC_TRIM_TEST(self, value):
        """
         Read Only bit field OSC_TRIM_TEST in the OSC_TRIM_TEST register. Skip the write.
        """

    def get_OSC_TRIM_TEST(self):
        """
        Reads the OSC_TRIM_TEST register
        
        :return: the shadow register OSC_TRIM_TEST.
        :rtype: int
        """
        self.read_OSC_TRIM_TEST()
        return self._BITFIELD['OSC_TRIM_TEST']

    def set_RSVD_7_2_OSC_CMP_HYST(self, value):
        """
         Read Only bit field RSVD_7_2_OSC_CMP_HYST in the OSC_CMP_HYST register. Skip the write.
        """

    def get_RSVD_7_2_OSC_CMP_HYST(self):
        """
        Reads the OSC_CMP_HYST register
        
        :return: the shadow register RSVD_7_2_OSC_CMP_HYST.
        :rtype: int
        """
        self.read_OSC_CMP_HYST()
        return self._BITFIELD['RSVD_7_2_OSC_CMP_HYST']

    def set_CMP_HYST(self, value):
        """
        Writes the CMP_HYST bitfield in the OSC_CMP_HYST register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_OSC_CMP_HYST()
        self._BITFIELD['CMP_HYST'] = value
        self.write_OSC_CMP_HYST()

    def get_CMP_HYST(self):
        """
        Reads the OSC_CMP_HYST register
        
        :return: the shadow register CMP_HYST.
        :rtype: int
        """
        self.read_OSC_CMP_HYST()
        return self._BITFIELD['CMP_HYST']

    def set_DAC_CLAMP_DIS(self, value):
        """
        Writes the DAC_CLAMP_DIS bitfield in the DAC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_TEST_CNTL()
        self._BITFIELD['DAC_CLAMP_DIS'] = value
        self.write_DAC_TEST_CNTL()

    def get_DAC_CLAMP_DIS(self):
        """
        Reads the DAC_TEST_CNTL register
        
        :return: the shadow register DAC_CLAMP_DIS.
        :rtype: int
        """
        self.read_DAC_TEST_CNTL()
        return self._BITFIELD['DAC_CLAMP_DIS']

    def set_RSVD_6_DAC_TEST_CNTL(self, value):
        """
         Read Only bit field RSVD_6_DAC_TEST_CNTL in the DAC_TEST_CNTL register. Skip the write.
        """

    def get_RSVD_6_DAC_TEST_CNTL(self):
        """
        Reads the DAC_TEST_CNTL register
        
        :return: the shadow register RSVD_6_DAC_TEST_CNTL.
        :rtype: int
        """
        self.read_DAC_TEST_CNTL()
        return self._BITFIELD['RSVD_6_DAC_TEST_CNTL']

    def set_DAC_HIZ_GROUP_B(self, value):
        """
        Writes the DAC_HIZ_GROUP_B bitfield in the DAC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_TEST_CNTL()
        self._BITFIELD['DAC_HIZ_GROUP_B'] = value
        self.write_DAC_TEST_CNTL()

    def get_DAC_HIZ_GROUP_B(self):
        """
        Reads the DAC_TEST_CNTL register
        
        :return: the shadow register DAC_HIZ_GROUP_B.
        :rtype: int
        """
        self.read_DAC_TEST_CNTL()
        return self._BITFIELD['DAC_HIZ_GROUP_B']

    def set_DAC_HIZ_GROUP_A(self, value):
        """
        Writes the DAC_HIZ_GROUP_A bitfield in the DAC_TEST_CNTL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_DAC_TEST_CNTL()
        self._BITFIELD['DAC_HIZ_GROUP_A'] = value
        self.write_DAC_TEST_CNTL()

    def get_DAC_HIZ_GROUP_A(self):
        """
        Reads the DAC_TEST_CNTL register
        
        :return: the shadow register DAC_HIZ_GROUP_A.
        :rtype: int
        """
        self.read_DAC_TEST_CNTL()
        return self._BITFIELD['DAC_HIZ_GROUP_A']

    def set_RSVD_3_0_DAC_TEST_CNTL(self, value):
        """
         Read Only bit field RSVD_3_0_DAC_TEST_CNTL in the DAC_TEST_CNTL register. Skip the write.
        """

    def get_RSVD_3_0_DAC_TEST_CNTL(self):
        """
        Reads the DAC_TEST_CNTL register
        
        :return: the shadow register RSVD_3_0_DAC_TEST_CNTL.
        :rtype: int
        """
        self.read_DAC_TEST_CNTL()
        return self._BITFIELD['RSVD_3_0_DAC_TEST_CNTL']

    def set_RSVD_7_2_GPIO_IN(self, value):
        """
         Read Only bit field RSVD_7_2_GPIO_IN in the GPIO_IN register. Skip the write.
        """

    def get_RSVD_7_2_GPIO_IN(self):
        """
        Reads the GPIO_IN register
        
        :return: the shadow register RSVD_7_2_GPIO_IN.
        :rtype: int
        """
        self.read_GPIO_IN()
        return self._BITFIELD['RSVD_7_2_GPIO_IN']

    def set_OUT_BEN_IN(self, value):
        """
         Read Only bit field OUT_BEN_IN in the GPIO_IN register. Skip the write.
        """

    def get_OUT_BEN_IN(self):
        """
        Reads the GPIO_IN register
        
        :return: the shadow register OUT_BEN_IN.
        :rtype: int
        """
        self.read_GPIO_IN()
        return self._BITFIELD['OUT_BEN_IN']

    def set_OUT_AEN_IN(self, value):
        """
         Read Only bit field OUT_AEN_IN in the GPIO_IN register. Skip the write.
        """

    def get_OUT_AEN_IN(self):
        """
        Reads the GPIO_IN register
        
        :return: the shadow register OUT_AEN_IN.
        :rtype: int
        """
        self.read_GPIO_IN()
        return self._BITFIELD['OUT_AEN_IN']

    def set_RSVD_7_2_GPIO_OUT(self, value):
        """
         Read Only bit field RSVD_7_2_GPIO_OUT in the GPIO_OUT register. Skip the write.
        """

    def get_RSVD_7_2_GPIO_OUT(self):
        """
        Reads the GPIO_OUT register
        
        :return: the shadow register RSVD_7_2_GPIO_OUT.
        :rtype: int
        """
        self.read_GPIO_OUT()
        return self._BITFIELD['RSVD_7_2_GPIO_OUT']

    def set_OUT_BEN_OUT(self, value):
        """
        Writes the OUT_BEN_OUT bitfield in the GPIO_OUT register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_OUT()
        self._BITFIELD['OUT_BEN_OUT'] = value
        self.write_GPIO_OUT()

    def get_OUT_BEN_OUT(self):
        """
        Reads the GPIO_OUT register
        
        :return: the shadow register OUT_BEN_OUT.
        :rtype: int
        """
        self.read_GPIO_OUT()
        return self._BITFIELD['OUT_BEN_OUT']

    def set_RSVD_0_GPIO_OUT(self, value):
        """
         Read Only bit field RSVD_0_GPIO_OUT in the GPIO_OUT register. Skip the write.
        """

    def get_RSVD_0_GPIO_OUT(self):
        """
        Reads the GPIO_OUT register
        
        :return: the shadow register RSVD_0_GPIO_OUT.
        :rtype: int
        """
        self.read_GPIO_OUT()
        return self._BITFIELD['RSVD_0_GPIO_OUT']

    def set_RSVD_7_3_GPIO_OEB(self, value):
        """
         Read Only bit field RSVD_7_3_GPIO_OEB in the GPIO_OEB register. Skip the write.
        """

    def get_RSVD_7_3_GPIO_OEB(self):
        """
        Reads the GPIO_OEB register
        
        :return: the shadow register RSVD_7_3_GPIO_OEB.
        :rtype: int
        """
        self.read_GPIO_OEB()
        return self._BITFIELD['RSVD_7_3_GPIO_OEB']

    def set_DAC_OUT_OK_OEB(self, value):
        """
        Writes the DAC_OUT_OK_OEB bitfield in the GPIO_OEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_OEB()
        self._BITFIELD['DAC_OUT_OK_OEB'] = value
        self.write_GPIO_OEB()

    def get_DAC_OUT_OK_OEB(self):
        """
        Reads the GPIO_OEB register
        
        :return: the shadow register DAC_OUT_OK_OEB.
        :rtype: int
        """
        self.read_GPIO_OEB()
        return self._BITFIELD['DAC_OUT_OK_OEB']

    def set_OUT_BEN_OEB(self, value):
        """
        Writes the OUT_BEN_OEB bitfield in the GPIO_OEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_OEB()
        self._BITFIELD['OUT_BEN_OEB'] = value
        self.write_GPIO_OEB()

    def get_OUT_BEN_OEB(self):
        """
        Reads the GPIO_OEB register
        
        :return: the shadow register OUT_BEN_OEB.
        :rtype: int
        """
        self.read_GPIO_OEB()
        return self._BITFIELD['OUT_BEN_OEB']

    def set_RSVD_0_GPIO_OEB(self, value):
        """
         Read Only bit field RSVD_0_GPIO_OEB in the GPIO_OEB register. Skip the write.
        """

    def get_RSVD_0_GPIO_OEB(self):
        """
        Reads the GPIO_OEB register
        
        :return: the shadow register RSVD_0_GPIO_OEB.
        :rtype: int
        """
        self.read_GPIO_OEB()
        return self._BITFIELD['RSVD_0_GPIO_OEB']

    def set_RSVD_7_GPIO_IEB(self, value):
        """
         Read Only bit field RSVD_7_GPIO_IEB in the GPIO_IEB register. Skip the write.
        """

    def get_RSVD_7_GPIO_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register RSVD_7_GPIO_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['RSVD_7_GPIO_IEB']

    def set_DAC_OUT_OK_IEB(self, value):
        """
        Writes the DAC_OUT_OK_IEB bitfield in the GPIO_IEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_IEB()
        self._BITFIELD['DAC_OUT_OK_IEB'] = value
        self.write_GPIO_IEB()

    def get_DAC_OUT_OK_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register DAC_OUT_OK_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['DAC_OUT_OK_IEB']

    def set_SDO_IEB(self, value):
        """
        Writes the SDO_IEB bitfield in the GPIO_IEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_IEB()
        self._BITFIELD['SDO_IEB'] = value
        self.write_GPIO_IEB()

    def get_SDO_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register SDO_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['SDO_IEB']

    def set_SDI_IEB(self, value):
        """
        Writes the SDI_IEB bitfield in the GPIO_IEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_IEB()
        self._BITFIELD['SDI_IEB'] = value
        self.write_GPIO_IEB()

    def get_SDI_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register SDI_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['SDI_IEB']

    def set_CSB_IEB(self, value):
        """
        Writes the CSB_IEB bitfield in the GPIO_IEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_IEB()
        self._BITFIELD['CSB_IEB'] = value
        self.write_GPIO_IEB()

    def get_CSB_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register CSB_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['CSB_IEB']

    def set_SCLK_IEB(self, value):
        """
        Writes the SCLK_IEB bitfield in the GPIO_IEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_IEB()
        self._BITFIELD['SCLK_IEB'] = value
        self.write_GPIO_IEB()

    def get_SCLK_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register SCLK_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['SCLK_IEB']

    def set_OUT_BEN_IEB(self, value):
        """
        Writes the OUT_BEN_IEB bitfield in the GPIO_IEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_IEB()
        self._BITFIELD['OUT_BEN_IEB'] = value
        self.write_GPIO_IEB()

    def get_OUT_BEN_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register OUT_BEN_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['OUT_BEN_IEB']

    def set_OUT_AEN_IEB(self, value):
        """
        Writes the OUT_AEN_IEB bitfield in the GPIO_IEB register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_GPIO_IEB()
        self._BITFIELD['OUT_AEN_IEB'] = value
        self.write_GPIO_IEB()

    def get_OUT_AEN_IEB(self):
        """
        Reads the GPIO_IEB register
        
        :return: the shadow register OUT_AEN_IEB.
        :rtype: int
        """
        self.read_GPIO_IEB()
        return self._BITFIELD['OUT_AEN_IEB']

    def set_I2C_SPIKE_OK(self, value):
        """
         Read Only bit field I2C_SPIKE_OK in the COMP_STATUS register. Skip the write.
        """

    def get_I2C_SPIKE_OK(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register I2C_SPIKE_OK.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['I2C_SPIKE_OK']

    def set_RSVD_6_COMP_STATUS(self, value):
        """
         Read Only bit field RSVD_6_COMP_STATUS in the COMP_STATUS register. Skip the write.
        """

    def get_RSVD_6_COMP_STATUS(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register RSVD_6_COMP_STATUS.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['RSVD_6_COMP_STATUS']

    def set_I3C_1P8V_MODE(self, value):
        """
         Read Only bit field I3C_1P8V_MODE in the COMP_STATUS register. Skip the write.
        """

    def get_I3C_1P8V_MODE(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register I3C_1P8V_MODE.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['I3C_1P8V_MODE']

    def set_SPI_I3C_SEL(self, value):
        """
         Read Only bit field SPI_I3C_SEL in the COMP_STATUS register. Skip the write.
        """

    def get_SPI_I3C_SEL(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register SPI_I3C_SEL.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['SPI_I3C_SEL']

    def set_A1_COMP2(self, value):
        """
         Read Only bit field A1_COMP2 in the COMP_STATUS register. Skip the write.
        """

    def get_A1_COMP2(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register A1_COMP2.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['A1_COMP2']

    def set_A1_COMP1(self, value):
        """
         Read Only bit field A1_COMP1 in the COMP_STATUS register. Skip the write.
        """

    def get_A1_COMP1(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register A1_COMP1.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['A1_COMP1']

    def set_A0_COMP2(self, value):
        """
         Read Only bit field A0_COMP2 in the COMP_STATUS register. Skip the write.
        """

    def get_A0_COMP2(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register A0_COMP2.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['A0_COMP2']

    def set_A0_COMP1(self, value):
        """
         Read Only bit field A0_COMP1 in the COMP_STATUS register. Skip the write.
        """

    def get_A0_COMP1(self):
        """
        Reads the COMP_STATUS register
        
        :return: the shadow register A0_COMP1.
        :rtype: int
        """
        self.read_COMP_STATUS()
        return self._BITFIELD['A0_COMP1']

    def set_DIFF10_OVRD_L(self, value):
        """
        Writes the DIFF10_OVRD_L bitfield in the CS_DIFF10_OVRD_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_DIFF10_OVRD_L()
        self._BITFIELD['DIFF10_OVRD_L'] = value
        self.write_CS_DIFF10_OVRD_L()

    def get_DIFF10_OVRD_L(self):
        """
        Reads the CS_DIFF10_OVRD_L register
        
        :return: the shadow register DIFF10_OVRD_L.
        :rtype: int
        """
        self.read_CS_DIFF10_OVRD_L()
        return self._BITFIELD['DIFF10_OVRD_L']

    def set_RSVD_7_5_CS_DIFF10_OVRD_H(self, value):
        """
         Read Only bit field RSVD_7_5_CS_DIFF10_OVRD_H in the CS_DIFF10_OVRD_H register. Skip the write.
        """

    def get_RSVD_7_5_CS_DIFF10_OVRD_H(self):
        """
        Reads the CS_DIFF10_OVRD_H register
        
        :return: the shadow register RSVD_7_5_CS_DIFF10_OVRD_H.
        :rtype: int
        """
        self.read_CS_DIFF10_OVRD_H()
        return self._BITFIELD['RSVD_7_5_CS_DIFF10_OVRD_H']

    def set_CS_DIFF10_OVRD_H_SIGN(self, value):
        """
        Writes the CS_DIFF10_OVRD_H_SIGN bitfield in the CS_DIFF10_OVRD_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_DIFF10_OVRD_H()
        self._BITFIELD['CS_DIFF10_OVRD_H_SIGN'] = value
        self.write_CS_DIFF10_OVRD_H()

    def get_CS_DIFF10_OVRD_H_SIGN(self):
        """
        Reads the CS_DIFF10_OVRD_H register
        
        :return: the shadow register CS_DIFF10_OVRD_H_SIGN.
        :rtype: int
        """
        self.read_CS_DIFF10_OVRD_H()
        return self._BITFIELD['CS_DIFF10_OVRD_H_SIGN']

    def set_DIFF10_OVRD_H(self, value):
        """
        Writes the DIFF10_OVRD_H bitfield in the CS_DIFF10_OVRD_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_DIFF10_OVRD_H()
        self._BITFIELD['DIFF10_OVRD_H'] = value
        self.write_CS_DIFF10_OVRD_H()

    def get_DIFF10_OVRD_H(self):
        """
        Reads the CS_DIFF10_OVRD_H register
        
        :return: the shadow register DIFF10_OVRD_H.
        :rtype: int
        """
        self.read_CS_DIFF10_OVRD_H()
        return self._BITFIELD['DIFF10_OVRD_H']

    def set_VCM_OVRD_L(self, value):
        """
        Writes the VCM_OVRD_L bitfield in the CS_VCM_OVRD_L register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_VCM_OVRD_L()
        self._BITFIELD['VCM_OVRD_L'] = value
        self.write_CS_VCM_OVRD_L()

    def get_VCM_OVRD_L(self):
        """
        Reads the CS_VCM_OVRD_L register
        
        :return: the shadow register VCM_OVRD_L.
        :rtype: int
        """
        self.read_CS_VCM_OVRD_L()
        return self._BITFIELD['VCM_OVRD_L']

    def set_RSVD_7_4_CS_VCM_OVRD_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_VCM_OVRD_H in the CS_VCM_OVRD_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_VCM_OVRD_H(self):
        """
        Reads the CS_VCM_OVRD_H register
        
        :return: the shadow register RSVD_7_4_CS_VCM_OVRD_H.
        :rtype: int
        """
        self.read_CS_VCM_OVRD_H()
        return self._BITFIELD['RSVD_7_4_CS_VCM_OVRD_H']

    def set_VCM_OVRD_H(self, value):
        """
        Writes the VCM_OVRD_H bitfield in the CS_VCM_OVRD_H register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_VCM_OVRD_H()
        self._BITFIELD['VCM_OVRD_H'] = value
        self.write_CS_VCM_OVRD_H()

    def get_VCM_OVRD_H(self):
        """
        Reads the CS_VCM_OVRD_H register
        
        :return: the shadow register VCM_OVRD_H.
        :rtype: int
        """
        self.read_CS_VCM_OVRD_H()
        return self._BITFIELD['VCM_OVRD_H']

    def set_CS_B_DTEST_EN(self, value):
        """
        Writes the CS_B_DTEST_EN bitfield in the CS_DTEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_DTEST_CTRL()
        self._BITFIELD['CS_B_DTEST_EN'] = value
        self.write_CS_DTEST_CTRL()

    def get_CS_B_DTEST_EN(self):
        """
        Reads the CS_DTEST_CTRL register
        
        :return: the shadow register CS_B_DTEST_EN.
        :rtype: int
        """
        self.read_CS_DTEST_CTRL()
        return self._BITFIELD['CS_B_DTEST_EN']

    def set_CS_B_DTEST_CTRL(self, value):
        """
        Writes the CS_B_DTEST_CTRL bitfield in the CS_DTEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_DTEST_CTRL()
        self._BITFIELD['CS_B_DTEST_CTRL'] = value
        self.write_CS_DTEST_CTRL()

    def get_CS_B_DTEST_CTRL(self):
        """
        Reads the CS_DTEST_CTRL register
        
        :return: the shadow register CS_B_DTEST_CTRL.
        :rtype: int
        """
        self.read_CS_DTEST_CTRL()
        return self._BITFIELD['CS_B_DTEST_CTRL']

    def set_CS_A_DTEST_EN(self, value):
        """
        Writes the CS_A_DTEST_EN bitfield in the CS_DTEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_DTEST_CTRL()
        self._BITFIELD['CS_A_DTEST_EN'] = value
        self.write_CS_DTEST_CTRL()

    def get_CS_A_DTEST_EN(self):
        """
        Reads the CS_DTEST_CTRL register
        
        :return: the shadow register CS_A_DTEST_EN.
        :rtype: int
        """
        self.read_CS_DTEST_CTRL()
        return self._BITFIELD['CS_A_DTEST_EN']

    def set_CS_A_DTEST_CTRL(self, value):
        """
        Writes the CS_A_DTEST_CTRL bitfield in the CS_DTEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_DTEST_CTRL()
        self._BITFIELD['CS_A_DTEST_CTRL'] = value
        self.write_CS_DTEST_CTRL()

    def get_CS_A_DTEST_CTRL(self):
        """
        Reads the CS_DTEST_CTRL register
        
        :return: the shadow register CS_A_DTEST_CTRL.
        :rtype: int
        """
        self.read_CS_DTEST_CTRL()
        return self._BITFIELD['CS_A_DTEST_CTRL']

    def set_RSVD_7_4_ADC_CTRL_SIG(self, value):
        """
         Read Only bit field RSVD_7_4_ADC_CTRL_SIG in the ADC_CTRL_SIG register. Skip the write.
        """

    def get_RSVD_7_4_ADC_CTRL_SIG(self):
        """
        Reads the ADC_CTRL_SIG register
        
        :return: the shadow register RSVD_7_4_ADC_CTRL_SIG.
        :rtype: int
        """
        self.read_ADC_CTRL_SIG()
        return self._BITFIELD['RSVD_7_4_ADC_CTRL_SIG']

    def set_ADC_CAL_START(self, value):
        """
        Writes the ADC_CAL_START bitfield in the ADC_CTRL_SIG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CTRL_SIG()
        self._BITFIELD['ADC_CAL_START'] = value
        self.write_ADC_CTRL_SIG()

    def get_ADC_CAL_START(self):
        """
        Reads the ADC_CTRL_SIG register
        
        :return: the shadow register ADC_CAL_START.
        :rtype: int
        """
        self.read_ADC_CTRL_SIG()
        return self._BITFIELD['ADC_CAL_START']

    def set_ADC_SAMPLE(self, value):
        """
        Writes the ADC_SAMPLE bitfield in the ADC_CTRL_SIG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CTRL_SIG()
        self._BITFIELD['ADC_SAMPLE'] = value
        self.write_ADC_CTRL_SIG()

    def get_ADC_SAMPLE(self):
        """
        Reads the ADC_CTRL_SIG register
        
        :return: the shadow register ADC_SAMPLE.
        :rtype: int
        """
        self.read_ADC_CTRL_SIG()
        return self._BITFIELD['ADC_SAMPLE']

    def set_ADC_SOC(self, value):
        """
        Writes the ADC_SOC bitfield in the ADC_CTRL_SIG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CTRL_SIG()
        self._BITFIELD['ADC_SOC'] = value
        self.write_ADC_CTRL_SIG()

    def get_ADC_SOC(self):
        """
        Reads the ADC_CTRL_SIG register
        
        :return: the shadow register ADC_SOC.
        :rtype: int
        """
        self.read_ADC_CTRL_SIG()
        return self._BITFIELD['ADC_SOC']

    def set_ADC_RESETB(self, value):
        """
        Writes the ADC_RESETB bitfield in the ADC_CTRL_SIG register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_ADC_CTRL_SIG()
        self._BITFIELD['ADC_RESETB'] = value
        self.write_ADC_CTRL_SIG()

    def get_ADC_RESETB(self):
        """
        Reads the ADC_CTRL_SIG register
        
        :return: the shadow register ADC_RESETB.
        :rtype: int
        """
        self.read_ADC_CTRL_SIG()
        return self._BITFIELD['ADC_RESETB']

    def set_CS_VCM_OC(self, value):
        """
        Writes the CS_VCM_OC bitfield in the CS_TEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_TEST_CTRL()
        self._BITFIELD['CS_VCM_OC'] = value
        self.write_CS_TEST_CTRL()

    def get_CS_VCM_OC(self):
        """
        Reads the CS_TEST_CTRL register
        
        :return: the shadow register CS_VCM_OC.
        :rtype: int
        """
        self.read_CS_TEST_CTRL()
        return self._BITFIELD['CS_VCM_OC']

    def set_CS_VCM_OCH(self, value):
        """
        Writes the CS_VCM_OCH bitfield in the CS_TEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_TEST_CTRL()
        self._BITFIELD['CS_VCM_OCH'] = value
        self.write_CS_TEST_CTRL()

    def get_CS_VCM_OCH(self):
        """
        Reads the CS_TEST_CTRL register
        
        :return: the shadow register CS_VCM_OCH.
        :rtype: int
        """
        self.read_CS_TEST_CTRL()
        return self._BITFIELD['CS_VCM_OCH']

    def set_CS_VCM_UPDATE(self, value):
        """
        Writes the CS_VCM_UPDATE bitfield in the CS_TEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_TEST_CTRL()
        self._BITFIELD['CS_VCM_UPDATE'] = value
        self.write_CS_TEST_CTRL()

    def get_CS_VCM_UPDATE(self):
        """
        Reads the CS_TEST_CTRL register
        
        :return: the shadow register CS_VCM_UPDATE.
        :rtype: int
        """
        self.read_CS_TEST_CTRL()
        return self._BITFIELD['CS_VCM_UPDATE']

    def set_CS_CAL_MODE(self, value):
        """
        Writes the CS_CAL_MODE bitfield in the CS_TEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_TEST_CTRL()
        self._BITFIELD['CS_CAL_MODE'] = value
        self.write_CS_TEST_CTRL()

    def get_CS_CAL_MODE(self):
        """
        Reads the CS_TEST_CTRL register
        
        :return: the shadow register CS_CAL_MODE.
        :rtype: int
        """
        self.read_CS_TEST_CTRL()
        return self._BITFIELD['CS_CAL_MODE']

    def set_CS_PHASE_CTRL(self, value):
        """
        Writes the CS_PHASE_CTRL bitfield in the CS_TEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_TEST_CTRL()
        self._BITFIELD['CS_PHASE_CTRL'] = value
        self.write_CS_TEST_CTRL()

    def get_CS_PHASE_CTRL(self):
        """
        Reads the CS_TEST_CTRL register
        
        :return: the shadow register CS_PHASE_CTRL.
        :rtype: int
        """
        self.read_CS_TEST_CTRL()
        return self._BITFIELD['CS_PHASE_CTRL']

    def set_CS_MUX_SEL(self, value):
        """
        Writes the CS_MUX_SEL bitfield in the CS_TEST_CTRL register with the shadow register contents.
        
        :param value: Integer to be written to the register.
        :type value: int
        """
        if self.readModifyWrite:
            self.read_CS_TEST_CTRL()
        self._BITFIELD['CS_MUX_SEL'] = value
        self.write_CS_TEST_CTRL()

    def get_CS_MUX_SEL(self):
        """
        Reads the CS_TEST_CTRL register
        
        :return: the shadow register CS_MUX_SEL.
        :rtype: int
        """
        self.read_CS_TEST_CTRL()
        return self._BITFIELD['CS_MUX_SEL']

    def set_ADC_DATA_L(self, value):
        """
         Read Only bit field ADC_DATA_L in the ADC_DATA_L register. Skip the write.
        """

    def get_ADC_DATA_L(self):
        """
        Reads the ADC_DATA_L register
        
        :return: the shadow register ADC_DATA_L.
        :rtype: int
        """
        self.read_ADC_DATA_L()
        return self._BITFIELD['ADC_DATA_L']

    def set_ADC_EOC(self, value):
        """
         Read Only bit field ADC_EOC in the ADC_DATA_H register. Skip the write.
        """

    def get_ADC_EOC(self):
        """
        Reads the ADC_DATA_H register
        
        :return: the shadow register ADC_EOC.
        :rtype: int
        """
        self.read_ADC_DATA_H()
        return self._BITFIELD['ADC_EOC']

    def set_RSVD_6_4_ADC_DATA_H(self, value):
        """
         Read Only bit field RSVD_6_4_ADC_DATA_H in the ADC_DATA_H register. Skip the write.
        """

    def get_RSVD_6_4_ADC_DATA_H(self):
        """
        Reads the ADC_DATA_H register
        
        :return: the shadow register RSVD_6_4_ADC_DATA_H.
        :rtype: int
        """
        self.read_ADC_DATA_H()
        return self._BITFIELD['RSVD_6_4_ADC_DATA_H']

    def set_ADC_DATA_H(self, value):
        """
         Read Only bit field ADC_DATA_H in the ADC_DATA_H register. Skip the write.
        """

    def get_ADC_DATA_H(self):
        """
        Reads the ADC_DATA_H register
        
        :return: the shadow register ADC_DATA_H.
        :rtype: int
        """
        self.read_ADC_DATA_H()
        return self._BITFIELD['ADC_DATA_H']

    def set_VCM_L(self, value):
        """
         Read Only bit field VCM_L in the CS_VCM_L register. Skip the write.
        """

    def get_VCM_L(self):
        """
        Reads the CS_VCM_L register
        
        :return: the shadow register VCM_L.
        :rtype: int
        """
        self.read_CS_VCM_L()
        return self._BITFIELD['VCM_L']

    def set_RSVD_7_4_CS_VCM_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_VCM_H in the CS_VCM_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_VCM_H(self):
        """
        Reads the CS_VCM_H register
        
        :return: the shadow register RSVD_7_4_CS_VCM_H.
        :rtype: int
        """
        self.read_CS_VCM_H()
        return self._BITFIELD['RSVD_7_4_CS_VCM_H']

    def set_VCM_H(self, value):
        """
         Read Only bit field VCM_H in the CS_VCM_H register. Skip the write.
        """

    def get_VCM_H(self):
        """
        Reads the CS_VCM_H register
        
        :return: the shadow register VCM_H.
        :rtype: int
        """
        self.read_CS_VCM_H()
        return self._BITFIELD['VCM_H']

    def set_DAC_MID_L(self, value):
        """
         Read Only bit field DAC_MID_L in the CS_DAC_MID_L register. Skip the write.
        """

    def get_DAC_MID_L(self):
        """
        Reads the CS_DAC_MID_L register
        
        :return: the shadow register DAC_MID_L.
        :rtype: int
        """
        self.read_CS_DAC_MID_L()
        return self._BITFIELD['DAC_MID_L']

    def set_RSVD_7_4_CS_DAC_MID_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_DAC_MID_H in the CS_DAC_MID_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_DAC_MID_H(self):
        """
        Reads the CS_DAC_MID_H register
        
        :return: the shadow register RSVD_7_4_CS_DAC_MID_H.
        :rtype: int
        """
        self.read_CS_DAC_MID_H()
        return self._BITFIELD['RSVD_7_4_CS_DAC_MID_H']

    def set_DAC_MID_H(self, value):
        """
         Read Only bit field DAC_MID_H in the CS_DAC_MID_H register. Skip the write.
        """

    def get_DAC_MID_H(self):
        """
        Reads the CS_DAC_MID_H register
        
        :return: the shadow register DAC_MID_H.
        :rtype: int
        """
        self.read_CS_DAC_MID_H()
        return self._BITFIELD['DAC_MID_H']

    def set_SENSE_P_DAC_L(self, value):
        """
         Read Only bit field SENSE_P_DAC_L in the CS_SENSE_P_DAC_L register. Skip the write.
        """

    def get_SENSE_P_DAC_L(self):
        """
        Reads the CS_SENSE_P_DAC_L register
        
        :return: the shadow register SENSE_P_DAC_L.
        :rtype: int
        """
        self.read_CS_SENSE_P_DAC_L()
        return self._BITFIELD['SENSE_P_DAC_L']

    def set_RSVD_7_4_CS_SENSE_P_DAC_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_SENSE_P_DAC_H in the CS_SENSE_P_DAC_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_SENSE_P_DAC_H(self):
        """
        Reads the CS_SENSE_P_DAC_H register
        
        :return: the shadow register RSVD_7_4_CS_SENSE_P_DAC_H.
        :rtype: int
        """
        self.read_CS_SENSE_P_DAC_H()
        return self._BITFIELD['RSVD_7_4_CS_SENSE_P_DAC_H']

    def set_SENSE_P_DAC_H(self, value):
        """
         Read Only bit field SENSE_P_DAC_H in the CS_SENSE_P_DAC_H register. Skip the write.
        """

    def get_SENSE_P_DAC_H(self):
        """
        Reads the CS_SENSE_P_DAC_H register
        
        :return: the shadow register SENSE_P_DAC_H.
        :rtype: int
        """
        self.read_CS_SENSE_P_DAC_H()
        return self._BITFIELD['SENSE_P_DAC_H']

    def set_SENSE_N_DAC_L(self, value):
        """
         Read Only bit field SENSE_N_DAC_L in the CS_SENSE_N_DAC_L register. Skip the write.
        """

    def get_SENSE_N_DAC_L(self):
        """
        Reads the CS_SENSE_N_DAC_L register
        
        :return: the shadow register SENSE_N_DAC_L.
        :rtype: int
        """
        self.read_CS_SENSE_N_DAC_L()
        return self._BITFIELD['SENSE_N_DAC_L']

    def set_RSVD_7_4_CS_SENSE_N_DAC_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_SENSE_N_DAC_H in the CS_SENSE_N_DAC_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_SENSE_N_DAC_H(self):
        """
        Reads the CS_SENSE_N_DAC_H register
        
        :return: the shadow register RSVD_7_4_CS_SENSE_N_DAC_H.
        :rtype: int
        """
        self.read_CS_SENSE_N_DAC_H()
        return self._BITFIELD['RSVD_7_4_CS_SENSE_N_DAC_H']

    def set_SENSE_N_DAC_H(self, value):
        """
         Read Only bit field SENSE_N_DAC_H in the CS_SENSE_N_DAC_H register. Skip the write.
        """

    def get_SENSE_N_DAC_H(self):
        """
        Reads the CS_SENSE_N_DAC_H register
        
        :return: the shadow register SENSE_N_DAC_H.
        :rtype: int
        """
        self.read_CS_SENSE_N_DAC_H()
        return self._BITFIELD['SENSE_N_DAC_H']

    def set_DAC_SHIFT_L(self, value):
        """
         Read Only bit field DAC_SHIFT_L in the CS_DAC_SHIFT_L register. Skip the write.
        """

    def get_DAC_SHIFT_L(self):
        """
        Reads the CS_DAC_SHIFT_L register
        
        :return: the shadow register DAC_SHIFT_L.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_L()
        return self._BITFIELD['DAC_SHIFT_L']

    def set_RSVD_7_2_CS_DAC_SHIFT_H(self, value):
        """
         Read Only bit field RSVD_7_2_CS_DAC_SHIFT_H in the CS_DAC_SHIFT_H register. Skip the write.
        """

    def get_RSVD_7_2_CS_DAC_SHIFT_H(self):
        """
        Reads the CS_DAC_SHIFT_H register
        
        :return: the shadow register RSVD_7_2_CS_DAC_SHIFT_H.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_H()
        return self._BITFIELD['RSVD_7_2_CS_DAC_SHIFT_H']

    def set_CS_DAC_SHIFT_H_SIGN(self, value):
        """
         Read Only bit field CS_DAC_SHIFT_H_SIGN in the CS_DAC_SHIFT_H register. Skip the write.
        """

    def get_CS_DAC_SHIFT_H_SIGN(self):
        """
        Reads the CS_DAC_SHIFT_H register
        
        :return: the shadow register CS_DAC_SHIFT_H_SIGN.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_H()
        return self._BITFIELD['CS_DAC_SHIFT_H_SIGN']

    def set_DAC_SHIFT_H(self, value):
        """
         Read Only bit field DAC_SHIFT_H in the CS_DAC_SHIFT_H register. Skip the write.
        """

    def get_DAC_SHIFT_H(self):
        """
        Reads the CS_DAC_SHIFT_H register
        
        :return: the shadow register DAC_SHIFT_H.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_H()
        return self._BITFIELD['DAC_SHIFT_H']

    def set_DAC_SHIFT_COR_L(self, value):
        """
         Read Only bit field DAC_SHIFT_COR_L in the CS_DAC_SHIFT_COR_L register. Skip the write.
        """

    def get_DAC_SHIFT_COR_L(self):
        """
        Reads the CS_DAC_SHIFT_COR_L register
        
        :return: the shadow register DAC_SHIFT_COR_L.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_COR_L()
        return self._BITFIELD['DAC_SHIFT_COR_L']

    def set_RSVD_7_2_CS_DAC_SHIFT_COR_H(self, value):
        """
         Read Only bit field RSVD_7_2_CS_DAC_SHIFT_COR_H in the CS_DAC_SHIFT_COR_H register. Skip the write.
        """

    def get_RSVD_7_2_CS_DAC_SHIFT_COR_H(self):
        """
        Reads the CS_DAC_SHIFT_COR_H register
        
        :return: the shadow register RSVD_7_2_CS_DAC_SHIFT_COR_H.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_COR_H()
        return self._BITFIELD['RSVD_7_2_CS_DAC_SHIFT_COR_H']

    def set_CS_DAC_SHIFT_COR_H_SIGN(self, value):
        """
         Read Only bit field CS_DAC_SHIFT_COR_H_SIGN in the CS_DAC_SHIFT_COR_H register. Skip the write.
        """

    def get_CS_DAC_SHIFT_COR_H_SIGN(self):
        """
        Reads the CS_DAC_SHIFT_COR_H register
        
        :return: the shadow register CS_DAC_SHIFT_COR_H_SIGN.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_COR_H()
        return self._BITFIELD['CS_DAC_SHIFT_COR_H_SIGN']

    def set_DAC_SHIFT_COR_H(self, value):
        """
         Read Only bit field DAC_SHIFT_COR_H in the CS_DAC_SHIFT_COR_H register. Skip the write.
        """

    def get_DAC_SHIFT_COR_H(self):
        """
        Reads the CS_DAC_SHIFT_COR_H register
        
        :return: the shadow register DAC_SHIFT_COR_H.
        :rtype: int
        """
        self.read_CS_DAC_SHIFT_COR_H()
        return self._BITFIELD['DAC_SHIFT_COR_H']

    def set_RSVD_7_CS_DAC_CODE(self, value):
        """
         Read Only bit field RSVD_7_CS_DAC_CODE in the CS_DAC_CODE register. Skip the write.
        """

    def get_RSVD_7_CS_DAC_CODE(self):
        """
        Reads the CS_DAC_CODE register
        
        :return: the shadow register RSVD_7_CS_DAC_CODE.
        :rtype: int
        """
        self.read_CS_DAC_CODE()
        return self._BITFIELD['RSVD_7_CS_DAC_CODE']

    def set_CS_DAC_CODE(self, value):
        """
         Read Only bit field CS_DAC_CODE in the CS_DAC_CODE register. Skip the write.
        """

    def get_CS_DAC_CODE(self):
        """
        Reads the CS_DAC_CODE register
        
        :return: the shadow register CS_DAC_CODE.
        :rtype: int
        """
        self.read_CS_DAC_CODE()
        return self._BITFIELD['CS_DAC_CODE']

    def set_SENSE_P10_L(self, value):
        """
         Read Only bit field SENSE_P10_L in the CS_SENSE_P10_L register. Skip the write.
        """

    def get_SENSE_P10_L(self):
        """
        Reads the CS_SENSE_P10_L register
        
        :return: the shadow register SENSE_P10_L.
        :rtype: int
        """
        self.read_CS_SENSE_P10_L()
        return self._BITFIELD['SENSE_P10_L']

    def set_RSVD_7_4_CS_SENSE_P10_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_SENSE_P10_H in the CS_SENSE_P10_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_SENSE_P10_H(self):
        """
        Reads the CS_SENSE_P10_H register
        
        :return: the shadow register RSVD_7_4_CS_SENSE_P10_H.
        :rtype: int
        """
        self.read_CS_SENSE_P10_H()
        return self._BITFIELD['RSVD_7_4_CS_SENSE_P10_H']

    def set_SENSE_P10_H(self, value):
        """
         Read Only bit field SENSE_P10_H in the CS_SENSE_P10_H register. Skip the write.
        """

    def get_SENSE_P10_H(self):
        """
        Reads the CS_SENSE_P10_H register
        
        :return: the shadow register SENSE_P10_H.
        :rtype: int
        """
        self.read_CS_SENSE_P10_H()
        return self._BITFIELD['SENSE_P10_H']

    def set_SENSE_N10_L(self, value):
        """
         Read Only bit field SENSE_N10_L in the CS_SENSE_N10_L register. Skip the write.
        """

    def get_SENSE_N10_L(self):
        """
        Reads the CS_SENSE_N10_L register
        
        :return: the shadow register SENSE_N10_L.
        :rtype: int
        """
        self.read_CS_SENSE_N10_L()
        return self._BITFIELD['SENSE_N10_L']

    def set_RSVD_7_4_CS_SENSE_N10_H(self, value):
        """
         Read Only bit field RSVD_7_4_CS_SENSE_N10_H in the CS_SENSE_N10_H register. Skip the write.
        """

    def get_RSVD_7_4_CS_SENSE_N10_H(self):
        """
        Reads the CS_SENSE_N10_H register
        
        :return: the shadow register RSVD_7_4_CS_SENSE_N10_H.
        :rtype: int
        """
        self.read_CS_SENSE_N10_H()
        return self._BITFIELD['RSVD_7_4_CS_SENSE_N10_H']

    def set_SENSE_N10_H(self, value):
        """
         Read Only bit field SENSE_N10_H in the CS_SENSE_N10_H register. Skip the write.
        """

    def get_SENSE_N10_H(self):
        """
        Reads the CS_SENSE_N10_H register
        
        :return: the shadow register SENSE_N10_H.
        :rtype: int
        """
        self.read_CS_SENSE_N10_H()
        return self._BITFIELD['SENSE_N10_H']

    def set_DIFF10_L(self, value):
        """
         Read Only bit field DIFF10_L in the CS_DIFF10_L register. Skip the write.
        """

    def get_DIFF10_L(self):
        """
        Reads the CS_DIFF10_L register
        
        :return: the shadow register DIFF10_L.
        :rtype: int
        """
        self.read_CS_DIFF10_L()
        return self._BITFIELD['DIFF10_L']

    def set_RSVD_7_5_CS_DIFF10_H(self, value):
        """
         Read Only bit field RSVD_7_5_CS_DIFF10_H in the CS_DIFF10_H register. Skip the write.
        """

    def get_RSVD_7_5_CS_DIFF10_H(self):
        """
        Reads the CS_DIFF10_H register
        
        :return: the shadow register RSVD_7_5_CS_DIFF10_H.
        :rtype: int
        """
        self.read_CS_DIFF10_H()
        return self._BITFIELD['RSVD_7_5_CS_DIFF10_H']

    def set_CS_DIFF10_H_SIGN(self, value):
        """
         Read Only bit field CS_DIFF10_H_SIGN in the CS_DIFF10_H register. Skip the write.
        """

    def get_CS_DIFF10_H_SIGN(self):
        """
        Reads the CS_DIFF10_H register
        
        :return: the shadow register CS_DIFF10_H_SIGN.
        :rtype: int
        """
        self.read_CS_DIFF10_H()
        return self._BITFIELD['CS_DIFF10_H_SIGN']

    def set_DIFF10_H(self, value):
        """
         Read Only bit field DIFF10_H in the CS_DIFF10_H register. Skip the write.
        """

    def get_DIFF10_H(self):
        """
        Reads the CS_DIFF10_H register
        
        :return: the shadow register DIFF10_H.
        :rtype: int
        """
        self.read_CS_DIFF10_H()
        return self._BITFIELD['DIFF10_H']

    def set_CAL_ER_L(self, value):
        """
         Read Only bit field CAL_ER_L in the CS_CAL_ER_L register. Skip the write.
        """

    def get_CAL_ER_L(self):
        """
        Reads the CS_CAL_ER_L register
        
        :return: the shadow register CAL_ER_L.
        :rtype: int
        """
        self.read_CS_CAL_ER_L()
        return self._BITFIELD['CAL_ER_L']

    def set_RSVD_7_5_CS_CAL_ER_H(self, value):
        """
         Read Only bit field RSVD_7_5_CS_CAL_ER_H in the CS_CAL_ER_H register. Skip the write.
        """

    def get_RSVD_7_5_CS_CAL_ER_H(self):
        """
        Reads the CS_CAL_ER_H register
        
        :return: the shadow register RSVD_7_5_CS_CAL_ER_H.
        :rtype: int
        """
        self.read_CS_CAL_ER_H()
        return self._BITFIELD['RSVD_7_5_CS_CAL_ER_H']

    def set_CS_CAL_ER_H_SIGN(self, value):
        """
         Read Only bit field CS_CAL_ER_H_SIGN in the CS_CAL_ER_H register. Skip the write.
        """

    def get_CS_CAL_ER_H_SIGN(self):
        """
        Reads the CS_CAL_ER_H register
        
        :return: the shadow register CS_CAL_ER_H_SIGN.
        :rtype: int
        """
        self.read_CS_CAL_ER_H()
        return self._BITFIELD['CS_CAL_ER_H_SIGN']

    def set_CAL_ER_H(self, value):
        """
         Read Only bit field CAL_ER_H in the CS_CAL_ER_H register. Skip the write.
        """

    def get_CAL_ER_H(self):
        """
        Reads the CS_CAL_ER_H register
        
        :return: the shadow register CAL_ER_H.
        :rtype: int
        """
        self.read_CS_CAL_ER_H()
        return self._BITFIELD['CAL_ER_H']

    def set_CAL_DIFF10_L(self, value):
        """
         Read Only bit field CAL_DIFF10_L in the CS_CAL_DIFF10_L register. Skip the write.
        """

    def get_CAL_DIFF10_L(self):
        """
        Reads the CS_CAL_DIFF10_L register
        
        :return: the shadow register CAL_DIFF10_L.
        :rtype: int
        """
        self.read_CS_CAL_DIFF10_L()
        return self._BITFIELD['CAL_DIFF10_L']

    def set_RSVD_7_5_CS_CAL_DIFF10_H(self, value):
        """
         Read Only bit field RSVD_7_5_CS_CAL_DIFF10_H in the CS_CAL_DIFF10_H register. Skip the write.
        """

    def get_RSVD_7_5_CS_CAL_DIFF10_H(self):
        """
        Reads the CS_CAL_DIFF10_H register
        
        :return: the shadow register RSVD_7_5_CS_CAL_DIFF10_H.
        :rtype: int
        """
        self.read_CS_CAL_DIFF10_H()
        return self._BITFIELD['RSVD_7_5_CS_CAL_DIFF10_H']

    def set_CS_CAL_DIFF10_H_SIGN(self, value):
        """
         Read Only bit field CS_CAL_DIFF10_H_SIGN in the CS_CAL_DIFF10_H register. Skip the write.
        """

    def get_CS_CAL_DIFF10_H_SIGN(self):
        """
        Reads the CS_CAL_DIFF10_H register
        
        :return: the shadow register CS_CAL_DIFF10_H_SIGN.
        :rtype: int
        """
        self.read_CS_CAL_DIFF10_H()
        return self._BITFIELD['CS_CAL_DIFF10_H_SIGN']

    def set_CAL_DIFF10_H(self, value):
        """
         Read Only bit field CAL_DIFF10_H in the CS_CAL_DIFF10_H register. Skip the write.
        """

    def get_CAL_DIFF10_H(self):
        """
        Reads the CS_CAL_DIFF10_H register
        
        :return: the shadow register CAL_DIFF10_H.
        :rtype: int
        """
        self.read_CS_CAL_DIFF10_H()
        return self._BITFIELD['CAL_DIFF10_H']

    def set_RSVD_7_6_CS_CAL_ER_LUTP(self, value):
        """
         Read Only bit field RSVD_7_6_CS_CAL_ER_LUTP in the CS_CAL_ER_LUTP register. Skip the write.
        """

    def get_RSVD_7_6_CS_CAL_ER_LUTP(self):
        """
        Reads the CS_CAL_ER_LUTP register
        
        :return: the shadow register RSVD_7_6_CS_CAL_ER_LUTP.
        :rtype: int
        """
        self.read_CS_CAL_ER_LUTP()
        return self._BITFIELD['RSVD_7_6_CS_CAL_ER_LUTP']

    def set_CAL_ER_LUTP(self, value):
        """
         Read Only bit field CAL_ER_LUTP in the CS_CAL_ER_LUTP register. Skip the write.
        """

    def get_CAL_ER_LUTP(self):
        """
        Reads the CS_CAL_ER_LUTP register
        
        :return: the shadow register CAL_ER_LUTP.
        :rtype: int
        """
        self.read_CS_CAL_ER_LUTP()
        return self._BITFIELD['CAL_ER_LUTP']

    def set_CAL_LUTS_L(self, value):
        """
         Read Only bit field CAL_LUTS_L in the CS_CAL_LUTS_L register. Skip the write.
        """

    def get_CAL_LUTS_L(self):
        """
        Reads the CS_CAL_LUTS_L register
        
        :return: the shadow register CAL_LUTS_L.
        :rtype: int
        """
        self.read_CS_CAL_LUTS_L()
        return self._BITFIELD['CAL_LUTS_L']

    def set_RSVD_7_5_CS_CAL_LUTS_H(self, value):
        """
         Read Only bit field RSVD_7_5_CS_CAL_LUTS_H in the CS_CAL_LUTS_H register. Skip the write.
        """

    def get_RSVD_7_5_CS_CAL_LUTS_H(self):
        """
        Reads the CS_CAL_LUTS_H register
        
        :return: the shadow register RSVD_7_5_CS_CAL_LUTS_H.
        :rtype: int
        """
        self.read_CS_CAL_LUTS_H()
        return self._BITFIELD['RSVD_7_5_CS_CAL_LUTS_H']

    def set_CS_CAL_LUTS_H_SIGN(self, value):
        """
         Read Only bit field CS_CAL_LUTS_H_SIGN in the CS_CAL_LUTS_H register. Skip the write.
        """

    def get_CS_CAL_LUTS_H_SIGN(self):
        """
        Reads the CS_CAL_LUTS_H register
        
        :return: the shadow register CS_CAL_LUTS_H_SIGN.
        :rtype: int
        """
        self.read_CS_CAL_LUTS_H()
        return self._BITFIELD['CS_CAL_LUTS_H_SIGN']

    def set_CAL_LUTS_H(self, value):
        """
         Read Only bit field CAL_LUTS_H in the CS_CAL_LUTS_H register. Skip the write.
        """

    def get_CAL_LUTS_H(self):
        """
        Reads the CS_CAL_LUTS_H register
        
        :return: the shadow register CAL_LUTS_H.
        :rtype: int
        """
        self.read_CS_CAL_LUTS_H()
        return self._BITFIELD['CAL_LUTS_H']

    def set_CS_CAL_ER_FRAC_SIGN(self, value):
        """
         Read Only bit field CS_CAL_ER_FRAC_SIGN in the CS_CAL_ER_FRAC register. Skip the write.
        """

    def get_CS_CAL_ER_FRAC_SIGN(self):
        """
        Reads the CS_CAL_ER_FRAC register
        
        :return: the shadow register CS_CAL_ER_FRAC_SIGN.
        :rtype: int
        """
        self.read_CS_CAL_ER_FRAC()
        return self._BITFIELD['CS_CAL_ER_FRAC_SIGN']

    def set_CAL_ER_FRAC(self, value):
        """
         Read Only bit field CAL_ER_FRAC in the CS_CAL_ER_FRAC register. Skip the write.
        """

    def get_CAL_ER_FRAC(self):
        """
        Reads the CS_CAL_ER_FRAC register
        
        :return: the shadow register CAL_ER_FRAC.
        :rtype: int
        """
        self.read_CS_CAL_ER_FRAC()
        return self._BITFIELD['CAL_ER_FRAC']

    def set_GAIN_ER_L(self, value):
        """
         Read Only bit field GAIN_ER_L in the CS_GAIN_ER_L register. Skip the write.
        """

    def get_GAIN_ER_L(self):
        """
        Reads the CS_GAIN_ER_L register
        
        :return: the shadow register GAIN_ER_L.
        :rtype: int
        """
        self.read_CS_GAIN_ER_L()
        return self._BITFIELD['GAIN_ER_L']

    def set_RSVD_7_1_CS_GAIN_ER_H(self, value):
        """
         Read Only bit field RSVD_7_1_CS_GAIN_ER_H in the CS_GAIN_ER_H register. Skip the write.
        """

    def get_RSVD_7_1_CS_GAIN_ER_H(self):
        """
        Reads the CS_GAIN_ER_H register
        
        :return: the shadow register RSVD_7_1_CS_GAIN_ER_H.
        :rtype: int
        """
        self.read_CS_GAIN_ER_H()
        return self._BITFIELD['RSVD_7_1_CS_GAIN_ER_H']

    def set_CS_GAIN_ER_H_SIGN(self, value):
        """
         Read Only bit field CS_GAIN_ER_H_SIGN in the CS_GAIN_ER_H register. Skip the write.
        """

    def get_CS_GAIN_ER_H_SIGN(self):
        """
        Reads the CS_GAIN_ER_H register
        
        :return: the shadow register CS_GAIN_ER_H_SIGN.
        :rtype: int
        """
        self.read_CS_GAIN_ER_H()
        return self._BITFIELD['CS_GAIN_ER_H_SIGN']

    def write_ADC_AVG(self):
        """
        Write the register ADC_AVG with the shadow register contents.
        """
        value = ((self._BITFIELD['ADC_AVG_ADC'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_AVG'], value)

    def write_ADC_CAL_CNTL(self):
        """
        Write the register ADC_CAL_CNTL with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_ADC_CAL_CNTL'] & 0x1) << 7) |
                 ((self._BITFIELD['OFFSET_EN'] & 0x1) << 6) |
                 ((self._BITFIELD['RSVD_5_3_ADC_CAL_CNTL'] & 0x7) << 3) |
                 ((self._BITFIELD['CS_FAST_AVG_EN'] & 0x1) << 2) |
                 (self._BITFIELD['ADC_SAMPLE_DLY'] & 0x3))
        self.write_register(self.REGISTER_ADDRESSES['ADC_CAL_CNTL'], value)

    def write_ADC_CFG(self):
        """
        Write the register ADC_CFG with the shadow register contents.
        """
        value = (((self._BITFIELD['CMODE'] & 0x1) << 7) |
                 ((self._BITFIELD['ADC_CONV_RATE'] & 0x3) << 5) |
                 ((self._BITFIELD['ADC_REF_BUFF'] & 0x1) << 4) |
                 (self._BITFIELD['RT_CONV_RATE'] & 0x3))
        self.write_register(self.REGISTER_ADDRESSES['ADC_CFG'], value)

    def write_ADC_CTRL_SIG(self):
        """
        Write the register ADC_CTRL_SIG with the shadow register contents.
        """
        value = (((self._BITFIELD['ADC_CAL_START'] & 0x1) << 3) |
                 ((self._BITFIELD['ADC_SAMPLE'] & 0x1) << 2) |
                 ((self._BITFIELD['ADC_SOC'] & 0x1) << 1) |
                 (self._BITFIELD['ADC_RESETB'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ADC_CTRL_SIG'], value)

    def write_ADC_IN0_HYST(self):
        """
        Write the register ADC_IN0_HYST with the shadow register contents.
        """
        value = ((self._BITFIELD['HYST_ADC_IN0'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN0_HYST'], value)

    def write_ADC_IN0_LO_THR_H(self):
        """
        Write the register ADC_IN0_LO_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_ADC_IN0_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN0_LO_THR_H'], value)

    def write_ADC_IN0_LO_THR_L(self):
        """
        Write the register ADC_IN0_LO_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_ADC_IN0_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN0_LO_THR_L'], value)

    def write_ADC_IN0_UP_THR_H(self):
        """
        Write the register ADC_IN0_UP_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_ADC_IN0_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN0_UP_THR_H'], value)

    def write_ADC_IN0_UP_THR_L(self):
        """
        Write the register ADC_IN0_UP_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_ADC_IN0_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN0_UP_THR_L'], value)

    def write_ADC_IN1_HYST(self):
        """
        Write the register ADC_IN1_HYST with the shadow register contents.
        """
        value = ((self._BITFIELD['HYST_ADC_IN1'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN1_HYST'], value)

    def write_ADC_IN1_LO_THR_H(self):
        """
        Write the register ADC_IN1_LO_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_ADC_IN1_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN1_LO_THR_H'], value)

    def write_ADC_IN1_LO_THR_L(self):
        """
        Write the register ADC_IN1_LO_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_ADC_IN1_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN1_LO_THR_L'], value)

    def write_ADC_IN1_UP_THR_H(self):
        """
        Write the register ADC_IN1_UP_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_ADC_IN1_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN1_UP_THR_H'], value)

    def write_ADC_IN1_UP_THR_L(self):
        """
        Write the register ADC_IN1_UP_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_ADC_IN1_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_IN1_UP_THR_L'], value)

    def write_ADC_LT_CAL(self):
        """
        Write the register ADC_LT_CAL with the shadow register contents.
        """
        value = (((self._BITFIELD['LT_SENSE_GAIN_CAL_H'] & 0x1F) << 3) |
                 (self._BITFIELD['LT_SENSE_GAIN_CAL_L'] & 0x7))
        self.write_register(self.REGISTER_ADDRESSES['ADC_LT_CAL'], value)

    def write_ADC_MUX_CFG(self):
        """
        Write the register ADC_MUX_CFG with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_6_ADC_MUX_CFG'] & 0x3) << 6) |
                 ((self._BITFIELD['RT_CH'] & 0x1) << 5) |
                 ((self._BITFIELD['LT_CH'] & 0x1) << 4) |
                 ((self._BITFIELD['CS_B'] & 0x1) << 3) |
                 ((self._BITFIELD['CS_A'] & 0x1) << 2) |
                 ((self._BITFIELD['ADC_IN1'] & 0x1) << 1) |
                 (self._BITFIELD['ADC_IN0'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ADC_MUX_CFG'], value)

    def write_ADC_OFFSET_ADC_IN_CAL(self):
        """
        Write the register ADC_OFFSET_ADC_IN_CAL with the shadow register contents.
        """
        value = (((self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['ADC_OFFSET_ADC_IN_CAL'], value)

    def write_ADC_OFFSET_CS_CAL(self):
        """
        Write the register ADC_OFFSET_CS_CAL with the shadow register contents.
        """
        value = (((self._BITFIELD['ADC_OFFSET_CS_CAL_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['ADC_OFFSET_CS_CAL_OFFSET_VALUE'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['ADC_OFFSET_CS_CAL'], value)

    def write_ADC_OFFSET_LT_CAL(self):
        """
        Write the register ADC_OFFSET_LT_CAL with the shadow register contents.
        """
        value = (((self._BITFIELD['ADC_OFFSET_LT_CAL_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['ADC_OFFSET_LT_CAL_OFFSET_VALUE'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['ADC_OFFSET_LT_CAL'], value)

    def write_ADC_OFFSET_RT_CAL(self):
        """
        Write the register ADC_OFFSET_RT_CAL with the shadow register contents.
        """
        value = (((self._BITFIELD['ADC_OFFSET_RT_CAL_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['ADC_OFFSET_RT_CAL_OFFSET_VALUE'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['ADC_OFFSET_RT_CAL'], value)

    def write_ADC_RT_CAL(self):
        """
        Write the register ADC_RT_CAL with the shadow register contents.
        """
        value = (((self._BITFIELD['RT_SENSE_GAIN_CAL_H'] & 0x1F) << 3) |
                 (self._BITFIELD['RT_SENSE_GAIN_CAL_L'] & 0x7))
        self.write_register(self.REGISTER_ADDRESSES['ADC_RT_CAL'], value)

    def write_ADC_TEST_CNTL(self):
        """
        Write the register ADC_TEST_CNTL with the shadow register contents.
        """
        value = (((self._BITFIELD['ADC_VCM_EN_SEL'] & 0x1) << 4) |
                 ((self._BITFIELD['ADC_CAL_TM_EN'] & 0x1) << 3) |
                 ((self._BITFIELD['ADC_CAL_OFFSET_EN'] & 0x1) << 2) |
                 ((self._BITFIELD['ADC_LDO_EN'] & 0x1) << 1) |
                 (self._BITFIELD['ADC_VCM_EN'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ADC_TEST_CNTL'], value)

    def write_ADC_TRIG(self):
        """
        Write the register ADC_TRIG with the shadow register contents.
        """
        value = ((self._BITFIELD['ICONV'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ADC_TRIG'], value)

    def write_ADC_TRIM_LDO(self):
        """
        Write the register ADC_TRIM_LDO with the shadow register contents.
        """
        value = ((self._BITFIELD['ADC_TRIM_LDO'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_TRIM_LDO'], value)

    def write_ADC_TRIM_REFBUF(self):
        """
        Write the register ADC_TRIM_REFBUF with the shadow register contents.
        """
        value = ((self._BITFIELD['ADC_TRIM_REFBUF'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_TRIM_REFBUF'], value)

    def write_ADC_TRIM_VCM(self):
        """
        Write the register ADC_TRIM_VCM with the shadow register contents.
        """
        value = ((self._BITFIELD['ADC_TRIM_VCM'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ADC_TRIM_VCM'], value)

    def write_ALR_CFG_0(self):
        """
        Write the register ALR_CFG_0 with the shadow register contents.
        """
        value = (((self._BITFIELD['RT_HIGH_ALR_STAT'] & 0x1) << 5) |
                 ((self._BITFIELD['RT_LOW_ALR_STAT'] & 0x1) << 4) |
                 ((self._BITFIELD['CS_B_ALR_STAT'] & 0x1) << 3) |
                 ((self._BITFIELD['CS_A_ALR_STAT'] & 0x1) << 2) |
                 ((self._BITFIELD['ADC_IN1_ALR_STAT'] & 0x1) << 1) |
                 (self._BITFIELD['ADC_IN0_ALR_STAT'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ALR_CFG_0'], value)

    def write_ALR_CFG_1(self):
        """
        Write the register ALR_CFG_1 with the shadow register contents.
        """
        value = (((self._BITFIELD['ALR_LATCH_DIS'] & 0x1) << 7) |
                 ((self._BITFIELD['S0S1_ERR_ALR'] & 0x1) << 5) |
                 ((self._BITFIELD['PAR_ERR_ALR'] & 0x1) << 4) |
                 ((self._BITFIELD['DAV_ALR'] & 0x1) << 3) |
                 ((self._BITFIELD['THERM_ALR'] & 0x1) << 2) |
                 ((self._BITFIELD['LT_HIGH_ALR'] & 0x1) << 1) |
                 (self._BITFIELD['LT_LOW_ALR'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ALR_CFG_1'], value)

    def write_ANATOP6(self):
        """
        Write the register ANATOP6 with the shadow register contents.
        """
        value = ((self._BITFIELD['ANATOP6'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ANATOP6'], value)

    def write_ANATOP7(self):
        """
        Write the register ANATOP7 with the shadow register contents.
        """
        value = ((self._BITFIELD['ANATOP7'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ANATOP7'], value)

    def write_ANATOP8(self):
        """
        Write the register ANATOP8 with the shadow register contents.
        """
        value = ((self._BITFIELD['ANATOP8'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ANATOP8'], value)

    def write_ANATOP9(self):
        """
        Write the register ANATOP9 with the shadow register contents.
        """
        value = ((self._BITFIELD['ANATOP9'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ANATOP9'], value)

    def write_ANA_DFT_CTRL(self):
        """
        Write the register ANA_DFT_CTRL with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_ANA_DFT_CTRL'] & 0x1) << 7) |
                 ((self._BITFIELD['EN_BYPASS_ANA_DFT_BUF'] & 0x1) << 6) |
                 ((self._BITFIELD['EN_RES_LADDER_CALIB'] & 0x3) << 4) |
                 ((self._BITFIELD['RES_DIV_SEL'] & 0x1) << 3) |
                 ((self._BITFIELD['EN_RES_DIV'] & 0x1) << 2) |
                 ((self._BITFIELD['EN_DIRECT_PATH'] & 0x1) << 1) |
                 (self._BITFIELD['EN_ANA_DFT_BUFFER'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ANA_DFT_CTRL'], value)

    def write_ANA_DFT_MUX_CTRL(self):
        """
        Write the register ANA_DFT_MUX_CTRL with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_4_ANA_DFT_MUX_CTRL'] & 0xF) << 4) |
                 ((self._BITFIELD['ANA_DFT_MUX_SEL'] & 0x7) << 1) |
                 (self._BITFIELD['EN_ANA_DFT_MUX'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ANA_DFT_MUX_CTRL'], value)

    def write_ATEST_CNTL0(self):
        """
        Write the register ATEST_CNTL0 with the shadow register contents.
        """
        value = ((self._BITFIELD['ATEST_CNTL0'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['ATEST_CNTL0'], value)

    def write_ATEST_CNTL1(self):
        """
        Write the register ATEST_CNTL1 with the shadow register contents.
        """
        value = ((self._BITFIELD['SPIKE_FILTER_TEST_MODE'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['ATEST_CNTL1'], value)

    def write_CS_A_DEL_ER_VCM0(self):
        """
        Write the register CS_A_DEL_ER_VCM0 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM0_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM0'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM0'], value)

    def write_CS_A_DEL_ER_VCM1(self):
        """
        Write the register CS_A_DEL_ER_VCM1 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM1_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM1'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM1'], value)

    def write_CS_A_DEL_ER_VCM10(self):
        """
        Write the register CS_A_DEL_ER_VCM10 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM10_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM10'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM10'], value)

    def write_CS_A_DEL_ER_VCM11(self):
        """
        Write the register CS_A_DEL_ER_VCM11 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM11_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM11'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM11'], value)

    def write_CS_A_DEL_ER_VCM12(self):
        """
        Write the register CS_A_DEL_ER_VCM12 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM12_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM12'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM12'], value)

    def write_CS_A_DEL_ER_VCM13(self):
        """
        Write the register CS_A_DEL_ER_VCM13 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM13_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM13'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM13'], value)

    def write_CS_A_DEL_ER_VCM14(self):
        """
        Write the register CS_A_DEL_ER_VCM14 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM14_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM14'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM14'], value)

    def write_CS_A_DEL_ER_VCM15(self):
        """
        Write the register CS_A_DEL_ER_VCM15 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM15_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM15'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM15'], value)

    def write_CS_A_DEL_ER_VCM16(self):
        """
        Write the register CS_A_DEL_ER_VCM16 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM16_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM16'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM16'], value)

    def write_CS_A_DEL_ER_VCM17(self):
        """
        Write the register CS_A_DEL_ER_VCM17 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM17_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM17'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM17'], value)

    def write_CS_A_DEL_ER_VCM18(self):
        """
        Write the register CS_A_DEL_ER_VCM18 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM18_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM18'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM18'], value)

    def write_CS_A_DEL_ER_VCM19(self):
        """
        Write the register CS_A_DEL_ER_VCM19 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM19_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM19'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM19'], value)

    def write_CS_A_DEL_ER_VCM2(self):
        """
        Write the register CS_A_DEL_ER_VCM2 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM2_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM2'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM2'], value)

    def write_CS_A_DEL_ER_VCM3(self):
        """
        Write the register CS_A_DEL_ER_VCM3 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM3_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM3'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM3'], value)

    def write_CS_A_DEL_ER_VCM4(self):
        """
        Write the register CS_A_DEL_ER_VCM4 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM4_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM4'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM4'], value)

    def write_CS_A_DEL_ER_VCM5(self):
        """
        Write the register CS_A_DEL_ER_VCM5 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM5_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM5'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM5'], value)

    def write_CS_A_DEL_ER_VCM6(self):
        """
        Write the register CS_A_DEL_ER_VCM6 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM6_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM6'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM6'], value)

    def write_CS_A_DEL_ER_VCM7(self):
        """
        Write the register CS_A_DEL_ER_VCM7 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM7_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM7'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM7'], value)

    def write_CS_A_DEL_ER_VCM8(self):
        """
        Write the register CS_A_DEL_ER_VCM8 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM8_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM8'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM8'], value)

    def write_CS_A_DEL_ER_VCM9(self):
        """
        Write the register CS_A_DEL_ER_VCM9 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_DEL_ER_VCM9_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_A_DEL_ER_VCM9'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM9'], value)

    def write_CS_A_ER_VCM_BASE_H(self):
        """
        Write the register CS_A_ER_VCM_BASE_H with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_CAL_ALU_BYP'] & 0x1) << 7) |
                 ((self._BITFIELD['RSVD_6_5_CS_A_ER_VCM_BASE_H'] & 0x3) << 5) |
                 ((self._BITFIELD['CS_A_ER_VCM_BASE_H_SIGN'] & 0x1) << 4) |
                 (self._BITFIELD['CS_A_ER_VCM_BASE_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_ER_VCM_BASE_H'], value)

    def write_CS_A_ER_VCM_BASE_L(self):
        """
        Write the register CS_A_ER_VCM_BASE_L with the shadow register contents.
        """
        value = ((self._BITFIELD['CS_A_ER_VCM_BASE_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_ER_VCM_BASE_L'], value)

    def write_CS_A_GAIN_ERROR(self):
        """
        Write the register CS_A_GAIN_ERROR with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_A_GAIN_ERROR_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['GAIN_ERROR_CS_A_GAIN_ERROR'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_GAIN_ERROR'], value)

    def write_CS_A_HYST(self):
        """
        Write the register CS_A_HYST with the shadow register contents.
        """
        value = ((self._BITFIELD['HYST_CS_A'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_HYST'], value)

    def write_CS_A_LO_THR_H(self):
        """
        Write the register CS_A_LO_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_CS_A_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_LO_THR_H'], value)

    def write_CS_A_LO_THR_L(self):
        """
        Write the register CS_A_LO_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_CS_A_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_LO_THR_L'], value)

    def write_CS_A_LUT0_OFFSET(self):
        """
        Write the register CS_A_LUT0_OFFSET with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_6_CS_A_LUT0_OFFSET'] & 0x3) << 6) |
                 (self._BITFIELD['CS_A_LUT0_OFFSET_LUT0_OFFSET'] & 0x3F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_LUT0_OFFSET'], value)

    def write_CS_A_LUT1_OFFSET(self):
        """
        Write the register CS_A_LUT1_OFFSET with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_6_CS_A_LUT1_OFFSET'] & 0x3) << 6) |
                 (self._BITFIELD['CS_A_LUT1_OFFSET'] & 0x3F))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_LUT1_OFFSET'], value)

    def write_CS_A_UP_THR_H(self):
        """
        Write the register CS_A_UP_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_CS_A_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_UP_THR_H'], value)

    def write_CS_A_UP_THR_L(self):
        """
        Write the register CS_A_UP_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_CS_A_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_UP_THR_L'], value)

    def write_CS_A_VCM_BASE_H(self):
        """
        Write the register CS_A_VCM_BASE_H with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_4_CS_A_VCM_BASE_H'] & 0xF) << 4) |
                 (self._BITFIELD['CS_A_VCM_BASE_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_VCM_BASE_H'], value)

    def write_CS_A_VCM_BASE_L(self):
        """
        Write the register CS_A_VCM_BASE_L with the shadow register contents.
        """
        value = ((self._BITFIELD['CS_A_VCM_BASE_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_VCM_BASE_L'], value)

    def write_CS_A_VCM_SLOPE_H(self):
        """
        Write the register CS_A_VCM_SLOPE_H with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_5_CS_A_VCM_SLOPE_H'] & 0x7) << 5) |
                 ((self._BITFIELD['CS_A_VCM_SLOPE_H_SIGN'] & 0x1) << 4) |
                 (self._BITFIELD['CS_A_VCM_SLOPE_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_VCM_SLOPE_H'], value)

    def write_CS_A_VCM_SLOPE_L(self):
        """
        Write the register CS_A_VCM_SLOPE_L with the shadow register contents.
        """
        value = ((self._BITFIELD['CS_A_VCM_SLOPE_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_A_VCM_SLOPE_L'], value)

    def write_CS_B_DEL_ER_VCM0(self):
        """
        Write the register CS_B_DEL_ER_VCM0 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM0_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM0'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM0'], value)

    def write_CS_B_DEL_ER_VCM1(self):
        """
        Write the register CS_B_DEL_ER_VCM1 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM1_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM1'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM1'], value)

    def write_CS_B_DEL_ER_VCM10(self):
        """
        Write the register CS_B_DEL_ER_VCM10 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM10_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM10'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM10'], value)

    def write_CS_B_DEL_ER_VCM11(self):
        """
        Write the register CS_B_DEL_ER_VCM11 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM11_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM11'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM11'], value)

    def write_CS_B_DEL_ER_VCM12(self):
        """
        Write the register CS_B_DEL_ER_VCM12 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM12_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM12'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM12'], value)

    def write_CS_B_DEL_ER_VCM13(self):
        """
        Write the register CS_B_DEL_ER_VCM13 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM13_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM13'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM13'], value)

    def write_CS_B_DEL_ER_VCM14(self):
        """
        Write the register CS_B_DEL_ER_VCM14 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM14_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM14'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM14'], value)

    def write_CS_B_DEL_ER_VCM15(self):
        """
        Write the register CS_B_DEL_ER_VCM15 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM15_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM15'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM15'], value)

    def write_CS_B_DEL_ER_VCM16(self):
        """
        Write the register CS_B_DEL_ER_VCM16 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM16_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM16'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM16'], value)

    def write_CS_B_DEL_ER_VCM17(self):
        """
        Write the register CS_B_DEL_ER_VCM17 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM17_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM17'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM17'], value)

    def write_CS_B_DEL_ER_VCM18(self):
        """
        Write the register CS_B_DEL_ER_VCM18 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM18_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM18'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM18'], value)

    def write_CS_B_DEL_ER_VCM19(self):
        """
        Write the register CS_B_DEL_ER_VCM19 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM19_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM19'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM19'], value)

    def write_CS_B_DEL_ER_VCM2(self):
        """
        Write the register CS_B_DEL_ER_VCM2 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM2_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM2'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM2'], value)

    def write_CS_B_DEL_ER_VCM3(self):
        """
        Write the register CS_B_DEL_ER_VCM3 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM3_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM3'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM3'], value)

    def write_CS_B_DEL_ER_VCM4(self):
        """
        Write the register CS_B_DEL_ER_VCM4 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM4_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM4'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM4'], value)

    def write_CS_B_DEL_ER_VCM5(self):
        """
        Write the register CS_B_DEL_ER_VCM5 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM5_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM5'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM5'], value)

    def write_CS_B_DEL_ER_VCM6(self):
        """
        Write the register CS_B_DEL_ER_VCM6 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM6_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM6'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM6'], value)

    def write_CS_B_DEL_ER_VCM7(self):
        """
        Write the register CS_B_DEL_ER_VCM7 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM7_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM7'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM7'], value)

    def write_CS_B_DEL_ER_VCM8(self):
        """
        Write the register CS_B_DEL_ER_VCM8 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM8_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM8'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM8'], value)

    def write_CS_B_DEL_ER_VCM9(self):
        """
        Write the register CS_B_DEL_ER_VCM9 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DEL_ER_VCM9_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['CS_B_DEL_ER_VCM9'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM9'], value)

    def write_CS_B_ER_VCM_BASE_H(self):
        """
        Write the register CS_B_ER_VCM_BASE_H with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_CAL_ALU_BYP'] & 0x1) << 7) |
                 ((self._BITFIELD['RSVD_6_5_CS_B_ER_VCM_BASE_H'] & 0x3) << 5) |
                 ((self._BITFIELD['CS_B_ER_VCM_BASE_H_SIGN'] & 0x1) << 4) |
                 (self._BITFIELD['CS_B_ER_VCM_BASE_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_ER_VCM_BASE_H'], value)

    def write_CS_B_ER_VCM_BASE_L(self):
        """
        Write the register CS_B_ER_VCM_BASE_L with the shadow register contents.
        """
        value = ((self._BITFIELD['CS_B_ER_VCM_BASE_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_ER_VCM_BASE_L'], value)

    def write_CS_B_GAIN_ERROR(self):
        """
        Write the register CS_B_GAIN_ERROR with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_GAIN_ERROR_SIGN'] & 0x1) << 7) |
                 (self._BITFIELD['GAIN_ERROR_CS_B_GAIN_ERROR'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_GAIN_ERROR'], value)

    def write_CS_B_HYST(self):
        """
        Write the register CS_B_HYST with the shadow register contents.
        """
        value = ((self._BITFIELD['HYST_CS_B'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_HYST'], value)

    def write_CS_B_LO_THR_H(self):
        """
        Write the register CS_B_LO_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_CS_B_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_LO_THR_H'], value)

    def write_CS_B_LO_THR_L(self):
        """
        Write the register CS_B_LO_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_CS_B_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_LO_THR_L'], value)

    def write_CS_B_LUT0_OFFSET(self):
        """
        Write the register CS_B_LUT0_OFFSET with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_6_CS_B_LUT0_OFFSET'] & 0x3) << 6) |
                 (self._BITFIELD['CS_B_LUT0_OFFSET_LUT0_OFFSET'] & 0x3F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_LUT0_OFFSET'], value)

    def write_CS_B_LUT1_OFFSET(self):
        """
        Write the register CS_B_LUT1_OFFSET with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_6_CS_B_LUT1_OFFSET'] & 0x3) << 6) |
                 (self._BITFIELD['CS_B_LUT1_OFFSET'] & 0x3F))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_LUT1_OFFSET'], value)

    def write_CS_B_UP_THR_H(self):
        """
        Write the register CS_B_UP_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_CS_B_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_UP_THR_H'], value)

    def write_CS_B_UP_THR_L(self):
        """
        Write the register CS_B_UP_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_CS_B_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_UP_THR_L'], value)

    def write_CS_B_VCM_BASE_H(self):
        """
        Write the register CS_B_VCM_BASE_H with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_4_CS_B_VCM_BASE_H'] & 0xF) << 4) |
                 (self._BITFIELD['CS_B_VCM_BASE_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_VCM_BASE_H'], value)

    def write_CS_B_VCM_BASE_L(self):
        """
        Write the register CS_B_VCM_BASE_L with the shadow register contents.
        """
        value = ((self._BITFIELD['CS_B_VCM_BASE_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_VCM_BASE_L'], value)

    def write_CS_B_VCM_SLOPE_H(self):
        """
        Write the register CS_B_VCM_SLOPE_H with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_5_CS_B_VCM_SLOPE_H'] & 0x7) << 5) |
                 ((self._BITFIELD['CS_B_VCM_SLOPE_H_SIGN'] & 0x1) << 4) |
                 (self._BITFIELD['CS_B_VCM_SLOPE_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_VCM_SLOPE_H'], value)

    def write_CS_B_VCM_SLOPE_L(self):
        """
        Write the register CS_B_VCM_SLOPE_L with the shadow register contents.
        """
        value = ((self._BITFIELD['CS_B_VCM_SLOPE_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_B_VCM_SLOPE_L'], value)

    def write_CS_CFG_0(self):
        """
        Write the register CS_CFG_0 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_DAC_MODE'] & 0x1) << 7) |
                 ((self._BITFIELD['CS_DATA_CLAMP_EN'] & 0x1) << 6) |
                 ((self._BITFIELD['CS_ADC_ACQ_DLY_EN'] & 0x1) << 5) |
                 ((self._BITFIELD['CS_CFG_0_SIGN'] & 0x1) << 4) |
                 (self._BITFIELD['CS_A_DAC_OFFSET'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_CFG_0'], value)

    def write_CS_CFG_1(self):
        """
        Write the register CS_CFG_1 with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_CONV_RATE'] & 0x7) << 5) |
                 ((self._BITFIELD['CS_CFG_1_SIGN'] & 0x1) << 4) |
                 (self._BITFIELD['CS_B_DAC_OFFSET'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_CFG_1'], value)

    def write_CS_CFG_2(self):
        """
        Write the register CS_CFG_2 with the shadow register contents.
        """
        value = (((self._BITFIELD['DAC_CODE_BYPASS'] & 0x1) << 7) |
                 (self._BITFIELD['CS_CFG_2_DAC_CODE'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['CS_CFG_2'], value)

    def write_CS_DIFF10_OVRD_H(self):
        """
        Write the register CS_DIFF10_OVRD_H with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_DIFF10_OVRD_H_SIGN'] & 0x1) << 4) |
                 (self._BITFIELD['DIFF10_OVRD_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_DIFF10_OVRD_H'], value)

    def write_CS_DIFF10_OVRD_L(self):
        """
        Write the register CS_DIFF10_OVRD_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DIFF10_OVRD_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_DIFF10_OVRD_L'], value)

    def write_CS_DTEST_CTRL(self):
        """
        Write the register CS_DTEST_CTRL with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_B_DTEST_EN'] & 0x1) << 7) |
                 ((self._BITFIELD['CS_B_DTEST_CTRL'] & 0x7) << 4) |
                 ((self._BITFIELD['CS_A_DTEST_EN'] & 0x1) << 3) |
                 (self._BITFIELD['CS_A_DTEST_CTRL'] & 0x7))
        self.write_register(self.REGISTER_ADDRESSES['CS_DTEST_CTRL'], value)

    def write_CS_TEST_CTRL(self):
        """
        Write the register CS_TEST_CTRL with the shadow register contents.
        """
        value = (((self._BITFIELD['CS_VCM_OC'] & 0x1) << 7) |
                 ((self._BITFIELD['CS_VCM_OCH'] & 0x1) << 6) |
                 ((self._BITFIELD['CS_VCM_UPDATE'] & 0x1) << 5) |
                 ((self._BITFIELD['CS_CAL_MODE'] & 0x1) << 4) |
                 ((self._BITFIELD['CS_PHASE_CTRL'] & 0x1) << 3) |
                 (self._BITFIELD['CS_MUX_SEL'] & 0x7))
        self.write_register(self.REGISTER_ADDRESSES['CS_TEST_CTRL'], value)

    def write_CS_VCM_OVRD_H(self):
        """
        Write the register CS_VCM_OVRD_H with the shadow register contents.
        """
        value = ((self._BITFIELD['VCM_OVRD_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['CS_VCM_OVRD_H'], value)

    def write_CS_VCM_OVRD_L(self):
        """
        Write the register CS_VCM_OVRD_L with the shadow register contents.
        """
        value = ((self._BITFIELD['VCM_OVRD_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['CS_VCM_OVRD_L'], value)

    def write_DAC0_DATA_H(self):
        """
        Write the register DAC0_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC0_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC0_DATA_H'], value)

    def write_DAC0_DATA_L(self):
        """
        Write the register DAC0_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC0_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC0_DATA_L'], value)

    def write_DAC0_GAIN_CAL_R00(self):
        """
        Write the register DAC0_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC0_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC0_GAIN_CAL_R00'], value)

    def write_DAC0_GAIN_CAL_R11(self):
        """
        Write the register DAC0_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC0_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC0_GAIN_CAL_R11'], value)

    def write_DAC0_OFFSET_CAL_R00(self):
        """
        Write the register DAC0_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC0_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC0_OFFSET_CAL_R00'], value)

    def write_DAC0_OFFSET_CAL_R11(self):
        """
        Write the register DAC0_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC0_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC0_OFFSET_CAL_R11'], value)

    def write_DAC1_DATA_H(self):
        """
        Write the register DAC1_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC1_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC1_DATA_H'], value)

    def write_DAC1_DATA_L(self):
        """
        Write the register DAC1_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC1_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC1_DATA_L'], value)

    def write_DAC1_GAIN_CAL_R00(self):
        """
        Write the register DAC1_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC1_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC1_GAIN_CAL_R00'], value)

    def write_DAC1_GAIN_CAL_R11(self):
        """
        Write the register DAC1_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC1_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC1_GAIN_CAL_R11'], value)

    def write_DAC1_OFFSET_CAL_R00(self):
        """
        Write the register DAC1_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC1_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC1_OFFSET_CAL_R00'], value)

    def write_DAC1_OFFSET_CAL_R11(self):
        """
        Write the register DAC1_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC1_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC1_OFFSET_CAL_R11'], value)

    def write_DAC2_DATA_H(self):
        """
        Write the register DAC2_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC2_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC2_DATA_H'], value)

    def write_DAC2_DATA_L(self):
        """
        Write the register DAC2_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC2_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC2_DATA_L'], value)

    def write_DAC2_GAIN_CAL_R00(self):
        """
        Write the register DAC2_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC2_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC2_GAIN_CAL_R00'], value)

    def write_DAC2_GAIN_CAL_R11(self):
        """
        Write the register DAC2_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC2_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC2_GAIN_CAL_R11'], value)

    def write_DAC2_OFFSET_CAL_R00(self):
        """
        Write the register DAC2_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC2_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC2_OFFSET_CAL_R00'], value)

    def write_DAC2_OFFSET_CAL_R11(self):
        """
        Write the register DAC2_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC2_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC2_OFFSET_CAL_R11'], value)

    def write_DAC3_DATA_H(self):
        """
        Write the register DAC3_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC3_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC3_DATA_H'], value)

    def write_DAC3_DATA_L(self):
        """
        Write the register DAC3_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC3_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC3_DATA_L'], value)

    def write_DAC3_GAIN_CAL_R00(self):
        """
        Write the register DAC3_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC3_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC3_GAIN_CAL_R00'], value)

    def write_DAC3_GAIN_CAL_R11(self):
        """
        Write the register DAC3_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC3_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC3_GAIN_CAL_R11'], value)

    def write_DAC3_OFFSET_CAL_R00(self):
        """
        Write the register DAC3_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC3_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC3_OFFSET_CAL_R00'], value)

    def write_DAC3_OFFSET_CAL_R11(self):
        """
        Write the register DAC3_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC3_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC3_OFFSET_CAL_R11'], value)

    def write_DAC4_DATA_H(self):
        """
        Write the register DAC4_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC4_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC4_DATA_H'], value)

    def write_DAC4_DATA_L(self):
        """
        Write the register DAC4_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC4_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC4_DATA_L'], value)

    def write_DAC4_GAIN_CAL_R00(self):
        """
        Write the register DAC4_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC4_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC4_GAIN_CAL_R00'], value)

    def write_DAC4_GAIN_CAL_R11(self):
        """
        Write the register DAC4_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC4_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC4_GAIN_CAL_R11'], value)

    def write_DAC4_OFFSET_CAL_R00(self):
        """
        Write the register DAC4_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC4_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC4_OFFSET_CAL_R00'], value)

    def write_DAC4_OFFSET_CAL_R11(self):
        """
        Write the register DAC4_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC4_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC4_OFFSET_CAL_R11'], value)

    def write_DAC5_DATA_H(self):
        """
        Write the register DAC5_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC5_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC5_DATA_H'], value)

    def write_DAC5_DATA_L(self):
        """
        Write the register DAC5_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC5_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC5_DATA_L'], value)

    def write_DAC5_GAIN_CAL_R00(self):
        """
        Write the register DAC5_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC5_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC5_GAIN_CAL_R00'], value)

    def write_DAC5_GAIN_CAL_R11(self):
        """
        Write the register DAC5_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC5_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC5_GAIN_CAL_R11'], value)

    def write_DAC5_OFFSET_CAL_R00(self):
        """
        Write the register DAC5_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC5_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC5_OFFSET_CAL_R00'], value)

    def write_DAC5_OFFSET_CAL_R11(self):
        """
        Write the register DAC5_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC5_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC5_OFFSET_CAL_R11'], value)

    def write_DAC6_DATA_H(self):
        """
        Write the register DAC6_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC6_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC6_DATA_H'], value)

    def write_DAC6_DATA_L(self):
        """
        Write the register DAC6_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC6_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC6_DATA_L'], value)

    def write_DAC6_GAIN_CAL_R00(self):
        """
        Write the register DAC6_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC6_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC6_GAIN_CAL_R00'], value)

    def write_DAC6_GAIN_CAL_R11(self):
        """
        Write the register DAC6_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC6_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC6_GAIN_CAL_R11'], value)

    def write_DAC6_OFFSET_CAL_R00(self):
        """
        Write the register DAC6_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC6_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC6_OFFSET_CAL_R00'], value)

    def write_DAC6_OFFSET_CAL_R11(self):
        """
        Write the register DAC6_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC6_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC6_OFFSET_CAL_R11'], value)

    def write_DAC7_DATA_H(self):
        """
        Write the register DAC7_DATA_H with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC7_DATA_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['DAC7_DATA_H'], value)

    def write_DAC7_DATA_L(self):
        """
        Write the register DAC7_DATA_L with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC7_DATA_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC7_DATA_L'], value)

    def write_DAC7_GAIN_CAL_R00(self):
        """
        Write the register DAC7_GAIN_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC7_GAIN_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC7_GAIN_CAL_R00'], value)

    def write_DAC7_GAIN_CAL_R11(self):
        """
        Write the register DAC7_GAIN_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC7_GAIN_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC7_GAIN_CAL_R11'], value)

    def write_DAC7_OFFSET_CAL_R00(self):
        """
        Write the register DAC7_OFFSET_CAL_R00 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC7_OFFSET_CAL_R00'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC7_OFFSET_CAL_R00'], value)

    def write_DAC7_OFFSET_CAL_R11(self):
        """
        Write the register DAC7_OFFSET_CAL_R11 with the shadow register contents.
        """
        value = ((self._BITFIELD['DAC7_OFFSET_CAL_R11'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['DAC7_OFFSET_CAL_R11'], value)

    def write_DAC_CLR(self):
        """
        Write the register DAC_CLR with the shadow register contents.
        """
        value = (((self._BITFIELD['CLR_B7'] & 0x1) << 7) |
                 ((self._BITFIELD['CLR_B6'] & 0x1) << 6) |
                 ((self._BITFIELD['CLR_B5'] & 0x1) << 5) |
                 ((self._BITFIELD['CLR_B4'] & 0x1) << 4) |
                 ((self._BITFIELD['CLR_A3'] & 0x1) << 3) |
                 ((self._BITFIELD['CLR_A2'] & 0x1) << 2) |
                 ((self._BITFIELD['CLR_A1'] & 0x1) << 1) |
                 (self._BITFIELD['CLR_A0'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['DAC_CLR'], value)

    def write_DAC_CLR_EN(self):
        """
        Write the register DAC_CLR_EN with the shadow register contents.
        """
        value = (((self._BITFIELD['CLREN_B7'] & 0x1) << 7) |
                 ((self._BITFIELD['CLREN_B6'] & 0x1) << 6) |
                 ((self._BITFIELD['CLREN_B5'] & 0x1) << 5) |
                 ((self._BITFIELD['CLREN_B4'] & 0x1) << 4) |
                 ((self._BITFIELD['CLREN_A3'] & 0x1) << 3) |
                 ((self._BITFIELD['CLREN_A2'] & 0x1) << 2) |
                 ((self._BITFIELD['CLREN_A1'] & 0x1) << 1) |
                 (self._BITFIELD['CLREN_A0'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['DAC_CLR_EN'], value)

    def write_DAC_CLR_SRC_0(self):
        """
        Write the register DAC_CLR_SRC_0 with the shadow register contents.
        """
        value = (((self._BITFIELD['RT_HIGH_ALR_CLR'] & 0x1) << 5) |
                 ((self._BITFIELD['RT_LOW_ALR_CLR'] & 0x1) << 4) |
                 ((self._BITFIELD['CS_B_ALR_CLR'] & 0x1) << 3) |
                 ((self._BITFIELD['CS_A_ALR_CLR'] & 0x1) << 2) |
                 ((self._BITFIELD['ADC_IN1_ALR_CLR'] & 0x1) << 1) |
                 (self._BITFIELD['ADC_IN0_ALR_CLR'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['DAC_CLR_SRC_0'], value)

    def write_DAC_CLR_SRC_1(self):
        """
        Write the register DAC_CLR_SRC_1 with the shadow register contents.
        """
        value = (((self._BITFIELD['THERM_ALR_CLR'] & 0x1) << 2) |
                 ((self._BITFIELD['LT_HIGH_ALR_CLR'] & 0x1) << 1) |
                 (self._BITFIELD['LT_LOW_ALR_CLR'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['DAC_CLR_SRC_1'], value)

    def write_DAC_OUT_OK_CFG(self):
        """
        Write the register DAC_OUT_OK_CFG with the shadow register contents.
        """
        value = (((self._BITFIELD['ASSERT'] & 0x1) << 7) |
                 (self._BITFIELD['TIMER'] & 0x7F))
        self.write_register(self.REGISTER_ADDRESSES['DAC_OUT_OK_CFG'], value)

    def write_DAC_RANGE(self):
        """
        Write the register DAC_RANGE with the shadow register contents.
        """
        value = (((self._BITFIELD['DAC_RANGEB'] & 0x7) << 4) |
                 (self._BITFIELD['DAC_RANGEA'] & 0x7))
        self.write_register(self.REGISTER_ADDRESSES['DAC_RANGE'], value)

    def write_DAC_SW_EN(self):
        """
        Write the register DAC_SW_EN with the shadow register contents.
        """
        value = (((self._BITFIELD['DAC_B2_SW_EN'] & 0x1) << 3) |
                 ((self._BITFIELD['DAC_B0_SW_EN'] & 0x1) << 2) |
                 ((self._BITFIELD['DAC_A2_SW_EN'] & 0x1) << 1) |
                 (self._BITFIELD['DAC_A0_SW_EN'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['DAC_SW_EN'], value)

    def write_DAC_TEST_CNTL(self):
        """
        Write the register DAC_TEST_CNTL with the shadow register contents.
        """
        value = (((self._BITFIELD['DAC_CLAMP_DIS'] & 0x1) << 7) |
                 ((self._BITFIELD['DAC_HIZ_GROUP_B'] & 0x1) << 5) |
                 ((self._BITFIELD['DAC_HIZ_GROUP_A'] & 0x1) << 4) |
                 0)
        self.write_register(self.REGISTER_ADDRESSES['DAC_TEST_CNTL'], value)

    def write_DTEST_CNTL0(self):
        """
        Write the register DTEST_CNTL0 with the shadow register contents.
        """
        value = (((self._BITFIELD['TRIM_DIS'] & 0x1) << 7) |
                 ((self._BITFIELD['OSC_CLK_DIS'] & 0x1) << 6) |
                 ((self._BITFIELD['ADC_TEST'] & 0x1) << 5) |
                 ((self._BITFIELD['OSC_TEST_ENABLE'] & 0x1) << 4) |
                 ((self._BITFIELD['TRACE_PORT'] & 0x1) << 3) |
                 ((self._BITFIELD['OSC_CLK_EXT'] & 0x1) << 2) |
                 ((self._BITFIELD['IO_TEST'] & 0x1) << 1) |
                 (self._BITFIELD['SCAN_TEST'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['DTEST_CNTL0'], value)

    def write_E2P_PD_DAC(self):
        """
        Write the register E2P_PD_DAC with the shadow register contents.
        """
        value = ((self._BITFIELD['PD_DAC'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['E2P_PD_DAC'], value)

    def write_EEPROM_CFG(self):
        """
        Write the register EEPROM_CFG with the shadow register contents.
        """
        value = (((self._BITFIELD['E2P_FAST_MODE'] & 0x1) << 1) |
                 (self._BITFIELD['ECC_DIS'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['EEPROM_CFG'], value)

    def write_EEPROM_CNTL(self):
        """
        Write the register EEPROM_CNTL with the shadow register contents.
        """
        value = ((self._BITFIELD['CMD_STATUS'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['EEPROM_CNTL'], value)

    def write_FALSE_ALR_CFG(self):
        """
        Write the register FALSE_ALR_CFG with the shadow register contents.
        """
        value = (((self._BITFIELD['CH_FALR_CT'] & 0x7) << 5) |
                 ((self._BITFIELD['LT_FALR_CT'] & 0x3) << 3) |
                 ((self._BITFIELD['RT_FALR_CT'] & 0x3) << 1) |
                 0)
        self.write_register(self.REGISTER_ADDRESSES['FALSE_ALR_CFG'], value)

    def write_GPIO_IEB(self):
        """
        Write the register GPIO_IEB with the shadow register contents.
        """
        value = (((self._BITFIELD['DAC_OUT_OK_IEB'] & 0x1) << 6) |
                 ((self._BITFIELD['SDO_IEB'] & 0x1) << 5) |
                 ((self._BITFIELD['SDI_IEB'] & 0x1) << 4) |
                 ((self._BITFIELD['CSB_IEB'] & 0x1) << 3) |
                 ((self._BITFIELD['SCLK_IEB'] & 0x1) << 2) |
                 ((self._BITFIELD['OUT_BEN_IEB'] & 0x1) << 1) |
                 (self._BITFIELD['OUT_AEN_IEB'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['GPIO_IEB'], value)

    def write_GPIO_OEB(self):
        """
        Write the register GPIO_OEB with the shadow register contents.
        """
        value = (((self._BITFIELD['DAC_OUT_OK_OEB'] & 0x1) << 2) |
                 ((self._BITFIELD['OUT_BEN_OEB'] & 0x1) << 1) |
                 0)
        self.write_register(self.REGISTER_ADDRESSES['GPIO_OEB'], value)

    def write_GPIO_OUT(self):
        """
        Write the register GPIO_OUT with the shadow register contents.
        """
        value = (((self._BITFIELD['OUT_BEN_OUT'] & 0x1) << 1) |
                 0)
        self.write_register(self.REGISTER_ADDRESSES['GPIO_OUT'], value)

    def write_GPIO_TRACE(self):
        """
        Write the register GPIO_TRACE with the shadow register contents.
        """
        value = ((self._BITFIELD['GPIO_TRACE'] & 0x1F))
        self.write_register(self.REGISTER_ADDRESSES['GPIO_TRACE'], value)

    def write_IF_CFG_0(self):
        """
        Write the register IF_CFG_0 with the shadow register contents.
        """
        value = (((self._BITFIELD['SOFT_RESET'] & 0x1) << 7) |
                 ((self._BITFIELD['ADDR_ASCEND'] & 0x1) << 5) |
                 0)
        self.write_register(self.REGISTER_ADDRESSES['IF_CFG_0'], value)

    def write_IF_CFG_1(self):
        """
        Write the register IF_CFG_1 with the shadow register contents.
        """
        value = (((self._BITFIELD['SINGLE_INSTR'] & 0x1) << 7) |
                 ((self._BITFIELD['READBACK'] & 0x1) << 5) |
                 ((self._BITFIELD['ADDR_MODE'] & 0x1) << 4) |
                 0)
        self.write_register(self.REGISTER_ADDRESSES['IF_CFG_1'], value)

    def write_LDO_TRIM_IOVDD(self):
        """
        Write the register LDO_TRIM_IOVDD with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_5_LDO_TRIM_IOVDD'] & 0x7) << 5) |
                 ((self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_20MA'] & 0x1) << 4) |
                 ((self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_10MA'] & 0x1) << 3) |
                 ((self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_5MA'] & 0x1) << 2) |
                 ((self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P9V'] & 0x1) << 1) |
                 (self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P85V'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['LDO_TRIM_IOVDD'], value)

    def write_LDO_TRIM_VDDD(self):
        """
        Write the register LDO_TRIM_VDDD with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_5_LDO_TRIM_VDDD'] & 0x7) << 5) |
                 ((self._BITFIELD['LDO_TRIM_VDDD_CURRENT_20MA'] & 0x1) << 4) |
                 ((self._BITFIELD['LDO_TRIM_VDDD_CURRENT_10MA'] & 0x1) << 3) |
                 ((self._BITFIELD['LDO_TRIM_VDDD_CURRENT_5MA'] & 0x1) << 2) |
                 ((self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P9V'] & 0x1) << 1) |
                 (self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P85V'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['LDO_TRIM_VDDD'], value)

    def write_LT_HYST(self):
        """
        Write the register LT_HYST with the shadow register contents.
        """
        value = ((self._BITFIELD['HYST_LT'] & 0x1F))
        self.write_register(self.REGISTER_ADDRESSES['LT_HYST'], value)

    def write_LT_LO_THR_H(self):
        """
        Write the register LT_LO_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_LT_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['LT_LO_THR_H'], value)

    def write_LT_LO_THR_L(self):
        """
        Write the register LT_LO_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_LT_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['LT_LO_THR_L'], value)

    def write_LT_THERM_THR_H(self):
        """
        Write the register LT_THERM_THR_H with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_4_LT_THERM_THR_H'] & 0xF) << 4) |
                 (self._BITFIELD['THRT_LT_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['LT_THERM_THR_H'], value)

    def write_LT_THERM_THR_L(self):
        """
        Write the register LT_THERM_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRT_LT_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['LT_THERM_THR_L'], value)

    def write_LT_UP_THR_H(self):
        """
        Write the register LT_UP_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_LT_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['LT_UP_THR_H'], value)

    def write_LT_UP_THR_L(self):
        """
        Write the register LT_UP_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_LT_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['LT_UP_THR_L'], value)

    def write_MISC_CNTL(self):
        """
        Write the register MISC_CNTL with the shadow register contents.
        """
        value = (((self._BITFIELD['I3C_MAX_DS'] & 0x7) << 5) |
                 ((self._BITFIELD['I2C_SPIKE_DIS'] & 0x1) << 4) |
                 ((self._BITFIELD['DAC_CLAMP_EN'] & 0x3) << 2) |
                 ((self._BITFIELD['DAC_ICALP'] & 0x1) << 1) |
                 (self._BITFIELD['DAC_ICALN'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['MISC_CNTL'], value)

    def write_OSC_CMP_HYST(self):
        """
        Write the register OSC_CMP_HYST with the shadow register contents.
        """
        value = ((self._BITFIELD['CMP_HYST'] & 0x3))
        self.write_register(self.REGISTER_ADDRESSES['OSC_CMP_HYST'], value)

    def write_OSC_CNT_CMP_H(self):
        """
        Write the register OSC_CNT_CMP_H with the shadow register contents.
        """
        value = ((self._BITFIELD['CLK_CNT_CMP_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['OSC_CNT_CMP_H'], value)

    def write_OSC_CNT_CMP_L(self):
        """
        Write the register OSC_CNT_CMP_L with the shadow register contents.
        """
        value = ((self._BITFIELD['CLK_CNT_CMP_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['OSC_CNT_CMP_L'], value)

    def write_OUT_AEN_GROUPA(self):
        """
        Write the register OUT_AEN_GROUPA with the shadow register contents.
        """
        value = (((self._BITFIELD['FETDRV_A2_AEN_GROUPA'] & 0x1) << 6) |
                 ((self._BITFIELD['FETDRV_A0_AEN_GROUPA'] & 0x1) << 4) |
                 ((self._BITFIELD['DAC_A3_AEN_GROUPA'] & 0x1) << 3) |
                 ((self._BITFIELD['DAC_A2_AEN_GROUPA'] & 0x1) << 2) |
                 ((self._BITFIELD['DAC_A1_AEN_GROUPA'] & 0x1) << 1) |
                 (self._BITFIELD['DAC_A0_AEN_GROUPA'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['OUT_AEN_GROUPA'], value)

    def write_OUT_AEN_GROUPB(self):
        """
        Write the register OUT_AEN_GROUPB with the shadow register contents.
        """
        value = (((self._BITFIELD['FETDRV_B2_AEN_GROUPB'] & 0x1) << 6) |
                 ((self._BITFIELD['FETDRV_B0_AEN_GROUPB'] & 0x1) << 4) |
                 ((self._BITFIELD['DAC_B3_AEN_GROUPB'] & 0x1) << 3) |
                 ((self._BITFIELD['DAC_B2_AEN_GROUPB'] & 0x1) << 2) |
                 ((self._BITFIELD['DAC_B1_AEN_GROUPB'] & 0x1) << 1) |
                 (self._BITFIELD['DAC_B0_AEN_GROUPB'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['OUT_AEN_GROUPB'], value)

    def write_OUT_BEN_GROUPA(self):
        """
        Write the register OUT_BEN_GROUPA with the shadow register contents.
        """
        value = (((self._BITFIELD['FETDRV_A2_BEN_GROUPA'] & 0x1) << 6) |
                 ((self._BITFIELD['FETDRV_A0_BEN_GROUPA'] & 0x1) << 4) |
                 ((self._BITFIELD['DAC_A3_BEN_GROUPA'] & 0x1) << 3) |
                 ((self._BITFIELD['DAC_A2_BEN_GROUPA'] & 0x1) << 2) |
                 ((self._BITFIELD['DAC_A1_BEN_GROUPA'] & 0x1) << 1) |
                 (self._BITFIELD['DAC_A0_BEN_GROUPA'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['OUT_BEN_GROUPA'], value)

    def write_OUT_BEN_GROUPB(self):
        """
        Write the register OUT_BEN_GROUPB with the shadow register contents.
        """
        value = (((self._BITFIELD['FETDRV_B2_BEN_GROUPB'] & 0x1) << 6) |
                 ((self._BITFIELD['FETDRV_B0_BEN_GROUPB'] & 0x1) << 4) |
                 ((self._BITFIELD['DAC_B3_BEN_GROUPB'] & 0x1) << 3) |
                 ((self._BITFIELD['DAC_B2_BEN_GROUPB'] & 0x1) << 2) |
                 ((self._BITFIELD['DAC_B1_BEN_GROUPB'] & 0x1) << 1) |
                 (self._BITFIELD['DAC_B0_BEN_GROUPB'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['OUT_BEN_GROUPB'], value)

    def write_PD_ADC(self):
        """
        Write the register PD_ADC with the shadow register contents.
        """
        value = ((self._BITFIELD['PADC'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['PD_ADC'], value)

    def write_PD_CS(self):
        """
        Write the register PD_CS with the shadow register contents.
        """
        value = (((self._BITFIELD['PCS_B'] & 0x1) << 1) |
                 (self._BITFIELD['PCS_A'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['PD_CS'], value)

    def write_PD_DAC(self):
        """
        Write the register PD_DAC with the shadow register contents.
        """
        value = (((self._BITFIELD['PDAC_B7'] & 0x1) << 7) |
                 ((self._BITFIELD['PDAC_B6'] & 0x1) << 6) |
                 ((self._BITFIELD['PDAC_B5'] & 0x1) << 5) |
                 ((self._BITFIELD['PDAC_B4'] & 0x1) << 4) |
                 ((self._BITFIELD['PDAC_A3'] & 0x1) << 3) |
                 ((self._BITFIELD['PDAC_A2'] & 0x1) << 2) |
                 ((self._BITFIELD['PDAC_A1'] & 0x1) << 1) |
                 (self._BITFIELD['PDAC_A0'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['PD_DAC'], value)

    def write_PD_DAC_CFG(self):
        """
        Write the register PD_DAC_CFG with the shadow register contents.
        """
        value = (((self._BITFIELD['RSVD_7_3_PD_DAC_CFG'] & 0x1F) << 3) |
                 ((self._BITFIELD['TIM_DAC_DEL_EN'] & 0x1) << 2) |
                 (self._BITFIELD['TIM_DAC_DEL'] & 0x3))
        self.write_register(self.REGISTER_ADDRESSES['PD_DAC_CFG'], value)

    def write_POR_BYPASS_H(self):
        """
        Write the register POR_BYPASS_H with the shadow register contents.
        """
        value = ((self._BITFIELD['POR_BYPASS_H'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['POR_BYPASS_H'], value)

    def write_POR_BYPASS_L(self):
        """
        Write the register POR_BYPASS_L with the shadow register contents.
        """
        value = ((self._BITFIELD['POR_BYPASS_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['POR_BYPASS_L'], value)

    def write_REG_UPDATE(self):
        """
        Write the register REG_UPDATE with the shadow register contents.
        """
        value = (((self._BITFIELD['ADC_UPDATE'] & 0x1) << 4) |
                 (self._BITFIELD['DAC_UPDATE'] & 0x1))
        self.write_register(self.REGISTER_ADDRESSES['REG_UPDATE'], value)

    def write_RT_HYST(self):
        """
        Write the register RT_HYST with the shadow register contents.
        """
        value = ((self._BITFIELD['HYST_RT'] & 0x1F))
        self.write_register(self.REGISTER_ADDRESSES['RT_HYST'], value)

    def write_RT_LO_THR_H(self):
        """
        Write the register RT_LO_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_RT_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['RT_LO_THR_H'], value)

    def write_RT_LO_THR_L(self):
        """
        Write the register RT_LO_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRL_RT_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['RT_LO_THR_L'], value)

    def write_RT_UP_THR_H(self):
        """
        Write the register RT_UP_THR_H with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_RT_H'] & 0xF))
        self.write_register(self.REGISTER_ADDRESSES['RT_UP_THR_H'], value)

    def write_RT_UP_THR_L(self):
        """
        Write the register RT_UP_THR_L with the shadow register contents.
        """
        value = ((self._BITFIELD['THRU_RT_L'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['RT_UP_THR_L'], value)

    def write_SPIKE_FILTER_CAL_SCL(self):
        """
        Write the register SPIKE_FILTER_CAL_SCL with the shadow register contents.
        """
        value = ((self._BITFIELD['SPIKE_FILTER_CAL_SCL'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['SPIKE_FILTER_CAL_SCL'], value)

    def write_SPIKE_FILTER_CAL_SDA(self):
        """
        Write the register SPIKE_FILTER_CAL_SDA with the shadow register contents.
        """
        value = ((self._BITFIELD['SPIKE_FILTER_CAL_SDA'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['SPIKE_FILTER_CAL_SDA'], value)

    def write_TEST_KEY(self):
        """
        Write the register TEST_KEY with the shadow register contents.
        """
        value = ((self._BITFIELD['KEY_STATUS'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['TEST_KEY'], value)

    def write_TRIM_BG(self):
        """
        Write the register TRIM_BG with the shadow register contents.
        """
        value = ((self._BITFIELD['TRIM_BG'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['TRIM_BG'], value)

    def write_TRIM_OSC(self):
        """
        Write the register TRIM_OSC with the shadow register contents.
        """
        value = ((self._BITFIELD['TRIM_OSC'] & 0xFF))
        self.write_register(self.REGISTER_ADDRESSES['TRIM_OSC'], value)

    def read_ADC_AVG(self):
        """
        Read the register ADC_AVG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_AVG'])
        value = readValue & self.READ_COMP_MASK['ADC_AVG']
        self._BITFIELD['RSVD_7_4_ADC_AVG'] = (value & 0xF0) >> 4
        self._BITFIELD['ADC_AVG_ADC'] = (value & 0x0F)

    def read_ADC_CAL_CNTL(self):
        """
        Read the register ADC_CAL_CNTL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_CAL_CNTL'])
        value = readValue & self.READ_COMP_MASK['ADC_CAL_CNTL']
        self._BITFIELD['RSVD_7_ADC_CAL_CNTL'] = (value & 0x80) >> 7
        self._BITFIELD['OFFSET_EN'] = (value & 0x40) >> 6
        self._BITFIELD['RSVD_5_3_ADC_CAL_CNTL'] = (value & 0x38) >> 3
        self._BITFIELD['CS_FAST_AVG_EN'] = (value & 0x04) >> 2
        self._BITFIELD['ADC_SAMPLE_DLY'] = (value & 0x03)

    def read_ADC_CFG(self):
        """
        Read the register ADC_CFG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_CFG'])
        value = readValue & self.READ_COMP_MASK['ADC_CFG']
        self._BITFIELD['CMODE'] = (value & 0x80) >> 7
        self._BITFIELD['ADC_CONV_RATE'] = (value & 0x60) >> 5
        self._BITFIELD['ADC_REF_BUFF'] = (value & 0x10) >> 4
        self._BITFIELD['RSVD_3_2_ADC_CFG'] = (value & 0x0C) >> 2
        self._BITFIELD['RT_CONV_RATE'] = (value & 0x03)

    def read_ADC_CTRL_SIG(self):
        """
        Read the register ADC_CTRL_SIG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_CTRL_SIG'])
        value = readValue & self.READ_COMP_MASK['ADC_CTRL_SIG']
        self._BITFIELD['RSVD_7_4_ADC_CTRL_SIG'] = (value & 0xF0) >> 4
        self._BITFIELD['ADC_CAL_START'] = (value & 0x08) >> 3
        self._BITFIELD['ADC_SAMPLE'] = (value & 0x04) >> 2
        self._BITFIELD['ADC_SOC'] = (value & 0x02) >> 1
        self._BITFIELD['ADC_RESETB'] = (value & 0x01)

    def read_ADC_DATA_H(self):
        """
        Read the register ADC_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_DATA_H'])
        value = readValue & self.READ_COMP_MASK['ADC_DATA_H']
        self._BITFIELD['ADC_EOC'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_4_ADC_DATA_H'] = (value & 0x70) >> 4
        self._BITFIELD['ADC_DATA_H'] = (value & 0x0F)

    def read_ADC_DATA_L(self):
        """
        Read the register ADC_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_DATA_L'])
        value = readValue & self.READ_COMP_MASK['ADC_DATA_L']
        self._BITFIELD['ADC_DATA_L'] = (value & 0xFF)

    def read_ADC_IN0_DATA_H(self):
        """
        Read the register ADC_IN0_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN0_DATA_H'])
        value = readValue & self.READ_COMP_MASK['ADC_IN0_DATA_H']
        self._BITFIELD['RSVD_7_4_ADC_IN0_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['ADC_IN0_DATA_H'] = (value & 0x0F)

    def read_ADC_IN0_DATA_L(self):
        """
        Read the register ADC_IN0_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN0_DATA_L'])
        value = readValue & self.READ_COMP_MASK['ADC_IN0_DATA_L']
        self._BITFIELD['ADC_IN0_DATA_L'] = (value & 0xFF)

    def read_ADC_IN0_HYST(self):
        """
        Read the register ADC_IN0_HYST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN0_HYST'])
        value = readValue & self.READ_COMP_MASK['ADC_IN0_HYST']
        self._BITFIELD['RSVD_7_ADC_IN0_HYST'] = (value & 0x80) >> 7
        self._BITFIELD['HYST_ADC_IN0'] = (value & 0x7F)

    def read_ADC_IN0_LO_THR_H(self):
        """
        Read the register ADC_IN0_LO_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN0_LO_THR_H'])
        value = readValue & self.READ_COMP_MASK['ADC_IN0_LO_THR_H']
        self._BITFIELD['RSVD_7_4_ADC_IN0_LO_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRL_ADC_IN0_H'] = (value & 0x0F)

    def read_ADC_IN0_LO_THR_L(self):
        """
        Read the register ADC_IN0_LO_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN0_LO_THR_L'])
        value = readValue & self.READ_COMP_MASK['ADC_IN0_LO_THR_L']
        self._BITFIELD['THRL_ADC_IN0_L'] = (value & 0xFF)

    def read_ADC_IN0_UP_THR_H(self):
        """
        Read the register ADC_IN0_UP_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN0_UP_THR_H'])
        value = readValue & self.READ_COMP_MASK['ADC_IN0_UP_THR_H']
        self._BITFIELD['RSVD_7_4_ADC_IN0_UP_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRU_ADC_IN0_H'] = (value & 0x0F)

    def read_ADC_IN0_UP_THR_L(self):
        """
        Read the register ADC_IN0_UP_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN0_UP_THR_L'])
        value = readValue & self.READ_COMP_MASK['ADC_IN0_UP_THR_L']
        self._BITFIELD['THRU_ADC_IN0_L'] = (value & 0xFF)

    def read_ADC_IN1_DATA_H(self):
        """
        Read the register ADC_IN1_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN1_DATA_H'])
        value = readValue & self.READ_COMP_MASK['ADC_IN1_DATA_H']
        self._BITFIELD['RSVD_7_4_ADC_IN1_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['ADC_IN1_DATA_H'] = (value & 0x0F)

    def read_ADC_IN1_DATA_L(self):
        """
        Read the register ADC_IN1_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN1_DATA_L'])
        value = readValue & self.READ_COMP_MASK['ADC_IN1_DATA_L']
        self._BITFIELD['ADC_IN1_DATA_L'] = (value & 0xFF)

    def read_ADC_IN1_HYST(self):
        """
        Read the register ADC_IN1_HYST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN1_HYST'])
        value = readValue & self.READ_COMP_MASK['ADC_IN1_HYST']
        self._BITFIELD['RSVD_7_ADC_IN1_HYST'] = (value & 0x80) >> 7
        self._BITFIELD['HYST_ADC_IN1'] = (value & 0x7F)

    def read_ADC_IN1_LO_THR_H(self):
        """
        Read the register ADC_IN1_LO_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN1_LO_THR_H'])
        value = readValue & self.READ_COMP_MASK['ADC_IN1_LO_THR_H']
        self._BITFIELD['RSVD_7_4_ADC_IN1_LO_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRL_ADC_IN1_H'] = (value & 0x0F)

    def read_ADC_IN1_LO_THR_L(self):
        """
        Read the register ADC_IN1_LO_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN1_LO_THR_L'])
        value = readValue & self.READ_COMP_MASK['ADC_IN1_LO_THR_L']
        self._BITFIELD['THRL_ADC_IN1_L'] = (value & 0xFF)

    def read_ADC_IN1_UP_THR_H(self):
        """
        Read the register ADC_IN1_UP_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN1_UP_THR_H'])
        value = readValue & self.READ_COMP_MASK['ADC_IN1_UP_THR_H']
        self._BITFIELD['RSVD_7_4_ADC_IN1_UP_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRU_ADC_IN1_H'] = (value & 0x0F)

    def read_ADC_IN1_UP_THR_L(self):
        """
        Read the register ADC_IN1_UP_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_IN1_UP_THR_L'])
        value = readValue & self.READ_COMP_MASK['ADC_IN1_UP_THR_L']
        self._BITFIELD['THRU_ADC_IN1_L'] = (value & 0xFF)

    def read_ADC_LT_CAL(self):
        """
        Read the register ADC_LT_CAL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_LT_CAL'])
        value = readValue & self.READ_COMP_MASK['ADC_LT_CAL']
        self._BITFIELD['LT_SENSE_GAIN_CAL_H'] = (value & 0xF8) >> 3
        self._BITFIELD['LT_SENSE_GAIN_CAL_L'] = (value & 0x07)

    def read_ADC_MUX_CFG(self):
        """
        Read the register ADC_MUX_CFG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_MUX_CFG'])
        value = readValue & self.READ_COMP_MASK['ADC_MUX_CFG']
        self._BITFIELD['RSVD_7_6_ADC_MUX_CFG'] = (value & 0xC0) >> 6
        self._BITFIELD['RT_CH'] = (value & 0x20) >> 5
        self._BITFIELD['LT_CH'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B'] = (value & 0x08) >> 3
        self._BITFIELD['CS_A'] = (value & 0x04) >> 2
        self._BITFIELD['ADC_IN1'] = (value & 0x02) >> 1
        self._BITFIELD['ADC_IN0'] = (value & 0x01)

    def read_ADC_OFFSET_ADC_IN_CAL(self):
        """
        Read the register ADC_OFFSET_ADC_IN_CAL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_OFFSET_ADC_IN_CAL'])
        value = readValue & self.READ_COMP_MASK['ADC_OFFSET_ADC_IN_CAL']
        self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE'] = (value & 0x7F)

    def read_ADC_OFFSET_CS_CAL(self):
        """
        Read the register ADC_OFFSET_CS_CAL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_OFFSET_CS_CAL'])
        value = readValue & self.READ_COMP_MASK['ADC_OFFSET_CS_CAL']
        self._BITFIELD['ADC_OFFSET_CS_CAL_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['ADC_OFFSET_CS_CAL_OFFSET_VALUE'] = (value & 0x7F)

    def read_ADC_OFFSET_LT_CAL(self):
        """
        Read the register ADC_OFFSET_LT_CAL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_OFFSET_LT_CAL'])
        value = readValue & self.READ_COMP_MASK['ADC_OFFSET_LT_CAL']
        self._BITFIELD['ADC_OFFSET_LT_CAL_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['ADC_OFFSET_LT_CAL_OFFSET_VALUE'] = (value & 0x7F)

    def read_ADC_OFFSET_RT_CAL(self):
        """
        Read the register ADC_OFFSET_RT_CAL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_OFFSET_RT_CAL'])
        value = readValue & self.READ_COMP_MASK['ADC_OFFSET_RT_CAL']
        self._BITFIELD['ADC_OFFSET_RT_CAL_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['ADC_OFFSET_RT_CAL_OFFSET_VALUE'] = (value & 0x7F)

    def read_ADC_RT_CAL(self):
        """
        Read the register ADC_RT_CAL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_RT_CAL'])
        value = readValue & self.READ_COMP_MASK['ADC_RT_CAL']
        self._BITFIELD['RT_SENSE_GAIN_CAL_H'] = (value & 0xF8) >> 3
        self._BITFIELD['RT_SENSE_GAIN_CAL_L'] = (value & 0x07)

    def read_ADC_TEST_CNTL(self):
        """
        Read the register ADC_TEST_CNTL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_TEST_CNTL'])
        value = readValue & self.READ_COMP_MASK['ADC_TEST_CNTL']
        self._BITFIELD['RSVD_7_5_ADC_TEST_CNTL'] = (value & 0xE0) >> 5
        self._BITFIELD['ADC_VCM_EN_SEL'] = (value & 0x10) >> 4
        self._BITFIELD['ADC_CAL_TM_EN'] = (value & 0x08) >> 3
        self._BITFIELD['ADC_CAL_OFFSET_EN'] = (value & 0x04) >> 2
        self._BITFIELD['ADC_LDO_EN'] = (value & 0x02) >> 1
        self._BITFIELD['ADC_VCM_EN'] = (value & 0x01)

    def read_ADC_TRIG(self):
        """
        Read the register ADC_TRIG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_TRIG'])
        value = readValue & self.READ_COMP_MASK['ADC_TRIG']
        self._BITFIELD['RSVD_7_1_ADC_TRIG'] = (value & 0xFE) >> 1
        self._BITFIELD['ICONV'] = (value & 0x01)

    def read_ADC_TRIM_LDO(self):
        """
        Read the register ADC_TRIM_LDO and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_TRIM_LDO'])
        value = readValue & self.READ_COMP_MASK['ADC_TRIM_LDO']
        self._BITFIELD['ADC_TRIM_LDO'] = (value & 0xFF)

    def read_ADC_TRIM_REFBUF(self):
        """
        Read the register ADC_TRIM_REFBUF and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_TRIM_REFBUF'])
        value = readValue & self.READ_COMP_MASK['ADC_TRIM_REFBUF']
        self._BITFIELD['ADC_TRIM_REFBUF'] = (value & 0xFF)

    def read_ADC_TRIM_VCM(self):
        """
        Read the register ADC_TRIM_VCM and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ADC_TRIM_VCM'])
        value = readValue & self.READ_COMP_MASK['ADC_TRIM_VCM']
        self._BITFIELD['ADC_TRIM_VCM'] = (value & 0xFF)

    def read_ALR_CFG_0(self):
        """
        Read the register ALR_CFG_0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ALR_CFG_0'])
        value = readValue & self.READ_COMP_MASK['ALR_CFG_0']
        self._BITFIELD['RSVD_7_6_ALR_CFG_0'] = (value & 0xC0) >> 6
        self._BITFIELD['RT_HIGH_ALR_STAT'] = (value & 0x20) >> 5
        self._BITFIELD['RT_LOW_ALR_STAT'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B_ALR_STAT'] = (value & 0x08) >> 3
        self._BITFIELD['CS_A_ALR_STAT'] = (value & 0x04) >> 2
        self._BITFIELD['ADC_IN1_ALR_STAT'] = (value & 0x02) >> 1
        self._BITFIELD['ADC_IN0_ALR_STAT'] = (value & 0x01)

    def read_ALR_CFG_1(self):
        """
        Read the register ALR_CFG_1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ALR_CFG_1'])
        value = readValue & self.READ_COMP_MASK['ALR_CFG_1']
        self._BITFIELD['ALR_LATCH_DIS'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_ALR_CFG_1'] = (value & 0x40) >> 6
        self._BITFIELD['S0S1_ERR_ALR'] = (value & 0x20) >> 5
        self._BITFIELD['PAR_ERR_ALR'] = (value & 0x10) >> 4
        self._BITFIELD['DAV_ALR'] = (value & 0x08) >> 3
        self._BITFIELD['THERM_ALR'] = (value & 0x04) >> 2
        self._BITFIELD['LT_HIGH_ALR'] = (value & 0x02) >> 1
        self._BITFIELD['LT_LOW_ALR'] = (value & 0x01)

    def read_ALR_STAT_0(self):
        """
        Read the register ALR_STAT_0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ALR_STAT_0'])
        value = readValue & self.READ_COMP_MASK['ALR_STAT_0']
        self._BITFIELD['RSVD_7_4_ALR_STAT_0'] = (value & 0xC0) >> 6
        self._BITFIELD['RT_HIGH_ALR'] = (value & 0x20) >> 5
        self._BITFIELD['RT_LOW_ALR'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B_ALR'] = (value & 0x08) >> 3
        self._BITFIELD['CS_A_ALR'] = (value & 0x04) >> 2
        self._BITFIELD['ADC_IN1_ALR'] = (value & 0x02) >> 1
        self._BITFIELD['ADC_IN0_ALR'] = (value & 0x01)

    def read_ALR_STAT_1(self):
        """
        Read the register ALR_STAT_1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ALR_STAT_1'])
        value = readValue & self.READ_COMP_MASK['ALR_STAT_1']
        self._BITFIELD['RSVD_7_6_ALR_STAT_1'] = (value & 0xC0) >> 6
        self._BITFIELD['S0S1_ERR_ALR_STAT'] = (value & 0x20) >> 5
        self._BITFIELD['PAR_ERR_ALR_STAT'] = (value & 0x10) >> 4
        self._BITFIELD['DAV_ALR_STAT'] = (value & 0x08) >> 3
        self._BITFIELD['THERM_ALR_STAT'] = (value & 0x04) >> 2
        self._BITFIELD['LT_HIGH_ALR_STAT'] = (value & 0x02) >> 1
        self._BITFIELD['LT_LOW_ALR_STAT'] = (value & 0x01)

    def read_ANATOP6(self):
        """
        Read the register ANATOP6 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ANATOP6'])
        value = readValue & self.READ_COMP_MASK['ANATOP6']
        self._BITFIELD['ANATOP6'] = (value & 0xFF)

    def read_ANATOP7(self):
        """
        Read the register ANATOP7 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ANATOP7'])
        value = readValue & self.READ_COMP_MASK['ANATOP7']
        self._BITFIELD['ANATOP7'] = (value & 0xFF)

    def read_ANATOP8(self):
        """
        Read the register ANATOP8 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ANATOP8'])
        value = readValue & self.READ_COMP_MASK['ANATOP8']
        self._BITFIELD['ANATOP8'] = (value & 0xFF)

    def read_ANATOP9(self):
        """
        Read the register ANATOP9 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ANATOP9'])
        value = readValue & self.READ_COMP_MASK['ANATOP9']
        self._BITFIELD['ANATOP9'] = (value & 0xFF)

    def read_ANA_DFT_CTRL(self):
        """
        Read the register ANA_DFT_CTRL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ANA_DFT_CTRL'])
        value = readValue & self.READ_COMP_MASK['ANA_DFT_CTRL']
        self._BITFIELD['RSVD_7_ANA_DFT_CTRL'] = (value & 0x80) >> 7
        self._BITFIELD['EN_BYPASS_ANA_DFT_BUF'] = (value & 0x40) >> 6
        self._BITFIELD['EN_RES_LADDER_CALIB'] = (value & 0x30) >> 4
        self._BITFIELD['RES_DIV_SEL'] = (value & 0x08) >> 3
        self._BITFIELD['EN_RES_DIV'] = (value & 0x04) >> 2
        self._BITFIELD['EN_DIRECT_PATH'] = (value & 0x02) >> 1
        self._BITFIELD['EN_ANA_DFT_BUFFER'] = (value & 0x01)

    def read_ANA_DFT_MUX_CTRL(self):
        """
        Read the register ANA_DFT_MUX_CTRL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ANA_DFT_MUX_CTRL'])
        value = readValue & self.READ_COMP_MASK['ANA_DFT_MUX_CTRL']
        self._BITFIELD['RSVD_7_4_ANA_DFT_MUX_CTRL'] = (value & 0xF0) >> 4
        self._BITFIELD['ANA_DFT_MUX_SEL'] = (value & 0x0E) >> 1
        self._BITFIELD['EN_ANA_DFT_MUX'] = (value & 0x01)

    def read_ATEST_CNTL0(self):
        """
        Read the register ATEST_CNTL0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ATEST_CNTL0'])
        value = readValue & self.READ_COMP_MASK['ATEST_CNTL0']
        self._BITFIELD['ATEST_CNTL0'] = (value & 0xFF)

    def read_ATEST_CNTL1(self):
        """
        Read the register ATEST_CNTL1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['ATEST_CNTL1'])
        value = readValue & self.READ_COMP_MASK['ATEST_CNTL1']
        self._BITFIELD['RSVD_7_1_ATEST_CNTL1'] = (value & 0xFE) >> 1
        self._BITFIELD['SPIKE_FILTER_TEST_MODE'] = (value & 0x01)

    def read_CHIP_ID_H(self):
        """
        Read the register CHIP_ID_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CHIP_ID_H'])
        value = readValue & self.READ_COMP_MASK['CHIP_ID_H']
        self._BITFIELD['CHIPDID_HIGH'] = (value & 0xFF)

    def read_CHIP_ID_L(self):
        """
        Read the register CHIP_ID_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CHIP_ID_L'])
        value = readValue & self.READ_COMP_MASK['CHIP_ID_L']
        self._BITFIELD['CHIPDID_LOW'] = (value & 0xFF)

    def read_CHIP_TYPE(self):
        """
        Read the register CHIP_TYPE and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CHIP_TYPE'])
        value = readValue & self.READ_COMP_MASK['CHIP_TYPE']
        self._BITFIELD['RSVD_7_4_CHIP_TYPE'] = (value & 0xF0) >> 4
        self._BITFIELD['CHIP_TYPE'] = (value & 0x0F)

    def read_CHIP_VARIANT(self):
        """
        Read the register CHIP_VARIANT and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CHIP_VARIANT'])
        value = readValue & self.READ_COMP_MASK['CHIP_VARIANT']
        self._BITFIELD['RSVD_7_4_CHIP_VARIANT'] = (value & 0xF0) >> 4
        self._BITFIELD['CHIP_VARIANT'] = (value & 0x0F)

    def read_CHIP_VERSION(self):
        """
        Read the register CHIP_VERSION and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CHIP_VERSION'])
        value = readValue & self.READ_COMP_MASK['CHIP_VERSION']
        self._BITFIELD['VERSIONID'] = (value & 0xFF)

    def read_COMP_STATUS(self):
        """
        Read the register COMP_STATUS and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['COMP_STATUS'])
        value = readValue & self.READ_COMP_MASK['COMP_STATUS']
        self._BITFIELD['I2C_SPIKE_OK'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_COMP_STATUS'] = (value & 0x40) >> 6
        self._BITFIELD['I3C_1P8V_MODE'] = (value & 0x20) >> 5
        self._BITFIELD['SPI_I3C_SEL'] = (value & 0x10) >> 4
        self._BITFIELD['A1_COMP2'] = (value & 0x08) >> 3
        self._BITFIELD['A1_COMP1'] = (value & 0x04) >> 2
        self._BITFIELD['A0_COMP2'] = (value & 0x02) >> 1
        self._BITFIELD['A0_COMP1'] = (value & 0x01)

    def read_CS_A_DATA_H(self):
        """
        Read the register CS_A_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DATA_H'])
        value = readValue & self.READ_COMP_MASK['CS_A_DATA_H']
        self._BITFIELD['RSVD_7_5_CS_A_DATA_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_A_DATA_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_A_DATA_H'] = (value & 0x0F)

    def read_CS_A_DATA_L(self):
        """
        Read the register CS_A_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DATA_L'])
        value = readValue & self.READ_COMP_MASK['CS_A_DATA_L']
        self._BITFIELD['CS_A_DATA_L'] = (value & 0xFF)

    def read_CS_A_DEL_ER_VCM0(self):
        """
        Read the register CS_A_DEL_ER_VCM0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM0'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM0']
        self._BITFIELD['CS_A_DEL_ER_VCM0_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM0'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM1(self):
        """
        Read the register CS_A_DEL_ER_VCM1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM1'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM1']
        self._BITFIELD['CS_A_DEL_ER_VCM1_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM1'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM10(self):
        """
        Read the register CS_A_DEL_ER_VCM10 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM10'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM10']
        self._BITFIELD['CS_A_DEL_ER_VCM10_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM10'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM11(self):
        """
        Read the register CS_A_DEL_ER_VCM11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM11'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM11']
        self._BITFIELD['CS_A_DEL_ER_VCM11_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM11'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM12(self):
        """
        Read the register CS_A_DEL_ER_VCM12 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM12'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM12']
        self._BITFIELD['CS_A_DEL_ER_VCM12_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM12'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM13(self):
        """
        Read the register CS_A_DEL_ER_VCM13 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM13'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM13']
        self._BITFIELD['CS_A_DEL_ER_VCM13_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM13'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM14(self):
        """
        Read the register CS_A_DEL_ER_VCM14 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM14'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM14']
        self._BITFIELD['CS_A_DEL_ER_VCM14_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM14'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM15(self):
        """
        Read the register CS_A_DEL_ER_VCM15 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM15'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM15']
        self._BITFIELD['CS_A_DEL_ER_VCM15_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM15'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM16(self):
        """
        Read the register CS_A_DEL_ER_VCM16 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM16'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM16']
        self._BITFIELD['CS_A_DEL_ER_VCM16_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM16'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM17(self):
        """
        Read the register CS_A_DEL_ER_VCM17 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM17'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM17']
        self._BITFIELD['CS_A_DEL_ER_VCM17_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM17'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM18(self):
        """
        Read the register CS_A_DEL_ER_VCM18 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM18'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM18']
        self._BITFIELD['CS_A_DEL_ER_VCM18_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM18'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM19(self):
        """
        Read the register CS_A_DEL_ER_VCM19 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM19'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM19']
        self._BITFIELD['CS_A_DEL_ER_VCM19_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM19'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM2(self):
        """
        Read the register CS_A_DEL_ER_VCM2 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM2'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM2']
        self._BITFIELD['CS_A_DEL_ER_VCM2_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM2'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM3(self):
        """
        Read the register CS_A_DEL_ER_VCM3 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM3'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM3']
        self._BITFIELD['CS_A_DEL_ER_VCM3_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM3'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM4(self):
        """
        Read the register CS_A_DEL_ER_VCM4 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM4'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM4']
        self._BITFIELD['CS_A_DEL_ER_VCM4_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM4'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM5(self):
        """
        Read the register CS_A_DEL_ER_VCM5 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM5'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM5']
        self._BITFIELD['CS_A_DEL_ER_VCM5_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM5'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM6(self):
        """
        Read the register CS_A_DEL_ER_VCM6 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM6'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM6']
        self._BITFIELD['CS_A_DEL_ER_VCM6_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM6'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM7(self):
        """
        Read the register CS_A_DEL_ER_VCM7 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM7'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM7']
        self._BITFIELD['CS_A_DEL_ER_VCM7_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM7'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM8(self):
        """
        Read the register CS_A_DEL_ER_VCM8 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM8'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM8']
        self._BITFIELD['CS_A_DEL_ER_VCM8_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM8'] = (value & 0x7F)

    def read_CS_A_DEL_ER_VCM9(self):
        """
        Read the register CS_A_DEL_ER_VCM9 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_DEL_ER_VCM9'])
        value = readValue & self.READ_COMP_MASK['CS_A_DEL_ER_VCM9']
        self._BITFIELD['CS_A_DEL_ER_VCM9_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_A_DEL_ER_VCM9'] = (value & 0x7F)

    def read_CS_A_ER_VCM_BASE_H(self):
        """
        Read the register CS_A_ER_VCM_BASE_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_ER_VCM_BASE_H'])
        value = readValue & self.READ_COMP_MASK['CS_A_ER_VCM_BASE_H']
        self._BITFIELD['CS_A_CAL_ALU_BYP'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_5_CS_A_ER_VCM_BASE_H'] = (value & 0x60) >> 5
        self._BITFIELD['CS_A_ER_VCM_BASE_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_A_ER_VCM_BASE_H'] = (value & 0x0F)

    def read_CS_A_ER_VCM_BASE_L(self):
        """
        Read the register CS_A_ER_VCM_BASE_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_ER_VCM_BASE_L'])
        value = readValue & self.READ_COMP_MASK['CS_A_ER_VCM_BASE_L']
        self._BITFIELD['CS_A_ER_VCM_BASE_L'] = (value & 0xFF)

    def read_CS_A_GAIN_ERROR(self):
        """
        Read the register CS_A_GAIN_ERROR and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_GAIN_ERROR'])
        value = readValue & self.READ_COMP_MASK['CS_A_GAIN_ERROR']
        self._BITFIELD['CS_A_GAIN_ERROR_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['GAIN_ERROR_CS_A_GAIN_ERROR'] = (value & 0x7F)

    def read_CS_A_HYST(self):
        """
        Read the register CS_A_HYST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_HYST'])
        value = readValue & self.READ_COMP_MASK['CS_A_HYST']
        self._BITFIELD['RSVD_7_CS_A_HYST'] = (value & 0x80) >> 7
        self._BITFIELD['HYST_CS_A'] = (value & 0x7F)

    def read_CS_A_LO_THR_H(self):
        """
        Read the register CS_A_LO_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_LO_THR_H'])
        value = readValue & self.READ_COMP_MASK['CS_A_LO_THR_H']
        self._BITFIELD['RSVD_7_4_CS_A_LO_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRL_CS_A_H'] = (value & 0x0F)

    def read_CS_A_LO_THR_L(self):
        """
        Read the register CS_A_LO_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_LO_THR_L'])
        value = readValue & self.READ_COMP_MASK['CS_A_LO_THR_L']
        self._BITFIELD['THRL_CS_A_L'] = (value & 0xFF)

    def read_CS_A_LUT0_OFFSET(self):
        """
        Read the register CS_A_LUT0_OFFSET and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_LUT0_OFFSET'])
        value = readValue & self.READ_COMP_MASK['CS_A_LUT0_OFFSET']
        self._BITFIELD['RSVD_7_6_CS_A_LUT0_OFFSET'] = (value & 0xC0) >> 6
        self._BITFIELD['CS_A_LUT0_OFFSET_LUT0_OFFSET'] = (value & 0x3F)

    def read_CS_A_LUT1_OFFSET(self):
        """
        Read the register CS_A_LUT1_OFFSET and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_LUT1_OFFSET'])
        value = readValue & self.READ_COMP_MASK['CS_A_LUT1_OFFSET']
        self._BITFIELD['RSVD_7_6_CS_A_LUT1_OFFSET'] = (value & 0xC0) >> 6
        self._BITFIELD['CS_A_LUT1_OFFSET'] = (value & 0x3F)

    def read_CS_A_UP_THR_H(self):
        """
        Read the register CS_A_UP_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_UP_THR_H'])
        value = readValue & self.READ_COMP_MASK['CS_A_UP_THR_H']
        self._BITFIELD['RSVD_7_4_CS_A_UP_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRU_CS_A_H'] = (value & 0x0F)

    def read_CS_A_UP_THR_L(self):
        """
        Read the register CS_A_UP_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_UP_THR_L'])
        value = readValue & self.READ_COMP_MASK['CS_A_UP_THR_L']
        self._BITFIELD['THRU_CS_A_L'] = (value & 0xFF)

    def read_CS_A_VCM_BASE_H(self):
        """
        Read the register CS_A_VCM_BASE_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_VCM_BASE_H'])
        value = readValue & self.READ_COMP_MASK['CS_A_VCM_BASE_H']
        self._BITFIELD['RSVD_7_4_CS_A_VCM_BASE_H'] = (value & 0xF0) >> 4
        self._BITFIELD['CS_A_VCM_BASE_H'] = (value & 0x0F)

    def read_CS_A_VCM_BASE_L(self):
        """
        Read the register CS_A_VCM_BASE_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_VCM_BASE_L'])
        value = readValue & self.READ_COMP_MASK['CS_A_VCM_BASE_L']
        self._BITFIELD['CS_A_VCM_BASE_L'] = (value & 0xFF)

    def read_CS_A_VCM_SLOPE_H(self):
        """
        Read the register CS_A_VCM_SLOPE_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_VCM_SLOPE_H'])
        value = readValue & self.READ_COMP_MASK['CS_A_VCM_SLOPE_H']
        self._BITFIELD['RSVD_7_5_CS_A_VCM_SLOPE_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_A_VCM_SLOPE_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_A_VCM_SLOPE_H'] = (value & 0x0F)

    def read_CS_A_VCM_SLOPE_L(self):
        """
        Read the register CS_A_VCM_SLOPE_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_A_VCM_SLOPE_L'])
        value = readValue & self.READ_COMP_MASK['CS_A_VCM_SLOPE_L']
        self._BITFIELD['CS_A_VCM_SLOPE_L'] = (value & 0xFF)

    def read_CS_B_DATA_H(self):
        """
        Read the register CS_B_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DATA_H'])
        value = readValue & self.READ_COMP_MASK['CS_B_DATA_H']
        self._BITFIELD['RSVD_7_5_CS_B_DATA_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_B_DATA_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B_DATA_H'] = (value & 0x0F)

    def read_CS_B_DATA_L(self):
        """
        Read the register CS_B_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DATA_L'])
        value = readValue & self.READ_COMP_MASK['CS_B_DATA_L']
        self._BITFIELD['CS_B_DATA_L'] = (value & 0xFF)

    def read_CS_B_DEL_ER_VCM0(self):
        """
        Read the register CS_B_DEL_ER_VCM0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM0'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM0']
        self._BITFIELD['CS_B_DEL_ER_VCM0_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM0'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM1(self):
        """
        Read the register CS_B_DEL_ER_VCM1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM1'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM1']
        self._BITFIELD['CS_B_DEL_ER_VCM1_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM1'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM10(self):
        """
        Read the register CS_B_DEL_ER_VCM10 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM10'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM10']
        self._BITFIELD['CS_B_DEL_ER_VCM10_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM10'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM11(self):
        """
        Read the register CS_B_DEL_ER_VCM11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM11'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM11']
        self._BITFIELD['CS_B_DEL_ER_VCM11_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM11'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM12(self):
        """
        Read the register CS_B_DEL_ER_VCM12 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM12'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM12']
        self._BITFIELD['CS_B_DEL_ER_VCM12_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM12'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM13(self):
        """
        Read the register CS_B_DEL_ER_VCM13 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM13'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM13']
        self._BITFIELD['CS_B_DEL_ER_VCM13_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM13'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM14(self):
        """
        Read the register CS_B_DEL_ER_VCM14 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM14'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM14']
        self._BITFIELD['CS_B_DEL_ER_VCM14_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM14'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM15(self):
        """
        Read the register CS_B_DEL_ER_VCM15 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM15'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM15']
        self._BITFIELD['CS_B_DEL_ER_VCM15_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM15'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM16(self):
        """
        Read the register CS_B_DEL_ER_VCM16 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM16'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM16']
        self._BITFIELD['CS_B_DEL_ER_VCM16_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM16'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM17(self):
        """
        Read the register CS_B_DEL_ER_VCM17 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM17'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM17']
        self._BITFIELD['CS_B_DEL_ER_VCM17_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM17'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM18(self):
        """
        Read the register CS_B_DEL_ER_VCM18 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM18'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM18']
        self._BITFIELD['CS_B_DEL_ER_VCM18_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM18'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM19(self):
        """
        Read the register CS_B_DEL_ER_VCM19 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM19'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM19']
        self._BITFIELD['CS_B_DEL_ER_VCM19_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM19'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM2(self):
        """
        Read the register CS_B_DEL_ER_VCM2 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM2'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM2']
        self._BITFIELD['CS_B_DEL_ER_VCM2_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM2'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM3(self):
        """
        Read the register CS_B_DEL_ER_VCM3 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM3'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM3']
        self._BITFIELD['CS_B_DEL_ER_VCM3_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM3'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM4(self):
        """
        Read the register CS_B_DEL_ER_VCM4 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM4'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM4']
        self._BITFIELD['CS_B_DEL_ER_VCM4_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM4'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM5(self):
        """
        Read the register CS_B_DEL_ER_VCM5 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM5'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM5']
        self._BITFIELD['CS_B_DEL_ER_VCM5_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM5'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM6(self):
        """
        Read the register CS_B_DEL_ER_VCM6 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM6'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM6']
        self._BITFIELD['CS_B_DEL_ER_VCM6_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM6'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM7(self):
        """
        Read the register CS_B_DEL_ER_VCM7 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM7'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM7']
        self._BITFIELD['CS_B_DEL_ER_VCM7_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM7'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM8(self):
        """
        Read the register CS_B_DEL_ER_VCM8 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM8'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM8']
        self._BITFIELD['CS_B_DEL_ER_VCM8_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM8'] = (value & 0x7F)

    def read_CS_B_DEL_ER_VCM9(self):
        """
        Read the register CS_B_DEL_ER_VCM9 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_DEL_ER_VCM9'])
        value = readValue & self.READ_COMP_MASK['CS_B_DEL_ER_VCM9']
        self._BITFIELD['CS_B_DEL_ER_VCM9_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DEL_ER_VCM9'] = (value & 0x7F)

    def read_CS_B_ER_VCM_BASE_H(self):
        """
        Read the register CS_B_ER_VCM_BASE_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_ER_VCM_BASE_H'])
        value = readValue & self.READ_COMP_MASK['CS_B_ER_VCM_BASE_H']
        self._BITFIELD['CS_B_CAL_ALU_BYP'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_5_CS_B_ER_VCM_BASE_H'] = (value & 0x60) >> 5
        self._BITFIELD['CS_B_ER_VCM_BASE_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B_ER_VCM_BASE_H'] = (value & 0x0F)

    def read_CS_B_ER_VCM_BASE_L(self):
        """
        Read the register CS_B_ER_VCM_BASE_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_ER_VCM_BASE_L'])
        value = readValue & self.READ_COMP_MASK['CS_B_ER_VCM_BASE_L']
        self._BITFIELD['CS_B_ER_VCM_BASE_L'] = (value & 0xFF)

    def read_CS_B_GAIN_ERROR(self):
        """
        Read the register CS_B_GAIN_ERROR and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_GAIN_ERROR'])
        value = readValue & self.READ_COMP_MASK['CS_B_GAIN_ERROR']
        self._BITFIELD['CS_B_GAIN_ERROR_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['GAIN_ERROR_CS_B_GAIN_ERROR'] = (value & 0x7F)

    def read_CS_B_HYST(self):
        """
        Read the register CS_B_HYST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_HYST'])
        value = readValue & self.READ_COMP_MASK['CS_B_HYST']
        self._BITFIELD['RSVD_7_CS_B_HYST'] = (value & 0x80) >> 7
        self._BITFIELD['HYST_CS_B'] = (value & 0x7F)

    def read_CS_B_LO_THR_H(self):
        """
        Read the register CS_B_LO_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_LO_THR_H'])
        value = readValue & self.READ_COMP_MASK['CS_B_LO_THR_H']
        self._BITFIELD['RSVD_7_4_CS_B_LO_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRL_CS_B_H'] = (value & 0x0F)

    def read_CS_B_LO_THR_L(self):
        """
        Read the register CS_B_LO_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_LO_THR_L'])
        value = readValue & self.READ_COMP_MASK['CS_B_LO_THR_L']
        self._BITFIELD['THRL_CS_B_L'] = (value & 0xFF)

    def read_CS_B_LUT0_OFFSET(self):
        """
        Read the register CS_B_LUT0_OFFSET and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_LUT0_OFFSET'])
        value = readValue & self.READ_COMP_MASK['CS_B_LUT0_OFFSET']
        self._BITFIELD['RSVD_7_6_CS_B_LUT0_OFFSET'] = (value & 0xC0) >> 6
        self._BITFIELD['CS_B_LUT0_OFFSET_LUT0_OFFSET'] = (value & 0x3F)

    def read_CS_B_LUT1_OFFSET(self):
        """
        Read the register CS_B_LUT1_OFFSET and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_LUT1_OFFSET'])
        value = readValue & self.READ_COMP_MASK['CS_B_LUT1_OFFSET']
        self._BITFIELD['RSVD_7_6_CS_B_LUT1_OFFSET'] = (value & 0xC0) >> 6
        self._BITFIELD['CS_B_LUT1_OFFSET'] = (value & 0x3F)

    def read_CS_B_UP_THR_H(self):
        """
        Read the register CS_B_UP_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_UP_THR_H'])
        value = readValue & self.READ_COMP_MASK['CS_B_UP_THR_H']
        self._BITFIELD['RSVD_7_4_CS_B_UP_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRU_CS_B_H'] = (value & 0x0F)

    def read_CS_B_UP_THR_L(self):
        """
        Read the register CS_B_UP_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_UP_THR_L'])
        value = readValue & self.READ_COMP_MASK['CS_B_UP_THR_L']
        self._BITFIELD['THRU_CS_B_L'] = (value & 0xFF)

    def read_CS_B_VCM_BASE_H(self):
        """
        Read the register CS_B_VCM_BASE_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_VCM_BASE_H'])
        value = readValue & self.READ_COMP_MASK['CS_B_VCM_BASE_H']
        self._BITFIELD['RSVD_7_4_CS_B_VCM_BASE_H'] = (value & 0xF0) >> 4
        self._BITFIELD['CS_B_VCM_BASE_H'] = (value & 0x0F)

    def read_CS_B_VCM_BASE_L(self):
        """
        Read the register CS_B_VCM_BASE_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_VCM_BASE_L'])
        value = readValue & self.READ_COMP_MASK['CS_B_VCM_BASE_L']
        self._BITFIELD['CS_B_VCM_BASE_L'] = (value & 0xFF)

    def read_CS_B_VCM_SLOPE_H(self):
        """
        Read the register CS_B_VCM_SLOPE_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_VCM_SLOPE_H'])
        value = readValue & self.READ_COMP_MASK['CS_B_VCM_SLOPE_H']
        self._BITFIELD['RSVD_7_5_CS_B_VCM_SLOPE_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_B_VCM_SLOPE_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B_VCM_SLOPE_H'] = (value & 0x0F)

    def read_CS_B_VCM_SLOPE_L(self):
        """
        Read the register CS_B_VCM_SLOPE_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_B_VCM_SLOPE_L'])
        value = readValue & self.READ_COMP_MASK['CS_B_VCM_SLOPE_L']
        self._BITFIELD['CS_B_VCM_SLOPE_L'] = (value & 0xFF)

    def read_CS_CAL_DIFF10_H(self):
        """
        Read the register CS_CAL_DIFF10_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_DIFF10_H'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_DIFF10_H']
        self._BITFIELD['RSVD_7_5_CS_CAL_DIFF10_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_CAL_DIFF10_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CAL_DIFF10_H'] = (value & 0x0F)

    def read_CS_CAL_DIFF10_L(self):
        """
        Read the register CS_CAL_DIFF10_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_DIFF10_L'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_DIFF10_L']
        self._BITFIELD['CAL_DIFF10_L'] = (value & 0xFF)

    def read_CS_CAL_ER_FRAC(self):
        """
        Read the register CS_CAL_ER_FRAC and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_ER_FRAC'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_ER_FRAC']
        self._BITFIELD['CS_CAL_ER_FRAC_SIGN'] = (value & 0x80) >> 7
        self._BITFIELD['CAL_ER_FRAC'] = (value & 0x7F)

    def read_CS_CAL_ER_H(self):
        """
        Read the register CS_CAL_ER_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_ER_H'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_ER_H']
        self._BITFIELD['RSVD_7_5_CS_CAL_ER_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_CAL_ER_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CAL_ER_H'] = (value & 0x0F)

    def read_CS_CAL_ER_L(self):
        """
        Read the register CS_CAL_ER_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_ER_L'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_ER_L']
        self._BITFIELD['CAL_ER_L'] = (value & 0xFF)

    def read_CS_CAL_ER_LUTP(self):
        """
        Read the register CS_CAL_ER_LUTP and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_ER_LUTP'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_ER_LUTP']
        self._BITFIELD['RSVD_7_6_CS_CAL_ER_LUTP'] = (value & 0xC0) >> 6
        self._BITFIELD['CAL_ER_LUTP'] = (value & 0x3F)

    def read_CS_CAL_LUTS_H(self):
        """
        Read the register CS_CAL_LUTS_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_LUTS_H'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_LUTS_H']
        self._BITFIELD['RSVD_7_5_CS_CAL_LUTS_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_CAL_LUTS_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CAL_LUTS_H'] = (value & 0x0F)

    def read_CS_CAL_LUTS_L(self):
        """
        Read the register CS_CAL_LUTS_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CAL_LUTS_L'])
        value = readValue & self.READ_COMP_MASK['CS_CAL_LUTS_L']
        self._BITFIELD['CAL_LUTS_L'] = (value & 0xFF)

    def read_CS_CFG_0(self):
        """
        Read the register CS_CFG_0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CFG_0'])
        value = readValue & self.READ_COMP_MASK['CS_CFG_0']
        self._BITFIELD['CS_DAC_MODE'] = (value & 0x80) >> 7
        self._BITFIELD['CS_DATA_CLAMP_EN'] = (value & 0x40) >> 6
        self._BITFIELD['CS_ADC_ACQ_DLY_EN'] = (value & 0x20) >> 5
        self._BITFIELD['CS_CFG_0_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_A_DAC_OFFSET'] = (value & 0x0F)

    def read_CS_CFG_1(self):
        """
        Read the register CS_CFG_1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CFG_1'])
        value = readValue & self.READ_COMP_MASK['CS_CFG_1']
        self._BITFIELD['CS_CONV_RATE'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_CFG_1_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B_DAC_OFFSET'] = (value & 0x0F)

    def read_CS_CFG_2(self):
        """
        Read the register CS_CFG_2 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_CFG_2'])
        value = readValue & self.READ_COMP_MASK['CS_CFG_2']
        self._BITFIELD['DAC_CODE_BYPASS'] = (value & 0x80) >> 7
        self._BITFIELD['CS_CFG_2_DAC_CODE'] = (value & 0x7F)

    def read_CS_DAC_CODE(self):
        """
        Read the register CS_DAC_CODE and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DAC_CODE'])
        value = readValue & self.READ_COMP_MASK['CS_DAC_CODE']
        self._BITFIELD['RSVD_7_CS_DAC_CODE'] = (value & 0x80) >> 7
        self._BITFIELD['CS_DAC_CODE'] = (value & 0x7F)

    def read_CS_DAC_MID_H(self):
        """
        Read the register CS_DAC_MID_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DAC_MID_H'])
        value = readValue & self.READ_COMP_MASK['CS_DAC_MID_H']
        self._BITFIELD['RSVD_7_4_CS_DAC_MID_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC_MID_H'] = (value & 0x0F)

    def read_CS_DAC_MID_L(self):
        """
        Read the register CS_DAC_MID_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DAC_MID_L'])
        value = readValue & self.READ_COMP_MASK['CS_DAC_MID_L']
        self._BITFIELD['DAC_MID_L'] = (value & 0xFF)

    def read_CS_DAC_SHIFT_COR_H(self):
        """
        Read the register CS_DAC_SHIFT_COR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DAC_SHIFT_COR_H'])
        value = readValue & self.READ_COMP_MASK['CS_DAC_SHIFT_COR_H']
        self._BITFIELD['RSVD_7_2_CS_DAC_SHIFT_COR_H'] = (value & 0xFC) >> 2
        self._BITFIELD['CS_DAC_SHIFT_COR_H_SIGN'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_SHIFT_COR_H'] = (value & 0x01)

    def read_CS_DAC_SHIFT_COR_L(self):
        """
        Read the register CS_DAC_SHIFT_COR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DAC_SHIFT_COR_L'])
        value = readValue & self.READ_COMP_MASK['CS_DAC_SHIFT_COR_L']
        self._BITFIELD['DAC_SHIFT_COR_L'] = (value & 0xFF)

    def read_CS_DAC_SHIFT_H(self):
        """
        Read the register CS_DAC_SHIFT_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DAC_SHIFT_H'])
        value = readValue & self.READ_COMP_MASK['CS_DAC_SHIFT_H']
        self._BITFIELD['RSVD_7_2_CS_DAC_SHIFT_H'] = (value & 0xFC) >> 2
        self._BITFIELD['CS_DAC_SHIFT_H_SIGN'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_SHIFT_H'] = (value & 0x01)

    def read_CS_DAC_SHIFT_L(self):
        """
        Read the register CS_DAC_SHIFT_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DAC_SHIFT_L'])
        value = readValue & self.READ_COMP_MASK['CS_DAC_SHIFT_L']
        self._BITFIELD['DAC_SHIFT_L'] = (value & 0xFF)

    def read_CS_DIFF10_H(self):
        """
        Read the register CS_DIFF10_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DIFF10_H'])
        value = readValue & self.READ_COMP_MASK['CS_DIFF10_H']
        self._BITFIELD['RSVD_7_5_CS_DIFF10_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_DIFF10_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['DIFF10_H'] = (value & 0x0F)

    def read_CS_DIFF10_L(self):
        """
        Read the register CS_DIFF10_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DIFF10_L'])
        value = readValue & self.READ_COMP_MASK['CS_DIFF10_L']
        self._BITFIELD['DIFF10_L'] = (value & 0xFF)

    def read_CS_DIFF10_OVRD_H(self):
        """
        Read the register CS_DIFF10_OVRD_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DIFF10_OVRD_H'])
        value = readValue & self.READ_COMP_MASK['CS_DIFF10_OVRD_H']
        self._BITFIELD['RSVD_7_5_CS_DIFF10_OVRD_H'] = (value & 0xE0) >> 5
        self._BITFIELD['CS_DIFF10_OVRD_H_SIGN'] = (value & 0x10) >> 4
        self._BITFIELD['DIFF10_OVRD_H'] = (value & 0x0F)

    def read_CS_DIFF10_OVRD_L(self):
        """
        Read the register CS_DIFF10_OVRD_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DIFF10_OVRD_L'])
        value = readValue & self.READ_COMP_MASK['CS_DIFF10_OVRD_L']
        self._BITFIELD['DIFF10_OVRD_L'] = (value & 0xFF)

    def read_CS_DTEST_CTRL(self):
        """
        Read the register CS_DTEST_CTRL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_DTEST_CTRL'])
        value = readValue & self.READ_COMP_MASK['CS_DTEST_CTRL']
        self._BITFIELD['CS_B_DTEST_EN'] = (value & 0x80) >> 7
        self._BITFIELD['CS_B_DTEST_CTRL'] = (value & 0x70) >> 4
        self._BITFIELD['CS_A_DTEST_EN'] = (value & 0x08) >> 3
        self._BITFIELD['CS_A_DTEST_CTRL'] = (value & 0x07)

    def read_CS_GAIN_ER_H(self):
        """
        Read the register CS_GAIN_ER_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_GAIN_ER_H'])
        value = readValue & self.READ_COMP_MASK['CS_GAIN_ER_H']
        self._BITFIELD['RSVD_7_1_CS_GAIN_ER_H'] = (value & 0xFE) >> 1
        self._BITFIELD['CS_GAIN_ER_H_SIGN'] = (value & 0x01)

    def read_CS_GAIN_ER_L(self):
        """
        Read the register CS_GAIN_ER_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_GAIN_ER_L'])
        value = readValue & self.READ_COMP_MASK['CS_GAIN_ER_L']
        self._BITFIELD['GAIN_ER_L'] = (value & 0xFF)

    def read_CS_SENSE_N10_H(self):
        """
        Read the register CS_SENSE_N10_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_N10_H'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_N10_H']
        self._BITFIELD['RSVD_7_4_CS_SENSE_N10_H'] = (value & 0xF0) >> 4
        self._BITFIELD['SENSE_N10_H'] = (value & 0x0F)

    def read_CS_SENSE_N10_L(self):
        """
        Read the register CS_SENSE_N10_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_N10_L'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_N10_L']
        self._BITFIELD['SENSE_N10_L'] = (value & 0xFF)

    def read_CS_SENSE_N_DAC_H(self):
        """
        Read the register CS_SENSE_N_DAC_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_N_DAC_H'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_N_DAC_H']
        self._BITFIELD['RSVD_7_4_CS_SENSE_N_DAC_H'] = (value & 0xF0) >> 4
        self._BITFIELD['SENSE_N_DAC_H'] = (value & 0x0F)

    def read_CS_SENSE_N_DAC_L(self):
        """
        Read the register CS_SENSE_N_DAC_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_N_DAC_L'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_N_DAC_L']
        self._BITFIELD['SENSE_N_DAC_L'] = (value & 0xFF)

    def read_CS_SENSE_P10_H(self):
        """
        Read the register CS_SENSE_P10_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_P10_H'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_P10_H']
        self._BITFIELD['RSVD_7_4_CS_SENSE_P10_H'] = (value & 0xF0) >> 4
        self._BITFIELD['SENSE_P10_H'] = (value & 0x0F)

    def read_CS_SENSE_P10_L(self):
        """
        Read the register CS_SENSE_P10_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_P10_L'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_P10_L']
        self._BITFIELD['SENSE_P10_L'] = (value & 0xFF)

    def read_CS_SENSE_P_DAC_H(self):
        """
        Read the register CS_SENSE_P_DAC_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_P_DAC_H'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_P_DAC_H']
        self._BITFIELD['RSVD_7_4_CS_SENSE_P_DAC_H'] = (value & 0xF0) >> 4
        self._BITFIELD['SENSE_P_DAC_H'] = (value & 0x0F)

    def read_CS_SENSE_P_DAC_L(self):
        """
        Read the register CS_SENSE_P_DAC_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_SENSE_P_DAC_L'])
        value = readValue & self.READ_COMP_MASK['CS_SENSE_P_DAC_L']
        self._BITFIELD['SENSE_P_DAC_L'] = (value & 0xFF)

    def read_CS_TEST_CTRL(self):
        """
        Read the register CS_TEST_CTRL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_TEST_CTRL'])
        value = readValue & self.READ_COMP_MASK['CS_TEST_CTRL']
        self._BITFIELD['CS_VCM_OC'] = (value & 0x80) >> 7
        self._BITFIELD['CS_VCM_OCH'] = (value & 0x40) >> 6
        self._BITFIELD['CS_VCM_UPDATE'] = (value & 0x20) >> 5
        self._BITFIELD['CS_CAL_MODE'] = (value & 0x10) >> 4
        self._BITFIELD['CS_PHASE_CTRL'] = (value & 0x08) >> 3
        self._BITFIELD['CS_MUX_SEL'] = (value & 0x07)

    def read_CS_VCM_H(self):
        """
        Read the register CS_VCM_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_VCM_H'])
        value = readValue & self.READ_COMP_MASK['CS_VCM_H']
        self._BITFIELD['RSVD_7_4_CS_VCM_H'] = (value & 0xF0) >> 4
        self._BITFIELD['VCM_H'] = (value & 0x0F)

    def read_CS_VCM_L(self):
        """
        Read the register CS_VCM_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_VCM_L'])
        value = readValue & self.READ_COMP_MASK['CS_VCM_L']
        self._BITFIELD['VCM_L'] = (value & 0xFF)

    def read_CS_VCM_OVRD_H(self):
        """
        Read the register CS_VCM_OVRD_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_VCM_OVRD_H'])
        value = readValue & self.READ_COMP_MASK['CS_VCM_OVRD_H']
        self._BITFIELD['RSVD_7_4_CS_VCM_OVRD_H'] = (value & 0xF0) >> 4
        self._BITFIELD['VCM_OVRD_H'] = (value & 0x0F)

    def read_CS_VCM_OVRD_L(self):
        """
        Read the register CS_VCM_OVRD_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['CS_VCM_OVRD_L'])
        value = readValue & self.READ_COMP_MASK['CS_VCM_OVRD_L']
        self._BITFIELD['VCM_OVRD_L'] = (value & 0xFF)

    def read_DAC0_DATA_H(self):
        """
        Read the register DAC0_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC0_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC0_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC0_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC0_DATA_H'] = (value & 0x0F)

    def read_DAC0_DATA_L(self):
        """
        Read the register DAC0_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC0_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC0_DATA_L']
        self._BITFIELD['DAC0_DATA_L'] = (value & 0xFF)

    def read_DAC0_GAIN_CAL_R00(self):
        """
        Read the register DAC0_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC0_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC0_GAIN_CAL_R00']
        self._BITFIELD['DAC0_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC0_GAIN_CAL_R11(self):
        """
        Read the register DAC0_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC0_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC0_GAIN_CAL_R11']
        self._BITFIELD['DAC0_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC0_OFFSET_CAL_R00(self):
        """
        Read the register DAC0_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC0_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC0_OFFSET_CAL_R00']
        self._BITFIELD['DAC0_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC0_OFFSET_CAL_R11(self):
        """
        Read the register DAC0_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC0_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC0_OFFSET_CAL_R11']
        self._BITFIELD['DAC0_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC1_DATA_H(self):
        """
        Read the register DAC1_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC1_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC1_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC1_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC1_DATA_H'] = (value & 0x0F)

    def read_DAC1_DATA_L(self):
        """
        Read the register DAC1_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC1_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC1_DATA_L']
        self._BITFIELD['DAC1_DATA_L'] = (value & 0xFF)

    def read_DAC1_GAIN_CAL_R00(self):
        """
        Read the register DAC1_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC1_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC1_GAIN_CAL_R00']
        self._BITFIELD['DAC1_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC1_GAIN_CAL_R11(self):
        """
        Read the register DAC1_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC1_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC1_GAIN_CAL_R11']
        self._BITFIELD['DAC1_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC1_OFFSET_CAL_R00(self):
        """
        Read the register DAC1_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC1_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC1_OFFSET_CAL_R00']
        self._BITFIELD['DAC1_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC1_OFFSET_CAL_R11(self):
        """
        Read the register DAC1_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC1_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC1_OFFSET_CAL_R11']
        self._BITFIELD['DAC1_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC2_DATA_H(self):
        """
        Read the register DAC2_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC2_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC2_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC2_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC2_DATA_H'] = (value & 0x0F)

    def read_DAC2_DATA_L(self):
        """
        Read the register DAC2_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC2_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC2_DATA_L']
        self._BITFIELD['DAC2_DATA_L'] = (value & 0xFF)

    def read_DAC2_GAIN_CAL_R00(self):
        """
        Read the register DAC2_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC2_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC2_GAIN_CAL_R00']
        self._BITFIELD['DAC2_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC2_GAIN_CAL_R11(self):
        """
        Read the register DAC2_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC2_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC2_GAIN_CAL_R11']
        self._BITFIELD['DAC2_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC2_OFFSET_CAL_R00(self):
        """
        Read the register DAC2_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC2_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC2_OFFSET_CAL_R00']
        self._BITFIELD['DAC2_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC2_OFFSET_CAL_R11(self):
        """
        Read the register DAC2_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC2_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC2_OFFSET_CAL_R11']
        self._BITFIELD['DAC2_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC3_DATA_H(self):
        """
        Read the register DAC3_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC3_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC3_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC3_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC3_DATA_H'] = (value & 0x0F)

    def read_DAC3_DATA_L(self):
        """
        Read the register DAC3_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC3_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC3_DATA_L']
        self._BITFIELD['DAC3_DATA_L'] = (value & 0xFF)

    def read_DAC3_GAIN_CAL_R00(self):
        """
        Read the register DAC3_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC3_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC3_GAIN_CAL_R00']
        self._BITFIELD['DAC3_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC3_GAIN_CAL_R11(self):
        """
        Read the register DAC3_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC3_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC3_GAIN_CAL_R11']
        self._BITFIELD['DAC3_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC3_OFFSET_CAL_R00(self):
        """
        Read the register DAC3_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC3_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC3_OFFSET_CAL_R00']
        self._BITFIELD['DAC3_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC3_OFFSET_CAL_R11(self):
        """
        Read the register DAC3_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC3_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC3_OFFSET_CAL_R11']
        self._BITFIELD['DAC3_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC4_DATA_H(self):
        """
        Read the register DAC4_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC4_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC4_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC4_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC4_DATA_H'] = (value & 0x0F)

    def read_DAC4_DATA_L(self):
        """
        Read the register DAC4_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC4_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC4_DATA_L']
        self._BITFIELD['DAC4_DATA_L'] = (value & 0xFF)

    def read_DAC4_GAIN_CAL_R00(self):
        """
        Read the register DAC4_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC4_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC4_GAIN_CAL_R00']
        self._BITFIELD['DAC4_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC4_GAIN_CAL_R11(self):
        """
        Read the register DAC4_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC4_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC4_GAIN_CAL_R11']
        self._BITFIELD['DAC4_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC4_OFFSET_CAL_R00(self):
        """
        Read the register DAC4_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC4_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC4_OFFSET_CAL_R00']
        self._BITFIELD['DAC4_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC4_OFFSET_CAL_R11(self):
        """
        Read the register DAC4_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC4_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC4_OFFSET_CAL_R11']
        self._BITFIELD['DAC4_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC5_DATA_H(self):
        """
        Read the register DAC5_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC5_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC5_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC5_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC5_DATA_H'] = (value & 0x0F)

    def read_DAC5_DATA_L(self):
        """
        Read the register DAC5_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC5_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC5_DATA_L']
        self._BITFIELD['DAC5_DATA_L'] = (value & 0xFF)

    def read_DAC5_GAIN_CAL_R00(self):
        """
        Read the register DAC5_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC5_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC5_GAIN_CAL_R00']
        self._BITFIELD['DAC5_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC5_GAIN_CAL_R11(self):
        """
        Read the register DAC5_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC5_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC5_GAIN_CAL_R11']
        self._BITFIELD['DAC5_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC5_OFFSET_CAL_R00(self):
        """
        Read the register DAC5_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC5_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC5_OFFSET_CAL_R00']
        self._BITFIELD['DAC5_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC5_OFFSET_CAL_R11(self):
        """
        Read the register DAC5_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC5_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC5_OFFSET_CAL_R11']
        self._BITFIELD['DAC5_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC6_DATA_H(self):
        """
        Read the register DAC6_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC6_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC6_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC6_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC6_DATA_H'] = (value & 0x0F)

    def read_DAC6_DATA_L(self):
        """
        Read the register DAC6_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC6_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC6_DATA_L']
        self._BITFIELD['DAC6_DATA_L'] = (value & 0xFF)

    def read_DAC6_GAIN_CAL_R00(self):
        """
        Read the register DAC6_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC6_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC6_GAIN_CAL_R00']
        self._BITFIELD['DAC6_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC6_GAIN_CAL_R11(self):
        """
        Read the register DAC6_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC6_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC6_GAIN_CAL_R11']
        self._BITFIELD['DAC6_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC6_OFFSET_CAL_R00(self):
        """
        Read the register DAC6_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC6_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC6_OFFSET_CAL_R00']
        self._BITFIELD['DAC6_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC6_OFFSET_CAL_R11(self):
        """
        Read the register DAC6_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC6_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC6_OFFSET_CAL_R11']
        self._BITFIELD['DAC6_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC7_DATA_H(self):
        """
        Read the register DAC7_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC7_DATA_H'])
        value = readValue & self.READ_COMP_MASK['DAC7_DATA_H']
        self._BITFIELD['RSVD_7_4_DAC7_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC7_DATA_H'] = (value & 0x0F)

    def read_DAC7_DATA_L(self):
        """
        Read the register DAC7_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC7_DATA_L'])
        value = readValue & self.READ_COMP_MASK['DAC7_DATA_L']
        self._BITFIELD['DAC7_DATA_L'] = (value & 0xFF)

    def read_DAC7_GAIN_CAL_R00(self):
        """
        Read the register DAC7_GAIN_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC7_GAIN_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC7_GAIN_CAL_R00']
        self._BITFIELD['DAC7_GAIN_CAL_R00'] = (value & 0xFF)

    def read_DAC7_GAIN_CAL_R11(self):
        """
        Read the register DAC7_GAIN_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC7_GAIN_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC7_GAIN_CAL_R11']
        self._BITFIELD['DAC7_GAIN_CAL_R11'] = (value & 0xFF)

    def read_DAC7_OFFSET_CAL_R00(self):
        """
        Read the register DAC7_OFFSET_CAL_R00 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC7_OFFSET_CAL_R00'])
        value = readValue & self.READ_COMP_MASK['DAC7_OFFSET_CAL_R00']
        self._BITFIELD['DAC7_OFFSET_CAL_R00'] = (value & 0xFF)

    def read_DAC7_OFFSET_CAL_R11(self):
        """
        Read the register DAC7_OFFSET_CAL_R11 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC7_OFFSET_CAL_R11'])
        value = readValue & self.READ_COMP_MASK['DAC7_OFFSET_CAL_R11']
        self._BITFIELD['DAC7_OFFSET_CAL_R11'] = (value & 0xFF)

    def read_DAC_CLR(self):
        """
        Read the register DAC_CLR and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_CLR'])
        value = readValue & self.READ_COMP_MASK['DAC_CLR']
        self._BITFIELD['CLR_B7'] = (value & 0x80) >> 7
        self._BITFIELD['CLR_B6'] = (value & 0x40) >> 6
        self._BITFIELD['CLR_B5'] = (value & 0x20) >> 5
        self._BITFIELD['CLR_B4'] = (value & 0x10) >> 4
        self._BITFIELD['CLR_A3'] = (value & 0x08) >> 3
        self._BITFIELD['CLR_A2'] = (value & 0x04) >> 2
        self._BITFIELD['CLR_A1'] = (value & 0x02) >> 1
        self._BITFIELD['CLR_A0'] = (value & 0x01)

    def read_DAC_CLR_EN(self):
        """
        Read the register DAC_CLR_EN and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_CLR_EN'])
        value = readValue & self.READ_COMP_MASK['DAC_CLR_EN']
        self._BITFIELD['CLREN_B7'] = (value & 0x80) >> 7
        self._BITFIELD['CLREN_B6'] = (value & 0x40) >> 6
        self._BITFIELD['CLREN_B5'] = (value & 0x20) >> 5
        self._BITFIELD['CLREN_B4'] = (value & 0x10) >> 4
        self._BITFIELD['CLREN_A3'] = (value & 0x08) >> 3
        self._BITFIELD['CLREN_A2'] = (value & 0x04) >> 2
        self._BITFIELD['CLREN_A1'] = (value & 0x02) >> 1
        self._BITFIELD['CLREN_A0'] = (value & 0x01)

    def read_DAC_CLR_SRC_0(self):
        """
        Read the register DAC_CLR_SRC_0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_CLR_SRC_0'])
        value = readValue & self.READ_COMP_MASK['DAC_CLR_SRC_0']
        self._BITFIELD['RSVD_7_6_DAC_CLR_SRC_0'] = (value & 0xC0) >> 6
        self._BITFIELD['RT_HIGH_ALR_CLR'] = (value & 0x20) >> 5
        self._BITFIELD['RT_LOW_ALR_CLR'] = (value & 0x10) >> 4
        self._BITFIELD['CS_B_ALR_CLR'] = (value & 0x08) >> 3
        self._BITFIELD['CS_A_ALR_CLR'] = (value & 0x04) >> 2
        self._BITFIELD['ADC_IN1_ALR_CLR'] = (value & 0x02) >> 1
        self._BITFIELD['ADC_IN0_ALR_CLR'] = (value & 0x01)

    def read_DAC_CLR_SRC_1(self):
        """
        Read the register DAC_CLR_SRC_1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_CLR_SRC_1'])
        value = readValue & self.READ_COMP_MASK['DAC_CLR_SRC_1']
        self._BITFIELD['RSVD_7_3_DAC_CLR_SRC_1'] = (value & 0xF8) >> 3
        self._BITFIELD['THERM_ALR_CLR'] = (value & 0x04) >> 2
        self._BITFIELD['LT_HIGH_ALR_CLR'] = (value & 0x02) >> 1
        self._BITFIELD['LT_LOW_ALR_CLR'] = (value & 0x01)

    def read_DAC_OUT_OK_CFG(self):
        """
        Read the register DAC_OUT_OK_CFG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_OUT_OK_CFG'])
        value = readValue & self.READ_COMP_MASK['DAC_OUT_OK_CFG']
        self._BITFIELD['ASSERT'] = (value & 0x80) >> 7
        self._BITFIELD['TIMER'] = (value & 0x7F)

    def read_DAC_RANGE(self):
        """
        Read the register DAC_RANGE and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_RANGE'])
        value = readValue & self.READ_COMP_MASK['DAC_RANGE']
        self._BITFIELD['RSVD_7_DAC_RANGE'] = (value & 0x80) >> 7
        self._BITFIELD['DAC_RANGEB'] = (value & 0x70) >> 4
        self._BITFIELD['RSVD_3_DAC_RANGE'] = (value & 0x08) >> 3
        self._BITFIELD['DAC_RANGEA'] = (value & 0x07)

    def read_DAC_SW_EN(self):
        """
        Read the register DAC_SW_EN and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_SW_EN'])
        value = readValue & self.READ_COMP_MASK['DAC_SW_EN']
        self._BITFIELD['RSVD_7_4_DAC_SW_EN'] = (value & 0xF0) >> 4
        self._BITFIELD['DAC_B2_SW_EN'] = (value & 0x08) >> 3
        self._BITFIELD['DAC_B0_SW_EN'] = (value & 0x04) >> 2
        self._BITFIELD['DAC_A2_SW_EN'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_A0_SW_EN'] = (value & 0x01)

    def read_DAC_TEST_CNTL(self):
        """
        Read the register DAC_TEST_CNTL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DAC_TEST_CNTL'])
        value = readValue & self.READ_COMP_MASK['DAC_TEST_CNTL']
        self._BITFIELD['DAC_CLAMP_DIS'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_DAC_TEST_CNTL'] = (value & 0x40) >> 6
        self._BITFIELD['DAC_HIZ_GROUP_B'] = (value & 0x20) >> 5
        self._BITFIELD['DAC_HIZ_GROUP_A'] = (value & 0x10) >> 4
        self._BITFIELD['RSVD_3_0_DAC_TEST_CNTL'] = (value & 0x0F)

    def read_DTEST_CNTL0(self):
        """
        Read the register DTEST_CNTL0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['DTEST_CNTL0'])
        value = readValue & self.READ_COMP_MASK['DTEST_CNTL0']
        self._BITFIELD['TRIM_DIS'] = (value & 0x80) >> 7
        self._BITFIELD['OSC_CLK_DIS'] = (value & 0x40) >> 6
        self._BITFIELD['ADC_TEST'] = (value & 0x20) >> 5
        self._BITFIELD['OSC_TEST_ENABLE'] = (value & 0x10) >> 4
        self._BITFIELD['TRACE_PORT'] = (value & 0x08) >> 3
        self._BITFIELD['OSC_CLK_EXT'] = (value & 0x04) >> 2
        self._BITFIELD['IO_TEST'] = (value & 0x02) >> 1
        self._BITFIELD['SCAN_TEST'] = (value & 0x01)

    def read_E2P_PD_DAC(self):
        """
        Read the register E2P_PD_DAC and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['E2P_PD_DAC'])
        value = readValue & self.READ_COMP_MASK['E2P_PD_DAC']
        self._BITFIELD['PD_DAC'] = (value & 0xFF)

    def read_EEPROM_CFG(self):
        """
        Read the register EEPROM_CFG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['EEPROM_CFG'])
        value = readValue & self.READ_COMP_MASK['EEPROM_CFG']
        self._BITFIELD['RSVD_7_2_EEPROM_CFG'] = (value & 0xFC) >> 2
        self._BITFIELD['E2P_FAST_MODE'] = (value & 0x02) >> 1
        self._BITFIELD['ECC_DIS'] = (value & 0x01)

    def read_EEPROM_CNTL(self):
        """
        Read the register EEPROM_CNTL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['EEPROM_CNTL'])
        value = readValue & self.READ_COMP_MASK['EEPROM_CNTL']
        self._BITFIELD['CMD_STATUS'] = (value & 0xFF)

    def read_FALSE_ALR_CFG(self):
        """
        Read the register FALSE_ALR_CFG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['FALSE_ALR_CFG'])
        value = readValue & self.READ_COMP_MASK['FALSE_ALR_CFG']
        self._BITFIELD['CH_FALR_CT'] = (value & 0xE0) >> 5
        self._BITFIELD['LT_FALR_CT'] = (value & 0x18) >> 3
        self._BITFIELD['RT_FALR_CT'] = (value & 0x06) >> 1
        self._BITFIELD['RSVD_0_FALSE_ALR_CFG'] = (value & 0x01)

    def read_GEN_STAT(self):
        """
        Read the register GEN_STAT and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GEN_STAT'])
        value = readValue & self.READ_COMP_MASK['GEN_STAT']
        self._BITFIELD['IBI_PEND'] = (value & 0x80) >> 7
        self._BITFIELD['IBI_ENABLE'] = (value & 0x40) >> 6
        self._BITFIELD['AVSSB'] = (value & 0x20) >> 5
        self._BITFIELD['AVSSA'] = (value & 0x10) >> 4
        self._BITFIELD['ADC_IDLE'] = (value & 0x08) >> 3
        self._BITFIELD['I3C_MODE'] = (value & 0x04) >> 2
        self._BITFIELD['GALR'] = (value & 0x02) >> 1
        self._BITFIELD['DAVF'] = (value & 0x01)

    def read_GEN_STAT_1(self):
        """
        Read the register GEN_STAT_1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GEN_STAT_1'])
        value = readValue & self.READ_COMP_MASK['GEN_STAT_1']
        self._BITFIELD['RSVD_7_2_GEN_STAT_1'] = (value & 0xFC) >> 2
        self._BITFIELD['AVCCB'] = (value & 0x02) >> 1
        self._BITFIELD['AVCCA'] = (value & 0x01)

    def read_GEN_STAT_2(self):
        """
        Read the register GEN_STAT_2 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GEN_STAT_2'])
        value = readValue & self.READ_COMP_MASK['GEN_STAT_2']
        self._BITFIELD['DAC_OUT_OK'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_GEN_STAT_2'] = (value & 0x40) >> 6
        self._BITFIELD['DAC_POWER_OK'] = (value & 0x20) >> 5
        self._BITFIELD['AVSS_OK'] = (value & 0x10) >> 4
        self._BITFIELD['AVCC_OK'] = (value & 0x08) >> 3
        self._BITFIELD['IOVDD_OK'] = (value & 0x04) >> 2
        self._BITFIELD['RSVD_1_GEN_STAT_2'] = (value & 0x02) >> 1
        self._BITFIELD['AVDD_OK'] = (value & 0x01)

    def read_GPIO_IEB(self):
        """
        Read the register GPIO_IEB and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GPIO_IEB'])
        value = readValue & self.READ_COMP_MASK['GPIO_IEB']
        self._BITFIELD['RSVD_7_GPIO_IEB'] = (value & 0x80) >> 7
        self._BITFIELD['DAC_OUT_OK_IEB'] = (value & 0x40) >> 6
        self._BITFIELD['SDO_IEB'] = (value & 0x20) >> 5
        self._BITFIELD['SDI_IEB'] = (value & 0x10) >> 4
        self._BITFIELD['CSB_IEB'] = (value & 0x08) >> 3
        self._BITFIELD['SCLK_IEB'] = (value & 0x04) >> 2
        self._BITFIELD['OUT_BEN_IEB'] = (value & 0x02) >> 1
        self._BITFIELD['OUT_AEN_IEB'] = (value & 0x01)

    def read_GPIO_IN(self):
        """
        Read the register GPIO_IN and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GPIO_IN'])
        value = readValue & self.READ_COMP_MASK['GPIO_IN']
        self._BITFIELD['RSVD_7_2_GPIO_IN'] = (value & 0xFC) >> 2
        self._BITFIELD['OUT_BEN_IN'] = (value & 0x02) >> 1
        self._BITFIELD['OUT_AEN_IN'] = (value & 0x01)

    def read_GPIO_OEB(self):
        """
        Read the register GPIO_OEB and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GPIO_OEB'])
        value = readValue & self.READ_COMP_MASK['GPIO_OEB']
        self._BITFIELD['RSVD_7_3_GPIO_OEB'] = (value & 0xF8) >> 3
        self._BITFIELD['DAC_OUT_OK_OEB'] = (value & 0x04) >> 2
        self._BITFIELD['OUT_BEN_OEB'] = (value & 0x02) >> 1
        self._BITFIELD['RSVD_0_GPIO_OEB'] = (value & 0x01)

    def read_GPIO_OUT(self):
        """
        Read the register GPIO_OUT and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GPIO_OUT'])
        value = readValue & self.READ_COMP_MASK['GPIO_OUT']
        self._BITFIELD['RSVD_7_2_GPIO_OUT'] = (value & 0xFC) >> 2
        self._BITFIELD['OUT_BEN_OUT'] = (value & 0x02) >> 1
        self._BITFIELD['RSVD_0_GPIO_OUT'] = (value & 0x01)

    def read_GPIO_TRACE(self):
        """
        Read the register GPIO_TRACE and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['GPIO_TRACE'])
        value = readValue & self.READ_COMP_MASK['GPIO_TRACE']
        self._BITFIELD['RSVD_7_5_GPIO_TRACE'] = (value & 0xE0) >> 5
        self._BITFIELD['GPIO_TRACE'] = (value & 0x1F)

    def read_IF_CFG_0(self):
        """
        Read the register IF_CFG_0 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['IF_CFG_0'])
        value = readValue & self.READ_COMP_MASK['IF_CFG_0']
        self._BITFIELD['SOFT_RESET'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_IF_CFG_0'] = (value & 0x40) >> 6
        self._BITFIELD['ADDR_ASCEND'] = (value & 0x20) >> 5
        self._BITFIELD['RSVD_4_0_IF_CFG_0'] = (value & 0x1F)

    def read_IF_CFG_1(self):
        """
        Read the register IF_CFG_1 and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['IF_CFG_1'])
        value = readValue & self.READ_COMP_MASK['IF_CFG_1']
        self._BITFIELD['SINGLE_INSTR'] = (value & 0x80) >> 7
        self._BITFIELD['RSVD_6_IF_CFG_1'] = (value & 0x40) >> 6
        self._BITFIELD['READBACK'] = (value & 0x20) >> 5
        self._BITFIELD['ADDR_MODE'] = (value & 0x10) >> 4
        self._BITFIELD['RSVD_3_0_IF_CFG_1'] = (value & 0x0F)

    def read_LDO_TRIM_IOVDD(self):
        """
        Read the register LDO_TRIM_IOVDD and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LDO_TRIM_IOVDD'])
        value = readValue & self.READ_COMP_MASK['LDO_TRIM_IOVDD']
        self._BITFIELD['RSVD_7_5_LDO_TRIM_IOVDD'] = (value & 0xE0) >> 5
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_20MA'] = (value & 0x10) >> 4
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_10MA'] = (value & 0x08) >> 3
        self._BITFIELD['LDO_TRIM_IOVDD_CURRENT_5MA'] = (value & 0x04) >> 2
        self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P9V'] = (value & 0x02) >> 1
        self._BITFIELD['LDO_TRIM_IOVDD_BOOST_1P85V'] = (value & 0x01)

    def read_LDO_TRIM_VDDD(self):
        """
        Read the register LDO_TRIM_VDDD and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LDO_TRIM_VDDD'])
        value = readValue & self.READ_COMP_MASK['LDO_TRIM_VDDD']
        self._BITFIELD['RSVD_7_5_LDO_TRIM_VDDD'] = (value & 0xE0) >> 5
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_20MA'] = (value & 0x10) >> 4
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_10MA'] = (value & 0x08) >> 3
        self._BITFIELD['LDO_TRIM_VDDD_CURRENT_5MA'] = (value & 0x04) >> 2
        self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P9V'] = (value & 0x02) >> 1
        self._BITFIELD['LDO_TRIM_VDDD_BOOST_1P85V'] = (value & 0x01)

    def read_LT_DATA_H(self):
        """
        Read the register LT_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_DATA_H'])
        value = readValue & self.READ_COMP_MASK['LT_DATA_H']
        self._BITFIELD['RSVD_7_4_LT_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['LT_DATA_H'] = (value & 0x0F)

    def read_LT_DATA_L(self):
        """
        Read the register LT_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_DATA_L'])
        value = readValue & self.READ_COMP_MASK['LT_DATA_L']
        self._BITFIELD['LT_DATA_L'] = (value & 0xFF)

    def read_LT_HYST(self):
        """
        Read the register LT_HYST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_HYST'])
        value = readValue & self.READ_COMP_MASK['LT_HYST']
        self._BITFIELD['RSVD_7_5_LT_HYST'] = (value & 0xE0) >> 5
        self._BITFIELD['HYST_LT'] = (value & 0x1F)

    def read_LT_LO_THR_H(self):
        """
        Read the register LT_LO_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_LO_THR_H'])
        value = readValue & self.READ_COMP_MASK['LT_LO_THR_H']
        self._BITFIELD['RSVD_7_4_LT_LO_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRL_LT_H'] = (value & 0x0F)

    def read_LT_LO_THR_L(self):
        """
        Read the register LT_LO_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_LO_THR_L'])
        value = readValue & self.READ_COMP_MASK['LT_LO_THR_L']
        self._BITFIELD['THRL_LT_L'] = (value & 0xFF)

    def read_LT_THERM_THR_H(self):
        """
        Read the register LT_THERM_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_THERM_THR_H'])
        value = readValue & self.READ_COMP_MASK['LT_THERM_THR_H']
        self._BITFIELD['RSVD_7_4_LT_THERM_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRT_LT_H'] = (value & 0x0F)

    def read_LT_THERM_THR_L(self):
        """
        Read the register LT_THERM_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_THERM_THR_L'])
        value = readValue & self.READ_COMP_MASK['LT_THERM_THR_L']
        self._BITFIELD['THRT_LT_L'] = (value & 0xFF)

    def read_LT_UP_THR_H(self):
        """
        Read the register LT_UP_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_UP_THR_H'])
        value = readValue & self.READ_COMP_MASK['LT_UP_THR_H']
        self._BITFIELD['RSVD_7_4_LT_UP_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRU_LT_H'] = (value & 0x0F)

    def read_LT_UP_THR_L(self):
        """
        Read the register LT_UP_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['LT_UP_THR_L'])
        value = readValue & self.READ_COMP_MASK['LT_UP_THR_L']
        self._BITFIELD['THRU_LT_L'] = (value & 0xFF)

    def read_MIPI_MAN_ID_H(self):
        """
        Read the register MIPI_MAN_ID_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['MIPI_MAN_ID_H'])
        value = readValue & self.READ_COMP_MASK['MIPI_MAN_ID_H']
        self._BITFIELD['MAN_ID_HIGH'] = (value & 0xFF)

    def read_MIPI_MAN_ID_L(self):
        """
        Read the register MIPI_MAN_ID_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['MIPI_MAN_ID_L'])
        value = readValue & self.READ_COMP_MASK['MIPI_MAN_ID_L']
        self._BITFIELD['MAN_ID_LOW'] = (value & 0xFE) >> 1
        self._BITFIELD['RSVD_0_MIPI_MAN_ID_L'] = (value & 0x01)

    def read_MISC_CNTL(self):
        """
        Read the register MISC_CNTL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['MISC_CNTL'])
        value = readValue & self.READ_COMP_MASK['MISC_CNTL']
        self._BITFIELD['I3C_MAX_DS'] = (value & 0xE0) >> 5
        self._BITFIELD['I2C_SPIKE_DIS'] = (value & 0x10) >> 4
        self._BITFIELD['DAC_CLAMP_EN'] = (value & 0x0C) >> 2
        self._BITFIELD['DAC_ICALP'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_ICALN'] = (value & 0x01)

    def read_OSC_CMP_HYST(self):
        """
        Read the register OSC_CMP_HYST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OSC_CMP_HYST'])
        value = readValue & self.READ_COMP_MASK['OSC_CMP_HYST']
        self._BITFIELD['RSVD_7_2_OSC_CMP_HYST'] = (value & 0xFC) >> 2
        self._BITFIELD['CMP_HYST'] = (value & 0x03)

    def read_OSC_CNT_CMP_H(self):
        """
        Read the register OSC_CNT_CMP_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OSC_CNT_CMP_H'])
        value = readValue & self.READ_COMP_MASK['OSC_CNT_CMP_H']
        self._BITFIELD['RSVD_7_4_OSC_CNT_CMP_H'] = (value & 0xF0) >> 4
        self._BITFIELD['CLK_CNT_CMP_H'] = (value & 0x0F)

    def read_OSC_CNT_CMP_L(self):
        """
        Read the register OSC_CNT_CMP_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OSC_CNT_CMP_L'])
        value = readValue & self.READ_COMP_MASK['OSC_CNT_CMP_L']
        self._BITFIELD['CLK_CNT_CMP_L'] = (value & 0xFF)

    def read_OSC_CNT_H(self):
        """
        Read the register OSC_CNT_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OSC_CNT_H'])
        value = readValue & self.READ_COMP_MASK['OSC_CNT_H']
        self._BITFIELD['RSVD_7_4_OSC_CNT_H'] = (value & 0xF0) >> 4
        self._BITFIELD['CLK_COUNT_H'] = (value & 0x0F)

    def read_OSC_CNT_L(self):
        """
        Read the register OSC_CNT_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OSC_CNT_L'])
        value = readValue & self.READ_COMP_MASK['OSC_CNT_L']
        self._BITFIELD['CLK_COUNT_L'] = (value & 0xFF)

    def read_OSC_TRIM_TEST(self):
        """
        Read the register OSC_TRIM_TEST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OSC_TRIM_TEST'])
        value = readValue & self.READ_COMP_MASK['OSC_TRIM_TEST']
        self._BITFIELD['OSC_TRIM_TEST'] = (value & 0xFF)

    def read_OUT_AEN_GROUPA(self):
        """
        Read the register OUT_AEN_GROUPA and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OUT_AEN_GROUPA'])
        value = readValue & self.READ_COMP_MASK['OUT_AEN_GROUPA']
        self._BITFIELD['RSVD_7_OUT_AEN_GROUPA'] = (value & 0x80) >> 7
        self._BITFIELD['FETDRV_A2_AEN_GROUPA'] = (value & 0x40) >> 6
        self._BITFIELD['RSVD_5_OUT_AEN_GROUPA'] = (value & 0x20) >> 5
        self._BITFIELD['FETDRV_A0_AEN_GROUPA'] = (value & 0x10) >> 4
        self._BITFIELD['DAC_A3_AEN_GROUPA'] = (value & 0x08) >> 3
        self._BITFIELD['DAC_A2_AEN_GROUPA'] = (value & 0x04) >> 2
        self._BITFIELD['DAC_A1_AEN_GROUPA'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_A0_AEN_GROUPA'] = (value & 0x01)

    def read_OUT_AEN_GROUPB(self):
        """
        Read the register OUT_AEN_GROUPB and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OUT_AEN_GROUPB'])
        value = readValue & self.READ_COMP_MASK['OUT_AEN_GROUPB']
        self._BITFIELD['RSVD_7_OUT_AEN_GROUPB'] = (value & 0x80) >> 7
        self._BITFIELD['FETDRV_B2_AEN_GROUPB'] = (value & 0x40) >> 6
        self._BITFIELD['RSVD_5_OUT_AEN_GROUPB'] = (value & 0x20) >> 5
        self._BITFIELD['FETDRV_B0_AEN_GROUPB'] = (value & 0x10) >> 4
        self._BITFIELD['DAC_B3_AEN_GROUPB'] = (value & 0x08) >> 3
        self._BITFIELD['DAC_B2_AEN_GROUPB'] = (value & 0x04) >> 2
        self._BITFIELD['DAC_B1_AEN_GROUPB'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_B0_AEN_GROUPB'] = (value & 0x01)

    def read_OUT_BEN_GROUPA(self):
        """
        Read the register OUT_BEN_GROUPA and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OUT_BEN_GROUPA'])
        value = readValue & self.READ_COMP_MASK['OUT_BEN_GROUPA']
        self._BITFIELD['RSVD_7_OUT_BEN_GROUPA'] = (value & 0x80) >> 7
        self._BITFIELD['FETDRV_A2_BEN_GROUPA'] = (value & 0x40) >> 6
        self._BITFIELD['RSVD_5_OUT_BEN_GROUPA'] = (value & 0x20) >> 5
        self._BITFIELD['FETDRV_A0_BEN_GROUPA'] = (value & 0x10) >> 4
        self._BITFIELD['DAC_A3_BEN_GROUPA'] = (value & 0x08) >> 3
        self._BITFIELD['DAC_A2_BEN_GROUPA'] = (value & 0x04) >> 2
        self._BITFIELD['DAC_A1_BEN_GROUPA'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_A0_BEN_GROUPA'] = (value & 0x01)

    def read_OUT_BEN_GROUPB(self):
        """
        Read the register OUT_BEN_GROUPB and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['OUT_BEN_GROUPB'])
        value = readValue & self.READ_COMP_MASK['OUT_BEN_GROUPB']
        self._BITFIELD['RSVD_7_OUT_BEN_GROUPB'] = (value & 0x80) >> 7
        self._BITFIELD['FETDRV_B2_BEN_GROUPB'] = (value & 0x40) >> 6
        self._BITFIELD['RSVD_5_OUT_BEN_GROUPB'] = (value & 0x20) >> 5
        self._BITFIELD['FETDRV_B0_BEN_GROUPB'] = (value & 0x10) >> 4
        self._BITFIELD['DAC_B3_BEN_GROUPB'] = (value & 0x08) >> 3
        self._BITFIELD['DAC_B2_BEN_GROUPB'] = (value & 0x04) >> 2
        self._BITFIELD['DAC_B1_BEN_GROUPB'] = (value & 0x02) >> 1
        self._BITFIELD['DAC_B0_BEN_GROUPB'] = (value & 0x01)

    def read_PD_ADC(self):
        """
        Read the register PD_ADC and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['PD_ADC'])
        value = readValue & self.READ_COMP_MASK['PD_ADC']
        self._BITFIELD['RSVD_7_1_PD_ADC'] = (value & 0xFE) >> 1
        self._BITFIELD['PADC'] = (value & 0x01)

    def read_PD_CS(self):
        """
        Read the register PD_CS and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['PD_CS'])
        value = readValue & self.READ_COMP_MASK['PD_CS']
        self._BITFIELD['RSVD_7_2_PD_CS'] = (value & 0xFC) >> 2
        self._BITFIELD['PCS_B'] = (value & 0x02) >> 1
        self._BITFIELD['PCS_A'] = (value & 0x01)

    def read_PD_DAC(self):
        """
        Read the register PD_DAC and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['PD_DAC'])
        value = readValue & self.READ_COMP_MASK['PD_DAC']
        self._BITFIELD['PDAC_B7'] = (value & 0x80) >> 7
        self._BITFIELD['PDAC_B6'] = (value & 0x40) >> 6
        self._BITFIELD['PDAC_B5'] = (value & 0x20) >> 5
        self._BITFIELD['PDAC_B4'] = (value & 0x10) >> 4
        self._BITFIELD['PDAC_A3'] = (value & 0x08) >> 3
        self._BITFIELD['PDAC_A2'] = (value & 0x04) >> 2
        self._BITFIELD['PDAC_A1'] = (value & 0x02) >> 1
        self._BITFIELD['PDAC_A0'] = (value & 0x01)

    def read_PD_DAC_CFG(self):
        """
        Read the register PD_DAC_CFG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['PD_DAC_CFG'])
        value = readValue & self.READ_COMP_MASK['PD_DAC_CFG']
        self._BITFIELD['RSVD_7_3_PD_DAC_CFG'] = (value & 0xF8) >> 3
        self._BITFIELD['TIM_DAC_DEL_EN'] = (value & 0x04) >> 2
        self._BITFIELD['TIM_DAC_DEL'] = (value & 0x03)

    def read_POR_BYPASS_H(self):
        """
        Read the register POR_BYPASS_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['POR_BYPASS_H'])
        value = readValue & self.READ_COMP_MASK['POR_BYPASS_H']
        self._BITFIELD['POR_BYPASS_H'] = (value & 0xFF)

    def read_POR_BYPASS_L(self):
        """
        Read the register POR_BYPASS_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['POR_BYPASS_L'])
        value = readValue & self.READ_COMP_MASK['POR_BYPASS_L']
        self._BITFIELD['POR_BYPASS_L'] = (value & 0xFF)

    def read_REG_UPDATE(self):
        """
        Read the register REG_UPDATE and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['REG_UPDATE'])
        value = readValue & self.READ_COMP_MASK['REG_UPDATE']
        self._BITFIELD['RSVD_7_5_REG_UPDATE'] = (value & 0xE0) >> 5
        self._BITFIELD['ADC_UPDATE'] = (value & 0x10) >> 4
        self._BITFIELD['RSVD_3_1_REG_UPDATE'] = (value & 0x0E) >> 1
        self._BITFIELD['DAC_UPDATE'] = (value & 0x01)

    def read_RT_DATA_H(self):
        """
        Read the register RT_DATA_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['RT_DATA_H'])
        value = readValue & self.READ_COMP_MASK['RT_DATA_H']
        self._BITFIELD['RSVD_7_4_RT_DATA_H'] = (value & 0xF0) >> 4
        self._BITFIELD['RT_DATA_H'] = (value & 0x0F)

    def read_RT_DATA_L(self):
        """
        Read the register RT_DATA_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['RT_DATA_L'])
        value = readValue & self.READ_COMP_MASK['RT_DATA_L']
        self._BITFIELD['RT_DATA_L'] = (value & 0xFF)

    def read_RT_HYST(self):
        """
        Read the register RT_HYST and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['RT_HYST'])
        value = readValue & self.READ_COMP_MASK['RT_HYST']
        self._BITFIELD['RSVD_7_5_RT_HYST'] = (value & 0xE0) >> 5
        self._BITFIELD['HYST_RT'] = (value & 0x1F)

    def read_RT_LO_THR_H(self):
        """
        Read the register RT_LO_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['RT_LO_THR_H'])
        value = readValue & self.READ_COMP_MASK['RT_LO_THR_H']
        self._BITFIELD['RSVD_7_4_RT_LO_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRL_RT_H'] = (value & 0x0F)

    def read_RT_LO_THR_L(self):
        """
        Read the register RT_LO_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['RT_LO_THR_L'])
        value = readValue & self.READ_COMP_MASK['RT_LO_THR_L']
        self._BITFIELD['THRL_RT_L'] = (value & 0xFF)

    def read_RT_UP_THR_H(self):
        """
        Read the register RT_UP_THR_H and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['RT_UP_THR_H'])
        value = readValue & self.READ_COMP_MASK['RT_UP_THR_H']
        self._BITFIELD['RSVD_7_4_RT_UP_THR_H'] = (value & 0xF0) >> 4
        self._BITFIELD['THRU_RT_H'] = (value & 0x0F)

    def read_RT_UP_THR_L(self):
        """
        Read the register RT_UP_THR_L and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['RT_UP_THR_L'])
        value = readValue & self.READ_COMP_MASK['RT_UP_THR_L']
        self._BITFIELD['THRU_RT_L'] = (value & 0xFF)

    def read_SPIKE_FILTER_CAL_SCL(self):
        """
        Read the register SPIKE_FILTER_CAL_SCL and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['SPIKE_FILTER_CAL_SCL'])
        value = readValue & self.READ_COMP_MASK['SPIKE_FILTER_CAL_SCL']
        self._BITFIELD['SPIKE_FILTER_CAL_SCL'] = (value & 0xFF)

    def read_SPIKE_FILTER_CAL_SDA(self):
        """
        Read the register SPIKE_FILTER_CAL_SDA and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['SPIKE_FILTER_CAL_SDA'])
        value = readValue & self.READ_COMP_MASK['SPIKE_FILTER_CAL_SDA']
        self._BITFIELD['SPIKE_FILTER_CAL_SDA'] = (value & 0xFF)

    def read_TEST_KEY(self):
        """
        Read the register TEST_KEY and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['TEST_KEY'])
        value = readValue & self.READ_COMP_MASK['TEST_KEY']
        self._BITFIELD['KEY_STATUS'] = (value & 0xFF)

    def read_TRIM_BG(self):
        """
        Read the register TRIM_BG and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['TRIM_BG'])
        value = readValue & self.READ_COMP_MASK['TRIM_BG']
        self._BITFIELD['TRIM_BG'] = (value & 0xFF)

    def read_TRIM_OSC(self):
        """
        Read the register TRIM_OSC and place the contents in the shadow registers.
        """
        readValue = self.read_register(self.REGISTER_ADDRESSES['TRIM_OSC'])
        value = readValue & self.READ_COMP_MASK['TRIM_OSC']
        self._BITFIELD['TRIM_OSC'] = (value & 0xFF)

    #################################################################
    # Property Definitions
    #################################################################

    # Define each of the setters and getters to a property
    SOFT_RESET = property(get_SOFT_RESET, set_SOFT_RESET)
    RSVD_6_IF_CFG_0 = property(get_RSVD_6_IF_CFG_0, set_RSVD_6_IF_CFG_0)
    ADDR_ASCEND = property(get_ADDR_ASCEND, set_ADDR_ASCEND)
    RSVD_4_0_IF_CFG_0 = property(get_RSVD_4_0_IF_CFG_0, set_RSVD_4_0_IF_CFG_0)
    SINGLE_INSTR = property(get_SINGLE_INSTR, set_SINGLE_INSTR)
    RSVD_6_IF_CFG_1 = property(get_RSVD_6_IF_CFG_1, set_RSVD_6_IF_CFG_1)
    READBACK = property(get_READBACK, set_READBACK)
    ADDR_MODE = property(get_ADDR_MODE, set_ADDR_MODE)
    RSVD_3_0_IF_CFG_1 = property(get_RSVD_3_0_IF_CFG_1, set_RSVD_3_0_IF_CFG_1)
    RSVD_7_4_CHIP_TYPE = property(get_RSVD_7_4_CHIP_TYPE, set_RSVD_7_4_CHIP_TYPE)
    CHIP_TYPE = property(get_CHIP_TYPE, set_CHIP_TYPE)
    CHIPDID_LOW = property(get_CHIPDID_LOW, set_CHIPDID_LOW)
    CHIPDID_HIGH = property(get_CHIPDID_HIGH, set_CHIPDID_HIGH)
    VERSIONID = property(get_VERSIONID, set_VERSIONID)
    RSVD_7_4_CHIP_VARIANT = property(get_RSVD_7_4_CHIP_VARIANT, set_RSVD_7_4_CHIP_VARIANT)
    CHIP_VARIANT = property(get_CHIP_VARIANT, set_CHIP_VARIANT)
    MAN_ID_LOW = property(get_MAN_ID_LOW, set_MAN_ID_LOW)
    RSVD_0_MIPI_MAN_ID_L = property(get_RSVD_0_MIPI_MAN_ID_L, set_RSVD_0_MIPI_MAN_ID_L)
    MAN_ID_HIGH = property(get_MAN_ID_HIGH, set_MAN_ID_HIGH)
    RSVD_7_5_REG_UPDATE = property(get_RSVD_7_5_REG_UPDATE, set_RSVD_7_5_REG_UPDATE)
    ADC_UPDATE = property(get_ADC_UPDATE, set_ADC_UPDATE)
    RSVD_3_1_REG_UPDATE = property(get_RSVD_3_1_REG_UPDATE, set_RSVD_3_1_REG_UPDATE)
    DAC_UPDATE = property(get_DAC_UPDATE, set_DAC_UPDATE)
    CMODE = property(get_CMODE, set_CMODE)
    ADC_CONV_RATE = property(get_ADC_CONV_RATE, set_ADC_CONV_RATE)
    ADC_REF_BUFF = property(get_ADC_REF_BUFF, set_ADC_REF_BUFF)
    RSVD_3_2_ADC_CFG = property(get_RSVD_3_2_ADC_CFG, set_RSVD_3_2_ADC_CFG)
    RT_CONV_RATE = property(get_RT_CONV_RATE, set_RT_CONV_RATE)
    CH_FALR_CT = property(get_CH_FALR_CT, set_CH_FALR_CT)
    LT_FALR_CT = property(get_LT_FALR_CT, set_LT_FALR_CT)
    RT_FALR_CT = property(get_RT_FALR_CT, set_RT_FALR_CT)
    RSVD_0_FALSE_ALR_CFG = property(get_RSVD_0_FALSE_ALR_CFG, set_RSVD_0_FALSE_ALR_CFG)
    RSVD_7_4_ADC_AVG = property(get_RSVD_7_4_ADC_AVG, set_RSVD_7_4_ADC_AVG)
    ADC_AVG_ADC = property(get_ADC_AVG_ADC, set_ADC_AVG_ADC)
    RSVD_7_6_ADC_MUX_CFG = property(get_RSVD_7_6_ADC_MUX_CFG, set_RSVD_7_6_ADC_MUX_CFG)
    RT_CH = property(get_RT_CH, set_RT_CH)
    LT_CH = property(get_LT_CH, set_LT_CH)
    CS_B = property(get_CS_B, set_CS_B)
    CS_A = property(get_CS_A, set_CS_A)
    ADC_IN1 = property(get_ADC_IN1, set_ADC_IN1)
    ADC_IN0 = property(get_ADC_IN0, set_ADC_IN0)
    ASSERT = property(get_ASSERT, set_ASSERT)
    TIMER = property(get_TIMER, set_TIMER)
    CLREN_B7 = property(get_CLREN_B7, set_CLREN_B7)
    CLREN_B6 = property(get_CLREN_B6, set_CLREN_B6)
    CLREN_B5 = property(get_CLREN_B5, set_CLREN_B5)
    CLREN_B4 = property(get_CLREN_B4, set_CLREN_B4)
    CLREN_A3 = property(get_CLREN_A3, set_CLREN_A3)
    CLREN_A2 = property(get_CLREN_A2, set_CLREN_A2)
    CLREN_A1 = property(get_CLREN_A1, set_CLREN_A1)
    CLREN_A0 = property(get_CLREN_A0, set_CLREN_A0)
    RSVD_7_6_DAC_CLR_SRC_0 = property(get_RSVD_7_6_DAC_CLR_SRC_0, set_RSVD_7_6_DAC_CLR_SRC_0)
    RT_HIGH_ALR_CLR = property(get_RT_HIGH_ALR_CLR, set_RT_HIGH_ALR_CLR)
    RT_LOW_ALR_CLR = property(get_RT_LOW_ALR_CLR, set_RT_LOW_ALR_CLR)
    CS_B_ALR_CLR = property(get_CS_B_ALR_CLR, set_CS_B_ALR_CLR)
    CS_A_ALR_CLR = property(get_CS_A_ALR_CLR, set_CS_A_ALR_CLR)
    ADC_IN1_ALR_CLR = property(get_ADC_IN1_ALR_CLR, set_ADC_IN1_ALR_CLR)
    ADC_IN0_ALR_CLR = property(get_ADC_IN0_ALR_CLR, set_ADC_IN0_ALR_CLR)
    RSVD_7_3_DAC_CLR_SRC_1 = property(get_RSVD_7_3_DAC_CLR_SRC_1, set_RSVD_7_3_DAC_CLR_SRC_1)
    THERM_ALR_CLR = property(get_THERM_ALR_CLR, set_THERM_ALR_CLR)
    LT_HIGH_ALR_CLR = property(get_LT_HIGH_ALR_CLR, set_LT_HIGH_ALR_CLR)
    LT_LOW_ALR_CLR = property(get_LT_LOW_ALR_CLR, set_LT_LOW_ALR_CLR)
    RSVD_7_6_ALR_CFG_0 = property(get_RSVD_7_6_ALR_CFG_0, set_RSVD_7_6_ALR_CFG_0)
    RT_HIGH_ALR_STAT = property(get_RT_HIGH_ALR_STAT, set_RT_HIGH_ALR_STAT)
    RT_LOW_ALR_STAT = property(get_RT_LOW_ALR_STAT, set_RT_LOW_ALR_STAT)
    CS_B_ALR_STAT = property(get_CS_B_ALR_STAT, set_CS_B_ALR_STAT)
    CS_A_ALR_STAT = property(get_CS_A_ALR_STAT, set_CS_A_ALR_STAT)
    ADC_IN1_ALR_STAT = property(get_ADC_IN1_ALR_STAT, set_ADC_IN1_ALR_STAT)
    ADC_IN0_ALR_STAT = property(get_ADC_IN0_ALR_STAT, set_ADC_IN0_ALR_STAT)
    ALR_LATCH_DIS = property(get_ALR_LATCH_DIS, set_ALR_LATCH_DIS)
    RSVD_6_ALR_CFG_1 = property(get_RSVD_6_ALR_CFG_1, set_RSVD_6_ALR_CFG_1)
    S0S1_ERR_ALR = property(get_S0S1_ERR_ALR, set_S0S1_ERR_ALR)
    PAR_ERR_ALR = property(get_PAR_ERR_ALR, set_PAR_ERR_ALR)
    DAV_ALR = property(get_DAV_ALR, set_DAV_ALR)
    THERM_ALR = property(get_THERM_ALR, set_THERM_ALR)
    LT_HIGH_ALR = property(get_LT_HIGH_ALR, set_LT_HIGH_ALR)
    LT_LOW_ALR = property(get_LT_LOW_ALR, set_LT_LOW_ALR)
    RSVD_7_DAC_RANGE = property(get_RSVD_7_DAC_RANGE, set_RSVD_7_DAC_RANGE)
    DAC_RANGEB = property(get_DAC_RANGEB, set_DAC_RANGEB)
    RSVD_3_DAC_RANGE = property(get_RSVD_3_DAC_RANGE, set_RSVD_3_DAC_RANGE)
    DAC_RANGEA = property(get_DAC_RANGEA, set_DAC_RANGEA)
    ADC_IN0_DATA_L = property(get_ADC_IN0_DATA_L, set_ADC_IN0_DATA_L)
    RSVD_7_4_ADC_IN0_DATA_H = property(get_RSVD_7_4_ADC_IN0_DATA_H, set_RSVD_7_4_ADC_IN0_DATA_H)
    ADC_IN0_DATA_H = property(get_ADC_IN0_DATA_H, set_ADC_IN0_DATA_H)
    ADC_IN1_DATA_L = property(get_ADC_IN1_DATA_L, set_ADC_IN1_DATA_L)
    RSVD_7_4_ADC_IN1_DATA_H = property(get_RSVD_7_4_ADC_IN1_DATA_H, set_RSVD_7_4_ADC_IN1_DATA_H)
    ADC_IN1_DATA_H = property(get_ADC_IN1_DATA_H, set_ADC_IN1_DATA_H)
    CS_A_DATA_L = property(get_CS_A_DATA_L, set_CS_A_DATA_L)
    RSVD_7_5_CS_A_DATA_H = property(get_RSVD_7_5_CS_A_DATA_H, set_RSVD_7_5_CS_A_DATA_H)
    CS_A_DATA_H_SIGN = property(get_CS_A_DATA_H_SIGN, set_CS_A_DATA_H_SIGN)
    CS_A_DATA_H = property(get_CS_A_DATA_H, set_CS_A_DATA_H)
    CS_B_DATA_L = property(get_CS_B_DATA_L, set_CS_B_DATA_L)
    RSVD_7_5_CS_B_DATA_H = property(get_RSVD_7_5_CS_B_DATA_H, set_RSVD_7_5_CS_B_DATA_H)
    CS_B_DATA_H_SIGN = property(get_CS_B_DATA_H_SIGN, set_CS_B_DATA_H_SIGN)
    CS_B_DATA_H = property(get_CS_B_DATA_H, set_CS_B_DATA_H)
    LT_DATA_L = property(get_LT_DATA_L, set_LT_DATA_L)
    RSVD_7_4_LT_DATA_H = property(get_RSVD_7_4_LT_DATA_H, set_RSVD_7_4_LT_DATA_H)
    LT_DATA_H = property(get_LT_DATA_H, set_LT_DATA_H)
    RT_DATA_L = property(get_RT_DATA_L, set_RT_DATA_L)
    RSVD_7_4_RT_DATA_H = property(get_RSVD_7_4_RT_DATA_H, set_RSVD_7_4_RT_DATA_H)
    RT_DATA_H = property(get_RT_DATA_H, set_RT_DATA_H)
    DAC0_DATA_L = property(get_DAC0_DATA_L, set_DAC0_DATA_L)
    RSVD_7_4_DAC0_DATA_H = property(get_RSVD_7_4_DAC0_DATA_H, set_RSVD_7_4_DAC0_DATA_H)
    DAC0_DATA_H = property(get_DAC0_DATA_H, set_DAC0_DATA_H)
    DAC1_DATA_L = property(get_DAC1_DATA_L, set_DAC1_DATA_L)
    RSVD_7_4_DAC1_DATA_H = property(get_RSVD_7_4_DAC1_DATA_H, set_RSVD_7_4_DAC1_DATA_H)
    DAC1_DATA_H = property(get_DAC1_DATA_H, set_DAC1_DATA_H)
    DAC2_DATA_L = property(get_DAC2_DATA_L, set_DAC2_DATA_L)
    RSVD_7_4_DAC2_DATA_H = property(get_RSVD_7_4_DAC2_DATA_H, set_RSVD_7_4_DAC2_DATA_H)
    DAC2_DATA_H = property(get_DAC2_DATA_H, set_DAC2_DATA_H)
    DAC3_DATA_L = property(get_DAC3_DATA_L, set_DAC3_DATA_L)
    RSVD_7_4_DAC3_DATA_H = property(get_RSVD_7_4_DAC3_DATA_H, set_RSVD_7_4_DAC3_DATA_H)
    DAC3_DATA_H = property(get_DAC3_DATA_H, set_DAC3_DATA_H)
    DAC4_DATA_L = property(get_DAC4_DATA_L, set_DAC4_DATA_L)
    RSVD_7_4_DAC4_DATA_H = property(get_RSVD_7_4_DAC4_DATA_H, set_RSVD_7_4_DAC4_DATA_H)
    DAC4_DATA_H = property(get_DAC4_DATA_H, set_DAC4_DATA_H)
    DAC5_DATA_L = property(get_DAC5_DATA_L, set_DAC5_DATA_L)
    RSVD_7_4_DAC5_DATA_H = property(get_RSVD_7_4_DAC5_DATA_H, set_RSVD_7_4_DAC5_DATA_H)
    DAC5_DATA_H = property(get_DAC5_DATA_H, set_DAC5_DATA_H)
    DAC6_DATA_L = property(get_DAC6_DATA_L, set_DAC6_DATA_L)
    RSVD_7_4_DAC6_DATA_H = property(get_RSVD_7_4_DAC6_DATA_H, set_RSVD_7_4_DAC6_DATA_H)
    DAC6_DATA_H = property(get_DAC6_DATA_H, set_DAC6_DATA_H)
    DAC7_DATA_L = property(get_DAC7_DATA_L, set_DAC7_DATA_L)
    RSVD_7_4_DAC7_DATA_H = property(get_RSVD_7_4_DAC7_DATA_H, set_RSVD_7_4_DAC7_DATA_H)
    DAC7_DATA_H = property(get_DAC7_DATA_H, set_DAC7_DATA_H)
    RSVD_7_4_ALR_STAT_0 = property(get_RSVD_7_4_ALR_STAT_0, set_RSVD_7_4_ALR_STAT_0)
    RT_HIGH_ALR = property(get_RT_HIGH_ALR, set_RT_HIGH_ALR)
    RT_LOW_ALR = property(get_RT_LOW_ALR, set_RT_LOW_ALR)
    CS_B_ALR = property(get_CS_B_ALR, set_CS_B_ALR)
    CS_A_ALR = property(get_CS_A_ALR, set_CS_A_ALR)
    ADC_IN1_ALR = property(get_ADC_IN1_ALR, set_ADC_IN1_ALR)
    ADC_IN0_ALR = property(get_ADC_IN0_ALR, set_ADC_IN0_ALR)
    RSVD_7_6_ALR_STAT_1 = property(get_RSVD_7_6_ALR_STAT_1, set_RSVD_7_6_ALR_STAT_1)
    S0S1_ERR_ALR_STAT = property(get_S0S1_ERR_ALR_STAT, set_S0S1_ERR_ALR_STAT)
    PAR_ERR_ALR_STAT = property(get_PAR_ERR_ALR_STAT, set_PAR_ERR_ALR_STAT)
    DAV_ALR_STAT = property(get_DAV_ALR_STAT, set_DAV_ALR_STAT)
    THERM_ALR_STAT = property(get_THERM_ALR_STAT, set_THERM_ALR_STAT)
    LT_HIGH_ALR_STAT = property(get_LT_HIGH_ALR_STAT, set_LT_HIGH_ALR_STAT)
    LT_LOW_ALR_STAT = property(get_LT_LOW_ALR_STAT, set_LT_LOW_ALR_STAT)
    IBI_PEND = property(get_IBI_PEND, set_IBI_PEND)
    IBI_ENABLE = property(get_IBI_ENABLE, set_IBI_ENABLE)
    AVSSB = property(get_AVSSB, set_AVSSB)
    AVSSA = property(get_AVSSA, set_AVSSA)
    ADC_IDLE = property(get_ADC_IDLE, set_ADC_IDLE)
    I3C_MODE = property(get_I3C_MODE, set_I3C_MODE)
    GALR = property(get_GALR, set_GALR)
    DAVF = property(get_DAVF, set_DAVF)
    RSVD_7_2_GEN_STAT_1 = property(get_RSVD_7_2_GEN_STAT_1, set_RSVD_7_2_GEN_STAT_1)
    AVCCB = property(get_AVCCB, set_AVCCB)
    AVCCA = property(get_AVCCA, set_AVCCA)
    DAC_OUT_OK = property(get_DAC_OUT_OK, set_DAC_OUT_OK)
    RSVD_6_GEN_STAT_2 = property(get_RSVD_6_GEN_STAT_2, set_RSVD_6_GEN_STAT_2)
    DAC_POWER_OK = property(get_DAC_POWER_OK, set_DAC_POWER_OK)
    AVSS_OK = property(get_AVSS_OK, set_AVSS_OK)
    AVCC_OK = property(get_AVCC_OK, set_AVCC_OK)
    IOVDD_OK = property(get_IOVDD_OK, set_IOVDD_OK)
    RSVD_1_GEN_STAT_2 = property(get_RSVD_1_GEN_STAT_2, set_RSVD_1_GEN_STAT_2)
    AVDD_OK = property(get_AVDD_OK, set_AVDD_OK)
    RSVD_7_4_DAC_SW_EN = property(get_RSVD_7_4_DAC_SW_EN, set_RSVD_7_4_DAC_SW_EN)
    DAC_B2_SW_EN = property(get_DAC_B2_SW_EN, set_DAC_B2_SW_EN)
    DAC_B0_SW_EN = property(get_DAC_B0_SW_EN, set_DAC_B0_SW_EN)
    DAC_A2_SW_EN = property(get_DAC_A2_SW_EN, set_DAC_A2_SW_EN)
    DAC_A0_SW_EN = property(get_DAC_A0_SW_EN, set_DAC_A0_SW_EN)
    RSVD_7_OUT_AEN_GROUPA = property(get_RSVD_7_OUT_AEN_GROUPA, set_RSVD_7_OUT_AEN_GROUPA)
    FETDRV_A2_AEN_GROUPA = property(get_FETDRV_A2_AEN_GROUPA, set_FETDRV_A2_AEN_GROUPA)
    RSVD_5_OUT_AEN_GROUPA = property(get_RSVD_5_OUT_AEN_GROUPA, set_RSVD_5_OUT_AEN_GROUPA)
    FETDRV_A0_AEN_GROUPA = property(get_FETDRV_A0_AEN_GROUPA, set_FETDRV_A0_AEN_GROUPA)
    DAC_A3_AEN_GROUPA = property(get_DAC_A3_AEN_GROUPA, set_DAC_A3_AEN_GROUPA)
    DAC_A2_AEN_GROUPA = property(get_DAC_A2_AEN_GROUPA, set_DAC_A2_AEN_GROUPA)
    DAC_A1_AEN_GROUPA = property(get_DAC_A1_AEN_GROUPA, set_DAC_A1_AEN_GROUPA)
    DAC_A0_AEN_GROUPA = property(get_DAC_A0_AEN_GROUPA, set_DAC_A0_AEN_GROUPA)
    RSVD_7_OUT_AEN_GROUPB = property(get_RSVD_7_OUT_AEN_GROUPB, set_RSVD_7_OUT_AEN_GROUPB)
    FETDRV_B2_AEN_GROUPB = property(get_FETDRV_B2_AEN_GROUPB, set_FETDRV_B2_AEN_GROUPB)
    RSVD_5_OUT_AEN_GROUPB = property(get_RSVD_5_OUT_AEN_GROUPB, set_RSVD_5_OUT_AEN_GROUPB)
    FETDRV_B0_AEN_GROUPB = property(get_FETDRV_B0_AEN_GROUPB, set_FETDRV_B0_AEN_GROUPB)
    DAC_B3_AEN_GROUPB = property(get_DAC_B3_AEN_GROUPB, set_DAC_B3_AEN_GROUPB)
    DAC_B2_AEN_GROUPB = property(get_DAC_B2_AEN_GROUPB, set_DAC_B2_AEN_GROUPB)
    DAC_B1_AEN_GROUPB = property(get_DAC_B1_AEN_GROUPB, set_DAC_B1_AEN_GROUPB)
    DAC_B0_AEN_GROUPB = property(get_DAC_B0_AEN_GROUPB, set_DAC_B0_AEN_GROUPB)
    RSVD_7_OUT_BEN_GROUPA = property(get_RSVD_7_OUT_BEN_GROUPA, set_RSVD_7_OUT_BEN_GROUPA)
    FETDRV_A2_BEN_GROUPA = property(get_FETDRV_A2_BEN_GROUPA, set_FETDRV_A2_BEN_GROUPA)
    RSVD_5_OUT_BEN_GROUPA = property(get_RSVD_5_OUT_BEN_GROUPA, set_RSVD_5_OUT_BEN_GROUPA)
    FETDRV_A0_BEN_GROUPA = property(get_FETDRV_A0_BEN_GROUPA, set_FETDRV_A0_BEN_GROUPA)
    DAC_A3_BEN_GROUPA = property(get_DAC_A3_BEN_GROUPA, set_DAC_A3_BEN_GROUPA)
    DAC_A2_BEN_GROUPA = property(get_DAC_A2_BEN_GROUPA, set_DAC_A2_BEN_GROUPA)
    DAC_A1_BEN_GROUPA = property(get_DAC_A1_BEN_GROUPA, set_DAC_A1_BEN_GROUPA)
    DAC_A0_BEN_GROUPA = property(get_DAC_A0_BEN_GROUPA, set_DAC_A0_BEN_GROUPA)
    RSVD_7_OUT_BEN_GROUPB = property(get_RSVD_7_OUT_BEN_GROUPB, set_RSVD_7_OUT_BEN_GROUPB)
    FETDRV_B2_BEN_GROUPB = property(get_FETDRV_B2_BEN_GROUPB, set_FETDRV_B2_BEN_GROUPB)
    RSVD_5_OUT_BEN_GROUPB = property(get_RSVD_5_OUT_BEN_GROUPB, set_RSVD_5_OUT_BEN_GROUPB)
    FETDRV_B0_BEN_GROUPB = property(get_FETDRV_B0_BEN_GROUPB, set_FETDRV_B0_BEN_GROUPB)
    DAC_B3_BEN_GROUPB = property(get_DAC_B3_BEN_GROUPB, set_DAC_B3_BEN_GROUPB)
    DAC_B2_BEN_GROUPB = property(get_DAC_B2_BEN_GROUPB, set_DAC_B2_BEN_GROUPB)
    DAC_B1_BEN_GROUPB = property(get_DAC_B1_BEN_GROUPB, set_DAC_B1_BEN_GROUPB)
    DAC_B0_BEN_GROUPB = property(get_DAC_B0_BEN_GROUPB, set_DAC_B0_BEN_GROUPB)
    THRU_ADC_IN0_L = property(get_THRU_ADC_IN0_L, set_THRU_ADC_IN0_L)
    RSVD_7_4_ADC_IN0_UP_THR_H = property(get_RSVD_7_4_ADC_IN0_UP_THR_H, set_RSVD_7_4_ADC_IN0_UP_THR_H)
    THRU_ADC_IN0_H = property(get_THRU_ADC_IN0_H, set_THRU_ADC_IN0_H)
    THRL_ADC_IN0_L = property(get_THRL_ADC_IN0_L, set_THRL_ADC_IN0_L)
    RSVD_7_4_ADC_IN0_LO_THR_H = property(get_RSVD_7_4_ADC_IN0_LO_THR_H, set_RSVD_7_4_ADC_IN0_LO_THR_H)
    THRL_ADC_IN0_H = property(get_THRL_ADC_IN0_H, set_THRL_ADC_IN0_H)
    THRU_ADC_IN1_L = property(get_THRU_ADC_IN1_L, set_THRU_ADC_IN1_L)
    RSVD_7_4_ADC_IN1_UP_THR_H = property(get_RSVD_7_4_ADC_IN1_UP_THR_H, set_RSVD_7_4_ADC_IN1_UP_THR_H)
    THRU_ADC_IN1_H = property(get_THRU_ADC_IN1_H, set_THRU_ADC_IN1_H)
    THRL_ADC_IN1_L = property(get_THRL_ADC_IN1_L, set_THRL_ADC_IN1_L)
    RSVD_7_4_ADC_IN1_LO_THR_H = property(get_RSVD_7_4_ADC_IN1_LO_THR_H, set_RSVD_7_4_ADC_IN1_LO_THR_H)
    THRL_ADC_IN1_H = property(get_THRL_ADC_IN1_H, set_THRL_ADC_IN1_H)
    THRU_CS_A_L = property(get_THRU_CS_A_L, set_THRU_CS_A_L)
    RSVD_7_4_CS_A_UP_THR_H = property(get_RSVD_7_4_CS_A_UP_THR_H, set_RSVD_7_4_CS_A_UP_THR_H)
    THRU_CS_A_H = property(get_THRU_CS_A_H, set_THRU_CS_A_H)
    THRL_CS_A_L = property(get_THRL_CS_A_L, set_THRL_CS_A_L)
    RSVD_7_4_CS_A_LO_THR_H = property(get_RSVD_7_4_CS_A_LO_THR_H, set_RSVD_7_4_CS_A_LO_THR_H)
    THRL_CS_A_H = property(get_THRL_CS_A_H, set_THRL_CS_A_H)
    THRU_CS_B_L = property(get_THRU_CS_B_L, set_THRU_CS_B_L)
    RSVD_7_4_CS_B_UP_THR_H = property(get_RSVD_7_4_CS_B_UP_THR_H, set_RSVD_7_4_CS_B_UP_THR_H)
    THRU_CS_B_H = property(get_THRU_CS_B_H, set_THRU_CS_B_H)
    THRL_CS_B_L = property(get_THRL_CS_B_L, set_THRL_CS_B_L)
    RSVD_7_4_CS_B_LO_THR_H = property(get_RSVD_7_4_CS_B_LO_THR_H, set_RSVD_7_4_CS_B_LO_THR_H)
    THRL_CS_B_H = property(get_THRL_CS_B_H, set_THRL_CS_B_H)
    THRU_LT_L = property(get_THRU_LT_L, set_THRU_LT_L)
    RSVD_7_4_LT_UP_THR_H = property(get_RSVD_7_4_LT_UP_THR_H, set_RSVD_7_4_LT_UP_THR_H)
    THRU_LT_H = property(get_THRU_LT_H, set_THRU_LT_H)
    THRL_LT_L = property(get_THRL_LT_L, set_THRL_LT_L)
    RSVD_7_4_LT_LO_THR_H = property(get_RSVD_7_4_LT_LO_THR_H, set_RSVD_7_4_LT_LO_THR_H)
    THRL_LT_H = property(get_THRL_LT_H, set_THRL_LT_H)
    THRU_RT_L = property(get_THRU_RT_L, set_THRU_RT_L)
    RSVD_7_4_RT_UP_THR_H = property(get_RSVD_7_4_RT_UP_THR_H, set_RSVD_7_4_RT_UP_THR_H)
    THRU_RT_H = property(get_THRU_RT_H, set_THRU_RT_H)
    THRL_RT_L = property(get_THRL_RT_L, set_THRL_RT_L)
    RSVD_7_4_RT_LO_THR_H = property(get_RSVD_7_4_RT_LO_THR_H, set_RSVD_7_4_RT_LO_THR_H)
    THRL_RT_H = property(get_THRL_RT_H, set_THRL_RT_H)
    RSVD_7_ADC_IN0_HYST = property(get_RSVD_7_ADC_IN0_HYST, set_RSVD_7_ADC_IN0_HYST)
    HYST_ADC_IN0 = property(get_HYST_ADC_IN0, set_HYST_ADC_IN0)
    RSVD_7_ADC_IN1_HYST = property(get_RSVD_7_ADC_IN1_HYST, set_RSVD_7_ADC_IN1_HYST)
    HYST_ADC_IN1 = property(get_HYST_ADC_IN1, set_HYST_ADC_IN1)
    RSVD_7_CS_A_HYST = property(get_RSVD_7_CS_A_HYST, set_RSVD_7_CS_A_HYST)
    HYST_CS_A = property(get_HYST_CS_A, set_HYST_CS_A)
    RSVD_7_CS_B_HYST = property(get_RSVD_7_CS_B_HYST, set_RSVD_7_CS_B_HYST)
    HYST_CS_B = property(get_HYST_CS_B, set_HYST_CS_B)
    RSVD_7_5_LT_HYST = property(get_RSVD_7_5_LT_HYST, set_RSVD_7_5_LT_HYST)
    HYST_LT = property(get_HYST_LT, set_HYST_LT)
    RSVD_7_5_RT_HYST = property(get_RSVD_7_5_RT_HYST, set_RSVD_7_5_RT_HYST)
    HYST_RT = property(get_HYST_RT, set_HYST_RT)
    CLR_B7 = property(get_CLR_B7, set_CLR_B7)
    CLR_B6 = property(get_CLR_B6, set_CLR_B6)
    CLR_B5 = property(get_CLR_B5, set_CLR_B5)
    CLR_B4 = property(get_CLR_B4, set_CLR_B4)
    CLR_A3 = property(get_CLR_A3, set_CLR_A3)
    CLR_A2 = property(get_CLR_A2, set_CLR_A2)
    CLR_A1 = property(get_CLR_A1, set_CLR_A1)
    CLR_A0 = property(get_CLR_A0, set_CLR_A0)
    PDAC_B7 = property(get_PDAC_B7, set_PDAC_B7)
    PDAC_B6 = property(get_PDAC_B6, set_PDAC_B6)
    PDAC_B5 = property(get_PDAC_B5, set_PDAC_B5)
    PDAC_B4 = property(get_PDAC_B4, set_PDAC_B4)
    PDAC_A3 = property(get_PDAC_A3, set_PDAC_A3)
    PDAC_A2 = property(get_PDAC_A2, set_PDAC_A2)
    PDAC_A1 = property(get_PDAC_A1, set_PDAC_A1)
    PDAC_A0 = property(get_PDAC_A0, set_PDAC_A0)
    RSVD_7_1_PD_ADC = property(get_RSVD_7_1_PD_ADC, set_RSVD_7_1_PD_ADC)
    PADC = property(get_PADC, set_PADC)
    RSVD_7_2_PD_CS = property(get_RSVD_7_2_PD_CS, set_RSVD_7_2_PD_CS)
    PCS_B = property(get_PCS_B, set_PCS_B)
    PCS_A = property(get_PCS_A, set_PCS_A)
    RSVD_7_1_ADC_TRIG = property(get_RSVD_7_1_ADC_TRIG, set_RSVD_7_1_ADC_TRIG)
    ICONV = property(get_ICONV, set_ICONV)
    DAC0_GAIN_CAL_R00 = property(get_DAC0_GAIN_CAL_R00, set_DAC0_GAIN_CAL_R00)
    DAC1_GAIN_CAL_R00 = property(get_DAC1_GAIN_CAL_R00, set_DAC1_GAIN_CAL_R00)
    DAC2_GAIN_CAL_R00 = property(get_DAC2_GAIN_CAL_R00, set_DAC2_GAIN_CAL_R00)
    DAC3_GAIN_CAL_R00 = property(get_DAC3_GAIN_CAL_R00, set_DAC3_GAIN_CAL_R00)
    DAC4_GAIN_CAL_R00 = property(get_DAC4_GAIN_CAL_R00, set_DAC4_GAIN_CAL_R00)
    DAC5_GAIN_CAL_R00 = property(get_DAC5_GAIN_CAL_R00, set_DAC5_GAIN_CAL_R00)
    DAC6_GAIN_CAL_R00 = property(get_DAC6_GAIN_CAL_R00, set_DAC6_GAIN_CAL_R00)
    DAC7_GAIN_CAL_R00 = property(get_DAC7_GAIN_CAL_R00, set_DAC7_GAIN_CAL_R00)
    DAC0_OFFSET_CAL_R00 = property(get_DAC0_OFFSET_CAL_R00, set_DAC0_OFFSET_CAL_R00)
    DAC1_OFFSET_CAL_R00 = property(get_DAC1_OFFSET_CAL_R00, set_DAC1_OFFSET_CAL_R00)
    DAC2_OFFSET_CAL_R00 = property(get_DAC2_OFFSET_CAL_R00, set_DAC2_OFFSET_CAL_R00)
    DAC3_OFFSET_CAL_R00 = property(get_DAC3_OFFSET_CAL_R00, set_DAC3_OFFSET_CAL_R00)
    DAC4_OFFSET_CAL_R00 = property(get_DAC4_OFFSET_CAL_R00, set_DAC4_OFFSET_CAL_R00)
    DAC5_OFFSET_CAL_R00 = property(get_DAC5_OFFSET_CAL_R00, set_DAC5_OFFSET_CAL_R00)
    DAC6_OFFSET_CAL_R00 = property(get_DAC6_OFFSET_CAL_R00, set_DAC6_OFFSET_CAL_R00)
    DAC7_OFFSET_CAL_R00 = property(get_DAC7_OFFSET_CAL_R00, set_DAC7_OFFSET_CAL_R00)
    DAC0_GAIN_CAL_R11 = property(get_DAC0_GAIN_CAL_R11, set_DAC0_GAIN_CAL_R11)
    DAC1_GAIN_CAL_R11 = property(get_DAC1_GAIN_CAL_R11, set_DAC1_GAIN_CAL_R11)
    DAC2_GAIN_CAL_R11 = property(get_DAC2_GAIN_CAL_R11, set_DAC2_GAIN_CAL_R11)
    DAC3_GAIN_CAL_R11 = property(get_DAC3_GAIN_CAL_R11, set_DAC3_GAIN_CAL_R11)
    DAC4_GAIN_CAL_R11 = property(get_DAC4_GAIN_CAL_R11, set_DAC4_GAIN_CAL_R11)
    DAC5_GAIN_CAL_R11 = property(get_DAC5_GAIN_CAL_R11, set_DAC5_GAIN_CAL_R11)
    DAC6_GAIN_CAL_R11 = property(get_DAC6_GAIN_CAL_R11, set_DAC6_GAIN_CAL_R11)
    DAC7_GAIN_CAL_R11 = property(get_DAC7_GAIN_CAL_R11, set_DAC7_GAIN_CAL_R11)
    DAC0_OFFSET_CAL_R11 = property(get_DAC0_OFFSET_CAL_R11, set_DAC0_OFFSET_CAL_R11)
    DAC1_OFFSET_CAL_R11 = property(get_DAC1_OFFSET_CAL_R11, set_DAC1_OFFSET_CAL_R11)
    DAC2_OFFSET_CAL_R11 = property(get_DAC2_OFFSET_CAL_R11, set_DAC2_OFFSET_CAL_R11)
    DAC3_OFFSET_CAL_R11 = property(get_DAC3_OFFSET_CAL_R11, set_DAC3_OFFSET_CAL_R11)
    DAC4_OFFSET_CAL_R11 = property(get_DAC4_OFFSET_CAL_R11, set_DAC4_OFFSET_CAL_R11)
    DAC5_OFFSET_CAL_R11 = property(get_DAC5_OFFSET_CAL_R11, set_DAC5_OFFSET_CAL_R11)
    DAC6_OFFSET_CAL_R11 = property(get_DAC6_OFFSET_CAL_R11, set_DAC6_OFFSET_CAL_R11)
    DAC7_OFFSET_CAL_R11 = property(get_DAC7_OFFSET_CAL_R11, set_DAC7_OFFSET_CAL_R11)
    TRIM_OSC = property(get_TRIM_OSC, set_TRIM_OSC)
    TRIM_BG = property(get_TRIM_BG, set_TRIM_BG)
    SPIKE_FILTER_CAL_SCL = property(get_SPIKE_FILTER_CAL_SCL, set_SPIKE_FILTER_CAL_SCL)
    SPIKE_FILTER_CAL_SDA = property(get_SPIKE_FILTER_CAL_SDA, set_SPIKE_FILTER_CAL_SDA)
    ADC_TRIM_REFBUF = property(get_ADC_TRIM_REFBUF, set_ADC_TRIM_REFBUF)
    ADC_TRIM_VCM = property(get_ADC_TRIM_VCM, set_ADC_TRIM_VCM)
    ADC_TRIM_LDO = property(get_ADC_TRIM_LDO, set_ADC_TRIM_LDO)
    PD_DAC = property(get_PD_DAC, set_PD_DAC)
    RSVD_7_3_PD_DAC_CFG = property(get_RSVD_7_3_PD_DAC_CFG, set_RSVD_7_3_PD_DAC_CFG)
    TIM_DAC_DEL_EN = property(get_TIM_DAC_DEL_EN, set_TIM_DAC_DEL_EN)
    TIM_DAC_DEL = property(get_TIM_DAC_DEL, set_TIM_DAC_DEL)
    CS_A_GAIN_ERROR_SIGN = property(get_CS_A_GAIN_ERROR_SIGN, set_CS_A_GAIN_ERROR_SIGN)
    GAIN_ERROR_CS_A_GAIN_ERROR = property(get_GAIN_ERROR_CS_A_GAIN_ERROR, set_GAIN_ERROR_CS_A_GAIN_ERROR)
    CS_B_GAIN_ERROR_SIGN = property(get_CS_B_GAIN_ERROR_SIGN, set_CS_B_GAIN_ERROR_SIGN)
    GAIN_ERROR_CS_B_GAIN_ERROR = property(get_GAIN_ERROR_CS_B_GAIN_ERROR, set_GAIN_ERROR_CS_B_GAIN_ERROR)
    RSVD_7_6_CS_A_LUT0_OFFSET = property(get_RSVD_7_6_CS_A_LUT0_OFFSET, set_RSVD_7_6_CS_A_LUT0_OFFSET)
    CS_A_LUT0_OFFSET_LUT0_OFFSET = property(get_CS_A_LUT0_OFFSET_LUT0_OFFSET, set_CS_A_LUT0_OFFSET_LUT0_OFFSET)
    RSVD_7_6_CS_A_LUT1_OFFSET = property(get_RSVD_7_6_CS_A_LUT1_OFFSET, set_RSVD_7_6_CS_A_LUT1_OFFSET)
    CS_A_LUT1_OFFSET = property(get_CS_A_LUT1_OFFSET, set_CS_A_LUT1_OFFSET)
    RSVD_7_6_CS_B_LUT0_OFFSET = property(get_RSVD_7_6_CS_B_LUT0_OFFSET, set_RSVD_7_6_CS_B_LUT0_OFFSET)
    CS_B_LUT0_OFFSET_LUT0_OFFSET = property(get_CS_B_LUT0_OFFSET_LUT0_OFFSET, set_CS_B_LUT0_OFFSET_LUT0_OFFSET)
    RSVD_7_6_CS_B_LUT1_OFFSET = property(get_RSVD_7_6_CS_B_LUT1_OFFSET, set_RSVD_7_6_CS_B_LUT1_OFFSET)
    CS_B_LUT1_OFFSET = property(get_CS_B_LUT1_OFFSET, set_CS_B_LUT1_OFFSET)
    ADC_OFFSET_ADC_IN_CAL_SIGN = property(get_ADC_OFFSET_ADC_IN_CAL_SIGN, set_ADC_OFFSET_ADC_IN_CAL_SIGN)
    ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE = property(get_ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE,
                                                  set_ADC_OFFSET_ADC_IN_CAL_OFFSET_VALUE)
    ADC_OFFSET_CS_CAL_SIGN = property(get_ADC_OFFSET_CS_CAL_SIGN, set_ADC_OFFSET_CS_CAL_SIGN)
    ADC_OFFSET_CS_CAL_OFFSET_VALUE = property(get_ADC_OFFSET_CS_CAL_OFFSET_VALUE, set_ADC_OFFSET_CS_CAL_OFFSET_VALUE)
    ADC_OFFSET_LT_CAL_SIGN = property(get_ADC_OFFSET_LT_CAL_SIGN, set_ADC_OFFSET_LT_CAL_SIGN)
    ADC_OFFSET_LT_CAL_OFFSET_VALUE = property(get_ADC_OFFSET_LT_CAL_OFFSET_VALUE, set_ADC_OFFSET_LT_CAL_OFFSET_VALUE)
    ADC_OFFSET_RT_CAL_SIGN = property(get_ADC_OFFSET_RT_CAL_SIGN, set_ADC_OFFSET_RT_CAL_SIGN)
    ADC_OFFSET_RT_CAL_OFFSET_VALUE = property(get_ADC_OFFSET_RT_CAL_OFFSET_VALUE, set_ADC_OFFSET_RT_CAL_OFFSET_VALUE)
    RSVD_7_ADC_CAL_CNTL = property(get_RSVD_7_ADC_CAL_CNTL, set_RSVD_7_ADC_CAL_CNTL)
    OFFSET_EN = property(get_OFFSET_EN, set_OFFSET_EN)
    RSVD_5_3_ADC_CAL_CNTL = property(get_RSVD_5_3_ADC_CAL_CNTL, set_RSVD_5_3_ADC_CAL_CNTL)
    CS_FAST_AVG_EN = property(get_CS_FAST_AVG_EN, set_CS_FAST_AVG_EN)
    ADC_SAMPLE_DLY = property(get_ADC_SAMPLE_DLY, set_ADC_SAMPLE_DLY)
    CS_A_VCM_BASE_L = property(get_CS_A_VCM_BASE_L, set_CS_A_VCM_BASE_L)
    RSVD_7_4_CS_A_VCM_BASE_H = property(get_RSVD_7_4_CS_A_VCM_BASE_H, set_RSVD_7_4_CS_A_VCM_BASE_H)
    CS_A_VCM_BASE_H = property(get_CS_A_VCM_BASE_H, set_CS_A_VCM_BASE_H)
    CS_A_ER_VCM_BASE_L = property(get_CS_A_ER_VCM_BASE_L, set_CS_A_ER_VCM_BASE_L)
    CS_A_CAL_ALU_BYP = property(get_CS_A_CAL_ALU_BYP, set_CS_A_CAL_ALU_BYP)
    RSVD_6_5_CS_A_ER_VCM_BASE_H = property(get_RSVD_6_5_CS_A_ER_VCM_BASE_H, set_RSVD_6_5_CS_A_ER_VCM_BASE_H)
    CS_A_ER_VCM_BASE_H_SIGN = property(get_CS_A_ER_VCM_BASE_H_SIGN, set_CS_A_ER_VCM_BASE_H_SIGN)
    CS_A_ER_VCM_BASE_H = property(get_CS_A_ER_VCM_BASE_H, set_CS_A_ER_VCM_BASE_H)
    CS_A_VCM_SLOPE_L = property(get_CS_A_VCM_SLOPE_L, set_CS_A_VCM_SLOPE_L)
    RSVD_7_5_CS_A_VCM_SLOPE_H = property(get_RSVD_7_5_CS_A_VCM_SLOPE_H, set_RSVD_7_5_CS_A_VCM_SLOPE_H)
    CS_A_VCM_SLOPE_H_SIGN = property(get_CS_A_VCM_SLOPE_H_SIGN, set_CS_A_VCM_SLOPE_H_SIGN)
    CS_A_VCM_SLOPE_H = property(get_CS_A_VCM_SLOPE_H, set_CS_A_VCM_SLOPE_H)
    CS_B_VCM_BASE_L = property(get_CS_B_VCM_BASE_L, set_CS_B_VCM_BASE_L)
    RSVD_7_4_CS_B_VCM_BASE_H = property(get_RSVD_7_4_CS_B_VCM_BASE_H, set_RSVD_7_4_CS_B_VCM_BASE_H)
    CS_B_VCM_BASE_H = property(get_CS_B_VCM_BASE_H, set_CS_B_VCM_BASE_H)
    CS_B_ER_VCM_BASE_L = property(get_CS_B_ER_VCM_BASE_L, set_CS_B_ER_VCM_BASE_L)
    CS_B_CAL_ALU_BYP = property(get_CS_B_CAL_ALU_BYP, set_CS_B_CAL_ALU_BYP)
    RSVD_6_5_CS_B_ER_VCM_BASE_H = property(get_RSVD_6_5_CS_B_ER_VCM_BASE_H, set_RSVD_6_5_CS_B_ER_VCM_BASE_H)
    CS_B_ER_VCM_BASE_H_SIGN = property(get_CS_B_ER_VCM_BASE_H_SIGN, set_CS_B_ER_VCM_BASE_H_SIGN)
    CS_B_ER_VCM_BASE_H = property(get_CS_B_ER_VCM_BASE_H, set_CS_B_ER_VCM_BASE_H)
    CS_B_VCM_SLOPE_L = property(get_CS_B_VCM_SLOPE_L, set_CS_B_VCM_SLOPE_L)
    RSVD_7_5_CS_B_VCM_SLOPE_H = property(get_RSVD_7_5_CS_B_VCM_SLOPE_H, set_RSVD_7_5_CS_B_VCM_SLOPE_H)
    CS_B_VCM_SLOPE_H_SIGN = property(get_CS_B_VCM_SLOPE_H_SIGN, set_CS_B_VCM_SLOPE_H_SIGN)
    CS_B_VCM_SLOPE_H = property(get_CS_B_VCM_SLOPE_H, set_CS_B_VCM_SLOPE_H)
    CS_DAC_MODE = property(get_CS_DAC_MODE, set_CS_DAC_MODE)
    CS_DATA_CLAMP_EN = property(get_CS_DATA_CLAMP_EN, set_CS_DATA_CLAMP_EN)
    CS_ADC_ACQ_DLY_EN = property(get_CS_ADC_ACQ_DLY_EN, set_CS_ADC_ACQ_DLY_EN)
    CS_CFG_0_SIGN = property(get_CS_CFG_0_SIGN, set_CS_CFG_0_SIGN)
    CS_A_DAC_OFFSET = property(get_CS_A_DAC_OFFSET, set_CS_A_DAC_OFFSET)
    CS_CONV_RATE = property(get_CS_CONV_RATE, set_CS_CONV_RATE)
    CS_CFG_1_SIGN = property(get_CS_CFG_1_SIGN, set_CS_CFG_1_SIGN)
    CS_B_DAC_OFFSET = property(get_CS_B_DAC_OFFSET, set_CS_B_DAC_OFFSET)
    DAC_CODE_BYPASS = property(get_DAC_CODE_BYPASS, set_DAC_CODE_BYPASS)
    CS_CFG_2_DAC_CODE = property(get_CS_CFG_2_DAC_CODE, set_CS_CFG_2_DAC_CODE)
    I3C_MAX_DS = property(get_I3C_MAX_DS, set_I3C_MAX_DS)
    I2C_SPIKE_DIS = property(get_I2C_SPIKE_DIS, set_I2C_SPIKE_DIS)
    DAC_CLAMP_EN = property(get_DAC_CLAMP_EN, set_DAC_CLAMP_EN)
    DAC_ICALP = property(get_DAC_ICALP, set_DAC_ICALP)
    DAC_ICALN = property(get_DAC_ICALN, set_DAC_ICALN)
    LT_SENSE_GAIN_CAL_H = property(get_LT_SENSE_GAIN_CAL_H, set_LT_SENSE_GAIN_CAL_H)
    LT_SENSE_GAIN_CAL_L = property(get_LT_SENSE_GAIN_CAL_L, set_LT_SENSE_GAIN_CAL_L)
    RT_SENSE_GAIN_CAL_H = property(get_RT_SENSE_GAIN_CAL_H, set_RT_SENSE_GAIN_CAL_H)
    RT_SENSE_GAIN_CAL_L = property(get_RT_SENSE_GAIN_CAL_L, set_RT_SENSE_GAIN_CAL_L)
    THRT_LT_L = property(get_THRT_LT_L, set_THRT_LT_L)
    RSVD_7_4_LT_THERM_THR_H = property(get_RSVD_7_4_LT_THERM_THR_H, set_RSVD_7_4_LT_THERM_THR_H)
    THRT_LT_H = property(get_THRT_LT_H, set_THRT_LT_H)
    CS_A_DEL_ER_VCM0_SIGN = property(get_CS_A_DEL_ER_VCM0_SIGN, set_CS_A_DEL_ER_VCM0_SIGN)
    CS_A_DEL_ER_VCM0 = property(get_CS_A_DEL_ER_VCM0, set_CS_A_DEL_ER_VCM0)
    CS_A_DEL_ER_VCM1_SIGN = property(get_CS_A_DEL_ER_VCM1_SIGN, set_CS_A_DEL_ER_VCM1_SIGN)
    CS_A_DEL_ER_VCM1 = property(get_CS_A_DEL_ER_VCM1, set_CS_A_DEL_ER_VCM1)
    CS_A_DEL_ER_VCM2_SIGN = property(get_CS_A_DEL_ER_VCM2_SIGN, set_CS_A_DEL_ER_VCM2_SIGN)
    CS_A_DEL_ER_VCM2 = property(get_CS_A_DEL_ER_VCM2, set_CS_A_DEL_ER_VCM2)
    CS_A_DEL_ER_VCM3_SIGN = property(get_CS_A_DEL_ER_VCM3_SIGN, set_CS_A_DEL_ER_VCM3_SIGN)
    CS_A_DEL_ER_VCM3 = property(get_CS_A_DEL_ER_VCM3, set_CS_A_DEL_ER_VCM3)
    CS_A_DEL_ER_VCM4_SIGN = property(get_CS_A_DEL_ER_VCM4_SIGN, set_CS_A_DEL_ER_VCM4_SIGN)
    CS_A_DEL_ER_VCM4 = property(get_CS_A_DEL_ER_VCM4, set_CS_A_DEL_ER_VCM4)
    CS_A_DEL_ER_VCM5_SIGN = property(get_CS_A_DEL_ER_VCM5_SIGN, set_CS_A_DEL_ER_VCM5_SIGN)
    CS_A_DEL_ER_VCM5 = property(get_CS_A_DEL_ER_VCM5, set_CS_A_DEL_ER_VCM5)
    CS_A_DEL_ER_VCM6_SIGN = property(get_CS_A_DEL_ER_VCM6_SIGN, set_CS_A_DEL_ER_VCM6_SIGN)
    CS_A_DEL_ER_VCM6 = property(get_CS_A_DEL_ER_VCM6, set_CS_A_DEL_ER_VCM6)
    CS_A_DEL_ER_VCM7_SIGN = property(get_CS_A_DEL_ER_VCM7_SIGN, set_CS_A_DEL_ER_VCM7_SIGN)
    CS_A_DEL_ER_VCM7 = property(get_CS_A_DEL_ER_VCM7, set_CS_A_DEL_ER_VCM7)
    CS_A_DEL_ER_VCM8_SIGN = property(get_CS_A_DEL_ER_VCM8_SIGN, set_CS_A_DEL_ER_VCM8_SIGN)
    CS_A_DEL_ER_VCM8 = property(get_CS_A_DEL_ER_VCM8, set_CS_A_DEL_ER_VCM8)
    CS_A_DEL_ER_VCM9_SIGN = property(get_CS_A_DEL_ER_VCM9_SIGN, set_CS_A_DEL_ER_VCM9_SIGN)
    CS_A_DEL_ER_VCM9 = property(get_CS_A_DEL_ER_VCM9, set_CS_A_DEL_ER_VCM9)
    CS_A_DEL_ER_VCM10_SIGN = property(get_CS_A_DEL_ER_VCM10_SIGN, set_CS_A_DEL_ER_VCM10_SIGN)
    CS_A_DEL_ER_VCM10 = property(get_CS_A_DEL_ER_VCM10, set_CS_A_DEL_ER_VCM10)
    CS_A_DEL_ER_VCM11_SIGN = property(get_CS_A_DEL_ER_VCM11_SIGN, set_CS_A_DEL_ER_VCM11_SIGN)
    CS_A_DEL_ER_VCM11 = property(get_CS_A_DEL_ER_VCM11, set_CS_A_DEL_ER_VCM11)
    CS_A_DEL_ER_VCM12_SIGN = property(get_CS_A_DEL_ER_VCM12_SIGN, set_CS_A_DEL_ER_VCM12_SIGN)
    CS_A_DEL_ER_VCM12 = property(get_CS_A_DEL_ER_VCM12, set_CS_A_DEL_ER_VCM12)
    CS_A_DEL_ER_VCM13_SIGN = property(get_CS_A_DEL_ER_VCM13_SIGN, set_CS_A_DEL_ER_VCM13_SIGN)
    CS_A_DEL_ER_VCM13 = property(get_CS_A_DEL_ER_VCM13, set_CS_A_DEL_ER_VCM13)
    CS_A_DEL_ER_VCM14_SIGN = property(get_CS_A_DEL_ER_VCM14_SIGN, set_CS_A_DEL_ER_VCM14_SIGN)
    CS_A_DEL_ER_VCM14 = property(get_CS_A_DEL_ER_VCM14, set_CS_A_DEL_ER_VCM14)
    CS_A_DEL_ER_VCM15_SIGN = property(get_CS_A_DEL_ER_VCM15_SIGN, set_CS_A_DEL_ER_VCM15_SIGN)
    CS_A_DEL_ER_VCM15 = property(get_CS_A_DEL_ER_VCM15, set_CS_A_DEL_ER_VCM15)
    CS_A_DEL_ER_VCM16_SIGN = property(get_CS_A_DEL_ER_VCM16_SIGN, set_CS_A_DEL_ER_VCM16_SIGN)
    CS_A_DEL_ER_VCM16 = property(get_CS_A_DEL_ER_VCM16, set_CS_A_DEL_ER_VCM16)
    CS_A_DEL_ER_VCM17_SIGN = property(get_CS_A_DEL_ER_VCM17_SIGN, set_CS_A_DEL_ER_VCM17_SIGN)
    CS_A_DEL_ER_VCM17 = property(get_CS_A_DEL_ER_VCM17, set_CS_A_DEL_ER_VCM17)
    CS_A_DEL_ER_VCM18_SIGN = property(get_CS_A_DEL_ER_VCM18_SIGN, set_CS_A_DEL_ER_VCM18_SIGN)
    CS_A_DEL_ER_VCM18 = property(get_CS_A_DEL_ER_VCM18, set_CS_A_DEL_ER_VCM18)
    CS_A_DEL_ER_VCM19_SIGN = property(get_CS_A_DEL_ER_VCM19_SIGN, set_CS_A_DEL_ER_VCM19_SIGN)
    CS_A_DEL_ER_VCM19 = property(get_CS_A_DEL_ER_VCM19, set_CS_A_DEL_ER_VCM19)
    CS_B_DEL_ER_VCM0_SIGN = property(get_CS_B_DEL_ER_VCM0_SIGN, set_CS_B_DEL_ER_VCM0_SIGN)
    CS_B_DEL_ER_VCM0 = property(get_CS_B_DEL_ER_VCM0, set_CS_B_DEL_ER_VCM0)
    CS_B_DEL_ER_VCM1_SIGN = property(get_CS_B_DEL_ER_VCM1_SIGN, set_CS_B_DEL_ER_VCM1_SIGN)
    CS_B_DEL_ER_VCM1 = property(get_CS_B_DEL_ER_VCM1, set_CS_B_DEL_ER_VCM1)
    CS_B_DEL_ER_VCM2_SIGN = property(get_CS_B_DEL_ER_VCM2_SIGN, set_CS_B_DEL_ER_VCM2_SIGN)
    CS_B_DEL_ER_VCM2 = property(get_CS_B_DEL_ER_VCM2, set_CS_B_DEL_ER_VCM2)
    CS_B_DEL_ER_VCM3_SIGN = property(get_CS_B_DEL_ER_VCM3_SIGN, set_CS_B_DEL_ER_VCM3_SIGN)
    CS_B_DEL_ER_VCM3 = property(get_CS_B_DEL_ER_VCM3, set_CS_B_DEL_ER_VCM3)
    CS_B_DEL_ER_VCM4_SIGN = property(get_CS_B_DEL_ER_VCM4_SIGN, set_CS_B_DEL_ER_VCM4_SIGN)
    CS_B_DEL_ER_VCM4 = property(get_CS_B_DEL_ER_VCM4, set_CS_B_DEL_ER_VCM4)
    CS_B_DEL_ER_VCM5_SIGN = property(get_CS_B_DEL_ER_VCM5_SIGN, set_CS_B_DEL_ER_VCM5_SIGN)
    CS_B_DEL_ER_VCM5 = property(get_CS_B_DEL_ER_VCM5, set_CS_B_DEL_ER_VCM5)
    CS_B_DEL_ER_VCM6_SIGN = property(get_CS_B_DEL_ER_VCM6_SIGN, set_CS_B_DEL_ER_VCM6_SIGN)
    CS_B_DEL_ER_VCM6 = property(get_CS_B_DEL_ER_VCM6, set_CS_B_DEL_ER_VCM6)
    CS_B_DEL_ER_VCM7_SIGN = property(get_CS_B_DEL_ER_VCM7_SIGN, set_CS_B_DEL_ER_VCM7_SIGN)
    CS_B_DEL_ER_VCM7 = property(get_CS_B_DEL_ER_VCM7, set_CS_B_DEL_ER_VCM7)
    CS_B_DEL_ER_VCM8_SIGN = property(get_CS_B_DEL_ER_VCM8_SIGN, set_CS_B_DEL_ER_VCM8_SIGN)
    CS_B_DEL_ER_VCM8 = property(get_CS_B_DEL_ER_VCM8, set_CS_B_DEL_ER_VCM8)
    CS_B_DEL_ER_VCM9_SIGN = property(get_CS_B_DEL_ER_VCM9_SIGN, set_CS_B_DEL_ER_VCM9_SIGN)
    CS_B_DEL_ER_VCM9 = property(get_CS_B_DEL_ER_VCM9, set_CS_B_DEL_ER_VCM9)
    CS_B_DEL_ER_VCM10_SIGN = property(get_CS_B_DEL_ER_VCM10_SIGN, set_CS_B_DEL_ER_VCM10_SIGN)
    CS_B_DEL_ER_VCM10 = property(get_CS_B_DEL_ER_VCM10, set_CS_B_DEL_ER_VCM10)
    CS_B_DEL_ER_VCM11_SIGN = property(get_CS_B_DEL_ER_VCM11_SIGN, set_CS_B_DEL_ER_VCM11_SIGN)
    CS_B_DEL_ER_VCM11 = property(get_CS_B_DEL_ER_VCM11, set_CS_B_DEL_ER_VCM11)
    CS_B_DEL_ER_VCM12_SIGN = property(get_CS_B_DEL_ER_VCM12_SIGN, set_CS_B_DEL_ER_VCM12_SIGN)
    CS_B_DEL_ER_VCM12 = property(get_CS_B_DEL_ER_VCM12, set_CS_B_DEL_ER_VCM12)
    CS_B_DEL_ER_VCM13_SIGN = property(get_CS_B_DEL_ER_VCM13_SIGN, set_CS_B_DEL_ER_VCM13_SIGN)
    CS_B_DEL_ER_VCM13 = property(get_CS_B_DEL_ER_VCM13, set_CS_B_DEL_ER_VCM13)
    CS_B_DEL_ER_VCM14_SIGN = property(get_CS_B_DEL_ER_VCM14_SIGN, set_CS_B_DEL_ER_VCM14_SIGN)
    CS_B_DEL_ER_VCM14 = property(get_CS_B_DEL_ER_VCM14, set_CS_B_DEL_ER_VCM14)
    CS_B_DEL_ER_VCM15_SIGN = property(get_CS_B_DEL_ER_VCM15_SIGN, set_CS_B_DEL_ER_VCM15_SIGN)
    CS_B_DEL_ER_VCM15 = property(get_CS_B_DEL_ER_VCM15, set_CS_B_DEL_ER_VCM15)
    CS_B_DEL_ER_VCM16_SIGN = property(get_CS_B_DEL_ER_VCM16_SIGN, set_CS_B_DEL_ER_VCM16_SIGN)
    CS_B_DEL_ER_VCM16 = property(get_CS_B_DEL_ER_VCM16, set_CS_B_DEL_ER_VCM16)
    CS_B_DEL_ER_VCM17_SIGN = property(get_CS_B_DEL_ER_VCM17_SIGN, set_CS_B_DEL_ER_VCM17_SIGN)
    CS_B_DEL_ER_VCM17 = property(get_CS_B_DEL_ER_VCM17, set_CS_B_DEL_ER_VCM17)
    CS_B_DEL_ER_VCM18_SIGN = property(get_CS_B_DEL_ER_VCM18_SIGN, set_CS_B_DEL_ER_VCM18_SIGN)
    CS_B_DEL_ER_VCM18 = property(get_CS_B_DEL_ER_VCM18, set_CS_B_DEL_ER_VCM18)
    CS_B_DEL_ER_VCM19_SIGN = property(get_CS_B_DEL_ER_VCM19_SIGN, set_CS_B_DEL_ER_VCM19_SIGN)
    CS_B_DEL_ER_VCM19 = property(get_CS_B_DEL_ER_VCM19, set_CS_B_DEL_ER_VCM19)
    CMD_STATUS = property(get_CMD_STATUS, set_CMD_STATUS)
    RSVD_7_2_EEPROM_CFG = property(get_RSVD_7_2_EEPROM_CFG, set_RSVD_7_2_EEPROM_CFG)
    E2P_FAST_MODE = property(get_E2P_FAST_MODE, set_E2P_FAST_MODE)
    ECC_DIS = property(get_ECC_DIS, set_ECC_DIS)
    KEY_STATUS = property(get_KEY_STATUS, set_KEY_STATUS)
    TRIM_DIS = property(get_TRIM_DIS, set_TRIM_DIS)
    OSC_CLK_DIS = property(get_OSC_CLK_DIS, set_OSC_CLK_DIS)
    ADC_TEST = property(get_ADC_TEST, set_ADC_TEST)
    OSC_TEST_ENABLE = property(get_OSC_TEST_ENABLE, set_OSC_TEST_ENABLE)
    TRACE_PORT = property(get_TRACE_PORT, set_TRACE_PORT)
    OSC_CLK_EXT = property(get_OSC_CLK_EXT, set_OSC_CLK_EXT)
    IO_TEST = property(get_IO_TEST, set_IO_TEST)
    SCAN_TEST = property(get_SCAN_TEST, set_SCAN_TEST)
    RSVD_7_5_ADC_TEST_CNTL = property(get_RSVD_7_5_ADC_TEST_CNTL, set_RSVD_7_5_ADC_TEST_CNTL)
    ADC_VCM_EN_SEL = property(get_ADC_VCM_EN_SEL, set_ADC_VCM_EN_SEL)
    ADC_CAL_TM_EN = property(get_ADC_CAL_TM_EN, set_ADC_CAL_TM_EN)
    ADC_CAL_OFFSET_EN = property(get_ADC_CAL_OFFSET_EN, set_ADC_CAL_OFFSET_EN)
    ADC_LDO_EN = property(get_ADC_LDO_EN, set_ADC_LDO_EN)
    ADC_VCM_EN = property(get_ADC_VCM_EN, set_ADC_VCM_EN)
    ATEST_CNTL0 = property(get_ATEST_CNTL0, set_ATEST_CNTL0)
    RSVD_7_ANA_DFT_CTRL = property(get_RSVD_7_ANA_DFT_CTRL, set_RSVD_7_ANA_DFT_CTRL)
    EN_BYPASS_ANA_DFT_BUF = property(get_EN_BYPASS_ANA_DFT_BUF, set_EN_BYPASS_ANA_DFT_BUF)
    EN_RES_LADDER_CALIB = property(get_EN_RES_LADDER_CALIB, set_EN_RES_LADDER_CALIB)
    RES_DIV_SEL = property(get_RES_DIV_SEL, set_RES_DIV_SEL)
    EN_RES_DIV = property(get_EN_RES_DIV, set_EN_RES_DIV)
    EN_DIRECT_PATH = property(get_EN_DIRECT_PATH, set_EN_DIRECT_PATH)
    EN_ANA_DFT_BUFFER = property(get_EN_ANA_DFT_BUFFER, set_EN_ANA_DFT_BUFFER)
    RSVD_7_4_ANA_DFT_MUX_CTRL = property(get_RSVD_7_4_ANA_DFT_MUX_CTRL, set_RSVD_7_4_ANA_DFT_MUX_CTRL)
    ANA_DFT_MUX_SEL = property(get_ANA_DFT_MUX_SEL, set_ANA_DFT_MUX_SEL)
    EN_ANA_DFT_MUX = property(get_EN_ANA_DFT_MUX, set_EN_ANA_DFT_MUX)
    RSVD_7_5_LDO_TRIM_VDDD = property(get_RSVD_7_5_LDO_TRIM_VDDD, set_RSVD_7_5_LDO_TRIM_VDDD)
    LDO_TRIM_VDDD_CURRENT_20MA = property(get_LDO_TRIM_VDDD_CURRENT_20MA, set_LDO_TRIM_VDDD_CURRENT_20MA)
    LDO_TRIM_VDDD_CURRENT_10MA = property(get_LDO_TRIM_VDDD_CURRENT_10MA, set_LDO_TRIM_VDDD_CURRENT_10MA)
    LDO_TRIM_VDDD_CURRENT_5MA = property(get_LDO_TRIM_VDDD_CURRENT_5MA, set_LDO_TRIM_VDDD_CURRENT_5MA)
    LDO_TRIM_VDDD_BOOST_1P9V = property(get_LDO_TRIM_VDDD_BOOST_1P9V, set_LDO_TRIM_VDDD_BOOST_1P9V)
    LDO_TRIM_VDDD_BOOST_1P85V = property(get_LDO_TRIM_VDDD_BOOST_1P85V, set_LDO_TRIM_VDDD_BOOST_1P85V)
    RSVD_7_5_LDO_TRIM_IOVDD = property(get_RSVD_7_5_LDO_TRIM_IOVDD, set_RSVD_7_5_LDO_TRIM_IOVDD)
    LDO_TRIM_IOVDD_CURRENT_20MA = property(get_LDO_TRIM_IOVDD_CURRENT_20MA, set_LDO_TRIM_IOVDD_CURRENT_20MA)
    LDO_TRIM_IOVDD_CURRENT_10MA = property(get_LDO_TRIM_IOVDD_CURRENT_10MA, set_LDO_TRIM_IOVDD_CURRENT_10MA)
    LDO_TRIM_IOVDD_CURRENT_5MA = property(get_LDO_TRIM_IOVDD_CURRENT_5MA, set_LDO_TRIM_IOVDD_CURRENT_5MA)
    LDO_TRIM_IOVDD_BOOST_1P9V = property(get_LDO_TRIM_IOVDD_BOOST_1P9V, set_LDO_TRIM_IOVDD_BOOST_1P9V)
    LDO_TRIM_IOVDD_BOOST_1P85V = property(get_LDO_TRIM_IOVDD_BOOST_1P85V, set_LDO_TRIM_IOVDD_BOOST_1P85V)
    ANATOP6 = property(get_ANATOP6, set_ANATOP6)
    ANATOP7 = property(get_ANATOP7, set_ANATOP7)
    ANATOP8 = property(get_ANATOP8, set_ANATOP8)
    ANATOP9 = property(get_ANATOP9, set_ANATOP9)
    RSVD_7_5_GPIO_TRACE = property(get_RSVD_7_5_GPIO_TRACE, set_RSVD_7_5_GPIO_TRACE)
    GPIO_TRACE = property(get_GPIO_TRACE, set_GPIO_TRACE)
    RSVD_7_1_ATEST_CNTL1 = property(get_RSVD_7_1_ATEST_CNTL1, set_RSVD_7_1_ATEST_CNTL1)
    SPIKE_FILTER_TEST_MODE = property(get_SPIKE_FILTER_TEST_MODE, set_SPIKE_FILTER_TEST_MODE)
    POR_BYPASS_L = property(get_POR_BYPASS_L, set_POR_BYPASS_L)
    POR_BYPASS_H = property(get_POR_BYPASS_H, set_POR_BYPASS_H)
    CLK_CNT_CMP_L = property(get_CLK_CNT_CMP_L, set_CLK_CNT_CMP_L)
    RSVD_7_4_OSC_CNT_CMP_H = property(get_RSVD_7_4_OSC_CNT_CMP_H, set_RSVD_7_4_OSC_CNT_CMP_H)
    CLK_CNT_CMP_H = property(get_CLK_CNT_CMP_H, set_CLK_CNT_CMP_H)
    CLK_COUNT_L = property(get_CLK_COUNT_L, set_CLK_COUNT_L)
    RSVD_7_4_OSC_CNT_H = property(get_RSVD_7_4_OSC_CNT_H, set_RSVD_7_4_OSC_CNT_H)
    CLK_COUNT_H = property(get_CLK_COUNT_H, set_CLK_COUNT_H)
    OSC_TRIM_TEST = property(get_OSC_TRIM_TEST, set_OSC_TRIM_TEST)
    RSVD_7_2_OSC_CMP_HYST = property(get_RSVD_7_2_OSC_CMP_HYST, set_RSVD_7_2_OSC_CMP_HYST)
    CMP_HYST = property(get_CMP_HYST, set_CMP_HYST)
    DAC_CLAMP_DIS = property(get_DAC_CLAMP_DIS, set_DAC_CLAMP_DIS)
    RSVD_6_DAC_TEST_CNTL = property(get_RSVD_6_DAC_TEST_CNTL, set_RSVD_6_DAC_TEST_CNTL)
    DAC_HIZ_GROUP_B = property(get_DAC_HIZ_GROUP_B, set_DAC_HIZ_GROUP_B)
    DAC_HIZ_GROUP_A = property(get_DAC_HIZ_GROUP_A, set_DAC_HIZ_GROUP_A)
    RSVD_3_0_DAC_TEST_CNTL = property(get_RSVD_3_0_DAC_TEST_CNTL, set_RSVD_3_0_DAC_TEST_CNTL)
    RSVD_7_2_GPIO_IN = property(get_RSVD_7_2_GPIO_IN, set_RSVD_7_2_GPIO_IN)
    OUT_BEN_IN = property(get_OUT_BEN_IN, set_OUT_BEN_IN)
    OUT_AEN_IN = property(get_OUT_AEN_IN, set_OUT_AEN_IN)
    RSVD_7_2_GPIO_OUT = property(get_RSVD_7_2_GPIO_OUT, set_RSVD_7_2_GPIO_OUT)
    OUT_BEN_OUT = property(get_OUT_BEN_OUT, set_OUT_BEN_OUT)
    RSVD_0_GPIO_OUT = property(get_RSVD_0_GPIO_OUT, set_RSVD_0_GPIO_OUT)
    RSVD_7_3_GPIO_OEB = property(get_RSVD_7_3_GPIO_OEB, set_RSVD_7_3_GPIO_OEB)
    DAC_OUT_OK_OEB = property(get_DAC_OUT_OK_OEB, set_DAC_OUT_OK_OEB)
    OUT_BEN_OEB = property(get_OUT_BEN_OEB, set_OUT_BEN_OEB)
    RSVD_0_GPIO_OEB = property(get_RSVD_0_GPIO_OEB, set_RSVD_0_GPIO_OEB)
    RSVD_7_GPIO_IEB = property(get_RSVD_7_GPIO_IEB, set_RSVD_7_GPIO_IEB)
    DAC_OUT_OK_IEB = property(get_DAC_OUT_OK_IEB, set_DAC_OUT_OK_IEB)
    SDO_IEB = property(get_SDO_IEB, set_SDO_IEB)
    SDI_IEB = property(get_SDI_IEB, set_SDI_IEB)
    CSB_IEB = property(get_CSB_IEB, set_CSB_IEB)
    SCLK_IEB = property(get_SCLK_IEB, set_SCLK_IEB)
    OUT_BEN_IEB = property(get_OUT_BEN_IEB, set_OUT_BEN_IEB)
    OUT_AEN_IEB = property(get_OUT_AEN_IEB, set_OUT_AEN_IEB)
    I2C_SPIKE_OK = property(get_I2C_SPIKE_OK, set_I2C_SPIKE_OK)
    RSVD_6_COMP_STATUS = property(get_RSVD_6_COMP_STATUS, set_RSVD_6_COMP_STATUS)
    I3C_1P8V_MODE = property(get_I3C_1P8V_MODE, set_I3C_1P8V_MODE)
    SPI_I3C_SEL = property(get_SPI_I3C_SEL, set_SPI_I3C_SEL)
    A1_COMP2 = property(get_A1_COMP2, set_A1_COMP2)
    A1_COMP1 = property(get_A1_COMP1, set_A1_COMP1)
    A0_COMP2 = property(get_A0_COMP2, set_A0_COMP2)
    A0_COMP1 = property(get_A0_COMP1, set_A0_COMP1)
    DIFF10_OVRD_L = property(get_DIFF10_OVRD_L, set_DIFF10_OVRD_L)
    RSVD_7_5_CS_DIFF10_OVRD_H = property(get_RSVD_7_5_CS_DIFF10_OVRD_H, set_RSVD_7_5_CS_DIFF10_OVRD_H)
    CS_DIFF10_OVRD_H_SIGN = property(get_CS_DIFF10_OVRD_H_SIGN, set_CS_DIFF10_OVRD_H_SIGN)
    DIFF10_OVRD_H = property(get_DIFF10_OVRD_H, set_DIFF10_OVRD_H)
    VCM_OVRD_L = property(get_VCM_OVRD_L, set_VCM_OVRD_L)
    RSVD_7_4_CS_VCM_OVRD_H = property(get_RSVD_7_4_CS_VCM_OVRD_H, set_RSVD_7_4_CS_VCM_OVRD_H)
    VCM_OVRD_H = property(get_VCM_OVRD_H, set_VCM_OVRD_H)
    CS_B_DTEST_EN = property(get_CS_B_DTEST_EN, set_CS_B_DTEST_EN)
    CS_B_DTEST_CTRL = property(get_CS_B_DTEST_CTRL, set_CS_B_DTEST_CTRL)
    CS_A_DTEST_EN = property(get_CS_A_DTEST_EN, set_CS_A_DTEST_EN)
    CS_A_DTEST_CTRL = property(get_CS_A_DTEST_CTRL, set_CS_A_DTEST_CTRL)
    RSVD_7_4_ADC_CTRL_SIG = property(get_RSVD_7_4_ADC_CTRL_SIG, set_RSVD_7_4_ADC_CTRL_SIG)
    ADC_CAL_START = property(get_ADC_CAL_START, set_ADC_CAL_START)
    ADC_SAMPLE = property(get_ADC_SAMPLE, set_ADC_SAMPLE)
    ADC_SOC = property(get_ADC_SOC, set_ADC_SOC)
    ADC_RESETB = property(get_ADC_RESETB, set_ADC_RESETB)
    CS_VCM_OC = property(get_CS_VCM_OC, set_CS_VCM_OC)
    CS_VCM_OCH = property(get_CS_VCM_OCH, set_CS_VCM_OCH)
    CS_VCM_UPDATE = property(get_CS_VCM_UPDATE, set_CS_VCM_UPDATE)
    CS_CAL_MODE = property(get_CS_CAL_MODE, set_CS_CAL_MODE)
    CS_PHASE_CTRL = property(get_CS_PHASE_CTRL, set_CS_PHASE_CTRL)
    CS_MUX_SEL = property(get_CS_MUX_SEL, set_CS_MUX_SEL)
    ADC_DATA_L = property(get_ADC_DATA_L, set_ADC_DATA_L)
    ADC_EOC = property(get_ADC_EOC, set_ADC_EOC)
    RSVD_6_4_ADC_DATA_H = property(get_RSVD_6_4_ADC_DATA_H, set_RSVD_6_4_ADC_DATA_H)
    ADC_DATA_H = property(get_ADC_DATA_H, set_ADC_DATA_H)
    VCM_L = property(get_VCM_L, set_VCM_L)
    RSVD_7_4_CS_VCM_H = property(get_RSVD_7_4_CS_VCM_H, set_RSVD_7_4_CS_VCM_H)
    VCM_H = property(get_VCM_H, set_VCM_H)
    DAC_MID_L = property(get_DAC_MID_L, set_DAC_MID_L)
    RSVD_7_4_CS_DAC_MID_H = property(get_RSVD_7_4_CS_DAC_MID_H, set_RSVD_7_4_CS_DAC_MID_H)
    DAC_MID_H = property(get_DAC_MID_H, set_DAC_MID_H)
    SENSE_P_DAC_L = property(get_SENSE_P_DAC_L, set_SENSE_P_DAC_L)
    RSVD_7_4_CS_SENSE_P_DAC_H = property(get_RSVD_7_4_CS_SENSE_P_DAC_H, set_RSVD_7_4_CS_SENSE_P_DAC_H)
    SENSE_P_DAC_H = property(get_SENSE_P_DAC_H, set_SENSE_P_DAC_H)
    SENSE_N_DAC_L = property(get_SENSE_N_DAC_L, set_SENSE_N_DAC_L)
    RSVD_7_4_CS_SENSE_N_DAC_H = property(get_RSVD_7_4_CS_SENSE_N_DAC_H, set_RSVD_7_4_CS_SENSE_N_DAC_H)
    SENSE_N_DAC_H = property(get_SENSE_N_DAC_H, set_SENSE_N_DAC_H)
    DAC_SHIFT_L = property(get_DAC_SHIFT_L, set_DAC_SHIFT_L)
    RSVD_7_2_CS_DAC_SHIFT_H = property(get_RSVD_7_2_CS_DAC_SHIFT_H, set_RSVD_7_2_CS_DAC_SHIFT_H)
    CS_DAC_SHIFT_H_SIGN = property(get_CS_DAC_SHIFT_H_SIGN, set_CS_DAC_SHIFT_H_SIGN)
    DAC_SHIFT_H = property(get_DAC_SHIFT_H, set_DAC_SHIFT_H)
    DAC_SHIFT_COR_L = property(get_DAC_SHIFT_COR_L, set_DAC_SHIFT_COR_L)
    RSVD_7_2_CS_DAC_SHIFT_COR_H = property(get_RSVD_7_2_CS_DAC_SHIFT_COR_H, set_RSVD_7_2_CS_DAC_SHIFT_COR_H)
    CS_DAC_SHIFT_COR_H_SIGN = property(get_CS_DAC_SHIFT_COR_H_SIGN, set_CS_DAC_SHIFT_COR_H_SIGN)
    DAC_SHIFT_COR_H = property(get_DAC_SHIFT_COR_H, set_DAC_SHIFT_COR_H)
    RSVD_7_CS_DAC_CODE = property(get_RSVD_7_CS_DAC_CODE, set_RSVD_7_CS_DAC_CODE)
    CS_DAC_CODE = property(get_CS_DAC_CODE, set_CS_DAC_CODE)
    SENSE_P10_L = property(get_SENSE_P10_L, set_SENSE_P10_L)
    RSVD_7_4_CS_SENSE_P10_H = property(get_RSVD_7_4_CS_SENSE_P10_H, set_RSVD_7_4_CS_SENSE_P10_H)
    SENSE_P10_H = property(get_SENSE_P10_H, set_SENSE_P10_H)
    SENSE_N10_L = property(get_SENSE_N10_L, set_SENSE_N10_L)
    RSVD_7_4_CS_SENSE_N10_H = property(get_RSVD_7_4_CS_SENSE_N10_H, set_RSVD_7_4_CS_SENSE_N10_H)
    SENSE_N10_H = property(get_SENSE_N10_H, set_SENSE_N10_H)
    DIFF10_L = property(get_DIFF10_L, set_DIFF10_L)
    RSVD_7_5_CS_DIFF10_H = property(get_RSVD_7_5_CS_DIFF10_H, set_RSVD_7_5_CS_DIFF10_H)
    CS_DIFF10_H_SIGN = property(get_CS_DIFF10_H_SIGN, set_CS_DIFF10_H_SIGN)
    DIFF10_H = property(get_DIFF10_H, set_DIFF10_H)
    CAL_ER_L = property(get_CAL_ER_L, set_CAL_ER_L)
    RSVD_7_5_CS_CAL_ER_H = property(get_RSVD_7_5_CS_CAL_ER_H, set_RSVD_7_5_CS_CAL_ER_H)
    CS_CAL_ER_H_SIGN = property(get_CS_CAL_ER_H_SIGN, set_CS_CAL_ER_H_SIGN)
    CAL_ER_H = property(get_CAL_ER_H, set_CAL_ER_H)
    CAL_DIFF10_L = property(get_CAL_DIFF10_L, set_CAL_DIFF10_L)
    RSVD_7_5_CS_CAL_DIFF10_H = property(get_RSVD_7_5_CS_CAL_DIFF10_H, set_RSVD_7_5_CS_CAL_DIFF10_H)
    CS_CAL_DIFF10_H_SIGN = property(get_CS_CAL_DIFF10_H_SIGN, set_CS_CAL_DIFF10_H_SIGN)
    CAL_DIFF10_H = property(get_CAL_DIFF10_H, set_CAL_DIFF10_H)
    RSVD_7_6_CS_CAL_ER_LUTP = property(get_RSVD_7_6_CS_CAL_ER_LUTP, set_RSVD_7_6_CS_CAL_ER_LUTP)
    CAL_ER_LUTP = property(get_CAL_ER_LUTP, set_CAL_ER_LUTP)
    CAL_LUTS_L = property(get_CAL_LUTS_L, set_CAL_LUTS_L)
    RSVD_7_5_CS_CAL_LUTS_H = property(get_RSVD_7_5_CS_CAL_LUTS_H, set_RSVD_7_5_CS_CAL_LUTS_H)
    CS_CAL_LUTS_H_SIGN = property(get_CS_CAL_LUTS_H_SIGN, set_CS_CAL_LUTS_H_SIGN)
    CAL_LUTS_H = property(get_CAL_LUTS_H, set_CAL_LUTS_H)
    CS_CAL_ER_FRAC_SIGN = property(get_CS_CAL_ER_FRAC_SIGN, set_CS_CAL_ER_FRAC_SIGN)
    CAL_ER_FRAC = property(get_CAL_ER_FRAC, set_CAL_ER_FRAC)
    GAIN_ER_L = property(get_GAIN_ER_L, set_GAIN_ER_L)
    RSVD_7_1_CS_GAIN_ER_H = property(get_RSVD_7_1_CS_GAIN_ER_H, set_RSVD_7_1_CS_GAIN_ER_H)
    CS_GAIN_ER_H_SIGN = property(get_CS_GAIN_ER_H_SIGN, set_CS_GAIN_ER_H_SIGN)
