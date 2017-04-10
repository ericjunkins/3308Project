#!/usr/bin/env python

import time
import pigpio


#sudokillall pigpiod 88888
#sudo pigpiod
#pigs pigpv
#pigs hwver

wid =0

class TextProcError(Exception):
        def _init_(self,msg):

                super().__init__(msg)

class RcFuncs:
                
        def __init__(self,num):
                if type(num) is not int:
                        raise TextProcError("Requires int")
                self.num = num


        def turn(self):
                x = self.num
                if (x >=-100 and x <=100):
                        GPIO =23
                        square=[]
                        pi = pigpio.pi()
                        pi.set_mode(GPIO,pigpio.OUTPUT)
                        pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                        square.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
                        square.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))
                        #print pulseLen
                        pi.wave_add_generic(square)

                        wid = pi.wave_create()

                        if wid	>= 0:
                                pi.wave_send_repeat(wid)
                                time.sleep(float(1)/float(10))
                                pi.wave_tx_stop()
                                pi.wave_delete(wid)

                                pi.stop
                                
                        return pulseLen
        

        def throttle(self):
                x = self.num
                if(x >=-100 and x<=100):
                        GPIO=14
                        square1=[]
                        square2=[]
                        pi = pigpio.pi()
                        pi.set_mode(GPIO,pigpio.OUTPUT)

                        square1.append(pigpio.pulse(1<<GPIO,0,1.5*1000))
                        square1.append(pigpio.pulse(0,1<<GPIO,8.5*1000))

                        pi.wave_add_generic(square1)

                        wid = pi.wave_create()

                        if wid >=0:
                                pi.wave_send_repeat(wid)
                                time.sleep(float(1)/float(10))
                                pi.wave_tx_stop()
                                pi.wave_delete(wid)

                        pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                        square2.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
                        square2.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))

                        pi.wave_add_generic(square2)

                        wid = pi.wave_create()

                        if wid >=0:
                                pi.wave_send_repeat(wid)
                                try:
                                        time.sleep(float(0.5))
                                        pi.wave_tx_stop()
                                        pi.wave_delete(wid)
                                except KeyboardInterrupt:
                                        pi.wave_tx_stop()
                                        pi.wave_delete(wid)
                                        print 'keyboard stopped'
                                        mybreak(GPIO)
                                        pi.stop

                return pulseLen



        def RC(x,y,z):
                if(x >=-100 and x<=100 and y >=-100 and y <= 100 and (z==0 or z==1)):
                        thrPin=14
                        stPin=21
                        thrBase=[]
                        thrSig=[]
                        stSig=[]
                        thrPi = pigpio.pi()
                        thrPi.set_mode(thrPin,pigpio.OUTPUT)
                        stPi = pigpio.pi()
                        stPi.set_mode(stPin,pigpio.OUTPUT)
                        #initialize the first signal to send to the throttle motor
                        
                        thrBase.append(pigpio.pulse(1<<thrPin,0,1.5*1000))
                        thrBase.append(pigpio.pulse(0,1<<thrPin,8.5*1000))

                        thrPi.wave_add_generic(thrBase)

                        thrWid = thrPi.wave_create()

                        if thrWid >=0:
                                thrPi.wave_send_repeat(thrWid)
                                time.sleep(float(1)/float(10))
                                thrPi.wave_tx_stop()
                                thrPi.wave_delete(thrWid)

                        thrPulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                        thrSig.append(pigpio.pulse(1<<thrPin,0,thrPulseLen*1000))
                        thrSig.append(pigpio.pulse(0,1<<thrPin,(10 - thrPulseLen)*1000))

                        stPulseLen = float(1.5)+ (float(0.5)*(float(x)/float(100)))
                        stSig.append(pigpio.pulse(1<<stPin,0,stPulseLen*1000))
                        stSig.append(pigpio.pulse(0,1<<stPin,(10-stPulseLen)*1000))

                        
                        thrPi.wave_add_generic(thrSig)
                        stPi.wave_add_generic(stSig)
                        

                        thrWid = thrPi.wave_create()
                        
                        stWid = stPi.wave_create()
                        
                        if (thrWid >=0 and stWid >=0):
                                thrPi.wave_send_repeat(thrWid)
                                stPi.wave_send_repeat(stWid)
                                try:
                                        time.sleep(float(0.5))
                                        thrPi.wave_tx_stop()
                                        thrPi.wave_delete(thrWid)
                                        stPi.wave_tx_stop()
                                        stPi.wave_delete(stWid)
                                except KeyboardInterrupt:
                                        thrPi.wave_tx_stop()
                                        thrPi.wave_delete(thrWid)
                                        stPi.wave_tx_stop()
                                        stPi.wave_delete(stWid)
                                        print 'keyboard stopped'
                                        mybreak(thrPin)
                                        thrPi.stop
                                        stPi.stop
                

        def mybreak(pin):
                bGPIO=pin
                bsquare=[]
                bpi = pigpio.pi()
                bpi.set_mode(bGPIO,pigpio.OUTPUT)

                bsquare.append(pigpio.pulse(1<<bGPIO,0,1.5*1000))
                bsquare.append(pigpio.pulse(0,1<<bGPIO,8.5*1000))

                bpi.wave_add_generic(bsquare)

                bwid = bpi.wave_create()
                if bwid >=0:
                        bpi.wave_send_repeat(bwid)
                        time.sleep(float(1)/float(2))
                        bpi.wave_tx_stop()
                        bpi.wave_delete(bwid)
                bpi.stop
                




pi2 = pigpio.pi()
pi2.set_mode(14,pigpio.OUTPUT)
base_thr = []
base_thr.append(pigpio.pulse(1<<14,0,1.5*1000))
base_thr.append(pigpio.pulse(0,1<<14, 8.5*1000))
pi2.wave_add_generic(base_thr)
th_wid = pi2.wave_create()
if th_wid >= 0:
        pi2.wave_send_repeat(th_wid)


pi1 = pigpio.pi()
pi1.set_mode(23,pigpio.OUTPUT)
base_st = []
base_st.append(pigpio.pulse(1<<23,0,1.5*1000))
base_st.append(pigpio.pulse(0,1<<23, 8.5*1000))
pi2.wave_add_generic(base_st)
st_wid = pi1.wave_create()
if st_wid >= 0:
        pi1.wave_send_repeat(st_wid)

def throttle(x,pi):
        if(x >=-100 and x<=100):
                pi.wave_tx_stop()
                GPIO=14
                square1=[]
                square2=[]
                pi = pigpio.pi()
                pi.set_mode(GPIO,pigpio.OUTPUT)
                if x <= 0:
                        square1.append(pigpio.pulse(1<<GPIO,0,1.5*1000))
                        square1.append(pigpio.pulse(0,1<<GPIO,8.5*1000))

                        pi.wave_add_generic(square1)

                        wid = pi.wave_create()

                        if wid >=0:
                                pi.wave_send_repeat(wid)
                                time.sleep(float(1)/float(20))
                                pi.wave_tx_stop()
                                pi.wave_delete(wid)

                pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                square2.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
                square2.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))
                pi.wave_add_generic(square2)
                wid = pi.wave_create()

                if wid >=0:
                        pi.wave_send_repeat(wid)
                        try:
                                time.sleep(float(0.5))
                                #pi.wave_tx_stop()
                                pi.wave_delete(wid)
                        except KeyboardInterrupt:
                                throttle(0,pi)

                return pi




def turn(x,pi):
        if (x >=-100 and x <=100):
                pi.wave_tx_stop()
                GPIO = 23
                square=[]
                pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                square.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
                square.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))
                pi.wave_add_generic(square)
                wid = pi.wave_create()
                try:
                        if wid	>= 0:
                                pi.wave_send_repeat(wid)
                                time.sleep(float(1)/float(10))
                                #time.sleep(1)
                                #pi.wave_tx_stop()
                                pi.wave_delete(wid)
                                pi.stop
                except KeyboardInterrupt:
                        turn(0,pi)
                return pi


class rcFull:

        def __init__(self,num1,num2,num3):
                if type(num1) is not int:
                        raise TextProcError("Requires int")
                if type(num2) is not int:
                        raise TextProcError("Requires int")
                if type(num3) is not int:
                        raise TextProcError("Requires int")
                self.num1 = num1
                self.num2 = num2
                self.num3 = num3

        
        def RC(self):
                x = self.num1
                y = self.num2
                z = self.num3
                if(x >=-100 and x<=100 and y >=-100 and y <= 100 and (z==0 or z==1)):
                        thrPin=14
                        stPin=21
                        thrBase=[]
                        thrSig=[]
                        stSig=[]
                        thrPi = pigpio.pi()
                        thrPi.set_mode(thrPin,pigpio.OUTPUT)
                        stPi = pigpio.pi()
                        stPi.set_mode(stPin,pigpio.OUTPUT)
                        #initialize the first signal to send to the throttle motor
                        
                        thrBase.append(pigpio.pulse(1<<thrPin,0,1.5*1000))
                        thrBase.append(pigpio.pulse(0,1<<thrPin,8.5*1000))

                        thrPi.wave_add_generic(thrBase)

                        thrWid = thrPi.wave_create()

                        if thrWid >=0:
                                thrPi.wave_send_repeat(thrWid)
                                time.sleep(float(1)/float(10))
                                thrPi.wave_tx_stop()
                                thrPi.wave_delete(thrWid)

                        thrPulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                        thrSig.append(pigpio.pulse(1<<thrPin,0,thrPulseLen*1000))
                        thrSig.append(pigpio.pulse(0,1<<thrPin,(10 - thrPulseLen)*1000))

                        stPulseLen = float(1.5)+ (float(0.5)*(float(y)/float(100)))
                        stSig.append(pigpio.pulse(1<<stPin,0,stPulseLen*1000))
                        stSig.append(pigpio.pulse(0,1<<stPin,(10-stPulseLen)*1000))

                        
                        thrPi.wave_add_generic(thrSig)
                        stPi.wave_add_generic(stSig)
                        

                        #thrWid = thrPi.wave_create()
                        
                        stWid = stPi.wave_create()
                        
                        if (thrWid >=0 and stWid >=0):
                                thrPi.wave_send_repeat(thrWid)
                                stPi.wave_send_repeat(stWid)
                                try:
                                        time.sleep(float(0.5))
                                        #thrPi.wave_tx_stop()
                                        #thrPi.wave_delete(thrWid)
                                        stPi.wave_tx_stop()
                                        stPi.wave_delete(stWid)
                                except KeyboardInterrupt:
                                        thrPi.wave_tx_stop()
                                        thrPi.wave_delete(thrWid)
                                        stPi.wave_tx_stop()
                                        stPi.wave_delete(stWid)
                                        print 'keyboard stopped'
                                        mybreak(thrPin)
                                        thrPi.stop
                                        stPi.stop

                else:
                        print "Usage: x,y between -100 and 100, z either 1 or 0"
                return (thrPulseLen, stPulseLen, z)


        
        def mybreak(pin):
                bGPIO=pin
                bsquare=[]
                bpi = pigpio.pi()
                bpi.set_mode(bGPIO,pigpio.OUTPUT)

                bsquare.append(pigpio.pulse(1<<bGPIO,0,1.5*1000))
                bsquare.append(pigpio.pulse(0,1<<bGPIO,8.5*1000))

                bpi.wave_add_generic(bsquare)

                bwid = bpi.wave_create()
                if bwid >=0:
                        bpi.wave_send_repeat(bwid)
                        time.sleep(float(1)/float(2))
                        bpi.wave_tx_stop()
                        bpi.wave_delete(bwid)
                bpi.stop
                return 1.5

for i in range(0,100,5):
	turn(i,pi1)

for i in range(0,100,5):
	turn(-i,pi1)
turn(0,pi1)

'''
while True:
        turn(80,pi1)
'''
for i in range(20,25):
	throttle(i,pi2)
	
for i in range(20,25):
	throttle(-i,pi2)

throttle(0,pi2)

'''
for i in range(20,25):
        #throttle(i)
        turn(i)
'''






