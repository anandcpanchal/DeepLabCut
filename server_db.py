import sqlite3 as sqlite
import os

class ServerDB:

	def __init__( self, db_path_ia, table_name_ia, debug=True):
		self.debug = debug
		self.path = db_path_ia
		self.table = table_name_ia
		self.db_present = self.check_for_db_presence()
		if not self.db_present:
			self.db_init()
		
		self.db = sqlite.connect( self.path)
		self.cursor = self.db.cursor()

	def __del__(self):
		self.cursor.close()
		self.db.commit()
		self.db.close()

	def check_for_db_presence(self):
		db_presence = os.path.exists( self.path ) 
		if self.debug:
			print(" DB Presence : ", db_presence)
		return db_presence

	def db_init(self):
		head_, tail_ = os.path.split( self.path)
		if not os.path.exists( head_):
			if self.debug: print(" Creating Directory : ", head_)
			os.makedirs( head_)
		# Create db
		conn_ = sqlite.connect( self.path)
		if self.debug: print(" Connected to db : ", self.path)
		# Create Table
		self.init_table( conn_)
		conn_.close()

	def init_table( self, connection_ia):
		cursor_ = connection_ia.cursor()
		make_table = "CREATE TABLE " + self.table + " (ID INT PRIMARY KEY,VIDEO CHAR(256),METADATA CHAR(1024), PROCESSED INT, PUBLISHED INT)"
		cursor_.execute( make_table)
		cursor_.close()
		connection_ia.commit()

	def get_table_name(self):
		return self.table

	def insert_record( self, record_ia):
		command_ = "INSERT INTO " + self.table + " values ( ? , ?, ?, ?, ?)"
		self.cursor.execute( command_, ( record_ia["id"], record_ia["video"], str(record_ia["metadata"]), str(record_ia["processed"]), str(record_ia["published"])))
		self.db.commit()

if __name__=="__main__":
	db_path = '/home/anand/Music/DeepLabCut/test.sqlite3'
	db = ServerDB( db_path, 'RECORD')