from sklearn.cluster import KMeans
import numpy as np
from numpy import array
from scipy.cluster.vq import vq, kmeans, whiten
import scipy as sc
import cv2
import numpy as np
import matplotlib.pyplot as plt

y = plt.imread('test.jpg')
imgplot = plt.imshow(y) 
plt.show()


X = plt.imread('test_scrambled.jpg')
imgplot = plt.imshow(X) 
plt.show()



new_X=X.reshape((-1,3))

print(X.shape)
print(new_X.shape)

kmeans = KMeans(n_clusters=10, random_state=0).fit(new_X)

print(kmeans.labels_.shape)

kmeans.predict([[100,100,100]])


#kmeans.cluster_centers_


new_kmeans = kmeans.labels_.argsort()
sorted_X = new_X[new_kmeans]
new_kmeans = sorted_X.reshape((X.shape[0],X.shape[1],3))
plt.imshow(new_kmeans)


type(new_kmeans)
plt.imshow(new_kmeans)

plt.show()