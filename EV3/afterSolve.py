#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Direction, Port
from pybricks.tools import print
import rcMover as rm
import sys
args = sys.argv
L = 40  #run_until_stalledメソッドを実行するときのトルクの強さ.

#平均律周波数.
lG = 195.998
lA = 220.000
lB = 246.942
dC = 261.626
dD = 293.665
dE = 329.628
dF = 349.228
dG = 391.995
dA = 440.000
dB = 493.883
hC = 523.251
hD = 587.330
hE = 659.255
hF = 698.456
hG = 783.991

def fanfare():
	b_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
	rm.reset_motor(L)
	rm.target_motor(200)
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