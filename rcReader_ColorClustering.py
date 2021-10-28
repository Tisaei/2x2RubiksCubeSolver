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

def read_all():
    print("ColorClustering")

if __name__ == '__main__':
	read_all()