import numpy as np

def align_n_elements(X, idx, centers):
    n_clusters = len(centers)
    def count_cluster_elements(id_x):
        num_elements = np.zeros(n_clusters)
        for k in range(n_clusters):
            num_elements[k] = len(X[id_x == k,:])
        return num_elements
    
    if len(idx) % n_clusters != 0:
        return idx
    goal_n_elements = int(len(idx) / n_clusters)

    n_elements = count_cluster_elements(idx)
    print(n_elements)
    while not np.all(n_elements == goal_n_elements): # すべてのクラスタの要素数がgoal_n_elementsになるまで繰り返す.
        cluster_has_many = np.argmax(n_elements) # 要素数が最も多いクラスタ.
        cluster = 0 # distanceが最も小さい組み合わせのクラスタの方
        element = 0 # distanceが最も小さい組み合わせの要素の方
        min_distance = np.inf
        for cluster_has_few in np.where(n_elements < goal_n_elements)[0]: # 要素数がgoal_n_elements未満のクラスタ達に対して,
            for i in np.where(idx == cluster_has_many)[0]: # 要素の多いクラスタに所属するデータのインデックスそれぞれに対して.
                distance = np.sum((X[i,:] - centers[cluster_has_few]) ** 2)
                if distance < min_distance: # もし今のところの距離の最小値をとったなら
                    min_distance = distance # 距離の最小値を更新
                    cluster = cluster_has_few # 
                    element = i
        idx[element] = cluster
        n_elements = count_cluster_elements(idx)
        print(n_elements)
    return idx

def kmeans(X,n_clusters,centers,iter):
    # X.shape[0]: サンプル数, X.shape[1]: 次元数.

    def count_cluster_elements(id_x):
        num_elements = np.zeros(n_clusters)
        for k in range(n_clusters):
            num_elements[k] = len(X[id_x == k,:])
        return num_elements

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
            centers[k,:] = X[idx==k,:].mean(axis=0) # 初期の重心がいい加減だと、白と黄色が近すぎてどっちかのクラスタがなくなり、idx==白or黄色に当てはまるものがなくなってエラーが起こる可能性がある.
        count += 1
    
    # 各クラスタの要素数を求め、4個超過のクラスタがあると、そのクラスタの要素と4個未満のクラスタの重心の距離が最も短い組み合わせを求め、その要素をそのクラスタに入れる. これをすべてのクラスタの要素数が4個になるまで繰り返す.
    idx = align_n_elements(X, idx, centers)

    return idx