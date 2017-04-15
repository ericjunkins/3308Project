#!/usr/bin/env python

import time
import pigpio

'''
#This file contains the methods used to control movement of the RC car. The
#methods turn and throttle will be called on numbers that are precentages of
#their max in each direction, and will output a signal and will not kill that
#signal until they are called again. This reduces the number of necessary
#function calls as well as speeds up the program by not having to talk to
#gpio pins more than necessary. 
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#      Uncomment the section below to run a test Function from this program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
pi1.wave_add_generic(base_st)
st_wid = pi1.wave_create()
if st_wid >= 0:
        pi1.wave_send_repeat(st_wid)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Need to have an initial wave id of zero
wid =0

#throttle is the function to move the Rc car forward/backward
def throttle(x,pi):
        
        #x is the percent of max to throttle forward (+) or backward(-)
        if(x >=-100 and x<=100):
                
                #have to stop the instance of pi to not crash the raspberry pi
                pi.wave_tx_stop()
                
                #throttle uses gpio pin 14
                GPIO=14
                square1=[]
                square2=[]
                pi = pigpio.pi()
                pi.set_mode(GPIO,pigpio.OUTPUT)
                
                #if you tell the car to go backwards it has to either have gotten
                #a negative value previously, or a baseline signal of 1.5
                #TODO build in check for previous output for that case
                if (x <= 0):
                        
                        #build base signal of 1.5ms on, 8.5 off
                        square1.append(pigpio.pulse(1<<GPIO,0,1.5*1000))
                        square1.append(pigpio.pulse(0,1<<GPIO,8.5*1000))

                        pi.wave_add_generic(square1)
                        wid = pi.wave_create()
                        
                        #if the wave id was created sucessfully
                        if wid >=0:
                                pi.wave_send_repeat(wid)
                                time.sleep(float(1)/float(20))
                                pi.wave_tx_stop()
                                pi.wave_delete(wid)
                                
                #pulseLen is the signal corresponding to turning. This will be
                #between 1.0ms and 2.0ms depending on input x
                                
                pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                square2.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
                square2.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))
                pi.wave_add_generic(square2)
                wid = pi.wave_create()

                if wid >=0:
                        pi.wave_send_repeat(wid)
                        pi.wave_delete(wid)
                        pi.stop()
                        '''
                        #important to note the signal is NOT stopped from this,
                        #it will continue until the function is called again
                        #and recieves pi.wave_tx_stop()
                        '''
                return pi



#turn is the function that control the steering of the RC car, it is almost
#identical to throttle except for output pins and not requiring a base signal       
def turn(x,pi):
        if (x >=-100 and x <=100):
                pi.wave_tx_stop()
                
                #steering uses gpio pin 23
                GPIO = 23
                square=[]
                pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                square.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
                square.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))
                pi.wave_add_generic(square)
                wid = pi.wave_create()
                if wid	>= 0:
                        pi.wave_send_repeat(wid)
                        pi.wave_delete(wid)
                        pi.stop

                return pi

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                             For Unittesting
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        
class TextProcError(Exception):
        def _init_(self,msg):

                super().__init__(msg)

class RcFuncs:
                
        def __init__(self,num):
                if type(num) is not int:
                        raise TextProcError("Requires int")
                self.num = num

        #Controls the steering of the Rc car
        def turn(self):
                x = self.num
                #Signals are percents of turning, negative meaning left
                if (x >=-100 and x <=100):
                        #Steering uses gpio pin 23
                        GPIO =23
                        square=[]
                        pi = pigpio.pi()
                        pi.set_mode(GPIO,pigpio.OUTPUT)
                        pulseLen = float(1.5)+(float(0.5)*(float(x)/float(100)))
                        square.append(pigpio.pulse(1<<GPIO,0,pulseLen*1000))
                        square.append(pigpio.pulse(0,1<<GPIO,(10 - pulseLen)*1000))
                        pi.wave_add_generic(square)

                        wid = pi.wave_create()

                        if wid	>= 0:
                                pi.wave_send_repeat(wid)
                                time.sleep(float(1)/float(10))
                                pi.wave_tx_stop()
                                pi.wave_delete(wid)

                                pi.stop
                                
                        return pulseLen
        
        #Controls the movemnt of the Rc car
        def throttle(self):
                x = self.num
                if(x >=-100 and x<=100):
                        #Throttle uses gpio pin 14
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






