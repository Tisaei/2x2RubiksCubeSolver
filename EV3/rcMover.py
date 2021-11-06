#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Direction, Port, Stop, SoundFile, Button, Color
from pybricks.tools import wait
from pybricks.tools import print
import re
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

# 各回転記号(UFRDYZ)の回転する向きは，以下参照. ただし，ZだけZとZ'が逆
# https://tribox.com/3x3x3/solution/notation/

amotor = Motor(Port.A)
bmotor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
cmotor = Motor(Port.C)
S = 190 #モーターの回るスピード.
L = 40  #run_until_stalledメソッドを実行するときのトルクの強さ.

def nsign(num):
    return -1 * ((num > 0) - (num < 0))

def reset_motor(torque):
	amotor.run_until_stalled(S,Stop.HOLD,torque)
	amotor.reset_angle(270) # マシンVer.3.0の時.
def target_motor(num):
	nsi = nsign(amotor.angle() - num)
	if nsi != 0:
		amotor.run_target(nsi*S, num, Stop.HOLD)

def most_ori(per_ori): # 向きの最上位ビットを求める
	if per_ori[0] % 2 == 0: # 順列が偶数ならば
		return ((per_ori[1] & 0b10) >> 1 ^ per_ori[1] & 0b01) & 0b01 # 最上位ビット = 最下位ビット xor 真ん中ビット
	else: # 順列が奇数ならば
		return ~((per_ori[1] & 0b10) >> 1 ^ per_ori[1] & 0b01) & 0b01 # 最上位ビット = not(最下位ビット xor 真ん中ビット)
def doY(now_per_ori): # Yした後のper_oriを求める
	next_per = now_per_ori[0] // 2 * 2 + 1 - now_per_ori[0] % 2
	next_ori = now_per_ori[1] >> 1 | ~(now_per_ori[1] & 0b01) << 1 & 0b10
	return (next_per, next_ori)
def doZ(now_per_ori): # Zした後のper_oriを求める
	next_per = (now_per_ori[0] + 3) % 6
	next_ori = ~(most_ori(now_per_ori) << 1) & 0b10 | now_per_ori[1] & 0b01
	return (next_per, next_ori)

def change_direction_to_0and0(pre_per_ori):
	# 入力のper_oriを(0,0b00)にするための動きを返す.
	change_way = ""
	if pre_per_ori[0] == 0 or pre_per_ori[0] == 1:
		temp_per_ori = pre_per_ori
	elif pre_per_ori[0] == 3 or pre_per_ori[0] == 4:
		temp_per_ori = doZ(pre_per_ori)
		change_way += "Z "
	else:
		temp_per_ori = doZ(doY(pre_per_ori))
		change_way = "Y Z "
	
	if most_ori(temp_per_ori) != 0:
		temp_per_ori = doZ(doZ(temp_per_ori))
		change_way += "Z2 "
	
	while(temp_per_ori[1] != 0b00):
		temp_per_ori = doY(temp_per_ori)
		change_way += "Y "
	return change_way.strip()

def main():
	brick.sound.beep(dC,150,50)
	wait(350)
	brick.sound.beep(dC,150,50)
	wait(350)
	brick.sound.beep(dC,150,50)
	wait(350)
	brick.sound.beep(hC,200.50)
	cmotor.run_until_stalled(-S,Stop.COAST,50)
	reset_motor(L)
	# way = "Z2 D2 Z D2 Y Z D3 Y Z D2 Z3 D3 Z D Z D2 Z D3 Y2 Z D"
	# #      8  2  7 2  4 7 3  4 7 2  9  3  7 3 7 2  7 3  5  7 1
	# w_r = "D3 Z3 Y2 D Z3 D2 Z3 D3 Z3 D Z D2 Z3 Y3 D Z3 Y3 D2 Z3 D2 Z2"
	way = 'D2 Z2 D2 Y Z D2 Z2 D2'
	execute(way)

def execute(way):
	reset_motor(L)
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
	}
	for move_name in way.split(' '):
		try:
			sum_angle = move_dict[move_name](sum_angle)
		except KeyError:
			break

D_target = 245
def Dd_move(target): # D
	reset_motor(L)
	target_motor(D_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+95, Stop.HOLD)
	bmotor.run_angle(-S, 5, Stop.HOLD)
	return target + 90

def D2_move(target): # D2
	reset_motor(L)
	target_motor(D_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+185, Stop.HOLD)
	bmotor.run_angle(-S, 5, Stop.HOLD)
	return target + 180

def Dc_move(target): # D'
	reset_motor(L)
	target_motor(D_target)
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+275, Stop.HOLD)
	bmotor.run_angle(-S, 5, Stop.HOLD)
	return target + 270

def Yd_move(target): # Y
	target_motor(200) # マシンVer.3.0の時.
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S,target + 270,Stop.HOLD)
	return target + 270

def Y2_move(target): # Y2
	target_motor(200) # マシンVer.3.0の時.
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+180, Stop.HOLD)
	return target + 180

def Yc_move(target): # Y'
	target_motor(200) # マシンVer.3.0の時.
	amotor.stop(Stop.HOLD)
	bmotor.run_target(S, target+90, Stop.HOLD)
	return target + 90

def Zd_move(target): # Z
	target_motor(180)
	amotor.run_angle(S,-130,Stop.HOLD)
	amotor.run_angle(S,40,Stop.HOLD)
	amotor.run_angle(S,-40,Stop.HOLD)
	reset_motor(L)
	return target

def Z2_move(target): # Z2
	target_motor(180)
	amotor.run_angle(S,-130,Stop.HOLD)
	amotor.run_angle(S,40,Stop.HOLD)
	amotor.run_angle(S,-40,Stop.HOLD)
	reset_motor(L)
	target_motor(180)
	amotor.run_angle(S,-130,Stop.HOLD)
	amotor.run_angle(S,40,Stop.HOLD)
	amotor.run_angle(S,-40,Stop.HOLD)
	reset_motor(L)
	return target

def Zc_move(target): #Z'
	target_motor(180)
	amotor.run_angle(S,-130,Stop.HOLD)
	amotor.run_angle(S,40,Stop.HOLD)
	amotor.run_angle(S,-40,Stop.HOLD)
	reset_motor(L)
	target_motor(180)
	amotor.run_angle(S,-130,Stop.HOLD)
	amotor.run_angle(S,40,Stop.HOLD)
	amotor.run_angle(S,-40,Stop.HOLD)
	reset_motor(L)
	target_motor(180)
	amotor.run_angle(S,-130,Stop.HOLD)
	amotor.run_angle(S,40,Stop.HOLD)
	amotor.run_angle(S,-40,Stop.HOLD)
	reset_motor(L)
	return target

if __name__ == '__main__':
	main()