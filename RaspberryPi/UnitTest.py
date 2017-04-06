#!/usr/bin/env python3
#unit testing pigpio
#DevOps Tools and methods

import unittest
import pigpioTest
import time

class pigpioTestCase(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
    def setUp(self):
        pass

    def tearDown(self):
        pass
 
    def test_init(self):
        pass     

    #Test the functions from the pigpioTest functions
    #the time.sleep call is to allow the hardware to have response time
    #during the test video for physical verification of signal

    
    def test_throttle4(self):
        time.sleep(1)
        forward = 25
        p = pigpioTest.RcFuncs(forward)
        movec1 = 1.625
        self.assertEqual(p.throttle(),movec1,"Throttle percent not correct")


    def test_throttle3(self):
        time.sleep(1)
        forward = 20
        p = pigpioTest.RcFuncs(forward)
        movec1 = 1.6
        self.assertEqual(p.throttle(),movec1,"Throttle percent not correct")

    def test_trottle2(self):
        time.sleep(1)
        back = -25
        p = pigpioTest.RcFuncs(back)
        moveB20 = 1.375
        self.assertEqual(p.throttle(), moveB20, "Backwards 20 percent not correct")

    def test_throttle1(self):
        time.sleep(1)
        back = -20
        p = pigpioTest.RcFuncs(back)
        moveB40 = 1.4
        self.assertEqual(p.throttle(), moveB40, "Backwards 40 percent not correct")

    def test_reset(self):
        time.sleep(1)
        center = 0
        p = pigpioTest.RcFuncs(center)
        cent0 = 1.5
        self.assertEqual(p.turn(), cent0, "did not get correct percent for original position")

    def test_turn6(self):
        time.sleep(1)
        left = 100
        p = pigpioTest.RcFuncs(left)
        turn = 2.0
        self.assertEqual(p.turn(), turn, "Full turn right percent not correct")
        
    def test_turn5(self):
        time.sleep(1)
        right = -100
        p = pigpioTest.RcFuncs(right)
        turnRF = 1.0
        self.assertEqual(p.turn(), turnRF, "Full turn right percent not correct")        
        
    def test_turn4(self):
        time.sleep(1)
        left = 60
        p = pigpioTest.RcFuncs(left)
        turnL60 = 1.8
        self.assertEqual(p.turn(), turnL60, "Turn L60 percent not correct")

    def test_turn3(self):
        time.sleep(1)
        right = -60
        p = pigpioTest.RcFuncs(right)
        turnR60 = 1.2
        self.assertEqual(p.turn(), turnR60, "Turn right percent not correct")
        
    def test_turn2(self):
        time.sleep(1)
        left = 20
        p = pigpioTest.RcFuncs(left)
        turnL20 = 1.6
        self.assertEqual(p.turn(),turnL20, "Turn percent not correct")

    def test_turn1(self):
        time.sleep(1)
        right = -20
        p = pigpioTest.RcFuncs(right)
        turn = 1.4
        self.assertEqual(p.turn(),turn, "Turn percent not correct")

    def test_RC(self):
        time.sleep(1)
        x,y,z = 20,70,0
        p = pigpioTest.rcFull(x,y,z)
        output = (1.6, 1.85,0)
        self.assertEqual(p.RC(),output,"Touples did not match")

    def test_init(self):
        myNum = 60
        p = pigpioTest.RcFuncs(myNum)
        self.assertEqual(p.num,myNum,"num does not match the number")



unittest.main()
#suite = unittest.TestLoader().loadTestsFromTestCase(pigpioTestCase)
#unittest.TextTestRunner(verbosity=2).run(suite)


