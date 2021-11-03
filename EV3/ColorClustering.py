#!/usr/bin/env python3

import numpy as np
from kmeanspp import KMeans_pp

def String_to_3d_Ndarray(string_data):
	string_data = string_data.strip()
	string_list = string_data.split('\n')
	string_part_list = list(map(lambda s: s.split(':'), string_list))
	string_color_list = []
	for part in string_part_list:
		string_color_list.append(list(map(lambda s: s.split(','), part)))
	color_ndarray = np.asarray(np.array(string_color_list), dtype=float)
	color_3d_ndarray = np.round(color_ndarray.reshape((-1, 3)), decimals=2)
	return color_3d_ndarray

def Identify_Color_of_UFR(cube_color_source, color_of_DBL_dict):
	cube_color = cube_color_source.copy()
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

def Clustering_Main(color_data_string):
	RGB_data = String_to_3d_Ndarray(color_data_string)

	n_cluster = 6
	model = KMeans_pp(n_cluster)
	model.fit(RGB_data)
	cube_color = model.labels_.reshape((-1, 3)).tolist()

	DLB_keys = ['D', 'B', 'L']
	color_of_DBL_dict = dict(zip(DLB_keys, cube_color[4].tolist()))
	color_of_UFR_dict = Identify_Color_of_UFR(cube_color.tolist(), color_of_DBL_dict)
	color_of_Side_dict = {**color_of_UFR_dict, **color_of_DBL_dict}

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
	state_cp = [-1 for i in range(8)]
	state_co = [-1 for i in range(8)]
	for i in range(len(cube_color)):
		part_color_set = set()
		for color in cube_color[i]:
			part_color_set.add([k for k, v in color_of_Side_dict.items() if v == color][0])
		state_cp[i] = part_sets[frozenset(part_color_set)]

		if color_of_Side_dict['U'] in cube_color[i]:
			state_co[i] = cube_color[i].index(color_of_Side_dict['U'])
		elif color_of_Side_dict['D'] in cube_color[i]:
			state_co[i] = cube_color[i].index(color_of_Side_dict['D'])

	return (state_cp, state_co, (0,0b00))
