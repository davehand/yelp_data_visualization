import numpy as np
from numpy import ma
import matplotlib.pyplot as plt
import scipy.interpolate
from scipy import misc
from pylab import *
import pylab
import views
import cx_Oracle

def generate_map(x, y, z, output):
	print(x)
	print(y)
	print(z)

	# Setting boundaries of images (should be same at maps.html)
	# x = np.insert(x, 0, -129.3) # At position 0 SW long
	# x = np.insert(x, 1, -62.3) # At position 1 NE long
	# y = np.insert(y, 0, 23.7) # At position 0 SW lat
	# y = np.insert(y, 1, 49.5) # At position 1 NE lat
	# z = np.insert(z, 0, 0) # 0 stars for bound
	# z = np.insert(z, 1, 0) # 0 stars for bound

	# Set up a regular grid of interpolation points
	xi, yi = np.linspace(x.min(), x.max(), 500), np.linspace(y.min(), y.max(), 500)
	xi, yi = np.meshgrid(xi, yi)

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

	col_map = matplotlib.colors.ListedColormap(['green', 'red'])
	plt.scatter(x, y, c=z, cmap=col_map)
	plt.axis('off')
	#plt.colorbar()
	#plt.show()
	savefig(output, transparent = True, bbox_inches='tight')

if __name__ == '__main__':
	sql = "Select b.latitude, b.longitude, br.avg_rating " + \
		"From business b, business_rating br " + \
		"Where b.business_id = br.business_id " + \
		"And b.name = 'McDonald''s' ORDER BY br.avg_rating DESC"

	con = cx_Oracle.connect(views.rds_conn_str)
	cur = con.cursor()
	cur.execute(sql)
	result = cur.fetchall()
	data = np.zeros((len(result), 3))

	i = 0
	for row in result:
		data[i, 0] = row[0]
		data[i, 1] = row[1]
		data[i, 2] = row[2]
		i += 1

	#x = -126.7+61.8*np.random.rand(30)
	#y = 16.7*np.random.rand(30) + 30.7
	#z = [3, 2, 3, 4, 5, 5, 4, 2, 1, 1, 2, 2, 3, 4, 5, 5, 4, 2, 1, 2, 3, 2, 3, 4, 5, 3, 2, 3, 4, 5]
	generate_map(data[:, 1], data[:, 0], data[:, 2], 'tmp.png')
	# generate_map(x, y, z, 'tmp.png')

