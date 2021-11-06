import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import socket

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

from kmeanspp import KMeans_pp
from kmeans_initSet import kmeans
import copy
def main():
	color_data_string = GetColorData()
	# f = open(readColor_path, 'r')
	# color_data_string = f.read()
	# f.close()

	RGB_data = String_to_3d_Ndarray(color_data_string)
	print(RGB_data)
	
	n_cluster = 6
	# model = KMeans_pp(n_cluster)
	# try:
	# 	model.fit(RGB_data)
	# except Exception as e:
	# 	print(e)
	# 	return
	# cube_color_ndarray = model.labels_.reshape((-1, 3))
	center = np.array(
		[[251, 255, 242], # 白
		[43, 170, 151], # 緑
		[241, 255, 255], # 黄色
		[37, 122, 135], # 青
		[195, 255, 246], # 橙
		[133, 42, 18]] # 赤
	)
	try:
		cube_color_ndarray = kmeans(RGB_data, n_cluster, center, 200).reshape((-1, 3))
	except Exception as e:
		print(e)
		return
	print(cube_color_ndarray)

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
	plt.show()

	cube_color = cube_color_ndarray.tolist()
	DLB_keys = ['D', 'B', 'L']
	color_of_DBL_dict = dict(zip(DLB_keys, cube_color[4]))
	try:
		color_of_UFR_dict = Identify_Color_of_UFR(copy.deepcopy(cube_color), color_of_DBL_dict)
	except Exception as e:
		print(e)
		return
	color_of_Side_dict = {**color_of_UFR_dict, **color_of_DBL_dict}
	print(color_of_Side_dict)

	part_sets = {
		frozenset(['U', 'L', 'B']): 0, 
		frozenset(['U', 'B', 'R']): 1, 
		frozenset(['U', 'R', 'F']): 2, 
		frozenset(['U', 'F', 'L']): 3, 
		frozenset(['D', 'B', 'L']): 4,
		frozenset(['D', 'R', 'B']): 5, 
		frozenset(['D', 'F', 'R']): 6, 
		frozenset(['D', 'L', 'F']): 7
	}
	state_co = [-1 for i in range(8)]
	state_cp = [-1 for i in range(8)]
	try:
		for i in range(len(cube_color)):
			if color_of_Side_dict['U'] in cube_color[i]:
				state_co[i] = cube_color[i].index(color_of_Side_dict['U'])
			elif color_of_Side_dict['D'] in cube_color[i]:
				state_co[i] = cube_color[i].index(color_of_Side_dict['D'])
			part_color_set = set()
			for color in cube_color[i]:
				part_color_set.add([k for k, v in color_of_Side_dict.items() if v == color][0])
			state_cp[i] = part_sets[frozenset(part_color_set)]
	except Exception as e:
		print(e)
		return
	print(state_co)
	print(state_cp)

	print('finish 1 turn.')

if __name__ == '__main__':
	while True:
		judgment = input('Ready. Start Connection? [y/n]')
		if judgment != 'y':
			break
		main()