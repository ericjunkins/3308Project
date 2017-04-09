import time
import RPi.GPIO as GPIO
#from _future_ import division

#Test script for motor control signals

ms_units = 1000
baseline = 1.5/ms_units
single = 1/ms_units
entire_cycle = 10
GPIO.setwarnings(False)

#want to command GPIO channel 14 on digital output signals
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(14,GPIO.OUT)

#the baseline signal should be sent constantly to the servo/speed
#controller while the device is one.
def base_signal():
	print 'high signal start',time.ctime()
	GPIO.output(14,True)
	time.sleep(baseline)
	print 'low signal start', time.ctime()
	GPIO.output(14,False)
	time.sleep(entire_cycle - baseline)
	print 'low signal end' , time.ctime()
	GPIO.cleanup()
	
def turn(x):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23,GPIO.OUT)
        pulseLen = float(1.5)-(float(0.5)*((float(x)/float(100))))
        #print pulseLen
        try:
                #print 'high signal start', time.ctime()
                GPIO.output(23,True)
                time.sleep(pulseLen/ms_units)
                #print 'high signal end', time.ctime()
                GPIO.output(23,False)
                time.sleep(((entire_cycle - pulseLen -.2)/ms_units))
                #print 'low signal stop', time.ctime()
        except KeyboardInterrupt:
                GPIO.cleanup()
                


def turn_left(x):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14,GPIO.OUT)
        #Sending pulse of 150hz
        for i in range(0,100):
                try:
                        pulseLen=1.5+(0.5*(x/100))
                        GPIO.output(14,True)
                        time.sleep(pulseLen/ms_units)
                        GPIO.output(14,False)
                        time.sleep((entire_cycle-pulseLen)/ms_units)
                except KeyboardInterrupt:
                        turn_left(0)
                        GPIO.cleanup() 
'''
'''
def gpioOutput(x):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(x,GPIO.OUT)
        try:
                GPIO.output(x,1)
                time.sleep(5)
                GPIO.output(x,0)
        except KeyboardInterrupt:
                GPIO.cleanup()
#gpioOutput(40)
#turn_left(100)
#turn_right(100)
'''                
turn_left(0)
time.sleep(1)
turn_right(100)
time.sleep(1)
turn_right(0)
time.sleep(1)
turn_left(100)
time.sleep(1)
turn_left(0)
time.sleep(1)
turn_left(100)
time.sleep(1)
turn_right(100)
'''

def ThrottleUp(x):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14,GPIO.OUT)
        for i in range(0,100):
                try:
                        T = 10
                        pulseLen = 0.2*(T)
                        #print 'high signal start', time.ctime()
                        GPIO.output(14,True)
                        time.sleep(pulseLen/ms_units)
                        #print 'high signal end', time.ctime()
                        GPIO.output(14,False)
                        time.sleep((T-pulseLen)/ms_units)
                        #print 'low signal stop', time.ctime()
                except KeyboardInterrupt:
                        GPIO.cleanup()


#ThrottleUp(1)
#turn_right(100)

def mytest():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14,GPIO.OUT)
        while(True):
                try:
                        GPIO.output(14,1)
                        time.sleep(2/1000)
                        GPIO.output(14,0)
                        time.sleep(8/1000)

                except KeyboardInterrupt:
                        GPIO.cleanup()

'''
for i in range(0,100):
        turn(i)
for i in range(0,100):
        turn(-i)
'''

while (True):
        turn(0)        

