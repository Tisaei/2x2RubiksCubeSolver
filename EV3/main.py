#!/usr/bin/env python3

#from ctypes.wintypes import POINT
from subprocess import run
import socket

IP_ADDRESS = '169.254.233.155'
PORT = 50010

readColor_path = 'readColor.txt'

def main():
	try:
		run(['./rcReader.py'])
	except KeyboardInterrupt:
		print('interrupted!')
		return
	f = open(readColor_path, 'r')
	color_data = f.read()
	f.close()
	print()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.settimeout(10.0)
		s.connect((IP_ADDRESS, PORT))
		s.send(color_data.encode('UTF-8'))
		recv_data = s.recv(4096).decode()
		print('"' + recv_data + '"\nfrom PC(server).')
	
	if recv_data == 'Error Happend!':
		return
	run(['./afterSolve.py', recv_data])

if __name__ == '__main__':
	while True:
		judgment = input('Ready. Solve? [y/n]')
		if judgment != 'y':
			really_judgment = input('Really? [y/n]')
			if really_judgment == 'y':
				break
		main()