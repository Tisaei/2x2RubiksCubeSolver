#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import print, wait
import rcMover as rm
import sys
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
S = 230
part_sets = {
		frozenset(['W', 'B', 'R']): 0, 
		frozenset(['W', 'R', 'G']): 1, 
		frozenset(['W', 'G', 'O']): 2, 
		frozenset(['W', 'O', 'B']): 3, 
		frozenset(['Y', 'R', 'B']): 4, # これを基準パーツとする
		frozenset(['Y', 'G', 'R']): 5, 
		frozenset(['Y', 'O', 'G']): 6, 
		frozenset(['Y', 'B', 'O']): 7
}
standard_orientation = { # (基準パーツの黄色の位置):(順列,方向の下2ビット)
		(0,0): (1,0b00),
		(0,1): (3,0b00),
		(0,2): (5,0b00),
		(1,0): (0,0b10),
		(1,1): (2,0b10),
		(1,2): (4,0b10),
		(2,0): (1,0b11),
		(2,1): (3,0b11),
		(2,2): (5,0b11),
		(3,0): (0,0b01),
		(3,1): (2,0b01),
		(3,2): (4,0b01),
		(4,0): (0,0b00),
		(4,1): (2,0b00),
		(4,2): (4,0b00),
		(5,0): (1,0b10),
		(5,1): (3,0b10),
		(5,2): (5,0b10),
		(6,0): (0,0b11),
		(6,1): (2,0b11),
		(6,2): (4,0b11),
		(7,0): (1,0b01),
		(7,1): (3,0b01),
		(7,2): (5,0b01)
}

pre_state = [[0 for i in range(3)] for j in range(8)]
state_co = [-1 for i in range(8)]
state_cp = [-1 for i in range(8)]

def read_color(index):
	thresholdBetweenRedOrange = 59
	color = cs.color()
	reflection = cs.reflection()
	if color == Color.BLACK:
		print("BLACK  - GREEN ,", reflection)
		color = 'G'
	elif color == Color.BLUE:
		if reflection < 21:
			print("BLUE  -BLUE  ,", reflection)
			color = 'B'
		elif reflection < 50 and reflection >= 21:
			print("BLUE  -WHITE ,", reflection)
			color = 'W'
		elif reflection < 71 and reflection >= 50:
			print("BLUE  -ORANGE,", reflection)
			color = "O"
		else:
			print("BLUE  -YELLOW,", reflection)
			color = 'Y'
	elif color == Color.GREEN:
		print("GREEN -GREEN ,", reflection)
		color = 'G'
	elif color == Color.YELLOW:
		if reflection < thresholdBetweenRedOrange:
			print("YELLOW-RED   ,", reflection)
			color = 'R'
		elif reflection < 71 and reflection >= thresholdBetweenRedOrange:
			print("YELLOW-ORANGE,", reflection)
			color = "O"
		else:
			print("YELLOW-YELLOW,", reflection)
			color = 'Y'
	elif color == Color.RED:
		if reflection < thresholdBetweenRedOrange:
			print("RED   -RED   ,", reflection)
			color = 'R'
		elif reflection < 71 and reflection >= thresholdBetweenRedOrange:
			print("RED   -ORANGE,", reflection)
			color = "O"
		else:
			print("RED   -YELLOW,", reflection)
			color = 'Y'
	elif color == Color.WHITE:
		if reflection < 19:
			print("WHITE -BLUE  ,", reflection)
			color = 'B'
		else:
			print("WHITE -WHITE ,", reflection)
			color = 'W'
	elif color == Color.BROWN:
		print("BROWN -BROWN ,", reflection)
		color = 'None'
	if color == 'None':
		brick.display.clear()
		print("Sorry, I can't read color.")
		for i in range(5):
			brick.sound.beep(hC)
			brick.sound.beep(dB)
		sys.exit()
	if color == 'W' or color == 'Y':
		if state_co[index[0]] == -1:
			state_co[index[0]] = index[1]
		else:
			brick.display.clear()
			print("I already assigned white or yellow:"+str(index[0])+","+str(index[1]))
			# for i in range(5):
			# 	brick.sound.beep(hC)
			# 	brick.sound.beep(dB)
			sys.exit()
	pre_state[index[0]][index[1]] = color

def read_four(first, second, third, fourth):
	degree = 30
	cmotor.run_until_stalled(S,Stop.COAST,60)
	cmotor.run_angle(-S,degree,Stop.HOLD)

	bmotor.reset_angle(0)
	bmotor.run_target(S,70,Stop.HOLD)
	read_color(first)
	bmotor.run_target(S,160,Stop.HOLD)
	read_color(second)
	bmotor.run_target(S,250,Stop.HOLD)
	read_color(third)
	bmotor.run_target(S,340,Stop.HOLD)
	read_color(fourth)
	bmotor.run_target(S,360,Stop.HOLD)
	print()

	cmotor.run_until_stalled(-S,Stop.BRAKE,100)

amotor = Motor(Port.A)
bmotor = Motor(Port.B)
cmotor = Motor(Port.C)
cs = ColorSensor(Port.S1)

def read_all():
	print("原色  -判断色,反射光")
	cmotor.run_until_stalled(-S,Stop.BRAKE,100)

	rm.reset_motor()
	amotor.run_angle(S,-90,Stop.HOLD)

	read_four((1,0), (2,0), (3,0), (0,0))
	rm.Zd_move(0)
	amotor.run_angle(S,-90,Stop.HOLD)

	read_four((5,1), (6,2), (2,1), (1,2))
	rm.Zd_move(0)
	amotor.run_angle(S,-90,Stop.HOLD)

	read_four((4,0), (7,0), (6,0), (5,0))
	rm.Zd_move(0)
	amotor.run_angle(S,-90,Stop.HOLD)

	read_four((0,1), (3,2), (7,1), (4,2))
	bmotor.reset_angle(0)
	rm.Yc_move(0)
	rm.Zd_move(0)
	amotor.run_angle(S,-90,Stop.HOLD)

	read_four((2,2), (6,1), (7,2), (3,1))
	rm.Z2_move(0)
	amotor.run_angle(S,-90,Stop.HOLD)

	read_four((0,2), (4,1), (5,2), (1,1))
	bmotor.reset_angle(0)
	ayd_angle = rm.Yd_move(0)
	rm.Zd_move(0)
	rm.Yd_move(ayd_angle)

	for i in range(8):
		if state_co[i] == -1:
			brick.display.clear()
			print("not input enough white or yellow")
			print(str(state_co))
			# for i in range(5):
			# 		brick.sound.beep(hC)
			# 		brick.sound.beep(dB)
			sys.exit()
	for i in range(8):
		if part_sets[frozenset(pre_state[i])] == 4:
			per_ori = standard_orientation[(i, pre_state[i].index('Y'))]
			break
	for i in range(8):
		state_cp[i] = part_sets[frozenset(pre_state[i])]
	
	return (state_cp, state_co, per_ori)

if __name__ == '__main__':
	read_all()