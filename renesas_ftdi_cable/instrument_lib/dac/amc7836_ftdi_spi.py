from enum import IntEnum

from instrument_lib.dac.ftdi_base import FTDI_BUS
from instrument_lib.dac.ftdi_base import FTDI_DIRECTION
from instrument_lib.dac.ftdi_spi import FtdiSpi


class ADDRESS_MODE(IntEnum):
    ONE_BYTE = 0
    TWO_BYTE = 1


class Amc7836FtdiSpi:
    """
    classdocs
    """

    def __init__(self,
                 serial_number: str = None,
                 readback: bool = False,
                 auto_open=False):
        """
        Constructor
        """
        self.clock_frequency_mhz = 1
        self._is_open = False
        self.READBACK_EVERY_WRITE = readback

        self._define_constants()
        self._define_ftdi_pin_assignments_and_defaults()

        if serial_number is None:

            # Start MPSSE and instantiate parent class settings
            self.mpsse = FtdiSpi(description="DUAL RS232-HS A")

            # Start MPSSE for Level Shifter and instantiate parent class settings
            self.mpsse_lev_shift = FtdiSpi(description="DUAL RS232-HS B")

        else:
            print("Attempting to open specific FTDI serial number %s" % serial_number)
            if len(serial_number) == 8:
                serial_num_port_a = serial_number + "A"
                serial_num_lev_shift = serial_number + "B"
            elif len(serial_number) == 9:
                serial_num_port_a = serial_number
                # Change the "A" to a "B" at the end of the SN
                serial_num_lev_shift = serial_number[0:len(serial_number) - 1] + "B"
            else:
                raise Exception('AMC7834:InvalidArgument', 'Invalid Serial Number String length')

            self.mpsse = FtdiSpi(desired_serial=serial_num_port_a)

            # Start MPSSE for Level Shifter and instantiate parent class settings
            self.mpsse_lev_shift = FtdiSpi(desired_serial=serial_num_lev_shift)

        if auto_open:
            self.open()

    def _define_constants(self):
        """
        Private method used to set the constants used in the class

        """

        self._MIN_REGISTER_VALUE = 0
        self._MAX_REGISTER_VALUE = 0xFF

        self._MIN_REGISTER_ADDRESS = 0
        self._MAX_REGISTER_ADDRESS = 0x7FFF

        self._REGISTER_BIT_SIZE = 0x8

        self._LOW = 0
        self._HIGH = 1

        self.WRITE = 1 << 7  # Write bit in the serial word
        self.READ = 0  # Read bit in the serial word
        self.RW = (0x1 << 7)

        self._DIRECTION_OUTPUT = 1
        self._DIRECTION_INPUT = 0

    def open(self) -> bool:
        """

        """

        self.mpsse.open()

        self.mpsse_lev_shift.open()

        # Set the default GPIO's for the low byte
        self.mpsse.set_port_d_low_byte_value(self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE,
                                             self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR)
        self.mpsse_lev_shift.set_port_d_low_byte_value(self._DEFAULT_FT_MPSSE_LEV_SHIFT_LOW_BUS_IDLE_VALUE,
                                                       self._DEFAULT_FT_MPSSE_LEV_SHIFT_LOW_BUS_IDLE_DIR)

        # Set the default GPIO's for the high byte
        self.mpsse.set_port_c_high_byte_value(self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE,
                                              self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR)
        self.mpsse_lev_shift.set_port_c_high_byte_value(self._DEFAULT_FT_MPSSE_LEV_SHIFT_HIGH_BUS_IDLE_VALUE,
                                                        self._DEFAULT_FT_MPSSE_LEV_SHIFT_HIGH_BUS_IDLE_DIR)

        self.mpsse.set_clock_frequency_mhz(self.clock_frequency_mhz)

        self.mpsse_lev_shift.set_clock_frequency_mhz(self.clock_frequency_mhz)

        self._is_open = True

        return True

    def close(self):
        """

        """
        if self._is_open:
            self.mpsse.close()
            self.mpsse_lev_shift.close()

    def _define_ftdi_pin_assignments_and_defaults(self):
        """
        Define the class private FTDI constants - this is called by the constructor.
        """

        self._SPI_CLK_DEFAULT = self._LOW
        self._SPI_CLK_BIT_NUMBER = 0

        self._SPI_MOSI_DEFAULT = self._LOW
        self._SPI_MOSI_BIT_NUMBER = 1

        self._SPI_MISO_DEFAULT = self._LOW
        self._SPI_MISO_BIT_NUMBER = 2

        self._SPI_CS0_DEFAULT = self._HIGH
        self._SPI_CS0_BIT_NUMBER = 3

        # Definitions for AMC7834 Rev A Board
        self._DAC_OUT_OK_DEFAULT = self._LOW
        self._DAC_OUT_OK_BIT_NUMBER = 4
        self._DAC_OUT_OK_GPIO_BUS = FTDI_BUS.AD_BUS
        self._DAC_OUT_OK_GPIO_DIR = FTDI_DIRECTION.INPUT

        # Definitions for AMC7834 Rev A Board
        self._ALARM_IN_B_DEFAULT = self._LOW
        self._ALARM_IN_B_BIT_NUMBER = 4
        self._ALARM_IN_B_GPIO_BUS = FTDI_BUS.AC_BUS
        self._ALARM_IN_B_DIR = FTDI_DIRECTION.OUTPUT

        self._ADC_TRIG_B_DEFAULT = self._LOW
        self._ADC_TRIG_B_GPIO_BUS = FTDI_BUS.AC_BUS
        self._ADC_TRIG_B_BIT_NUMBER = 0
        self._ADC_TRIG_B_DIR = FTDI_DIRECTION.OUTPUT

        self._DAV_DEFAULT = self._LOW
        self._DAV_B_GPIO_BUS = FTDI_BUS.AC_BUS
        self._DAV_B_BIT_NUMBER = 7
        self._DAV_B_DIR = FTDI_DIRECTION.INPUT

        # Definitions for All boards

        # I2C PULLUP_EN PIN: Bit 7 / 0x80 / Pin J3-1 / AC7
        # SPI Operation: 1
        # I3C Operation: 0      
        self._I2C_PULLUP_EN_GPIO_BIT_NUMBER = 7
        self._I2C_PULLUP_EN_GPIO_BUS = FTDI_BUS.AC_BUS
        self._I2C_PULLUP_EN_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._I2C_PULLUP_EN_GPIO_DEFAULT = self._HIGH

        # OUT_B_EN PIN: Bit 6 / 0x40 / Pin J3-2 / AC6
        # Operation: 1 to enable output
        # Operation: 0 to disable output
        self._OUT_B_EN_GPIO_BIT_NUMBER = 6
        self._OUT_B_EN_GPIO_BUS = FTDI_BUS.AC_BUS
        self._OUT_B_EN_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._OUT_B_EN_GPIO_DEFAULT = self._LOW

        # A0_FTDI: Bit 5 / 0x20 / Pin J3-4 / AC5
        # Operation: 
        self._A0_FTDI_GPIO_BIT_NUMBER = 5
        self._A0_FTDI_GPIO_BUS = FTDI_BUS.AC_BUS
        self._A0_FTDI_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._A0_FTDI_GPIO_DEFAULT = self._LOW

        # OUT A EN: Bit 4 / 0x10 / Pin J3-8 / AC4
        # Operation: 1 to enter IDLE state
        # Operation: 0 to exit IDLE state and begin sampling and conversion of the ADC
        self._OUT_A_EN_GPIO_BIT_NUMBER = 4
        self._OUT_A_EN_GPIO_BUS = FTDI_BUS.AC_BUS
        self._OUT_A_EN_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._OUT_A_EN_GPIO_DEFAULT = self._LOW

        # #I3C_SDA_EN: Bit 3 / 0x8 / Pin J3-5 / AC3
        # I3C Operation: 1 to READ
        # I3C Operation: 0 to WRITE
        # SPI Operation: 1 to TRI_STATE
        self._I3C_SDA_EN_GPIO_BIT_NUMBER = 3
        self._I3C_SDA_EN_GPIO_BUS = FTDI_BUS.AC_BUS
        self._I3C_SDA_EN_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._I3C_SDA_EN_GPIO_DEFAULT = self._HIGH

        # GPIO nRESET PIN: Bit 2 / 0x4 / Pin J3-6 / AC2
        # Operation: 1 to use the chip
        # RESET 0 to reset the chip
        self._nRESET_GPIO_BIT_NUMBER = 2
        self._nRESET_GPIO_BUS = FTDI_BUS.AC_BUS
        self._nRESET_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._nRESET_GPIO_DEFAULT = self._HIGH

        # SPI_MOSI_EN: Bit 1 / 0x2 / Pin J3-7 / AC1
        # SPI Operation: LOW
        # I3C Operation: HIGH
        self._SPI_MOSI_EN_GPIO_BIT_NUMBER = 1
        self._SPI_MOSI_EN_GPIO_BUS = FTDI_BUS.AC_BUS
        self._SPI_MOSI_EN_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._SPI_MOSI_EN_GPIO_DEFAULT = self._LOW

        # _CM_A2 PIN: Bit 0 / 0x01 / Pin J3-2 / AC0
        # Operation: 1 to enable output
        # Operation: 0 to disable output
        self._CM_A2_GPIO_BIT_NUMBER = 0
        self._CM_A2_GPIO_BUS = FTDI_BUS.AC_BUS
        self._CM_A2_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._CM_A2_GPIO_DEFAULT = self._LOW

        # F1590 Separated CM and A2 Pins

        # _CM PIN: Bit 5 / 0x20 / Pin J4-2 / AD5
        # Operation: 1 to enable output
        # Operation: 0 to disable output
        self._CM_GPIO_BIT_NUMBER = 5
        self._CM_GPIO_BUS = FTDI_BUS.AD_BUS
        self._CM_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._CM_GPIO_DEFAULT = self._LOW

        # _A2 PIN: Bit 0 / 0x01 / Pin J3-2 / AC0
        # Operation: 1 to enable output
        # Operation: 0 to disable output
        self._A2_GPIO_BIT_NUMBER = 0
        self._A2_GPIO_BUS = FTDI_BUS.AC_BUS
        self._A2_GPIO_DIR = FTDI_DIRECTION.OUTPUT
        self._A2_GPIO_DEFAULT = self._LOW

        # 0x0001 = AD0 = J3-16 = CLK
        # 0x0002 = AD1 = J3-18 = MOSI
        # 0x0004 = AD2 = J3-14 = MISO
        # 0x0008 = AD3 = J3-12 = CSB0
        # 0x0010 = AD4 = J4-1 = DAC_OUT_OK
        # 0x0020 = AD5 = J4-2 = N/C
        # 0x0040 = AD6 = J4-3 = N/C
        # 0x0080 = AD7 = J4-4 = N/C
        # 0x0100 = AC0 = J3-8 = CM_A2
        # 0x0200 = AC1 = J3-7 = SPI_MOSI_OUT_EN
        # 0x0400 = AC2 = J3-6 = nReset
        # 0x0800 = AC3 = J3-5 = I3C_SDA_OUT_EN
        # 0x1000 = AC4 = J3-4 = OUT_A_EN
        # 0x2000 = AC5 = J3-3 = A0_FTDI
        # 0x4000 = AC6 = J3-2 = OUT_B_EN 
        # 0x8000 = AC7 = J3-1 = #I2C_PULLUP_EN

        # Initialize the values with a 0 for bit manipulation
        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = 0
        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = 0
        self._DEFAULT_FT_MPSSE_LEV_SHIFT_LOW_BUS_IDLE_VALUE = 0
        # Level shifter direction is always output.  Value determines direction.
        self._DEFAULT_FT_MPSSE_LEV_SHIFT_LOW_BUS_IDLE_DIR = 0xFF

        self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = 0
        self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = 0

        self._DEFAULT_FT_MPSSE_LEV_SHIFT_HIGH_BUS_IDLE_VALUE = 0
        # Level shifter direction is always output.  Value determines direction. 
        self._DEFAULT_FT_MPSSE_LEV_SHIFT_HIGH_BUS_IDLE_DIR = 0xFF

        # Calculate AD Bus SPI values - direction is not configurable
        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                (2 ** self._SPI_CLK_BIT_NUMBER) * self._SPI_CLK_DEFAULT)  # AD0 = CLK = LOW - OUTPUT
        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                (2 ** self._SPI_CLK_BIT_NUMBER) * self._DIRECTION_OUTPUT)

        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                (2 ** self._SPI_MOSI_BIT_NUMBER) * self._SPI_MOSI_DEFAULT)  # AD1 = MOSI = LOW, - OUTPUT
        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                (2 ** self._SPI_MOSI_BIT_NUMBER) * self._DIRECTION_OUTPUT)

        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                (2 ** self._SPI_MISO_BIT_NUMBER) * self._SPI_MISO_DEFAULT)  # AD2 = MISO = LOW - INPUT
        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                (2 ** self._SPI_MISO_BIT_NUMBER) * self._DIRECTION_INPUT)

        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                (2 ** self._SPI_CS0_BIT_NUMBER) * self._SPI_CS0_DEFAULT)  # AD3 = CS0 = HIGH - OUTPUT
        self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                (2 ** self._SPI_CS0_BIT_NUMBER) * self._DIRECTION_OUTPUT)

        # I2C PULLUP_EN PIN: Bit 7 / 0x80 / Pin J3-1 / AC7
        # SPI Operation: 1
        # I3C Operation: 0
        if self._I2C_PULLUP_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._I2C_PULLUP_EN_GPIO_BIT_NUMBER) * self._I2C_PULLUP_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._I2C_PULLUP_EN_GPIO_BIT_NUMBER) * self._I2C_PULLUP_EN_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._I2C_PULLUP_EN_GPIO_BIT_NUMBER) * self._I2C_PULLUP_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._I2C_PULLUP_EN_GPIO_BIT_NUMBER) * self._I2C_PULLUP_EN_GPIO_DIR)

        # OUT_B_EN PIN: Bit 6 / 0x40 / Pin J3-2 / AC6
        # Operation: 1 to enable output
        # Operation: 0 to disable output
        if self._OUT_B_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._OUT_B_EN_GPIO_BIT_NUMBER) * self._OUT_B_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._OUT_B_EN_GPIO_BIT_NUMBER) * self._OUT_B_EN_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._OUT_B_EN_GPIO_BIT_NUMBER) * self._OUT_B_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._OUT_B_EN_GPIO_BIT_NUMBER) * self._OUT_B_EN_GPIO_DIR)

        # A0_FTDI: Bit 5 / 0x20 / Pin J3-4 / AC5
        # Operation:       
        if self._A0_FTDI_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._A0_FTDI_GPIO_BIT_NUMBER) * self._A0_FTDI_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._A0_FTDI_GPIO_BIT_NUMBER) * self._A0_FTDI_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._A0_FTDI_GPIO_BIT_NUMBER) * self._A0_FTDI_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._A0_FTDI_GPIO_BIT_NUMBER) * self._A0_FTDI_GPIO_DIR)

        # GPIO ADC_TRIG_B PIN: Bit 0 / 0x1 / Pin J3-8 / AC0
        # Operation: 1 to enter IDLE state
        # Operation: 0 to exit IDLE state and begin sampling and conversion of the ADC
        if self._OUT_A_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._OUT_A_EN_GPIO_BIT_NUMBER) * self._OUT_A_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._OUT_A_EN_GPIO_BIT_NUMBER) * self._OUT_A_EN_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._OUT_A_EN_GPIO_BIT_NUMBER) * self._OUT_A_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._OUT_A_EN_GPIO_BIT_NUMBER) * self._OUT_A_EN_GPIO_DIR)

        # #I3C_SDA_EN: Bit 3 / 0x8 / Pin J3-5 / AC3
        # I3C Operation: 1 to READ
        # I3C Operation: 0 to WRITE
        # SPI Operation: 1 to TRI_STATE
        if self._I3C_SDA_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._I3C_SDA_EN_GPIO_BIT_NUMBER) * self._I3C_SDA_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._I3C_SDA_EN_GPIO_BIT_NUMBER) * self._I3C_SDA_EN_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._I3C_SDA_EN_GPIO_BIT_NUMBER) * self._I3C_SDA_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._I3C_SDA_EN_GPIO_BIT_NUMBER) * self._I3C_SDA_EN_GPIO_DIR)

        # GPIO nRESET PIN: Bit 2 / 0x4 / Pin J3-6 / AC2
        # Operation: 1 to use the chip
        # RESET 0 to reset the chip
        if self._nRESET_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._nRESET_GPIO_BIT_NUMBER) * self._nRESET_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._nRESET_GPIO_BIT_NUMBER) * self._nRESET_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._nRESET_GPIO_BIT_NUMBER) * self._nRESET_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._nRESET_GPIO_BIT_NUMBER) * self._nRESET_GPIO_DIR)

        # SPI_MOSI_EN: Bit 1 / 0x2 / Pin J3-7 / AC1
        # SPI Operation: LOW
        # I3C Operation: HIGH
        if self._SPI_MOSI_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._SPI_MOSI_EN_GPIO_BIT_NUMBER) * self._SPI_MOSI_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._SPI_MOSI_EN_GPIO_BIT_NUMBER) * self._SPI_MOSI_EN_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._SPI_MOSI_EN_GPIO_BIT_NUMBER) * self._SPI_MOSI_EN_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._SPI_MOSI_EN_GPIO_BIT_NUMBER) * self._SPI_MOSI_EN_GPIO_DIR)

        # _CM_A2 PIN: Bit 0 / 0x01 / Pin J3-2 / AC0
        # Operation: 1 to enable output
        # Operation: 0 to disable output
        if self._CM_A2_GPIO_BUS == FTDI_BUS.AD_BUS:
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_VALUE | (
                    (2 ** self._CM_A2_GPIO_BIT_NUMBER) * self._CM_A2_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR | (
                    (2 ** self._CM_A2_GPIO_BIT_NUMBER) * self._CM_A2_GPIO_DIR)
        else:
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_VALUE | (
                    (2 ** self._CM_A2_GPIO_BIT_NUMBER) * self._CM_A2_GPIO_DEFAULT)
            self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR | (
                    (2 ** self._CM_A2_GPIO_BIT_NUMBER) * self._CM_A2_GPIO_DIR)

        # The level shifter value is the same as the bus direction
        self._DEFAULT_FT_MPSSE_LEV_SHIFT_LOW_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_LOW_BUS_IDLE_DIR
        self._DEFAULT_FT_MPSSE_LEV_SHIFT_HIGH_BUS_IDLE_VALUE = self._DEFAULT_FT_MPSSE_HIGH_BUS_IDLE_DIR

    def set_i2c_pullup_line(self, state: bool):
        """
        Sets the F159x i2c pullup en pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self._is_open:
            if self._I2C_PULLUP_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._I2C_PULLUP_EN_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._I2C_PULLUP_EN_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def set_out_ben_line(self, state: bool):
        """
        Sets the F159x set out_ben line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self._is_open:
            if self._OUT_B_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._OUT_B_EN_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._OUT_B_EN_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def set_a0_ftdi_line(self, state: bool):
        """
        Sets the F159x set_A0_FTDI_line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self._is_open:
            if self._A0_FTDI_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._A0_FTDI_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._A0_FTDI_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def set_out_aen_line(self, state: bool):
        """
        Sets the F159x set_out_aen_line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self._is_open:
            if self._OUT_A_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._OUT_A_EN_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._OUT_A_EN_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def set_i3c_sda_en_line(self, state: bool):
        """
        Sets the F159x set_i3c_sda_en_line pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self._is_open:
            if self._I3C_SDA_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._I3C_SDA_EN_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._I3C_SDA_EN_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def set_nreset_line(self, state: bool):
        """
        Sets the F159x nRESET pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self._is_open:
            if self._nRESET_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._nRESET_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._nRESET_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def toggle_nreset_line(self):
        """
        Toggle the reset line LOW -> HIGH. 
        """
        if self._is_open:
            if self._nRESET_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(self._LOW, self._nRESET_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
                self.mpsse.set_port_d_low_byte_bit_value(self._HIGH, self._nRESET_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)

            else:
                self.mpsse.set_port_c_high_byte_bit_value(self._LOW, self._nRESET_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)
                self.mpsse.set_port_c_high_byte_bit_value(self._HIGH, self._nRESET_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def set_spi_mosi_en_line(self, state):
        """
        Sets the F159x set_spi_mosi_en pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """
        if self._is_open:
            if self._SPI_MOSI_EN_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._SPI_MOSI_EN_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._SPI_MOSI_EN_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    def set_cm_a2_line(self, state):
        """
        Sets the F159x CM/A2 pin to the specified state.

        :param state: True for high (1), False for low (0).
        :type state: bool
        """

        if self._is_open:
            if self._CM_A2_GPIO_BUS == FTDI_BUS.AD_BUS:
                self.mpsse.set_port_d_low_byte_bit_value(state, self._CM_A2_GPIO_BIT_NUMBER,
                                                         FTDI_DIRECTION.OUTPUT)
            else:
                self.mpsse.set_port_c_high_byte_bit_value(state, self._CM_A2_GPIO_BIT_NUMBER,
                                                          FTDI_DIRECTION.OUTPUT)

    # ################################################################
    # GET GPIO Functions
    # NOTE:  THESE CURRRENTLY ONLY READ BACK THE STATE OF THE OUTPUT PIN
    # ################################################################

    def set_clock_frequency_mhz(self, clock_frequency_mhz: float):

        self.clock_frequency_mhz = clock_frequency_mhz

        if self._is_open:
            self.mpsse.set_clock_frequency_mhz(self.clock_frequency_mhz)
            self.mpsse_lev_shift.set_clock_frequency_mhz(self.clock_frequency_mhz)

    def read_register(self, register_address: int, read_length: int = 1,
                      addr_mode: ADDRESS_MODE = ADDRESS_MODE.ONE_BYTE):  # @UnusedVariable    #pylint: disable=unused-argument
        """
        Creates the SPI word to perform a Local SPI Read:
        
        Appears that SPI always uses a 15 bit register.  Added for compatibility.

        24 Bits total
        1st Byte
        Write = 0
        (14:0 = Register Address)
        14:8, 7 bits Register Address        
            
        2nd Byte        
        7:0, 8 bits remaining Register Address 
            
        3rd Byte 
        8 bits data        

        :param register_address: 7-bit address of the register to read from.
        :type register_address: int
        :param read_length: 7-bit address of the register to read from.
        :type read_length: int
        :param addr_mode: Ignored, left to be compatible with the I2C / I3C Classes.
        :type addr_mode: ADDRESS_MODE
        
        """
        if self._is_open:

            if read_length < 1:
                raise Exception('amc7836_ftdi_spi.py: Invalid value argument', 'Register read_length must be > 1')

            # Create the register read command
            data_write_buffer = [0] * (2 + read_length)

            # 7:5 = SPI MODE, 4:0 = RESERVED 0
            data_write_buffer[0] = ((int(self.RW) & 0x80) | (int(register_address) & 0x7F00) >> 8)

            # 7:0 = Register Address
            data_write_buffer[1] = int(register_address) & 0xFF

            read_array = self.mpsse.write_with_readback(bytes(data_write_buffer))

            if read_length == 1:
                # The read returns 8 bits
                value = int(read_array[2])

            else:
                value = [0] * read_length
                for idx in range(0, read_length):
                    value[idx] = int(read_array[idx + 2])

            # Returns int for single read or list for multiple read
            return value

    def write_register(self, register_address: int, value,
                       addr_mode: ADDRESS_MODE = ADDRESS_MODE.ONE_BYTE):  # @UnusedVariable    #pylint: disable=unused-argument
        """
                
        Creates the SPI word to perform a Local SPI Write:

        Appears that SPI always uses a 15 bit register.  Added for compatibility.

        24 Bits total
        1st Byte
        Write = 0
        (7:0 = Register Address)
            
        2nd Byte        
        15:8, 8 bits data MSB 
            
        3rd Byte 
        7:0 bits data         

        :param register_address: 7-bit address of the register to write to.
        :type register_address: int
        :param value: 16-bit data value to program.
        :type value: int or list
        :param addr_mode: Ignored, left to be compatible with the I2C / I3C Classes.
        :type addr_mode: ADDRESS_MODE
        """

        if self._is_open:

            if type(value) is int:
                write_length = 1
            elif type(value) is list:
                write_length = len(value)
            else:
                raise Exception('amc7836_ftdi_spi.py: Invalid value argument', 'Register value must be an int or list')

            # Create register write command
            # Create the empty list at the correct length 
            data_write_buffer = [0] * (2 + write_length)

            # 8 = Read/Write Command, 14:8 = Register Address
            data_write_buffer[0] = ((int(self.RW) & 0x0) | (int(register_address) & 0x7F00) >> 8)

            # 7:0 = Register Address
            data_write_buffer[1] = int(register_address) & 0xFF

            if write_length == 1:
                # 7:0 = Register value [7:0]
                data_write_buffer[2] = value & 0xFF

            else:
                for i in range(0, write_length):
                    # 7:0 = Register value [7:0]
                    data_write_buffer[i + 2] = value[i] & 0xFF

            # Amount of times to retry write if fail
            retry_max = 5

            for retryCount in range(1, retry_max + 1):
                self.mpsse.write(bytes(data_write_buffer))

                if self.READBACK_EVERY_WRITE:
                    if write_length == 1:
                        read_back = self.read_register(register_address)
                        fail = False
                        if value != read_back:
                            print('amc7836_ftdi_spi.py: Register readback failure #{0}.'
                                  ' Addr=0x{1:04X} Value=0x{2:02X} Readback=0x{3:02X}'.format(retryCount,
                                                                                              register_address,
                                                                                              value, read_back))
                            read_back = self.read_register(register_address)
                            if value != read_back:
                                print('amc7836_ftdi_spi.py: Register readback failure #{0} (second'
                                      ' readback without writing).'.format(retryCount))
                                fail = True
                            # Break if second read works.
                            else:
                                break

                        # Break if doesn't fail readback
                        else:
                            break

                    # Multiple write readback
                    else:
                        read_back = self.read_register(register_address, write_length)
                        fail = False
                        for idx in range(0, write_length):
                            addr = register_address + idx
                            read_value = read_back[idx]

                            if not value[idx] == read_value:
                                print('amc7836_ftdi_spi.py: Register readback failure #{0}.'
                                      ' Addr0x={1:04X} Value=0x{2:02X} Readback0x={3:02X}'.format(retryCount,
                                                                                                  addr,
                                                                                                  value[idx],
                                                                                                  read_value))
                                fail = True

                        if not fail:
                            break

                # Break if not reading back every write
                else:
                    break

            if self.READBACK_EVERY_WRITE and fail:
                raise Exception('f159x:Register Verify Error', 'Register verify error.')
