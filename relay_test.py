#!/usr/bin/env python
import str116
import time
# first variable is the relay number in decimal (0-15)
# second variable is off/on (0,1) in decimal

n=0
while n < 16:
    str116.set_relay(n, 0)
    #n+=1
    str116.set_relay(n, 1)
    # time.sleep()
    n+=1

str116.set_relay(15, 0)
