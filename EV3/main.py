#!/usr/bin/env python3

from subprocess import run, check_output, PIPE
from time import sleep
import socket
import ColorClustering as cc
readColor_path = 'readColor.txt'
state_path = 'cube_state_perori.txt'
way_path = 'solve_way.txt'

def main():
	run(['./rcReader.py'])
	f = open(readColor_path, 'r')
	color_data = f.read()
	f.close()
	print(color_data)
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(('169.254.227.203', 50010))
		s.send(color_data.encode('UTF-8'))
		recv_data = s.recv(4096).decode()
		print('"' + recv_data + '" from PC(server).')

	cp, co, per_ori = cc.Clustering_Main(color_data)
	cp_str = ','.join(map(str, cp))
	co_str = ','.join(map(str, co))
	per_ori_str = ','.join(map(str, per_ori))
	print('cp:', cp_str, ' co:', co_str)
	judgment = input('continue? [y/n]')
	if judgment != 'y':
		return

	print('Solving... ')
	run(['./rcSolver.out', cp_str, co_str])
	# runメソッドはサブプロセスが終わるまで待ってくれる.
	# この後solve_way.txtから解法を読み取ってaftersolve.pyを実行.
	print('Complete!')
	with open(way_path) as f:
		ways = f.read()
	run(['./afterSolve.py', ways, per_ori_str])

if __name__ == '__main__':
	while True:
		judgment = input('Ready. Solve? [y/n]')
		if judgment != 'y':
			break
		main()