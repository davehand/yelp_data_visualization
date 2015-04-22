import os
from base64 import b64encode, b64decode
import boto
from boto.dynamodb2.table import Table

class Dynamo:

    def __init__(self):
        self.conn = None
        try:
            self.conn = boto.connect_dynamodb(aws_access_key_id=os.environ.get('aws_access'), aws_secret_access_key=os.environ.get('aws_secret'))
        except:
            print "Error while attempting to connect to dynamo"

    def add_map(self, table, hash_key, range_key, map_data):
        try:
            table = self.conn.get_table(table)
            item_data={'map': b64encode(map_data)}
            user = table.new_item(hash_key=hash_key, range_key=range_key, attrs=item_data)
            user.put()
            return True
        except:
            print "Error while adding item to dynamo"
            return False

    def get_map(self, table, hash_key, range_key):
        try:
            table = self.conn.get_table(table)
            item = table.get_item(hash_key=hash_key, range_key=range_key, attributes_to_get=['map'])
            heat_map = item['map']
            return b64decode(heat_map)
        except:
            print "Error while retrieving item from dynamo"
            return None

