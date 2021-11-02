#!/usr/bin/env python3

from subprocess import run, check_output, PIPE
from time import sleep
import socket
readColor_path = 'readColor.txt'
state_path = 'cube_state_perori.txt'
way_path = 'solve_way.txt'

def main():
	run(['./rcReader.py'])
	f = open(readColor_path, 'r')
	color_data = f.read()
	f.close()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(('169.254.227.203', 50010))
		s.send(color_data.encode('UTF-8'))
		recv_data = s.recv(4096).decode()
		print('"' + recv_data + '" from PC(server).')

	# with open(state_path) as f:
	# 	cube_state_perori_s = f.read().strip()
	# cube_state_perori = cube_state_perori_s.split('_')
	# print('state:' + cube_state_perori[0])
	# print('per_ori:' + cube_state_perori[1])
	# state = cube_state_perori[0].split(':')
	# per_ori = cube_state_perori[1]

	# run(['./rcSolver.out', state[0], state[1]])
	# # runメソッドはサブプロセスが終わるまで待ってくれる.
	# # この後solve_way.txtから解法を読み取ってaftersolve.pyを実行.
	# with open(way_path) as f:
	# 	ways = f.read()
	# run(['./afterSolve.py', ways, per_ori])

if __name__ == '__main__':
	main()