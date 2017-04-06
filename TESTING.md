Who: Joseph Wroe, Eric Junkins, Vilok, JC

Title: RC Car

Vision: Easy access to remote control devices from mobile devices.

Automated Tests: ((Explanation and Screenshot))

User Acceptance Tests: See Below

Part 1:

	Usage:

		sudo pigpiod (note: requires RaspberryPi to run)
		python UnitTest.py 

	Output of Tests:
	
		All tests OK

Part 2:
	Test #1
		Use case name
			Verify calculations for waves
		Description 
			Test the turn() function wave generator calculations
		Pre-conditions
			A value between -100 and 100 was chosen to represent the turn percentage 
		Test steps
			1. python UnitTest.py 
		Expected Results	
			All tests OK
		Actual Results
			All tests OK
		Status
			Pass
		Notes 
			N/A
		Post-condition
			The wheel turned to a precentage corresponding to the input percentage
	Test #2
		Use case name
			Verify calculations for waves
		Description 
			Test the throttle() function wave generator calculations
		Pre-conditions
			A value between -100 and 100 was chosen to represent the throttle percentage 
		Test steps
			1. python UnitTest.py
		Expected Results
			All tests OK
		Actual Results 
			All tests OK
		Status
			Pass
		Notes 
			N/A
		Post-condition
			The throttle accelerated or decelerated corresponding to the input percentage
	Test #3
		Use case name
			Verify (int) checker for input parameter of functions
		Description
			Check that the user has only input a number between -100 and 100 for x,y and 0 or 1 for z
		Pre-conditions
			The user has input a value to turn or throttle
		Test steps
			1. python UnitTest.py
		Expected Results
			All tests OK
		Actual Results
			All tests OK
		Status
			Pass
		Notes
			N/A
		Post-condition
			The checker returned an error if the value was not in the range or the value was not an (int). The checker passed the test if the value was in the range and it was an (int).


