#!/usr/bin/env python

import time
import pigpio

wid =0

def turn(x):
	if (x >=-100 and x <=100):
		GPIO =21
		square=[]
		pi = pigpio.pi()
		pi.set_mode(GPIO,pigpio.OUTPUT)
		pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
		square.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
		square.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))

		pi.wave_add_generic(square)

		wid = pi.wave_create()

		if wid	>= 0:
			pi.wave_send_repeate(wid)
			time.sleep(float(1)/float(10))
			pi.wave_tx_stop()
			pi.wave__delete(wid)

			pi.stop


def throttle(x):
	if(x >=-100 and x<=100):
		GPIO=14
		square1=[]
		square2=[]
		pi = pigpio.pi()
		pi.set_mode(GPIO,pigpio.OUTPUT)

		square1.append(pigpio.pulse(1<<GPIO,0,1.5*1000))
		square1.append(pigpio.pulse(0,1<<GPIO,8.5*1000))

		pi.wave_add_generic(square1)

		wid = pi.wave_create(wid)

		if wid >=0:
			pi.wave_send_repeate(wid)
			time.sleep(float(1)/float(10))
			pi.wave_tx_stop()
			pi.wave__delete(wid)

		pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
		square2.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
		square2.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))

		pi.wave_add_generic(square2)

		wid = pi.wave_create()

		if wid >=0:
			pi.wave_send_repeate(wid)
			try:
				time.sleep(float(0.5))
				pi.wave_tx_stop()
				pi.wave__delete(wid)
			except KeyboardInterrupt:
				pi.wave_tx_stop()
				pi.wave__delete(wid)
				print 'keyboard stopped'
				mybreak(GPIO)
				pi.stop

def mybreak(pin):
	bGPIO=pin
	bsquare=[]
	bpi = pigpio.pi()
	bpi.set_mode(bGPIO,pigpio.OUTPUT)

	bsquare.append(pigpio.pulse(1<<bGPIO,0,1.3*1000))
	bsquare.append(pigpio.pulse(0,1<<bGPIO,8.7*1000))

	bpi.wave_add_generic(bsquare)

	bwid = bpi.wave_create()
	if bwid >=0:
		bpi.wave_send_repeate(bwid)
		time.sleep(float(1)/float(2))
		bpi.wave_tx_stop()
		bpi.wave__delete(bwdq)
	bpi.stop		

for i in range(0,100,5):
	turn(i)
for i in range(0,100,5):
	turn(-i)
turn(0)

for i in range(20,25):
	throttle(i)
for i in range(20,25):
	throttle(-i)
















