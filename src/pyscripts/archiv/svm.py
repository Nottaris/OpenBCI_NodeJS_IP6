from sklearn import svm
import numpy as np
X = np.array([[[1,2,3],[4,5,6],[10,20,30],[4,5,6],[1,2,3],[4,5,6],[1,2,3],[4,5,6]],
     [[1,2,3],[4,5,6],[1,2,3],[4,5,6],[1,2,3],[4,5,6],[1,2,3],[4,5,6]]])

nsamples, nx, ny = X.shape
print(nx)
print(ny)
X2d = X.reshape((nsamples,nx*ny))
print(X)
print(X2d)
y = [0, 1]
clf = svm.SVC()
clf.fit(X2d, y)
