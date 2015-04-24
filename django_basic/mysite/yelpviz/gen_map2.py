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
from sklearn.neighbors import NearestNeighbors
import scipy.ndimage as ndimage
import colorsys
import Image

from dynamo_connect import Dynamo

class MapGen:
	def __init__(self, entity, scale, is_business):
		entity = entity.replace("'", "''")
		if is_business:
			sql = "Select b.longitude, b.latitude, br.avg_rating " + \
					"From business b, business_rating br " + \
					"Where b.business_id = br.business_id " + \
					"And b.name = '" + entity + "'"

		else:
			sql = "SELECT b.longitude, b.latitude, br.avg_rating " + \
					"FROM business b, business_rating br, business_category bc " + \
					"WHERE b.business_id = br.business_id " + \
					"AND b.business_id = bc.business_id " + \
					"AND bc.category = '" + entity + "'"

		con = cx_Oracle.connect(views.rds_conn_str)
		cur = con.cursor()
		cur.execute(sql)
		result = cur.fetchall()
		cur.close()
		data = [];

		for res_row in result:
			row = []
			row.append(float(res_row[0]) + random.random()/100000.0)
			row.append(float(res_row[1]) + random.random()/100000.0 - 1) 
			row.append(float(res_row[2]) + random.random()/100000.0)

			# filter out of US data values
			if (row[1] <= 49.5 and row[1] >= 23.7 and row[0] <= -62.3 and row[0] >= -129.3):
				data.append(row)
			
		# cluster into some number of point clusters
		data = np.matrix(data)
		clusters = self.cluster(data, [0, 1])
		clusters = self.differentiate_no_cluster(clusters)
		clust_id = np.unique(clusters[:, 0].A1)
		clus_data = np.zeros((len(clust_id), 3))

		# convert into a data matrix that is based off of the lat/long & rating 
		# averages for a given cluster
		i = 0
		for c in clust_id:
			clus_data[i, 0] = np.average(clusters[(clusters[:, 0] == c).A1, 1])
			clus_data[i, 1] = np.average(clusters[(clusters[:, 0] == c).A1, 2])
			clus_data[i, 2] = np.average(clusters[(clusters[:, 0] == c).A1, 3])
			i += 1
		 
		self.x = data[:, 0].A1
		self.y = data[:, 1].A1
		self.z = data[:, 2].A1
		
		self.clust_data = clus_data
		self.scale = scale
		self.is_business = is_business
		self.entity = entity

	def gen_and_save(self, output, n_px):
		self.generate_map(output, 1, n_px)


	# Returns an interpolation based on the ratings of near by neighbors,
	# weighted proportional to the inverse distance from a given point
	def interp(self, x, y, z, xi, yi, ignore_dist):
		z_interp = np.zeros((xi.size, yi.size))

		knn = NearestNeighbors(n_neighbors=20)
		knn.fit(np.vstack((x, y)).T)

		xi, yi = np.meshgrid(xi, yi)
		pts = zip(xi.ravel(), yi.ravel())
		dists, idxs = knn.kneighbors(pts)

		z_flat = z_interp.flatten()
		for i in range(len(pts)):
			num = 0
			dnm = 0

			# loop over neighbors and calculate an inverse weighted average
			for neighbor in range(len(idxs[i])):
				d = dists[i][neighbor] + .0001
				r = z[idxs[i][neighbor]]
				if d <= ignore_dist:
					inv_dist = 1/d
					num += r * inv_dist
					dnm += inv_dist

			if dnm != 0:
				z_flat[i] = num/dnm

		z_interp = z_flat.reshape(z_interp.shape)
		return z_interp

	def ratingsToRGB(self, ratings):
		new_shape = list(ratings.shape)
		new_shape.append(4)
		rgb = np.zeros(new_shape, np.float)

		ratings = ratings - ratings.min()
		ratings = ratings / ratings.max()
		colors = [
			(255, 0, 0),
			(255, 0, 0),
			(255, 0, 0),
			(255, 0, 0),
			(255, 0, 0),
			(255, 0, 0),
			(255, 0, 0),
			(255, 0, 0),
			# (255, 0, 0),
			# (255, 0, 0),
			(255, 91, 0),
			(255, 127, 0),
			(255, 171, 0),
			(255, 208, 0),
			(255, 240, 0),
			(218, 255, 0),
			(128, 255, 0),
			(100, 255, 0),
			(60, 255, 0),
			(0, 255, 0),
		]#,
			# (0, 255, 255),
			# (0, 240, 255),
			# (0, 213, 255),
			# (0, 171, 255),
			# (0, 127, 255),
			# (0, 86, 255),
			# (0, 0, 255)]

		ncols = len(colors)
		for i in range(len(ratings)):
			for j in range(len(ratings[i])):
				r = ratings[i, j]
				col_idx = int(r * (ncols - 1))
				rgb[i, j, 0] = colors[col_idx][0]/255.0
				rgb[i, j, 1] = colors[col_idx][1]/255.0
				rgb[i, j, 2] = colors[col_idx][2]/255.0
				rgb[i, j, 3] = 1
		return rgb
				

	def generate_map(self, output, alpha, dim):

		x = self.x
		y = self.y
		z = self.z
		clus_data = self.clust_data

		# Setting boundaries of images (should be same at maps.html)
		x = np.insert(x, 0, -129.3)			# At position 0 SW long
		x = np.insert(x, 1, -62.3)			# At position 1 NE long
		y = np.insert(y, 0, 23.7)			# At position 0 SW lat
		y = np.insert(y, 1, 49.5)			# At position 1 NE lat
		z = np.insert(z, 0, 0)				# 0 stars for bound
		z = np.insert(z, 1, 0)				# 0 stars for bound

		xi, yi = np.linspace(x.min(), x.max(), dim), np.linspace(y.min(), y.max(), dim)

		# get a custom interpolation based off an a weighted average
		# of nearby weights
		z_interp = self.interp(x, y, z, xi, yi, 20)
		z_interp = self.ratingsToRGB(z_interp)

		# blur the output to smooth edges on rating boundary
		z_interp = ndimage.gaussian_filter(z_interp, sigma=(5, 5, 0), order=0)

		# use the mask from a regular RBF interpolation to cut out pieces of
		# the above result
		xi, yi = np.meshgrid(xi, yi)
		rbf = scipy.interpolate.Rbf(clus_data[:, 0], clus_data[:, 1], clus_data[:, 2], function='gaussian', epsilon=2, smooth=0.0)
		zi = rbf(xi, yi)
		zi[zi < self.scale] = 0
		zi[zi != 0] = alpha

		# apply the mask to the 4th channel, which identifies the alpha level
		z_interp[:, :, 3] = zi

		# save the output
		fig = plt.figure(frameon=False)
		ax = plt.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(z_interp, aspect='normal', origin='lower', extent=[x.min(), x.max(), y.min(), y.max()])
		savefig(output)


	"""
	Performs clustering on a matrix, X, using features FEATURES. FEATURES
	determines which columns will be used to cluster, and these columns will be
	treated as numeric values. For example, if FEATURES = [0, 2], then columns
	0 and 2 will be used as features to cluster the data on, but the returned 
	matrix includes all original features. The cluster value will be inserted
	as the first column. Data that was not included in any cluster is given a
	cluster ID of -1
	"""
	def cluster(self, x, features):
		x_to_clus = x[:, features].astype(float)
		# run DBSCAN clustering algorithm for fast clustering
		db = DBSCAN(eps = .58, min_samples = 2).fit(x_to_clus)
		labels = db.labels_
		labels = labels.reshape(len(labels), 1)
		x_clus = np.append(labels, x, axis = 1)
		return x_clus

	"""
	Converts all no-cluster rows to unique clusters
	"""
	def differentiate_no_cluster(self, x):
		new_clus = -1
		for i in range(len(x)):
			if x[i, 0] == -1:
				x[i, 0] = new_clus
				new_clus -= 1
		return x

if __name__ == '__main__':

	dyn = Dynamo()
	size = 1000
	scales = [0.5, 0.75, 1.0]
	sql_bz = 'SELECT * FROM (SELECT name from business GROUP BY name having COUNT(name) > 50 ORDER BY COUNT(name) DESC) WHERE ROWNUM <= 20'
	sql_cat = 'SELECT * FROM (SELECT category FROM business_category bc, business b WHERE bc.business_id = b.business_id HAVING COUNT(category) > 50 GROUP BY category ORDER BY COUNT(category) DESC) WHERE ROWNUM <= 20'

	con = cx_Oracle.connect(views.rds_conn_str)
	cur = con.cursor()
	cur.execute(sql_bz)
	result = cur.fetchall()

	# print("Generating business maps")
	# for row in result:
	# 	for scale in scales:
	# 		out = 'tmp_map_data/business_' + row[0] + '_' + str(scale) + '.png'
	# 		print("\t...generating '%s'" % out)

	# 		mg = MapGen(row[0], scale, True)
	# 		mg.gen_and_save(out, size)

	# 		f = open(out, 'rb')
	# 		img_data = f.read()
	# 		f.close()

	# 		dyn.add_map(table='Business', hash_key=row[0], range_key=str(scale), map_data=img_data)

	# cur.close()

	cur = con.cursor()
	cur.execute(sql_cat)
	result = cur.fetchall()

	print("Generating category maps")
	for row in result:
		for scale in scales:
			out = 'tmp_map_data/category_' + row[0] + '_' + str(scale) + '.png'
			print("\t...generating '%s'" % out)

			mg = MapGen(row[0], scale, False)
			mg.gen_and_save(out, size)

			f = open(out, 'rb')
			img_data = f.read()
			f.close()

			dyn.add_map(table='Business_Category', hash_key=row[0], range_key=str(scale), map_data=img_data)
















