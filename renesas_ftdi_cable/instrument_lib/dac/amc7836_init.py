from instrument_lib.dac.amc7836 import Amc7836


class Amc7836Init:
    @staticmethod
    def init(serial_number: str = None):
        print('Attempting to open DUT with FTDI SPI communication.')
        amc_7836 = Amc7836(serial_number=serial_number)
        success = amc_7836.open()
        if not success:
            print(
                'Hardware open was not successful.  Check the device if I3C - bus arbitration may not have completed.')
            exit()

        chip_type = amc_7836.read_register(amc_7836.REGISTER_ADDRESSES['CHIP_TYPE'], 1)
        print("Chip Type 0x%02X" % chip_type)

        chip_id = amc_7836.read_register(amc_7836.REGISTER_ADDRESSES['CHIP_ID_LO'], 2)
        print("Chip ID 0x%04X" % ((chip_id[1] << 8) + chip_id[0]))

        mfgr_id = amc_7836.read_register(amc_7836.REGISTER_ADDRESSES['MFGR_ID_LO'], 2)
        print("Manufacturer ID 0x%04X" % ((mfgr_id[1] << 8) + mfgr_id[0]))

        chip_version = amc_7836.read_register(amc_7836.REGISTER_ADDRESSES['CHIP_VERSION'], 1)
        print("Chip Version 0x%02X" % chip_version)

        return amc_7836
