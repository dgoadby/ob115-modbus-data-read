# Micropython Modbus read of OB115-MOD.
# Uses UModbus code and Micropython V1.18
# Note that the OB115-MOD data is differently structured to other visually similar devices. 
# In particular, the data is in IEEE format.
#
# Written by: David Goadby, March 1st 2022
#
# Released as-is under MIT license.

# Imports
from machine import UART
import time
import uModBusSerial as ModBus
import struct

# Definitions for ESP32
TXPIN = 14
RXPIN = 27
PINS = [TXPIN, RXPIN]
BAUD_RATE = 9600
DATA_BITS = 8
STOP_BITS = 1
PARITY = None
SLAVE_ADDRESS = 1
UART_NO = 2

# The registers are not contiguous so we need to read 0x2 to 0xe and 0x160 to 0x16a
reg_list = [(0x2, 14), (0x160, 12)] # starting register and count to read.

# Dictionary of registers and their names
reg_names ={0x2: "Voltage",
            0x4: "Frequency",
            0x6: "Current",
            0x8: "Active Power",
            0xa: "Apparent Power",
            0xc: "Reactive Power",
            0xe: "power Factor",
            0x160: "Import Active Energy",
            0x162: "Import Reactive Energy",
            0x164: "Reserved",
            0x166: "Export Active Energy",
            0x168: "Export Reactive Energy",
            0x16a: "Total Active Energy"}

# Convert 4 bytes to ieee754.
# Incoming data format is two 16 bit words in big-endian. (High word is lower address).
def convert_2words_to_float(high_word, low_word):
    long_word = (high_word << 16) | low_word            # make into one word
    packed_value = struct.pack('>L', long_word)         # byte list from Big-Endian long.
    float_value = struct.unpack('>f', packed_value)[0]  # float from list
    return (float_value)

# Create modbus reader object for OB115.
OB115 = ModBus.uModBusSerial(UART_NO, BAUD_RATE, DATA_BITS, STOP_BITS, PARITY, PINS)

count = 0  # loop count

while True:
    for register, reg_count in reg_list:
        # As we are expecting 4 bytes of IEEE754 for each register then all returned data are unsigned words.
        message = OB115.read_input_registers(SLAVE_ADDRESS, register, reg_count, signed = False)
    #    print(f"Message: {message}")

    # Now turn it into something useful.
    # Message is tuple of registers which are in IEEE754 format.
    # Extract high and low words from results and then convert.
        for word_pair in range(0, len(message), 2):  # step 2
            hi_word = message[word_pair]
            lo_word = message[word_pair + 1]
            float_value = convert_2words_to_float(hi_word, lo_word) # Big-Endian

            # Display registername and value
            if register + word_pair == 0x16a:
                print(f"{reg_names[register + word_pair]:>22} : {round(float_value, 6): 8.2f}")
            else:
                print(f"{reg_names[register + word_pair]:>22} : {round(float_value, 3): 8.2f}")

    count += 1
    print(f"---- {count}")
    time.sleep(60)

print("\nDone") # Should never happen unless Modbus error.
OB115.close()








