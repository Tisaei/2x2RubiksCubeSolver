#!/usr/bin/env python3

from subprocess import run
import ColorClustering as cc
from WayOriConverter import UFR_to_DYZ
readColor_path = 'readColor.txt'
way_path = 'solve_way.txt'

def main():
	run(['./rcReader.py'])
	f = open(readColor_path, 'r')
	color_data = f.read()
	f.close()
	print()

	try:
		cp, co, per_ori = cc.Clustering_Main(color_data)
	except Exception as e:
		print(e)
		return
	cp_str = ','.join(map(str, cp))
	co_str = ','.join(map(str, co))
	print('cp:', cp_str, ' co:', co_str)

	print('Solving... ')
	run(['./rcSolver.out', cp_str, co_str])
	# runメソッドはサブプロセスが終わるまで待ってくれる.
	# この後solve_way.txtから解法を読み取ってaftersolve.pyを実行.
	print('Complete!')
	with open(way_path) as f:
		ways = f.read()
	UFR_to_DYZ(ways, per_ori)
	run(['./afterSolve.py', ways])

if __name__ == '__main__':
	while True:
		judgment = input('Ready. Solve? [y/n]')
		if judgment != 'y':
			really_judgment = input('Really? [y/n]')
			if really_judgment == 'y':
				break
		main()