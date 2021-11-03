#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Direction, Port, Stop, Color
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

readColor_path = 'readColor.txt'

S = 230

state_rgb = [[(0.0, 0.0, 0.0) for i in range(3)] for j in range(8)]
state_co = [-1 for i in range(8)]
state_cp = [-1 for i in range(8)]

amotor = Motor(Port.A)
bmotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
cmotor = Motor(Port.C)
cs = ColorSensor(Port.S1)

def read_color(index):
	rgb = cs.rgb()
	rgb255 = tuple(map(lambda x: x * 2.55, rgb))
	print('R:' + str(round(rgb255[0], 2)) + ' G:' + str(round(rgb255[1], 2)) + ' B:' + str(round(rgb255[2], 2)))
	state_rgb[index[0]][index[1]] = rgb255

def read_four(first, second, third, fourth):
	cmotor.run_until_stalled(S,Stop.COAST,60)

	bmotor.reset_angle(0)
	bmotor.run_target(S,90,Stop.HOLD)
	read_color(first)
	bmotor.run_target(S,180,Stop.HOLD)
	read_color(second)
	bmotor.run_target(S,270,Stop.HOLD)
	read_color(third)
	bmotor.run_target(S,360,Stop.HOLD)
	read_color(fourth)

	cmotor.run_until_stalled(-S,Stop.BRAKE,100)

def RGB_to_HSV(rgb):
	max_value = 0.0
	max_index = 0
	for i, v in enumerate(rgb):
		if v > max_value:
			max_value = v
			max_index = i
	min_value = min(rgb)
	V = max_value
	H = 0.0
	S = 0.0

	if max_value == 0.0:
		return (H, S, V)
	max_sub_min = max_value - min_value
	S = 255 * max_sub_min / max_value

	if max_index == 0:
		H = 60 * (rgb[1] - rgb[2]) / max_sub_min
	elif max_index == 1:
		H = 60 * (2 + (rgb[2] - rgb[0]) / max_sub_min)
	elif max_index == 2:
		H = 60 * (4 + (rgb[0] - rgb[1]) / max_sub_min)
	if H < 0.0:
		H += 360
	return (H, S, V)

def read_all():
	L = 40  #run_until_stalledメソッドを実行するときのトルクの強さ.
	cmotor.run_until_stalled(-S,Stop.BRAKE,100)

	rm.reset_motor(L)
	rm.target_motor(200)

	read_four((1,0), (2,0), (3,0), (0,0))
	rm.Zd_move(0)
	rm.target_motor(200)

	read_four((5,1), (6,2), (2,1), (1,2))
	rm.Zd_move(0)
	rm.target_motor(200)

	read_four((4,0), (7,0), (6,0), (5,0))
	rm.Zd_move(0)
	rm.target_motor(200)

	read_four((0,1), (3,2), (7,1), (4,2))
	bmotor.reset_angle(0)
	rm.Yc_move(0)
	rm.Zd_move(0)
	rm.target_motor(200)

	read_four((2,2), (6,1), (7,2), (3,1))
	rm.Z2_move(0)
	rm.target_motor(200)

	read_four((0,2), (4,1), (5,2), (1,1))
	bmotor.reset_angle(0)
	ayd_angle = rm.Yd_move(0)
	rm.Zd_move(0)
	rm.Yd_move(ayd_angle)

	with open(readColor_path, mode="w") as f:
		for part in state_rgb:
			part_color_list = []
			for rgb in part:
				part_color_list.append(','.join(map(str, rgb)))
			f.write(':'.join(part_color_list) + '\n')

if __name__ == '__main__':
	read_all()