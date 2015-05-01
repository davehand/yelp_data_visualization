
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
	

if __name__ == '__main__':
	
	entity = "McDonald''s"

	sql = "Select b.longitude, b.latitude, b.business_id, br.avg_rating " + \
		"From business b, business_rating br " + \
		"Where b.business_id = br.business_id " + \
		"And b.name = '" + entity + "' ORDER BY b.longitude DESC, b.latitude DESC"

	con = cx_Oracle.connect(views.rds_conn_str)
	cur = con.cursor()
	cur.execute(sql)
	result = cur.fetchall()

	data = [];

	for res_row in result:
		row = []
		row.append(float(res_row[0]))
		row.append(float(res_row[1]))
		row.append(res_row[2])
		row.append(float(res_row[3]))

		if (row[1] <= 49.5 and row[1] >= 23.7 and row[0] <= -62.3 and row[0] >= -129.3):
			data.append(row)
	print data

