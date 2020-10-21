from __future__ import print_function

import hid
import time


# try opening a device, then perform write and read

def pellet(num=1):
    print("Opening the device")
    h = hid.device()
    h.open(2567, 200) # USB relay VendorID/ProductID
#2567
    # enable non-blocking mode
    h.set_nonblocking(1)
    
    for i in range(num):
        # SK3 command
        h.write([1, 83, 75, 48])

        # wait
        time.sleep(.25)

        # RK3 command
        h.write([1, 82, 75, 48])

        # wait
        time.sleep(.05)

        print("Closing the device")
    
    h.close()

    # wait
    time.sleep(.05)

# print("Add pellet to log")
# print("Done")

if __name__ == "__main__":
    pellet()
