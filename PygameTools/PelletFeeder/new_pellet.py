import usb.core
import usb.backend.libusb1
from time import sleep

def write_to_adu(dev, msg_str):
    print('Writing command: {}'.format(msg_str))

    # message structure:
    #   message is an ASCII string containing the command
    #   8 bytes in length
    #   0th byte must always be 0x01 (decimal 1)
    #   bytes 1 to 7 are ASCII character values representing the command
    #   remainder of message is padded to 8 bytes with character code 0

    byte_str = chr(0x01) + msg_str + chr(0) * max(7 - len(msg_str), 0)

    num_bytes_written = 0

    try:	# 0x01 is the OUT endpoint
        num_bytes_written = dev.write(0x01, byte_str)
    except usb.core.USBError as e:
        print (e.args)

    return num_bytes_written

def read_from_adu(dev, timeout):
    try:	# try to read a maximum of 64 bytes from 0x81 (IN endpoint)
        data = dev.read(0x81, 8, timeout)
    except usb.core.USBError as e:
        print ("Error reading response: {}".format(e.args))
        return None

    byte_str = ''.join(chr(n) for n in data[1:]) # construct a string out of the read values, starting from the 2nd byte
    result_str = byte_str.split('\x00',1)[0] # remove the trailing null '\x00' characters

    if len(result_str) == 0:
        return None

    return result_str

def main():
    VENDOR_ID = 0x0a07
    PRODUCT_ID = 0x00c8
    
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if device is None:
        raise ValueError('ADU Device not found. Please ensure it is connected to the tablet.')
        sys.exit(1)


    # Claim interface 0 - this interface provides IN and OUT endpoints to write to and read from
    try:
        usb.util.claim_interface(device, 0)
    except usb.core.USBError as e:
        print('detaching kernel driver')
        device.detach_kernel_driver(0)
        usb.util.claim_interface(device, 0)


    #usb.util.claim_interface(device, 0)
    #device.detach_kernel_driver(0)
    #usb.util.claim_interface(device, 0)

    #bytes_written = write_to_adu(device, 'RK0') # reset relay 0
    bytes_written = write_to_adu(device, 'SK0') # set realay 0

    sleep(0.25)

    bytes_written = write_to_adu(device, 'RK0') # reset relay 0
    #bytes_written = write_to_adu(device, 'RPA0')
    #print(bytes_written)
    

    #data = read_from_adu(device, 10000)

    #data = read_from_adu(device, 10000)

    #print(data)



main()
