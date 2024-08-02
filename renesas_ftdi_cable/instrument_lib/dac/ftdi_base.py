from enum import IntEnum
from math import floor

from ftd2xx import defines
from ftd2xx import ftd2xx


class FTDI_DIRECTION(IntEnum):
    INPUT = 0
    OUTPUT = 1


class FTDI_BUS_MASK(IntEnum):
    FT_MASK_AD0 = 0x1
    FT_MASK_AD1 = 0x2
    FT_MASK_AD2 = 0x4
    FT_MASK_AD3 = 0x8
    FT_MASK_AD4 = 0x10
    FT_MASK_AD5 = 0x20
    FT_MASK_AD6 = 0x40
    FT_MASK_AD7 = 0x80

    FT_MASK_AC0 = 0x1
    FT_MASK_AC1 = 0x2
    FT_MASK_AC2 = 0x4
    FT_MASK_AC3 = 0x8
    FT_MASK_AC4 = 0x10
    FT_MASK_AC5 = 0x20
    FT_MASK_AC6 = 0x40
    FT_MASK_AC7 = 0x80


class FTDI_BUS(IntEnum):
    AD_BUS = 0
    AC_BUS = 1


class FTDI_TRIGGER_MASK(IntEnum):
    # Triggers are only the D Bus (LOW) So they can trigger at the same time
    FT_TRIGGER_MASK_0 = 0x10  # AD4
    FT_TRIGGER_MASK_1 = 0x20  # AD5
    FT_TRIGGER_MASK_2 = 0x40  # AD6
    FT_TRIGGER_MASK_3 = 0x80  # AD7


class FTDI_DEVICE_TYPE(IntEnum):
    DEVICE_232BM = 0
    DEVICE_232AM = 1
    DEVICE_100AX = 2
    DEVICE_UNKNOWN = 3
    DEVICE_2232C = 4
    DEVICE_232R = 5
    DEVICE_2232H = 6
    DEVICE_4232H = 7
    DEVICE_232H = 8
    DEVICE_X_SERIES = 9


class FTDI_BIT_MODE(IntEnum):
    RESET = 0
    ASYNCHRONOUS_BIT_BANG = 0x1
    MPSSE = 0x2
    SYNCHRONOUS_BIT_BANG = 0x4
    MCU_HOST_BUS_EMULATION_MODE = 0x8
    FAST_OPTO_ISOLATED_SERIAL_MODE = 0x10
    CBUS_BIT_BANG_MODE = 0x20
    SINGLE_CHANNEL_SYNCHRONOUS_245_FIFO_MODE = 0x80


class FTDI_OUTPUT_MODE(IntEnum):
    ALL_OUTPUTS = 0xFF
    ALL_INPUTS = 0x0


class FTDI_MPSSE_COMMANDS:
    # FTDI MPSSE Commands MSB First
    FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_NO_READ_MSB_FIRST = 0x11
    FT_MPSSE_WR_BYTES_CMD_RISING_CLOCK_EDGE_NO_READ_MSB_FIRST = 0x10

    FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST = 0x31
    FT_MPSSE_WR_BYTES_CMD_RISING_CLOCK_EDGE_WITH_READ_MSB_FIRST = 0x34

    # FTDI MPSSE Commands LSB First
    FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_NO_READ_LSB_FIRST = 0x19
    FT_MPSSE_WR_BYTES_CMD_RISING_CLOCK_EDGE_NO_READ_LSB_FIRST = 0x18

    FT_MPSSE_WR_BYTES_CMD_FALLING_CLOCK_EDGE_WITH_READ_LSB_FIRST = 0x39
    FT_MPSSE_WR_BYTES_CMD_RISING_CLOCK_EDGE_WITH_READ_LSB_FIRST = 0x3C

    # FTDI MPSSE BIT Commands MSB First
    FT_MPSSE_WR_BITS_CMD_FALLING_CLOCK_EDGE_NO_READ_MSB_FIRST = 0x13
    FT_MPSSE_WR_BITS_CMD_RISING_CLOCK_EDGE_NO_READ_MSB_FIRST = 0x12

    FT_MPSSE_WR_BITS_CMD_FALLING_CLOCK_EDGE_WITH_READ_MSB_FIRST = 0x33
    FT_MPSSE_WR_BITS_CMD_RISING_CLOCK_EDGE_WITH_READ_MSB_FIRST = 0x36

    # FTDI MPSSE BIT Commands LSB First
    FT_MPSSE_WR_BITS_CMD_FALLING_CLOCK_EDGE_NO_READ_LSB_FIRST = 0x1B
    FT_MPSSE_WR_BITS_CMD_RISING_CLOCK_EDGE_NO_READ_LSB_FIRST = 0x1A

    FT_MPSSE_WR_BITS_CMD_FALLING_CLOCK_EDGE_WITH_READ_LSB_FIRST = 0x3B
    FT_MPSSE_WR_BITS_CMD_RISING_CLOCK_EDGE_WITH_READ_LSB_FIRST = 0x3E

    # This is the return code from the MPSSE engine when a command fails
    FT_MPSSE_FAILCODE = 0xfa

    FT_MPSSE_SET_GPIO_LOW_COMMAND = 0x80
    FT_MPSSE_SET_GPIO_HIGH_COMMAND = 0x82

    FT_MPSSE_GET_GPIO_LOW_COMMAND = 0x81
    FT_MPSSE_GET_GPIO_HIGH_COMMAND = 0x83

    FT_MPSSE_DISABLE_LOOPBACK_COMMAND = 0x85
    FT_MPSSE_ENABLE_LOOPBACK_COMMAND = 0x84

    FT_MPSSE_CLOCK_DIVDER_COMMAND = 0x86

    FT_MPSSE_DISABLE_CLOCK_DIVIDE_BY_FIVE_COMMAND = 0x8A
    FT_MPSSE_ENABLE_CLOCK_DIVIDE_BY_FIVE_COMMAND = 0x8B

    FT_MPSSE_DISABLE_ADAPTIVE_CLOCKING_COMMAND = 0x97
    FT_MPSSE_ENABLE_ADAPTIVE_CLOCKING_COMMAND = 0x96

    FT_MPSSE_DISABLE_THREE_PHASE_CLOCKING_COMMAND = 0x8D
    FT_MPSSE_ENABLE_THREE_PHASE_CLOCKING_COMMAND = 0x8C

    FT_MPSSE_FLUSH_COMMAND = 0x87


class FtdiBase:
    ftdiInstance = 0
    deviceCount = 0

    LATENCY = 8  # mS
    RX_TIMEOUT = 50  # mS
    TX_TIMEOUT = 50  # mS
    WRITE_MASK = 0xFF
    DEADMAN_TIMEOUT = 500  # 500mS

    BUFFER_ENABLE_REPEAT_COUNT = 3
    BUFFER_DISABLE_REPEAT_COUNT = 2

    TRIGGER_REPEAT_COUNT = 3

    MAX_CLOCK_FREQ_MHZ = 30
    MIN_CLOCK_FREQ_MHZ = 0.001

    WRITE_BYTE_HEADER_LENGTH = 3
    WRITE_GPIO_HEADER_LENGTH = 3
    WRITE_BIT_MESSAGE_LENGTH = 3
    FLUSH_HEADER_LENGTH = 1

    # Properties
    # This is clock polarity = 0 and clock phase = 0
    # clock is normally low
    # data changes on negative clock pulses
    # ONLY SUPPORTS SPI MODES 0 and SPI MODE 2
    SPI_MODE = 0

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

    def __init__(self, description: str = "DUAL RS232-HS A",
                 device_type: str = "DEVICE_2232H",
                 desired_serial: str = None):

        self._desiredDescription = description
        self._desiredDeviceTypeString = device_type
        self._desiredDeviceTypeInt = getattr(defines, device_type)
        self._desiredSerial = desired_serial
        self.index = -1
        self.serial = None
        if desired_serial is None:
            self._searchForSpecificSerialNumber = False
        else:
            self._searchForSpecificSerialNumber = True

        self._isOpen = False

    def open(self):

        self.deviceCount = ftd2xx.createDeviceInfoList()
        if self.deviceCount == 0:
            raise Exception('ftdi_base.py: No FTDI devices found on the USB Bus.')
        else:
            print("Number of USB interface adapters connected to the system is %d" % self.deviceCount)

        # Get information about the boards   
        # device_info_detail = ftd2xx.getDeviceInfoDetail()
        # serialNumbers = ftd2xx.listDevices(defines.OPEN_BY_SERIAL_NUMBER)
        # descriptions = ftd2xx.listDevices(defines.OPEN_BY_DESCRIPTION)

        found_correct_board = False
        for idx in range(0, self.deviceCount + 1):
            device_info_detail = ftd2xx.getDeviceInfoDetail(idx)
            # print(device_info_detail)
            ptr = device_info_detail['handle']

            if self._searchForSpecificSerialNumber:
                if (device_info_detail['serial'].decode("utf-8").casefold() == self._desiredSerial.casefold() and
                        device_info_detail['type'] == self._desiredDeviceTypeInt):  # and

                    if ptr.value is not None:
                        # Device is in use
                        print("FTDI device Description=%s Serial=%s detected as in-use and not available." % (
                            device_info_detail['description'].decode("utf-8"),
                            device_info_detail['serial'].decode("utf-8")))
                        continue
                    found_correct_board = True
                    self.serial = device_info_detail['serial'].decode("utf-8")
                    self.index = device_info_detail['index']
                    break
                else:
                    continue
            else:
                if (device_info_detail['type'] == self._desiredDeviceTypeInt and
                        device_info_detail['description'].decode(
                            "utf-8").casefold() == self._desiredDescription.casefold()):
                    if ptr.value is not None:
                        # Device is in use
                        print("FTDI device Description=%s detected as in-use and not available." % (
                            device_info_detail['description'].decode("utf-8")))
                        continue
                    found_correct_board = True
                    self.serial = device_info_detail['serial'].decode("utf-8")
                    self.index = device_info_detail['index']
                    break
                else:
                    continue

        if not found_correct_board:
            if self._searchForSpecificSerialNumber:
                raise Exception(
                    'ftdi_base.py: Serial number %s is not found on the system.' % self._desiredSerial)
            else:
                raise Exception('ftdi_base.py: Board Type %s and Description %s is not found on the system.' %
                                (self._desiredDeviceTypeString, self._desiredDescription))

        else:
            print("FTDI device type=%s Description=%s Serial=%s detected" % (
                self._desiredDeviceTypeString, self._desiredDescription, self.serial))

        # We stored the index of the board when we searched so we open by index
        self.ftdiInstance = ftd2xx.open(self.index)
        print("USB Adapter %s %s SN %s is opened and ready for use." % (
            self._desiredDeviceTypeString, self._desiredDescription, self.serial))

        # Reset the device
        self.ftdiInstance.setBitMode(self.FT_MPSSE_LOW_BUS_IDLE_DIR, int(FTDI_BIT_MODE.RESET))

    def close(self):

        # Close the port if it's open
        if self._isOpen:
            self.ftdiInstance.close()
            self._isOpen = False

    def set_mpsse_mode(self):

        # Reset the IC
        self.ftdiInstance.setBitMode(self.FT_MPSSE_LOW_BUS_IDLE_DIR, int(FTDI_BIT_MODE.RESET))

        # Configure the MPSSE engine
        self.ftdiInstance.setBitMode(self.FT_MPSSE_LOW_BUS_IDLE_DIR, int(FTDI_BIT_MODE.MPSSE))

        # Set Latency Timer
        self.ftdiInstance.setLatencyTimer(self.LATENCY)

        # Set Flow Control
        self.ftdiInstance.setFlowControl(defines.FLOW_RTS_CTS, 0, 0)

        # Set Timeouts
        self.ftdiInstance.setTimeouts(self.RX_TIMEOUT, self.TX_TIMEOUT)

        # Flush the buffer to clear out any content
        self.ftdiInstance.purge(defines.PURGE_TX | defines.PURGE_RX)

        # First test of the MPSSE Engine - Send a bad command and look for response
        mpsse_test_failcode = 0xA
        write_array = []
        response_length = 2
        rx_buffer = self.send_mpsse_command(mpsse_test_failcode, write_array, response_length)

        # Insure the MPSSE Engine responds properly
        if not (len(rx_buffer) == 2 and rx_buffer[0] == FTDI_MPSSE_COMMANDS.FT_MPSSE_FAILCODE and rx_buffer[1] == mpsse_test_failcode):
            raise Exception('ftdi_base.py: Error initializing MPSSE engine.')

        # Second test of MPSSE Engine - Should be able to remove this
        mpsse_test_failcode = 0xAB
        write_array = []
        response_length = 2
        rx_buffer = self.send_mpsse_command(mpsse_test_failcode, write_array, response_length)

        # Insure the MPSSE Engine responds properly
        if not (len(rx_buffer) == 2 and rx_buffer[0] == FTDI_MPSSE_COMMANDS.FT_MPSSE_FAILCODE and rx_buffer[1] == mpsse_test_failcode):
            raise Exception('ftdi_base.py: Error initializing MPSSE engine.')

        # Set Idle State values for Low bus GPIO lines
        self.set_mpsse_gpio_low_byte(self.FT_MPSSE_LOW_BUS_IDLE_VALUE, self.FT_MPSSE_LOW_BUS_IDLE_DIR)

        # Set Idle State values for HIgh bus GPIO lines
        self.set_mpsse_gpio_high_byte(self.FT_MPSSE_HIGH_BUS_IDLE_VALUE, self.FT_MPSSE_HIGH_BUS_IDLE_DIR)

        # Disable data loop back
        self.set_mpsse_disable_loopback()

        # Disable clock divide by 5
        self.set_mpsse_disable_clock_divide_by_five()

        # Disable Adaptive Clocking
        self.set_mpsse_disable_adaptive_clocking()

        # Set the default clock frequency     
        self.set_clock_frequency_mhz(self.clock_frequency_mhz)

    def send_mpsse_command(self, command, data_array, response_length):

        write_array = [0] * (1 + len(data_array))
        write_array[0] = command

        # Copy the contents of dataArray into the write array
        if len(data_array) > 0:
            write_array[1:] = data_array[:]

        # Flush the buffer to clear out any content
        self.ftdiInstance.purge(defines.PURGE_TX | defines.PURGE_RX)

        # Send the bytes
        bytes_sent = self.ftdiInstance.write(bytes(write_array))

        if len(write_array) != bytes_sent:
            raise Exception('ftdi_base.py: sendMpsseCommand Bytes written does not match desired write length.')

        if response_length > 0:
            # Read the response
            rx_buffer = self.ftdiInstance.read(response_length)
        else:
            # This is an error check - looking for errors generated by
            # the FTDI MPSSE Engine
            rx_queue_length = self.ftdiInstance.getQueueStatus()
            if rx_queue_length > 0:
                rx_buffer = self.ftdiInstance.read(response_length)
            else:
                rx_buffer = None

        return rx_buffer

    def set_mpsse_disable_loopback(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_DISABLE_LOOPBACK_COMMAND, write_array, response_length)

    def set_mpsse_enable_loopback(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_ENABLE_LOOPBACK_COMMAND, write_array, response_length)

    def set_mpsse_disable_clock_divide_by_five(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_DISABLE_CLOCK_DIVIDE_BY_FIVE_COMMAND, write_array,
                                response_length)

    def set_mpsse_enable_clock_divide_by_five(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_ENABLE_CLOCK_DIVIDE_BY_FIVE_COMMAND, write_array,
                                response_length)

    def set_mpsse_disable_adaptive_clocking(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_DISABLE_ADAPTIVE_CLOCKING_COMMAND, write_array,
                                response_length)

    def set_mpsse_enable_adaptive_clocking(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_ENABLE_ADAPTIVE_CLOCKING_COMMAND, write_array,
                                response_length)

    def set_mpsse_disable_three_phase_clocking(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_DISABLE_THREE_PHASE_CLOCKING_COMMAND, write_array,
                                response_length)

    def set_mpsse_enable_three_phase_clocking(self):
        response_length = 0
        write_array = []
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_ENABLE_THREE_PHASE_CLOCKING_COMMAND, write_array,
                                response_length)

    def set_mpsse_gpio_low_byte(self, value, direction):
        write_array = [value, direction]
        response_length = 0
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_LOW_COMMAND, write_array, response_length)

    def set_mpsse_gpio_high_byte(self, value, direction):
        write_array = [value, direction]
        response_length = 0
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_SET_GPIO_HIGH_COMMAND, write_array, response_length)

    def get_mpsse_gpio_low_byte(self) -> int:
        write_array = []
        response_length = 1
        read_data = self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_GET_GPIO_LOW_COMMAND, write_array,
                                            response_length)
        return int(read_data[1])

    def get_mpsse_gpio_high_byte(self) -> int:
        write_array = []
        response_length = 1
        read_data = self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_GET_GPIO_HIGH_COMMAND, write_array,
                                            response_length)
        return int.from_bytes(read_data, "big")

    def _write_byte(self, write_data):
        # Purge the buffer
        self.ftdiInstance.purge(defines.PURGE_RX)

        byte_count = len(write_data)

        # Write the command
        bytes_written = self.ftdiInstance.write(write_data)

        if bytes_written != byte_count:
            raise Exception(
                'ftdi_base.py:  Unsuccessful FTDI Write command. Number of bytes clocked out (%d) do not match bytes sent (%d).' % (
                    bytes_written, byte_count))

    def read_data(self, bytes_to_read):

        read_iteration = 0
        max_number_of_read_iterations = 50000
        queue_timeout_flag = False
        rx_queue_length = 0
        rx_bytes_read = 0
        rx_buffer_index = 0

        rx_buffer = [0] * bytes_to_read

        while (rx_bytes_read < bytes_to_read) and (not queue_timeout_flag):

            rx_queue_length = self.ftdiInstance.getQueueStatus()
            max_number_of_read_iterations += 1

            if rx_queue_length > 0:

                read_buffer = self.ftdiInstance.read(rx_queue_length)
                rx_bytes_read = len(read_buffer)

                if rx_bytes_read <= bytes_to_read:
                    rx_buffer[rx_buffer_index:rx_buffer_index + rx_bytes_read - 1] = read_buffer[:]
                    rx_buffer_index = rx_buffer_index + rx_bytes_read
                    read_iteration = read_iteration + 1
                else:
                    rx_buffer[rx_buffer_index:rx_buffer_index + rx_bytes_read - 1] = read_buffer[:]
                    break

                if read_iteration >= max_number_of_read_iterations:
                    queue_timeout_flag = True

            else:
                if read_iteration >= max_number_of_read_iterations:
                    queue_timeout_flag = True
                else:
                    read_iteration = read_iteration + 1

        if rx_buffer_index < bytes_to_read:
            raise Exception('ftdiMpsseBase.py Error reading bytes from device.')

        return bytes(rx_buffer)

    def flush_buffer(self):
        rx_queue_length = self.ftdiInstance.getQueueStatus()
        if rx_queue_length > 0:
            read_buffer = self.ftdiInstance.read(rx_queue_length)
            if len(read_buffer) < rx_queue_length:
                raise Exception('ftdiMpsseBase.py Error reading bytes from device.')
        return read_buffer

    def set_clock_frequency_mhz(self, clock_freq_m_hz):

        self.clock_frequency_mhz = clock_freq_m_hz

        if clock_freq_m_hz > self.MAX_CLOCK_FREQ_MHZ:
            raise Exception('ftdi_base.py:  Max clock Frequency of %.2f exceeded.' % self.MAX_CLOCK_FREQ_MHZ)
        elif clock_freq_m_hz < self.MIN_CLOCK_FREQ_MHZ:
            raise Exception('ftdi_base.py:  Minimum clock Frequency of %.2f required.' % self.MIN_CLOCK_FREQ_MHZ)

        # Calculate the divisor   Page 9 of the FTDI AN_135 Manual
        divisor = int(floor(((60E6 / (clock_freq_m_hz * 1E6)) / 2) - 1))

        # Create the command to set the clock divider
        data_write_buffer = [(divisor & 255), (divisor >> 8)]
        response_length = 0
        self.send_mpsse_command(FTDI_MPSSE_COMMANDS.FT_MPSSE_CLOCK_DIVDER_COMMAND, data_write_buffer, response_length)

    def set_mpsse_low_byte_outputs_low(self):
        # Write the data to the device
        self.set_mpsse_gpio_low_byte(0, self.FT_MPSSE_LOW_BUS_IDLE_DIR)

    def set_mpsse_high_byte_outputs_low(self):
        # Write the data to the device
        self.set_mpsse_gpio_high_byte(0, self.FT_MPSSE_HIGH_BUS_IDLE_DIR)

    def set_port_d_low_byte_bit_value(self, value, bit, direction):
        # Direction
        # 1 = output
        # 0 = input

        if direction == 1:
            self.FT_MPSSE_LOW_BUS_IDLE_DIR = self.FT_MPSSE_LOW_BUS_IDLE_DIR | 2 ** bit  # Set the bit
        else:
            self.FT_MPSSE_LOW_BUS_IDLE_DIR = ((2 ** bit) ^ 0xFF) & self.FT_MPSSE_LOW_BUS_IDLE_DIR  # Clear the bit

        if value == 1:
            self.FT_MPSSE_LOW_BUS_IDLE_VALUE = self.FT_MPSSE_LOW_BUS_IDLE_VALUE | 2 ** bit  # Set the bit
        else:
            self.FT_MPSSE_LOW_BUS_IDLE_VALUE = ((2 ** bit) ^ 0xFF) & self.FT_MPSSE_LOW_BUS_IDLE_VALUE  # Clear the bit

        #  Write the data to the device
        self.set_mpsse_gpio_low_byte(self.FT_MPSSE_LOW_BUS_IDLE_VALUE, self.FT_MPSSE_LOW_BUS_IDLE_DIR)

    def set_port_d_low_byte_value(self, value, direction):
        # Direction
        # 1 = output
        # 0 = input
        self.FT_MPSSE_LOW_BUS_IDLE_VALUE = value
        self.FT_MPSSE_LOW_BUS_IDLE_DIR = direction

        # Write the data to the device
        self.set_mpsse_gpio_low_byte(self.FT_MPSSE_LOW_BUS_IDLE_VALUE, self.FT_MPSSE_LOW_BUS_IDLE_DIR)

    def set_port_c_high_byte_bit_value(self, value, bit, direction):
        # Direction
        # 1 = output
        # 0 = input

        if direction == 1:
            self.FT_MPSSE_HIGH_BUS_IDLE_DIR = self.FT_MPSSE_HIGH_BUS_IDLE_DIR | 2 ** bit  # Set the bit
        else:
            self.FT_MPSSE_HIGH_BUS_IDLE_DIR = ((2 ** bit) ^ 0xFF) & self.FT_MPSSE_HIGH_BUS_IDLE_DIR  # Clear the bit

        if value == 1:
            self.FT_MPSSE_HIGH_BUS_IDLE_VALUE = self.FT_MPSSE_HIGH_BUS_IDLE_VALUE | 2 ** bit  # Set the bit
        else:
            self.FT_MPSSE_HIGH_BUS_IDLE_VALUE = ((2 ** bit) ^ 0xFF) & self.FT_MPSSE_HIGH_BUS_IDLE_VALUE  # Clear the bit

        #  Write the data to the device
        self.set_mpsse_gpio_high_byte(self.FT_MPSSE_HIGH_BUS_IDLE_VALUE, self.FT_MPSSE_HIGH_BUS_IDLE_DIR)

    def set_port_c_high_byte_value(self, value, direction):

        # Direction
        # 1 = output
        # 0 = input

        self.FT_MPSSE_HIGH_BUS_IDLE_DIR = direction
        self.FT_MPSSE_HIGH_BUS_IDLE_VALUE = value

        # Write the data to the device
        self.set_mpsse_gpio_high_byte(self.FT_MPSSE_HIGH_BUS_IDLE_VALUE, self.FT_MPSSE_HIGH_BUS_IDLE_DIR)

    def get_port_c_high_byte_value(self) -> int:
        return self.get_mpsse_gpio_high_byte()

    def get_port_d_low_byte_value(self) -> int:
        return self.get_mpsse_gpio_low_byte()
