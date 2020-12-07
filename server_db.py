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
	
	def init_record_table( self, connection_ia):
		cursor_ = connection_ia.cursor()
		make_table = "CREATE TABLE " + self.table + " (ITEM INT NOT NULL AUTO_INCREMENT PRIMARY KEY UNIQUE, ID CHAR(256) UNIQUE, VIDEO CHAR(256),METADATA CHAR(1024), PROCESSED INT, PUBLISHED INT, PRIMARY_COUNT INT, SECONDARY_COUNT INT)"
		cursor_.execute( make_table)
		cursor_.close()
		connection_ia.commit()

	def db_init(self):
		head_, tail_ = os.path.split( self.path)
		if not os.path.exists( head_):
			if self.debug: print(" Creating Directory : ", head_)
			os.makedirs( head_)
		# Create db
		conn_ = sqlite.connect( self.path)
		if self.debug: print(" Connected to db : ", self.path)
		# Create Table
		self.init_record_table( conn_)
		conn_.close()


	def get_table_name(self):
		return self.table

	def insert_record( self, record_ia):
		command_ = "INSERT INTO " + self.table + "(ID, VIDEO, METADATA, PROCESSED, PUBLISHED, PRIMARY_COUNT, SECONDARY_COUNT) values ( ?, ?, ?, ?, ?, ?, ?)"
		try:
			self.cursor.execute( command_, ( record_ia["id"], record_ia["video"], str(record_ia["metadata"]), str(record_ia["processed"]), str(record_ia["published"]), '0', '0'))
			self.db.commit()
		except sqlite.IntegrityError:
			raise 

	def get_unprocessed_record(self):
		command_ = "SELECT * from record where PROCESSED is 0"
		self.cursor.execute( command_)
		data_ = self.cursor.fetchone()
		data_dict_o = {}
		if data_:
			data_dict_o["id"] = data_[0]
			data_dict_o["video"] = data_[1]
			data_dict_o["metadata"] = data_[2]
			data_dict_o["processed"] = data_[3]
			data_dict_o["published"] = data_[4]
			return data_dict_o
		else:
			return data_dict_o
	
	def update_result( self, id_ia, primary_count_ia, secondary_count_ia):
		command_ = "UPDATE " + self.table + " SET PRIMARY_COUNT = " + str( primary_count_ia) + ", SECONDARY_COUNT = " + str( secondary_count_ia) + " WHERE ID = " + str(id_ia)
		try:
			self.cursor.execute( command_)
			self.db.commit()
		except sqlite.IntegrityError:
			raise 

	def update_processed_flag( self, id_ia, value_ia):
		command_ = "UPDATE " + self.table + " SET PROCESSED = " + str( value_ia) + " WHERE id = " + str( id_ia)
		self.cursor.execute(command_)
		self.db.commit()

	def update_published_flag( self, id_ia, value_ia):
		command_ = "UPDATE " + self.table + " SET PUBLISHED = " + str( value_ia) + " WHERE id = " + str( id_ia)
		self.cursor.execute(command_)
		self.db.commit()

if __name__=="__main__":
	db_path = '/home/anand/Music/DeepLabCut/test.sqlite3'
	db = ServerDB( db_path, 'RECORD')
	print(db.get_unprocessed_record())
	print(db.update_processed_flag(1234, 1))
	print(db.update_published_flag(1234, 1))