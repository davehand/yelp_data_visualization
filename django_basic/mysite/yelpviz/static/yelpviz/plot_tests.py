import numpy as np
from numpy import ma
import matplotlib.pyplot as plt
import scipy.interpolate
from scipy import misc
from pylab import *
import pylab

# Generate data:   x: latitude, y: longitude, z: stars
x = -126.7+61.8*np.random.rand(30)
y = 16.7*np.random.rand(30) + 30.7
z = [3, 2, 3, 4, 5, 5, 4, 2, 1, 1, 2, 2, 3, 4, 5, 5, 4, 2, 1, 2, 3, 2, 3, 4, 5, 3, 2, 3, 4, 5]

# Setting boundaries of images (should be same at maps.html)
x = np.insert(x, 0, -129.3) # At position 0 SW long
x = np.insert(x, 1, -65.3) # At position 1 NE long
y = np.insert(y, 0, 23.7) # At position 0 SW lat
y = np.insert(y, 1, 49.5) # At position 1 NE lat
z = np.insert(z, 0, 0) # 0 stars for bound
z = np.insert(z, 1, 0) # 0 stars for bound

# Set up a regular grid of interpolation points
xi, yi = np.linspace(x.min(), x.max(), 500), np.linspace(y.min(), y.max(), 500)
xi, yi = np.meshgrid(xi, yi)

# Interpolate
rbf = scipy.interpolate.Rbf(x, y, z, function='gaussian', epsilon=2, smooth=0.0)
# rbf = scipy.interpolate.Rbf(x, y, z, function='linear', smooth=0.0)
zi = rbf(xi, yi)

# Mask to remove ratings less than 1
zi[zi < 1] = 0
mask = ma.masked_where(zi < 1, zi)

# Generate figure from interpolation points
plt.figure(figsize=(40,20))
plt.imshow(mask, vmin=1, vmax=5, origin='lower',
           extent=[x.min(), x.max(), y.min(), y.max()], alpha = 0.4)

# Plot the actual positions
plt.scatter(x, y, c=z)
plt.axis('off')
#plt.colorbar()
#plt.show()
savefig('tmp.png', transparent = True, bbox_inches='tight')

