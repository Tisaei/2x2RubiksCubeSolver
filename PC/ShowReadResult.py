import numpy as np
import matplotlib.pyplot as plt
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('XXX.XXX.XXX.XXX', 50010))
    s.listen(1)
    print('Start program...')

    conn, addr = s.accept()
    print(f'Connection from {addr} has been established!')
    color_data = conn.recv(4096).decode()
    print(color_data)
    conn.send("I'm Received.".encode('UTF-8'))
    conn.close()

print('finish.')