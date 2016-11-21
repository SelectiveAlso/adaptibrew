#!/usr/bin/env python
import serial
import time

port = "/dev/ttyAMA0"
usart = serial.Serial (port,19200)
bytestring = "55AA0817020008012A77"
message_bytes = bytestring.decode("hex")
usart.write(message_bytes)
time.sleep(5)
message_bytes = "55AA0817020008002977".decode("hex")
usart.write(message_bytes)
