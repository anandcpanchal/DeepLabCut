from server_db import ServerDB
import time
import sys

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
	db_path = '/home/anand/Music/DeepLabCut/test.sqlite3'
	process = ServerProcess( db_path, 'RECORD')
	while True:
		if process.debug: print("Fetching record from db")
		record = process.get_record_for_processing()	
		if record:
			process.db.
			process.db.update_processed_flag( record["id"], 1)
			record["processed"] = 1
			if process.debug: print("Processing : ", record)
			
			process.db.update_published_flag( record["id"], 1)
			record["published"] = 1
			if process.debug: print("Published : ", record)
			
		else:
			if process.debug: print("No pending record found, sleeping for 10 sec")
			process.wait(10)
			pass