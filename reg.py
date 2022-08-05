def pointset_register_3d(p1_t, p2_t):
    import numpy as np

    ##Based on Arun et al., 1987

    #Take transpose as columns should be the points
    p1 = p1_t.transpose()
    p2 = p2_t.transpose()

    #Calculate centroids
    p1_c = np.mean(p1, axis = 1).reshape((-1,1))
    p2_c = np.mean(p2, axis = 1).reshape((-1,1))

    #Subtract centroids
    q1 = p1-p1_c
    q2 = p2-p2_c

    #Calculate covariance matrix
    H=np.matmul(q1,q2.transpose())

    #Calculate singular value decomposition (SVD)
    U, X, V_t = np.linalg.svd(H) #the SVD of linalg gives you Vt

    #Calculate rotation matrix
    R = np.matmul(V_t.transpose(),U.transpose())

    assert np.allclose(np.linalg.det(R), 1.0), \
    "Rotation matrix of N-point registration not 1, see paper Arun et al."

    #Calculate translation matrix
    T = p2_c - np.matmul(R,p1_c)
    
    return (np.dot(R, p1) + T).T