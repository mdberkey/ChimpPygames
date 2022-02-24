CFLAGS := -O2 -std=c99 -Wall

relay: relay.o
	$(CC) -o relay relay.o -lusb-1.0
	$(CC) -fPIC -shared -o relay.so relay.c

default: relay

clean:
	rm relay relay.o
