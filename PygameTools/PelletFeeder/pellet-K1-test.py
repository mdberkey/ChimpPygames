from ctypes import CDLL, RTLD_GLOBAL


def main():
    path = '/lib/arm-linux-gnueabihf/libusb-1.0.so.0.1.0'
    lib = CDLL(path, mode=RTLD_GLOBAL)
    relay = CDLL('PygameTools/PelletFeeder/relay.so')
    return relay.main()


if __name__ == '__main__':
    main()
