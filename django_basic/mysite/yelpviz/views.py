from django.http import HttpResponse
from django.shortcuts import render
import sys

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

def index(request):
	con = cx_Oracle.connect(rds_conn_str)
	cur = con.cursor()
	resp = "<b>These businesses have more than 50 locations!</b>\n"

	cur.execute('SELECT name from business GROUP BY name having COUNT(name) > 50')
	for result in cur:
		resp += result[0]
		resp += "<br></br>"

	cur.close()
	con.close()

	return HttpResponse(resp)
