#!/usr/bin/env python3

import re

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

def direction_change(pre_per_ori, rotate_side):
	if rotate_side == "U":
		base_per = 0
	elif rotate_side == "F":
		base_per = 4
	else:
		base_per = 2
	
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

def UFR_to_DYZ(UFR_ways, now_po): #now_po = now_per_ori
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