#!/usr/bin/env python3

from subprocess import run, check_output, PIPE
from time import sleep
state_path = 'cube_state_perori.txt'
way_path = 'solve_way.txt'

def main():
	run(['./beforeSolve.py'])
	with open(state_path) as f:
		cube_state_perori_s = f.read().strip()
	cube_state_perori = cube_state_perori_s.split('_')
	print('state:' + cube_state_perori[0])
	print('per_ori:' + cube_state_perori[1])
	state = cube_state_perori[0].split(':')
	per_ori = cube_state_perori[1]

	run(['./rcSolver.out', state[0], state[1]])
	# runメソッドはサブプロセスが終わるまで待ってくれる.
	# この後solve_way.txtから解法を読み取ってaftersolve.pyを実行.
	with open(way_path) as f:
		ways = f.read()
	run(['./afterSolve.py', ways, per_ori])

	# state = '5,2,6,3,4,7,1,0:0,0,0,0,0,0,2,1'.split(':')
	# run(['./rcSolver.out', state[0], state[1]])
	# with open(way_path) as f:
	# 	ways = f.read()
	# run(['./Test.py', ways])

if __name__ == '__main__':
	main()