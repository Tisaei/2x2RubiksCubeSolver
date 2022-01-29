import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import socket
from subprocess import run
import re

np.set_printoptions(suppress=True)
readColor_path = 'readColor2.txt'

def GetColorData():
	color_data = ""
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(('169.254.227.203', 50010))
		s.listen(1)
		print('Start program...')

		conn, addr = s.accept()
		print(f'Connection from {addr} has been established!')
		color_data = conn.recv(4096).decode()
		print(color_data)
		conn.send("I'm Received.".encode('UTF-8'))
		conn.close()
	
	return color_data

def String_to_3d_Ndarray(string_data):
	string_data = string_data.strip()
	string_list = string_data.split('\n')
	string_part_list = list(map(lambda s: s.split(':'), string_list))
	string_color_list = []
	for part in string_part_list:
		string_color_list.append(list(map(lambda s: s.split(','), part)))
	color_ndarray = np.asarray(np.array(string_color_list), dtype=float)
	# ndarray[start:stop:step]
	color_3d_ndarray = np.round(color_ndarray.reshape((-1, 3)), decimals=2)
	return color_3d_ndarray

def Clustering(RGB_data):
	n_cluster = 6
	center = np.array(
		[[251, 255, 242], # 白
		[43, 170, 151], # 緑
		[241, 255, 255], # 黄色
		[37, 122, 135], # 青
		[195, 255, 246], # 橙
		[133, 42, 18]] # 赤
	)

	def ShowResult():
		markers = ['+', '*', '<', 'o', '1', 's', 'd']
		color   = ['r', 'b', 'g', 'c', 'm', 'y', 'k']
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.set_xlabel("r", size = 14, color = "r")
		ax.set_ylabel("g", size = 14, color = "g")
		ax.set_zlabel("b", size = 14, color = "b")
		for i in range(n_cluster):
			p = RGB_data[cube_color_ndarray.ravel() == i, :]
			ax.scatter3D(p[:, 0], p[:, 1], p[:, 2], marker = markers[i], color = color[i])
		plt.show(block=False)
	
	try:
		cube_color_ndarray = kmeans(RGB_data, n_cluster, center, 200).reshape((-1, 3))
	except Exception as e:
		print(e)
		return None

	# ShowResult()

	return cube_color_ndarray

def Identify_Color_of_UFR(cube_color, color_of_DBL_dict):
	inverse_side = {'U':'D', 'F':'B', 'R':'L', 'D':'U', 'B':'F', 'L':'R'}
	color_of_UFR_dict = {}
	for i in range(8):
		if i == 4:
			continue
		side = {'U':True, 'F':True, 'R':True}
		for DBL_key, DBL_color in color_of_DBL_dict.items():
			if DBL_color in cube_color[i]:
				cube_color[i].remove(DBL_color)
				side[inverse_side[DBL_key]] = False
		if len(cube_color[i]) == 1:
			True_Keys = [k for k,v in side.items() if v]
			color_of_UFR_dict[True_Keys[0]] = cube_color[i][0]
	
	return color_of_UFR_dict

def Identify_State(cube_color, color_dict):
	part_sets = {
		frozenset(['U', 'L', 'B']): 0, 
		frozenset(['U', 'B', 'R']): 1, 
		frozenset(['U', 'R', 'F']): 2, 
		frozenset(['U', 'F', 'L']): 3, 
		frozenset(['D', 'B', 'L']): 4,
		frozenset(['D', 'R', 'B']): 5, 
		frozenset(['D', 'F', 'R']): 6, 
		frozenset(['D', 'L', 'F']): 7}
	cp = [-1 for i in range(8)]
	co = [-1 for i in range(8)]
	try:
		for i in range(len(cube_color)):
			part_color_set = set()
			for color in cube_color[i]:
				part_color_set.add([k for k, v in color_dict.items() if v == color][0])
			cp[i] = part_sets[frozenset(part_color_set)]

			if color_dict['U'] in cube_color[i]:
				co[i] = cube_color[i].index(color_dict['U'])
			elif color_dict['D'] in cube_color[i]:
				co[i] = cube_color[i].index(color_dict['D'])
	except Exception as e:
		print(e)
		return None, None
	print(cp)
	print(co)

	return cp, co

def UFR_to_DYZ(UFR_ways, now_po): #now_po = now_per_ori
	def direction_change(pre_per_ori, rotate_side):
		if rotate_side == "U":
			base_per = 0
		elif rotate_side == "F":
			base_per = 4
		else:
			base_per = 2
		
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
		
		if pre_per_ori[0] == base_per or pre_per_ori[0] == base_per + 1:
			if most_ori(pre_per_ori) == 1:
				return ("", pre_per_ori)
			else:
				return ("Z2", doZ(doZ(pre_per_ori)))
		elif pre_per_ori[0] == (base_per+3) % 6 or pre_per_ori[0] == (base_per+4) % 6:
			temp_per_ori = doZ(pre_per_ori)
			if most_ori(temp_per_ori) == 1:
				return ("Z", temp_per_ori)
			else:
				return ("Y2 Z", doZ(doY(doY(pre_per_ori))))
		else:
			temp_per_ori = doZ(doY(pre_per_ori))
			if most_ori(temp_per_ori) == 1:
				return ("Y Z", temp_per_ori)
			else:
				return ("Y3 Z", doZ(doY(doY(doY(pre_per_ori)))))

	po = now_po
	DYZ_ways = ""
	for move_name in UFR_ways.split(","):
		if move_name == "":
			return ""
		else:
			if re.match(r"^U.?$", move_name):
				direction_change_info = direction_change(po,"U")
				DYZ_ways += direction_change_info[0]
				po = direction_change_info[1]
			elif re.match(r"^F.?$", move_name):
				direction_change_info = direction_change(po,"F")
				DYZ_ways += direction_change_info[0]
				po = direction_change_info[1]
			else:
				direction_change_info = direction_change(po,"R")
				DYZ_ways += direction_change_info[0]
				po = direction_change_info[1]
			if re.match(r"^.2$", move_name):
				DYZ_ways += " D2 "
			elif re.match(r"^.3$", move_name):
				DYZ_ways += " D3 "
			else:
				DYZ_ways +=  " D "
	return DYZ_ways.strip()

from kmeans_initSet import kmeans
import copy
way_path = 'solve_way.txt'

def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# 接続準備.
		s.bind(('169.254.227.203', 50010))
		s.listen(1)
		print('Start program...')

		# EV3からカラーデータの受け取り.
		conn, addr = s.accept()
		print(f'Connection from {addr} has been established!')
		color_data_string = conn.recv(4096).decode()
		RGB_data = String_to_3d_Ndarray(color_data_string)
		print(RGB_data)

		# クラスタリング.
		cube_color_ndarray = Clustering(RGB_data)
		if cube_color_ndarray is None:
			conn.send("Error Happend!".encode('UTF-8'))
			conn.close()
			return
		print(cube_color_ndarray)

		# 何の色がどの面なのかの特定.
		cube_color = cube_color_ndarray.tolist()
		DLB_keys = ['D', 'B', 'L']
		color_of_DBL_dict = dict(zip(DLB_keys, cube_color[4]))
		try:
			color_of_UFR_dict = Identify_Color_of_UFR(copy.deepcopy(cube_color), color_of_DBL_dict)
		except Exception as e:
			print(e)
			conn.send("Error Happend!".encode('UTF-8'))
			conn.close()
			return
		color_of_Side_dict = {**color_of_UFR_dict, **color_of_DBL_dict}
		print(color_of_Side_dict)

		# cp, coの特定.
		cp, co = Identify_State(cube_color, color_of_Side_dict)
		if cp is None:
			conn.send("Error Happend!".encode('UTF-8'))
			conn.close()
			return
		cp_str = ','.join(map(str, cp))
		co_str = ','.join(map(str, co))

		# 解法の計算.
		try:
			run(['./rcSolver.exe', cp_str, co_str])
			# runメソッドはサブプロセスが終わるまで待ってくれる.
		except KeyboardInterrupt:
			print('interrupted!')
			return
		with open(way_path) as f:
			UFR_ways = f.read()

		# ルービックキューブソルバーで動かせるように変換.
		DYZ_ways = UFR_to_DYZ(UFR_ways, (0, 0b00))

		# 解法をEV3へ送信.
		conn.send(DYZ_ways.encode('UTF-8'))
		conn.close()

	print('finish 1 turn.')

if __name__ == '__main__':
	while True:
		judgment = input('Ready. Start Connection? [y/n]')
		if judgment != 'y':
			break
		main()