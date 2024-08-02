from enum import IntEnum

from ftd2xx import defines

from instrument_lib.dac.ftdi_base import FTDI_BUS_MASK
from instrument_lib.dac.ftdi_base import FTDI_MPSSE_COMMANDS
from instrument_lib.dac.ftdi_base import FTDI_TRIGGER_MASK
from instrument_lib.dac.ftdi_base import FtdiBase


class SPI_READ_MODE(IntEnum):
    FOUR_WIRE = 0
    THREE_WIRE = 1
    THREE_WIRE_TO_FOUR_WITH_BUFFER = 2


class SPI_READ_BIT_STATE(IntEnum):
    FT_RD_ACTIVE_LOW = 0
    FT_RD_ACTIVE_HIGH = 1


class SPI_READ_BUFFER_BIT(IntEnum):
    FT_GPIO_BIT_0 = 0
    FT_GPIO_BIT_1 = 1
    FT_GPIO_BIT_2 = 2
    FT_GPIO_BIT_3 = 3
    FT_GPIO_BIT_4 = 4
    FT_GPIO_BIT_5 = 5
    FT_GPIO_BIT_6 = 6
    FT_GPIO_BIT_7 = 7


class FTDI_CS(IntEnum):
    CHIP_SELECT_AD3 = 0
    CHIP_SELECT_AD4 = 1
    CHIP_SELECT_AD5 = 2
    CHIP_SELECT_AD6 = 3
    CHIP_SELECT_AD7 = 4

    CHIP_SELECT_AC0 = 10
    CHIP_SELECT_AC1 = 11
    CHIP_SELECT_AC2 = 12
    CHIP_SELECT_AC3 = 13
    CHIP_SELECT_AC4 = 14
    CHIP_SELECT_AC5 = 15
    CHIP_SELECT_AC6 = 16
    CHIP_SELECT_AC7 = 17


class FtdiSpi(FtdiBase):
    # Properties
    # This is clock polarity = 0 and clock phase = 0
    # clock is normally low
    # data changes on negative clock pulses
    # ONLY SUPPORTS SPI MODES 0 and SPI MODE 2
    SPI_MODE = 0

    CHIP_SELECT_LOW_REPEAT_COUNT = 3
    CHIP_SELECT_HIGH_REPEAT_COUNT = 5

    # All Low but CS at idle state
    # AD0 = CLK = LOW, AD1 = MOSI = LOW, AD2 = INPUT, AD3-AD7 = CSn = HIGH
    FT_MPSSE_LOW_BUS_IDLE_VALUE = 0xF8

    # AD0 = CLK, AD1 = MOSI, AD2 = MISO, AD3 = CS
    FT_MPSSE_LOW_BUS_IDLE_DIR = 0xFB

    # GPIO's
    # All Low at idle state
    FT_MPSSE_HIGH_BUS_IDLE_VALUE = 0x0

    # Set all outputs
    FT_MPSSE_HIGH_BUS_IDLE_DIR = 0xFF

    # Clock Frequency
    clock_frequency_mhz = 1.0

    # Nothing currently needed in the child class constructor, so allow the base class to be called     
    # def __init__(self, description:str="DUAL RS232-HS A",
    #             #deviceType:str="DEVICE_2232H",
    #             #desiredSerial:str=None):

    #    # Call the super Constructor
    #    super().__init__(description, deviceType, desiredSerial)

    def open(self):

        super().open()

        self.set_mpsse_mode()

        # Disable 3 phase clocking
        self.set_mpsse_disable_three_phase_clocking()

        self._isOpen = True

    def get_cs_cmd_mask(self, chip_select):

        # Add in the MPSEE commands into the buffer
        if chip_select == FTDI_CS.CHIP_SELECT_AD3:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AD3
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AD4:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AD4
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AD5:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AD5
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AD6:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AD6
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AD7:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AD7
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC0:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC0
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC1:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC1
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC2:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC2
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC3:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC3
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC4:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC4
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC5:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC5
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC6:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC6
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif chip_select == FTDI_CS.CHIP_SELECT_AC7:
            cs_mask = FTDI_BUS_MASK.FT_MASK_AC7
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        else:
            # Default to AD3
            cs_mask = FTDI_BUS_MASK.FT_MASK_AD3
            cs_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND

        if cs_cmd == FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND:
            # Calculate chip select mask active
            cs_active = self.FT_MPSSE_LOW_BUS_IDLE_VALUE & (cs_mask ^ 0xFF)
            # Calculate chip select mask inactive
            cs_inactive = self.FT_MPSSE_LOW_BUS_IDLE_VALUE | cs_mask
            cs_idle_dir = self.FT_MPSSE_LOW_BUS_IDLE_DIR
        else:
            # Calculate chip select mask active
            cs_active = self.FT_MPSSE_HIGH_BUS_IDLE_VALUE & (cs_mask ^ 0xFF)
            # Calculate chip select mask inactive
            cs_inactive = self.FT_MPSSE_HIGH_BUS_IDLE_VALUE | cs_mask
            cs_idle_dir = self.FT_MPSSE_HIGH_BUS_IDLE_DIR

        return cs_active, cs_inactive, cs_cmd, cs_idle_dir

    def write(self, byte_array,
              length_to_send=None,
              chip_select=FTDI_CS.CHIP_SELECT_AD3,
              trigger=FTDI_TRIGGER_MASK.FT_TRIGGER_MASK_0,
              trigger_enable=False,
              write_end_chip_select=True):

        if length_to_send is None:
            length_to_send = len(byte_array)

        # This will send bytes out the port falling edge MSB first
        # byte_write_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_NO_READ_MSB_FIRST
        byte_write_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST
        self._write_bytes_base(byte_array, length_to_send, chip_select, byte_write_cmd, trigger, trigger_enable,
                               write_end_chip_select)

    def write_chip_select_inactive(self, chip_select=FTDI_CS.CHIP_SELECT_AD3):

        write_length = ((self.CHIP_SELECT_HIGH_REPEAT_COUNT * self.WRITE_GPIO_HEADER_LENGTH) +
                        self.WRITE_GPIO_HEADER_LENGTH + self.FLUSH_HEADER_LENGTH)

        (csActive, csInactive, csCmd, csIdleDir) = self.get_cs_cmd_mask(chip_select)

        write_array = [0] * write_length
        idx = 0

        # This is to stretch the time after the last clock before CS goes high
        for count in range(0, self.CHIP_SELECT_HIGH_REPEAT_COUNT):  # @UnusedVariable
            write_array[idx] = csCmd
            idx += 1
            write_array[idx] = csActive
            idx += 1
            write_array[idx] = csIdleDir
            idx += 1

        # Write CS Inactive
        write_array[idx] = csCmd
        idx += 1
        write_array[idx] = csInactive
        idx += 1
        write_array[idx] = csIdleDir
        idx += 1

        write_array[idx] = FTDI_MPSSE_COMMANDS.FT_MPSSE_FLUSH_COMMAND

        rx_queue_length = self.ftdiInstance.getQueueStatus()

        if rx_queue_length > 0:
            self.ftdiInstance.purge(defines.PURGE_RX)

            rx_queue_length = self.ftdiInstance.getQueueStatus()

            if rx_queue_length > 0:
                raise Exception('ftdi_spi.py: Bytes left in Rx buffer.')

        bytes_sent = self.ftdiInstance.write(bytes(write_array))
        if len(write_array) != bytes_sent:
            raise Exception('ftdiMpsse.m Bytes written does not match desired write length.')

    def write_bits(self, byte_array,
                   length_to_send=None,
                   chip_select=FTDI_CS.CHIP_SELECT_AD3,
                   trigger=FTDI_TRIGGER_MASK.FT_TRIGGER_MASK_0,
                   trigger_enable=False,
                   write_start_chip_select=True,
                   write_end_chip_select=True):

        if length_to_send is None:
            length_to_send = len(byte_array)

        # This will send bits out the port falling edge MSB first
        # byte_write_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_NO_READ_MSB_FIRST
        byte_write_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BITS_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST
        self._write_bytes_base(byte_array, length_to_send, chip_select, byte_write_cmd, trigger, trigger_enable,
                               write_end_chip_select, write_start_chip_select)

    def _write_bytes_base(self, byte_array, length_to_send,
                          chip_select=FTDI_CS.CHIP_SELECT_AD3,
                          byte_write_cmd=FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST,
                          trigger=FTDI_TRIGGER_MASK.FT_TRIGGER_MASK_0,
                          trigger_enable=False,
                          write_end_chip_select=True,
                          write_start_chip_select=True):

        (csActive, csInactive, csCmd, csIdleDir) = self.get_cs_cmd_mask(chip_select)

        # Calculate trigger active
        trigger_active = csActive | trigger
        trigger_inactive = csActive

        write_length = (self.WRITE_BYTE_HEADER_LENGTH +
                        self.FLUSH_HEADER_LENGTH +
                        length_to_send)
        # Bit command length is only 1 byte length
        if (byte_write_cmd == FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BITS_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST or
                byte_write_cmd == FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BITS_CMD_RISING_CLOCK_EDGE_WITH_READ_MSB_FIRST):
            write_length = write_length - 1

        if write_end_chip_select:
            write_length += ((self.CHIP_SELECT_HIGH_REPEAT_COUNT * self.WRITE_GPIO_HEADER_LENGTH) +
                             self.WRITE_GPIO_HEADER_LENGTH)

        if write_start_chip_select:
            write_length += (self.CHIP_SELECT_LOW_REPEAT_COUNT * self.WRITE_GPIO_HEADER_LENGTH)

        write_array = [0] * write_length
        idx = 0

        if write_start_chip_select:
            # This is chip Select going low
            for count in range(0, self.CHIP_SELECT_LOW_REPEAT_COUNT):  # @UnusedVariable
                write_array[idx] = csCmd
                idx += 1
                write_array[idx] = csActive
                idx += 1
                write_array[idx] = csIdleDir
                idx += 1

        # Add data to the array
        write_array[idx] = byte_write_cmd
        idx += 1
        # Bit commands only take one byte length
        write_array[idx] = (length_to_send - 1) & 255  # Low byte of 16 bit write length 0 means 1 byte
        idx += 1
        if not (byte_write_cmd == FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BITS_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST or
                byte_write_cmd == FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BITS_CMD_RISING_CLOCK_EDGE_WITH_READ_MSB_FIRST):
            write_array[idx] = (length_to_send - 1) >> 8  # High byte of 16 bit write length
            idx += 1

        # List slice assignment the byte array into the new array
        write_array[idx:idx + length_to_send] = byte_array[:]
        idx = idx + length_to_send

        if trigger_enable:

            # Set the CS active and the trigger high
            for rptIdx in range(0, self.CHIP_SELECT_LOW_REPEAT_COUNT):  # @UnusedVariable
                write_array[idx] = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND
                idx += 1
                write_array[idx] = trigger_active
                idx += 1
                write_array[idx] = self.FT_MPSSE_LOW_BUS_IDLE_DIR
                idx += 1

            # Set the trigger low with CS still active
            write_array[idx] = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND
            idx += 1
            write_array[idx] = trigger_inactive
            idx += 1
            write_array[idx] = self.FT_MPSSE_LOW_BUS_IDLE_DIR
            idx += 1

        if write_end_chip_select:

            # This is to stretch the time after the last clock before CS goes high
            for count in range(0, self.CHIP_SELECT_HIGH_REPEAT_COUNT):  # @UnusedVariable
                write_array[idx] = csCmd
                idx += 1
                write_array[idx] = csActive
                idx += 1
                write_array[idx] = csIdleDir
                idx += 1

            # Write CS Inactive
            write_array[idx] = csCmd
            idx += 1
            write_array[idx] = csInactive
            idx += 1
            write_array[idx] = csIdleDir
            idx += 1

        write_array[idx] = FTDI_MPSSE_COMMANDS.FT_MPSSE_FLUSH_COMMAND

        rx_queue_length = self.ftdiInstance.getQueueStatus()

        if rx_queue_length > 0:
            self.ftdiInstance.purge(defines.PURGE_RX)

            rx_queue_length = self.ftdiInstance.getQueueStatus()

            if rx_queue_length > 0:
                raise Exception('ftdi_spi.py: Bytes left in Rx buffer.')

        bytes_sent = self.ftdiInstance.write(bytes(write_array))
        if len(write_array) != bytes_sent:
            raise Exception('ftdi_spi.py: Bytes written does not match desired write length.')

        # Now read back the queue status to see how many bytes are in the buffer to stay in sync without calling any delay functions
        for repeatIdx in range(10000):  # @UnusedVariable
            rx_queue_length = self.ftdiInstance.getQueueStatus()
            if rx_queue_length == length_to_send:
                break

        if rx_queue_length != length_to_send:
            raise Exception('ftdi_spi.py: Bytes in queue does not match desired read length.')

        # Purge the bytes without reading them
        # self.ftdiInstance.purge(ftd2xx.defines.PURGE_TX | ftd2xx.defines.PURGE_RX)

        # rx_queue_length = self.ftdiInstance.getQueueStatus()
        # if rx_queue_length > 0:
        #    raise Exception('ftdi_spi.py: Bytes left in receive buffer.')

        # It's 4 times faster to read the few bytes than it is to purge them
        rx_buffer = self.ftdiInstance.read(length_to_send)
        if len(rx_buffer) != length_to_send:
            raise Exception('ftdi_spi.py: Bytes in queue does not match desired read length.')

    def get_rd_cmd_mask(self, read_bit_number, active_read_state):

        # Add in the MPSEE commands into the buffer
        if read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_0:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC0
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_1:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC1
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_2:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC2
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_3:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC3
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_4:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC4
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_5:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC5
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_6:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC6
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        elif read_bit_number == SPI_READ_BUFFER_BIT.FT_GPIO_BIT_7:
            rd_mask = FTDI_BUS_MASK.FT_MASK_AC7
            rd_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND
        else:
            raise Exception('ftdi_spi.py: The buffer enable code is only supported on AC bus.')

        # Calculate chip select mask active
        if active_read_state == SPI_READ_BIT_STATE.FT_RD_ACTIVE_LOW:
            # Clear the bit
            rd_active = self.FT_MPSSE_HIGH_BUS_IDLE_VALUE & (0xFF ^ rd_mask)
            # set the bit
            rd_inactive = self.FT_MPSSE_HIGH_BUS_IDLE_VALUE | rd_mask
        else:
            # Set the bit
            rd_active = self.FT_MPSSE_HIGH_BUS_IDLE_VALUE | rd_mask
            # clear the bit
            rd_inactive = self.FT_MPSSE_HIGH_BUS_IDLE_VALUE & (0xFF ^ rd_mask)

        rd_idle_dir = self.FT_MPSSE_HIGH_BUS_IDLE_DIR

        return rd_active, rd_inactive, rd_cmd, rd_idle_dir

    def write_with_readback(self, byte_array,
                            length_to_send=None,
                            chip_select=FTDI_CS.CHIP_SELECT_AD3,
                            trigger=FTDI_TRIGGER_MASK.FT_TRIGGER_MASK_0,
                            trigger_enable=False,
                            write_end_chip_select=True,
                            spi_read_mode=SPI_READ_MODE.FOUR_WIRE,
                            buffer_read_enable_pin=SPI_READ_BUFFER_BIT.FT_GPIO_BIT_0,
                            spi_write_bytes_length=1,
                            active_read_state=SPI_READ_BIT_STATE.FT_RD_ACTIVE_LOW):

        if length_to_send is None:
            length_to_send = len(byte_array)

        # This will send bytes out the port falling edge MSB first
        byte_write_with_readback_cmd = FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST
        read_bytes = self._write_bytes_with_readback(byte_array, length_to_send, chip_select,
                                                     byte_write_with_readback_cmd, trigger,
                                                     trigger_enable, write_end_chip_select, spi_read_mode,
                                                     buffer_read_enable_pin,
                                                     spi_write_bytes_length, active_read_state)
        return read_bytes

    def _write_bytes_with_readback(self, byte_array,
                                   length_to_send=None,
                                   chip_select=FTDI_CS.CHIP_SELECT_AD3,
                                   byte_write_cmd=FTDI_MPSSE_COMMANDS.FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST,
                                   trigger=FTDI_TRIGGER_MASK.FT_TRIGGER_MASK_0,
                                   trigger_enable=False,
                                   write_end_chip_select=True,
                                   spi_read_mode=SPI_READ_MODE.FOUR_WIRE,
                                   buffer_read_enable_pin=SPI_READ_BUFFER_BIT.FT_GPIO_BIT_0,
                                   spi_write_bytes_length=0,
                                   active_read_state=SPI_READ_BIT_STATE.FT_RD_ACTIVE_LOW):

        # Trigger functionality in next release
        test = trigger  # @UnusedVariable
        test1 = trigger_enable  # @UnusedVariable

        if spi_read_mode == SPI_READ_MODE.FOUR_WIRE:
            (csActive, csInactive, csCmd, csIdleDir) = self.get_cs_cmd_mask(chip_select)
        elif spi_read_mode == SPI_READ_MODE.THREE_WIRE_TO_FOUR_WITH_BUFFER:
            (csActive, csInactive, csCmd, csIdleDir) = self.get_cs_cmd_mask(chip_select)
            (read_active, read_inactive, read_cmd, read_idle_dir) = self.get_rd_cmd_mask(buffer_read_enable_pin,
                                                                                         active_read_state)
        else:
            raise Exception('ftdi_spi.py: Three wire read is not supported.')

        write_length = (((
                                 self.CHIP_SELECT_LOW_REPEAT_COUNT + self.CHIP_SELECT_HIGH_REPEAT_COUNT + 1) * self.WRITE_GPIO_HEADER_LENGTH) +
                        self.WRITE_BYTE_HEADER_LENGTH + length_to_send +
                        self.FLUSH_HEADER_LENGTH)

        if spi_read_mode == SPI_READ_MODE.THREE_WIRE_TO_FOUR_WITH_BUFFER:
            write_length += (((
                                      self.BUFFER_ENABLE_REPEAT_COUNT + self.BUFFER_DISABLE_REPEAT_COUNT + 1) * self.WRITE_GPIO_HEADER_LENGTH) +
                             self.WRITE_BYTE_HEADER_LENGTH)

        write_array = [0] * write_length
        idx = 0

        # This is chip Select going low
        for count in range(0, self.CHIP_SELECT_LOW_REPEAT_COUNT):  # @UnusedVariable
            write_array[idx] = csCmd
            idx += 1
            write_array[idx] = csActive
            idx += 1
            write_array[idx] = csIdleDir
            idx += 1

        if spi_read_mode == SPI_READ_MODE.FOUR_WIRE:
            # Add data to the array
            write_array[idx] = byte_write_cmd
            idx += 1
            write_array[idx] = (length_to_send - 1) & 0xFF  # Low byte of 16 bit write length 0 means 1 byte
            idx += 1
            write_array[idx] = (length_to_send - 1) >> 8  # High byte of 16 bit write length
            idx += 1

            # Concatenate the byte array into the new array
            write_array[idx:idx + length_to_send] = byte_array[:]
            idx += length_to_send

        elif spi_read_mode == SPI_READ_MODE.THREE_WIRE_TO_FOUR_WITH_BUFFER:

            # Add the write portion of the data to the array
            write_array[idx] = byte_write_cmd
            idx += 1
            write_array[idx] = (spi_write_bytes_length - 1) & 0xFF  # Low byte of 16 bit write length 0 means 1 byte
            idx += 1
            write_array[idx] = (spi_write_bytes_length - 1) >> 8  # High byte of 16 bit write length
            idx += 1

            # Concatenate the SPI writebytes portion of the byteArray into the new array
            write_array[idx:idx + spi_write_bytes_length] = byte_array[0:spi_write_bytes_length]
            idx += spi_write_bytes_length

            # This is the enable actually being sent multiple times to mimic a delay
            for count in range(0, self.BUFFER_ENABLE_REPEAT_COUNT):  # @UnusedVariable
                write_array[idx] = read_cmd
                idx += 1
                write_array[idx] = read_active
                idx += 1
                write_array[idx] = read_idle_dir
                idx += 1

            # Add read data to the array
            write_array[idx] = byte_write_cmd
            idx += 1
            write_array[idx] = (
                                       length_to_send - spi_write_bytes_length - 1) & 0xFF  # Low byte of 16 bit write length 0 means 1 byte
            idx += 1
            write_array[idx] = (length_to_send - spi_write_bytes_length - 1) >> 8  # High byte of 16 bit write length
            idx += 1

            # Concatenate the SPI read data into the new array
            write_array[idx:idx + length_to_send - spi_write_bytes_length] = byte_array[
                                                                             spi_write_bytes_length:length_to_send]
            idx += length_to_send - spi_write_bytes_length

        if write_end_chip_select:
            for count in range(0, self.CHIP_SELECT_HIGH_REPEAT_COUNT):  # @UnusedVariable
                write_array[idx] = csCmd
                idx += 1
                write_array[idx] = csActive
                idx += 1
                write_array[idx] = csIdleDir
                idx += 1

            write_array[idx] = csCmd
            idx += 1
            write_array[idx] = csInactive
            idx += 1
            write_array[idx] = csIdleDir
            idx += 1

        if spi_read_mode == SPI_READ_MODE.THREE_WIRE_TO_FOUR_WITH_BUFFER:

            # Write the buffer GPIO to enable MOSI
            # Write the CS inactive again to delay the buffer disable
            for count in range(0, self.BUFFER_DISABLE_REPEAT_COUNT):  # @UnusedVariable
                write_array[idx] = csCmd
                idx += 1
                write_array[idx] = csInactive
                idx += 1
                write_array[idx] = csIdleDir
                idx += 1

            # This is buffer disable
            write_array[idx] = read_cmd
            idx += 1
            write_array[idx] = read_inactive
            idx += 1
            write_array[idx] = read_idle_dir
            idx += 1

        # Flush the contents of the buffers back to the host immediately
        write_array[idx] = FTDI_MPSSE_COMMANDS.FT_MPSSE_FLUSH_COMMAND

        # Check for error
        rx_queue_length = self.ftdiInstance.getQueueStatus()
        if rx_queue_length > 0:
            self.ftdiInstance.purge(defines.PURGE_RX)

            rx_queue_length = self.ftdiInstance.getQueueStatus()
            if rx_queue_length > 0:
                raise Exception('ftdi_spi.py: Bytes left in Rx buffer.')

        bytes_sent = self.ftdiInstance.write(bytes(write_array))
        if len(write_array) != bytes_sent:
            raise Exception('ftdi_spi.py: Bytes written does not match desired write length.')

        # Now read back the queue status to see how many bytes are in the buffer to stay in sync without calling any delay functions
        for repeatIdx in range(10000):  # @UnusedVariable
            rx_queue_length = self.ftdiInstance.getQueueStatus()
            if rx_queue_length == length_to_send:
                break

        if rx_queue_length != length_to_send:
            raise Exception('ftdi_spi.py: Bytes in queue does not match desired read length.')

        rx_buffer = self.ftdiInstance.read(length_to_send)
        if len(rx_buffer) != length_to_send:
            raise Exception('ftdi_spi.py: Bytes in queue does not match desired read length.')

        return rx_buffer
