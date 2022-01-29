import numpy as np

def kmeans(X,n_clusters,centers,iter):
    #Xのサンプル数だけ空のラベルを作る
    idx = np.zeros(X.shape[0])
    pre_idx = np.ones(X.shape[0])
    count = 0
    while not (idx == pre_idx).all() and count < iter:
        pre_idx = idx
        #距離の二乗が一番近い中心点のインデックスを返す。
        for i in range(X.shape[0]):
            idx[i] = np.argmin(np.sum((X[i,:] - centers)**2,axis=1))
        #中心の移動
        for k in range(n_clusters):
            centers[k,:] = X[idx==k,:].mean(axis=0)
        count += 1
        
    return idx