#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Direction, Port
from pybricks.tools import print
import rcMover as rm
import sys
args = sys.argv

def fanfare():
	b_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
	rm.reset_motor(rm.stall_torque)
	rm.target_motor(rm.Y_target)
	b_motor.run_angle(90,360)

def main():
	if len(args) < 2:
		print("Usage: rcSolver.py (solve way)")
		sys.exit()
	DYZ_ways = args[1]
	print("DYZ_ways:", DYZ_ways)
	rm.execute(DYZ_ways) # rcMoverで動かす.
	fanfare()

if __name__ == '__main__':
	main()