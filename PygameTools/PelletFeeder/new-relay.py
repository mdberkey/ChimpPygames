#!/usr/bin/env python

import time

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)

time.sleep(.5)

GPIO.output(17, GPIO.HIGH)
GPIO.cleanup()