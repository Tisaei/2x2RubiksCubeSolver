#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, InfraredSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import print, wait, StopWatch
import rcReader as rr
import rcMover as rm
path = "cube_state_perori.txt"

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

class State:
	def __init__(self, cp, co):
		self.cp = cp
		self.co = co

	def apply_move(self, move):
		new_cp = [self.cp[move.cp[i]] for i in range(8)]
		new_co = [(self.co[move.cp[i]]+move.co[i])%3 for i in range(8)]
		return State(new_cp, new_co)

real_move = {
	"Y" : State([3,0,1,2,7,4,5,6], [0,0,0,0,0,0,0,0]),
	"Y2": State([2,3,0,1,6,7,4,5], [0,0,0,0,0,0,0,0]),
	"Y3": State([1,2,3,0,5,6,7,4], [0,0,0,0,0,0,0,0]),
	"Z" : State([1,5,6,2,0,4,7,3], [1,2,1,2,2,1,2,1]),
	"Z2": State([5,4,7,6,1,0,3,2], [0,0,0,0,0,0,0,0]),
	"Z3": State([4,0,3,7,5,1,2,6], [1,2,1,2,2,1,2,1])
}

def angle_adjustment():
	ir = InfraredSensor(Port.S2)
	b_motor = Motor(Port.B)
	sw = StopWatch()
	threshold = 20
	speed = 25

	brick.sound.beep(220.000)
	brick.sound.beep(329.628)

	b_motor.run(speed * 5)
	ird = ir.distance()
	while threshold < ird:
		ird = ir.distance()
		print("\r    now distance: %s" % str(ird), end='')

	b_motor.run(speed * 2)
	while threshold >= ird:
		ird = ir.distance()
		print("\r    now distance: %s" % str(ird), end='')
	b_motor.stop(Stop.HOLD)
	wait(300)

	print()
	sw.resume()
	sw.reset()
	b_motor.run(-speed)
	wait(speed * 20) # speed=25だと500ms待つ.
	ird = ir.distance()
	while True:
		ird_p = ird
		ird = ir.distance()
		if ird_p > ird:
			sw.reset()
		elif ird_p < ird:
			break
		print("\rminimun distance: %s" % str(ird), end='')
	b_motor.stop(Stop.HOLD)
	passed_time = sw.time()
	print("\n            last: %s" % str(passed_time))

	b_motor.run(speed)
	wait(passed_time * 0.6 + 0.2)

	b_motor.stop(Stop.HOLD)


	print()
	brick.sound.beep(329.628)
	brick.sound.beep(220.000)
	wait(1000)

def main():
	# angle_adjustment()
	cp, co, per_ori = rr.read_all() # rcReaderで色を読む.
	cube = State(cp,co)
	alignment = rm.change_direction_to_0and0(per_ori)
	print('alignment: ', alignment)
	for move_name in alignment.split(' '): # rcSolverで解ける形に変換する.
		try:
			cube = cube.apply_move(real_move[move_name])
		except KeyError:
			break
	cp_str = ",".join(map(str,cube.cp))
	co_str = ",".join(map(str,cube.co))
	per_ori_str = ",".join(map(str,per_ori))
	with open(path, mode="w") as f:
		f.write(cp_str + ":" + co_str + "_" + per_ori_str)

if __name__ == "__main__":
	main()