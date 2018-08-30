import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import *

file = 'test'
format = '.jpg'

fname = file + format


def shuffle(ary):
    a = ary.__len__()
    b = a - 1
    for d in range(b, 0, -1):
        e = random.randint(0, d)
        ary[[d, e]] = ary[[e, d]]
    return ary


im = mpimg.imread(fname)

data = array(im)

shape = data.shape
data = data.reshape((shape[0] * shape[1], shape[2]))

data = shuffle(data)

data = data.reshape(shape)
plt.imsave(file + '_scrambled' + format, data)
plt.imshow(data)
plt.show()
