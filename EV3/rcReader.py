#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import print
import rcMover as rm

readColor_path = 'readColor.txt'
ac_S = rm.ac_S
b_S = rm.b_S

state_rgb = [[(0.0, 0.0, 0.0) for i in range(3)] for j in range(8)]
state_co = [-1 for i in range(8)]
state_cp = [-1 for i in range(8)]

amotor = Motor(Port.A)
bmotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
cmotor = Motor(Port.C)
cs = ColorSensor(Port.S1)

def read_color(index):
	rgb = cs.rgb()
	rgb255 = (rgb[0] * 2.55 * 255/180, rgb[1] * 2.55, rgb[2] * 2.55)
	print('R: {:7.2f} G: {:7.2f} B: {:7.2f}'.format(rgb255[0], rgb255[1], rgb255[2]))
	state_rgb[index[0]][index[1]] = rgb255

def read_four(first, second, third, fourth):
	cmotor.run_until_stalled(ac_S,Stop.HOLD,60)

	bmotor.reset_angle(0)
	bmotor.run_target(b_S,80,Stop.HOLD)
	read_color(first)
	bmotor.run_target(b_S,170,Stop.HOLD)
	read_color(second)
	bmotor.run_target(b_S,260,Stop.HOLD)
	read_color(third)
	bmotor.run_target(b_S,350,Stop.HOLD)
	read_color(fourth)
	bmotor.run_target(b_S,360,Stop.HOLD)

	cmotor.run_until_stalled(-ac_S,Stop.BRAKE,100)

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
	L = rm.stall_torque  # run_until_stalledメソッドを実行するときのトルクの強さ.
	A_target_of_Y = rm.Y_target  # YするときのAモーターのターゲット.
	cmotor.run_until_stalled(-ac_S,Stop.BRAKE,100)

	rm.reset_motor(L)
	rm.target_motor(A_target_of_Y)

	read_four((1,0), (2,0), (3,0), (0,0))
	rm.Zd_move(0)
	rm.target_motor(A_target_of_Y)

	read_four((5,1), (6,2), (2,1), (1,2))
	rm.Zd_move(0)
	rm.target_motor(A_target_of_Y)

	read_four((4,0), (7,0), (6,0), (5,0))
	rm.Zd_move(0)
	rm.target_motor(A_target_of_Y)

	read_four((0,1), (3,2), (7,1), (4,2))
	bmotor.reset_angle(0)
	rm.Yc_move(0)
	rm.Zd_move(0)
	rm.target_motor(A_target_of_Y)

	read_four((2,2), (6,1), (7,2), (3,1))
	rm.Z2_move(0)
	rm.target_motor(A_target_of_Y)

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