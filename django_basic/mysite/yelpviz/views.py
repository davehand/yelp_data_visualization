from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
import sys
from dynamo_connect import Dynamo

import os
os.environ['LD_LIBRARY_PATH'] = '/usr/lib/oracle/11.2/client64/lib/'
os.environ['ORACLE_HOME'] = '/usr/lib/oracle/11.2/client64/'
import cx_Oracle

rds_host =     'yelp.czscqrbdzjc7.us-east-1.rds.amazonaws.com'
rds_sid =      'ouryelp'
rds_username = 'damn'
rds_password = 'damnyelp'
rds_port =     1521
rds_dsn =      cx_Oracle.makedsn(rds_host, 1521, rds_sid)
rds_conn_str = rds_username + '/' + rds_password + '@' + rds_dsn

def bsearch(request):
	entity = request.GET.get('business').replace("''", "'")
	scale = request.GET.get('scale')

	if request.method == 'GET':
		print 'Querying business \'%s\' at scale %s' % (entity, scale)

	#logic for connecting to the dynamodb and getting the image
	dydb = Dynamo()
	#hash_key will be business name, range_key is scaling factor
	heat_map = dydb.get_map(table='Business', hash_key=entity, range_key=scale)
	if heat_map == None:
		#code for generating map on the fly and adding map to dynamo
		#need to turn the map generation code into a class with a method for this
		#someone else who is more familiar with that code should do this - Dave
		print "hi"
	else:
		f = open('/home/ec2-user/yelp_data_visualization/django_basic/mysite/yelpviz/static/yelpviz/tmp.png', 'wb')
		f.write(heat_map)
		f.close()

	#con = cx_Oracle.connect(rds_conn_str)
	#ur = con.cursor()
	#resp = "<b>These businesses have more than 50 locations!</b>\n"

	#cur.execute('SELECT name from business GROUP BY name having COUNT(name) > 50')
	#for result in cur:
	#	resp += result[0]
	#	resp += "<br></br>"

	#cur.close()
	#con.close()

	#return HttpResponse(resp)
	return render_to_response("yelpviz/map.html")

def csearch(request):
	entity = request.GET.get('business').replace("''", "'")
	scale = request.GET.get('scale')

	if request.method == 'GET':
		print 'Querying category \'%s\' at scale %s' % (entity, scale)
	
	
	#logic for connecting to the dynamodb and getting the image
	dydb = Dynamo()
	#hash_key will be business name, range_key is scaling factor
	heat_map = dydb.get_map(table='Business_Category', hash_key=entity, range_key=scale)
	if heat_map == None:
		#code for generating map on the fly and adding map to dynamo
		#need to turn the map generation code into a class with a method for this
		#someone else who is more familiar with that code should do this - Dave
		print "hi"
	else:
		f = open('/home/ec2-user/yelp_data_visualization/django_basic/mysite/yelpviz/static/yelpviz/tmp.png', 'wb')
		f.write(heat_map)
		f.close()

	#return HttpResponse(resp)
	return render_to_response("yelpviz/map.html")

def home(request):
	return render_to_response("yelpviz/map.html")
