import numpy as np
from numpy import ma
import matplotlib.pyplot as plt
import scipy.interpolate
from scipy import misc
from pylab import *
import pylab
import views
import cx_Oracle
import random
from sklearn.cluster import DBSCAN


def generate_map(x, y, z, output):
	print(x.shape)
	print(y.shape)
	print(z.shape)

	# Setting boundaries of images (should be same at maps.html)
	x = np.insert(x, 0, -129.3) # At position 0 SW long
	x = np.insert(x, 1, -62.3) # At position 1 NE long
	y = np.insert(y, 0, 23.7) # At position 0 SW lat
	y = np.insert(y, 1, 49.5) # At position 1 NE lat
	z = np.insert(z, 0, 0) # 0 stars for bound
	z = np.insert(z, 1, 0) # 0 stars for bound

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
	           extent=[x.min(), x.max(), y.min(), y.max()], alpha = 1)

	# Plot the actual positions

	# col_map = matplotlib.colors.ListedColormap(['green', 'red'])
	plt.scatter(x, y, c=z)#, cmap=col_map)
	plt.axis('off')
	#plt.colorbar()
	#plt.show()
	savefig(output, transparent = True, bbox_inches='tight')

"""
Performs clustering on a matrix, X, using features FEATURES. FEATURES
determines which columns will be used to cluster, and these columns will be
treated as numeric values. For example, if FEATURES = [0, 2], then columns
0 and 2 will be used as features to cluster the data on, but the returned 
matrix includes all original features. The cluster value will be inserted
as the first column. Data that was not included in any cluster is given a
cluster ID of -1
"""
def cluster(x, features):
	x_to_clus = x[:, features].astype(float)
	# run DBSCAN clustering algorithm for fast clustering
	db = DBSCAN(eps = .38, min_samples = 2).fit(x_to_clus)
	labels = db.labels_
	labels = labels.reshape(len(labels), 1)
	x_clus = np.append(labels, x, axis = 1)
	return x_clus

"""
Removes rows that have no cluster assignment
"""
def differentiate_no_cluster(x):
	new_clus = -1
	for i in range(len(x)):
		if x[i, 0] == -1:
			x[i, 0] = new_clus
			new_clus -= 1
	# x = x[x[:, 0].A1 != -1, :]
	return x

if __name__ == '__main__':
	sql = "Select b.longitude, b.latitude, br.avg_rating " + \
		"From business b, business_rating br " + \
		"Where b.business_id = br.business_id " + \
		"And b.name = 'McDonald''s' ORDER BY b.longitude DESC, b.latitude DESC"

	con = cx_Oracle.connect(views.rds_conn_str)
	cur = con.cursor()
	cur.execute(sql)
	result = cur.fetchall()
	# data = np.zeros((len(result), 3))
	data = [];

	# i = 0
	for res_row in result:
		row = []
		row.append(float(res_row[0]) + random.random())
		row.append(float(res_row[1]) + random.random())
		row.append(float(res_row[2]) + random.random())

		if (row[1] <= 49.5 and row[1] >= 23.7 and row[0] <= -62.3 and row[0] >= -129.3):
			data.append(row)
		

		# data[i, 0] = float(row[0])
		# data[i, 1] = float(row[1])
		# data[i, 2] = float(row[2])
		# i += 1

	data = np.matrix(data)
	clusters = cluster(data, [0, 1])
	clusters = differentiate_no_cluster(clusters)

	clust_id = np.unique(clusters[:, 0].A1)
	data = np.zeros((len(clust_id), 3))
	print(data)
	i = 0
	for c in clust_id:
		data[i, 0] = np.average(clusters[(clusters[:, 0] == c).A1, 1])
		data[i, 1] = np.average(clusters[(clusters[:, 0] == c).A1, 2])
		data[i, 2] = np.average(clusters[(clusters[:, 0] == c).A1, 3])
		i += 1



	#x = -126.7+61.8*np.random.rand(30)
	#y = 16.7*np.random.rand(30) + 30.7
	#z = [3, 2, 3, 4, 5, 5, 4, 2, 1, 1, 2, 2, 3, 4, 5, 5, 4, 2, 1, 2, 3, 2, 3, 4, 5, 3, 2, 3, 4, 5]
	generate_map(data[:, 0], data[:, 1], data[:, 2], 'static/yelpviz/tmp.png')
	# generate_map(x, y, z, 'tmp.png')

