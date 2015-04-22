import os
from base64 import b64encode, b64decode
import boto
from boto.dynamodb2.table import Table
from dynamo_connect import Dynamo

conn = Dynamo()

f = open('tmp.png', 'rb')
img_data = f.read()
f.close()

conn.add_map(table='Business', hash_key='2', range_key='0.5', map_data=img_data)
heat_map = conn.get_map(table='Business', hash_key='2', range_key='0.5')

#print conn.describe_table('Business')
#table = conn.get_table('Business')
#item_data={'map': b64encode(img_data)}
#user = table.new_item(hash_key='1', range_key='0.5', attrs=item_data)
#user.put()

#item = table.get_item(hash_key='1', range_key='0.5', attributes_to_get=['map'])
#heat_map = item['map']
#heat_map = b64decode(heat_map)

f = open('tmp2.png', 'wb')
f.write(heat_map)
f.close()
