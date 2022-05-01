#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Direction, Port, Stop
from pybricks.tools import wait

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

# 各回転記号(UFRDYZ)の回転する向きは，以下参照. ただし，ZだけZとZ'が逆
# https://tribox.com/3x3x3/solution/notation/

amotor = Motor(Port.A)
bmotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
cmotor = Motor(Port.C)
S = 230            #モーターの回るスピード.
stall_torque = 50  #run_until_stalledメソッドを実行するときのトルクの強さ.

def nsign(num):
    return -1 * ((num > 0) - (num < 0))

def reset_motor(torque):
	amotor.run_until_stalled(S,Stop.HOLD,torque)
	amotor.reset_angle(270) # マシンVer.3.0の時.
def target_motor(num):
	nsi = nsign(amotor.angle() - num)
	if nsi != 0:
		amotor.run_target(nsi*S, num, Stop.HOLD)

def main():
	brick.sound.beep(dC,150,50)
	wait(350)
	brick.sound.beep(lG,150,50)
	wait(350)
	brick.sound.beep(dC,150,50)
	wait(350)
	brick.sound.beep(hC,200.50)
	cmotor.run_until_stalled(-S,Stop.COAST,stall_torque)
	reset_motor(stall_torque)
	# way = "Z2 D2 Z D2 Y Z D3 Y Z D2 Z3 D3 Z D Z D2 Z D3 Y2 Z D"
	# #      8  2  7 2  4 7 3  4 7 2  9  3  7 3 7 2  7 3  5  7 1
	# w_r = "D3 Z3 Y2 D Z3 D2 Z3 D3 Z3 D Z D2 Z3 Y3 D Z3 Y3 D2 Z3 D2 Z2"
	way = 'Z2'
	execute(way)

def execute(way):
	reset_motor(stall_torque)
	bmotor.reset_angle(0)
	sum_angle = 0
	move_dict = {
		"D" : Dd_move,
		"D2": D2_move,
		"D3": Dc_move,
		"Y" : Yd_move,
		"Y2": Y2_move,
		"Y3": Yc_move,
		"Z" : Zd_move,
		"Z2": Z2_move,
		"Z3": Zc_move,
		"R" : Reset 
	}
	for move_name in way.split(' '):
		try:
			sum_angle = move_dict[move_name](sum_angle)
		except KeyError:
			break

D_target = 245
def Dd_move(target): # D
	reset_motor(stall_torque)
	target_motor(D_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+95, Stop.HOLD)
	bmotor.run_angle(-S, 5, Stop.HOLD)
	return target + 90

def D2_move(target): # D2
	reset_motor(stall_torque)
	target_motor(D_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+185, Stop.HOLD)
	bmotor.run_angle(-S, 5, Stop.HOLD)
	return target + 180

def Dc_move(target): # D'
	reset_motor(stall_torque)
	target_motor(D_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+275, Stop.HOLD)
	bmotor.run_angle(-S, 5, Stop.HOLD)
	return target + 270

Y_target = 190
def Yd_move(target): # Y
	target_motor(Y_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S,target + 270,Stop.HOLD)
	return target + 270

def Y2_move(target): # Y2
	target_motor(Y_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+180, Stop.HOLD)
	return target + 180

def Yc_move(target): # Y'
	target_motor(Y_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+90, Stop.HOLD)
	return target + 90

def Zd_move(target): # Z
	target_motor(180)
	amotor.run_angle(S,-140,Stop.HOLD)
	#amotor.run_angle(S,40,Stop.HOLD)
	#amotor.run_angle(S,-40,Stop.HOLD)
	reset_motor(stall_torque)
	return target

def Z2_move(target): # Z2
	Zd_move(target)
	Zd_move(target)
	return target

def Zc_move(target): # Z'
	Zd_move(target)
	Zd_move(target)
	Zd_move(target)
	return target

def Reset(target): # R
	target_motor(stall_torque)
	return target

if __name__ == '__main__':
	main()