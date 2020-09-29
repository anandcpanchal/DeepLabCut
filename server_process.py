from server_db import ServerDB
from process_video import process_video

import argparse as arg
import time
import sys
import json


class ServerProcess:

	def __init__(self, db_path_ia, record_name_ia, debug=True):
		self.debug = debug
		self.db= ServerDB( db_path_ia, record_name_ia)
		self.processing = False
		return
	def __del__(self):
		return

	def set_processing( self):
		self.processing = True

	def reset_processing( self):
		self.processing = False

	def is_processing( self):
		return self.processing

	def progressBar( self, current, total, barLength = 20):
		percent = float(current) * 100 / total
		arrow   = '-' * int(percent/100 * barLength - 1) + '>'
		spaces  = ' ' * (barLength - len(arrow))
		return( arrow, spaces, percent + 10)

	def wait(self, delay_ia):
		for i in range(1, delay_ia):
			print('Waiting : [%s%s] %d %%' % self.progressBar( i, delay_ia), end='\r')
			time.sleep( 1)

	def get_record_for_processing(self):
		record = self.db.get_unprocessed_record()
		if record:
			return record
		else:
			return None


if __name__ == "__main__":
	# Input Processing
    argparser = arg.ArgumentParser(description="Process video repetition count with DeepLabCut")
    argparser.add_argument('-c', dest="config", default="./inference_config.json", help="config_json_path", required=True)
    args = argparser.parse_args()

    wait_counter = 0

    inference_config_file = open( args.config )
    config = json.load( inference_config_file )
    db_path = config['db_path']
    process = ServerProcess( db_path, 'RECORD')
    while True:
    	if process.debug: print("Fetching record from db")
    	record = process.get_record_for_processing()	
    	if record:
    		wait_counter = 0
    		metadata = record['metadata']
    		output = process_video( config['inference_config'], record['video'], record['metadata'], config['output_video_boolean_flag'])
    		if process.debug: 
    			for key in output.keys():
    				print( key, " : ", output[key])
    		if output:
    			metadata = json.loads( metadata.replace('\'','\"') )# convert metadata string to dictionary
    			process.db.update_processed_flag( record["id"], 1)
    			record["processed"] = 1
    			if process.debug: print("Processing : ", record)
    			process.db.update_result( record['id'], output['counter_data'][ metadata['primary_organ']], output['counter_data'][ metadata['secondary_organ']])
    			process.db.update_published_flag( record["id"], 1)
    			record["published"] = 1
    			if process.debug: print("Published : ", record)
    	else:
    		wait_counter += 1
    		if process.debug: print(str( wait_counter) ," >> No pending record found, sleeping for 10 sec")    		
    		process.wait(10)
    		pass
