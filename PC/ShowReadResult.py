import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import socket

np.set_printoptions(suppress=True)
readColor_path = 'readColor.txt'

# color_data_string=(
#     '28,2.2,2.9:30,5.5,3.0:32,8.8,3.1\n'
#     '58,22,2.9:60,55,3.0:62,88,3.1\n'
#     '88,23,2.9:90,56,3.0:92,89,3.1\n'
#     '118,1.2,2.9:120,4.5,3.0:122,7.8,3.1\n'
# )

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
import copy
def main():
	# global color_data_string
	# color_data_string = GetColorData()
	f = open(readColor_path, 'r')
	color_data_string = f.read()
	f.close()
	RGB_data = String_to_3d_Ndarray(color_data_string)
	print(RGB_data)

	# xy_data = np.array([])
	# for datum in RGB_data:
	#     rad = np.radians(datum[0])
	#     xy_datum = datum[1] * np.array([np.cos(rad), np.sin(rad)])
	#     xy_data = np.append(xy_data, xy_datum)
	# xy_data = xy_data.reshape(RGB_data.shape)

	# fig = plt.figure()
	# ax = fig.add_subplot(111, projection='3d')
	# ax.scatter3D(RGB_data[:, 0], RGB_data[:, 1], RGB_data[:, 2])
	# plt.show()
	
	n_cluster = 6
	model = KMeans_pp(n_cluster)
	model.fit(RGB_data)
	cube_color_ndarray = model.labels_.reshape((-1, 3))
	print(cube_color_ndarray)

	# markers = ['+', '*', '<', 'o', '1', 's', 'd']
	# color   = ['r', 'b', 'g', 'c', 'm', 'y', 'k']
	# fig = plt.figure()
	# ax = fig.add_subplot(111, projection='3d')
	# for i in range(n_cluster):
	# 	p = RGB_data[model.labels_ == i, :]
	# 	ax.scatter3D(p[:, 0], p[:, 1], p[:, 2], marker = markers[i], color = color[i])
	# plt.show()

	cube_color = cube_color_ndarray.tolist()
	DLB_keys = ['D', 'B', 'L']
	color_of_DBL_dict = dict(zip(DLB_keys, cube_color[4]))
	color_of_UFR_dict = Identify_Color_of_UFR(copy.deepcopy(cube_color), color_of_DBL_dict)
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
	for i in range(len(cube_color)):
		if color_of_Side_dict['U'] in cube_color[i]:
			state_co[i] = cube_color[i].index(color_of_Side_dict['U'])
		elif color_of_Side_dict['D'] in cube_color[i]:
			state_co[i] = cube_color[i].index(color_of_Side_dict['D'])
		part_color_set = set()
		for color in cube_color[i]:
			part_color_set.add([k for k, v in color_of_Side_dict.items() if v == color][0])
		state_cp[i] = part_sets[frozenset(part_color_set)]
	print(state_co)
	print(state_cp)

	print('finish.')

if __name__ == '__main__':
	main()