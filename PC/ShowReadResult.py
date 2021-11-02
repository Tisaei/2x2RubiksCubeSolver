import numpy as np
import matplotlib.pyplot as plt
import socket
from kmeans import KMeans

color_data_string=(
    '28,2.2,2.9:30,5.5,3.0:32,8.8,3.1\n'
    '58,22,2.9:60,55,3.0:62,88,3.1\n'
    '88,23,2.9:90,56,3.0:92,89,3.1\n'
    '118,1.2,2.9:120,4.5,3.0:122,7.8,3.1\n'
)

def GetColorData():
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

def Convert_To_HV_2d_Ndarray(data):
    data = data.strip()
    string_list = data.split('\n')
    string_part_list = list(map(lambda s: s.split(':'), string_list))
    string_HSV_list = []
    for part in string_part_list:
        string_HSV_list.append(list(map(lambda s: s.split(','), part)))
    HV_ndarray = np.asarray(np.array(string_HSV_list), dtype=float)[:,:,::2]
    # ndarray[start:stop:step]
    HV_2d_ndarray = HV_ndarray.reshape((-1, 2))
    return HV_2d_ndarray

def main():
    global color_data_string
    # color_data_string = GetColorData()
    data = Convert_To_HV_2d_Ndarray(color_data_string)
    print(data)

    xy_data = np.array([])
    for datum in data:
        rad = np.radians(datum[0])
        xy_datum = datum[1] * np.array([np.cos(rad), np.sin(rad)])
        xy_data = np.append(xy_data, xy_datum)
    xy_data = xy_data.reshape(data.shape)
    
    n_cluster = 4
    model = KMeans(n_cluster)
    model.fit(xy_data)

    print(model.labels_)
    markers = ["+", "*", "o", "<"]
    color = ['r', 'b', 'g', 'm']
    for i in range(n_cluster):
        p = xy_data[model.labels_ == i, :]
        plt.scatter(p[:, 0], p[:, 1], marker = markers[i], color = color[i])
    plt.show()

    print('finish.')

if __name__ == '__main__':
    main()