from tornado.web import Application, RequestHandler, HTTPError
from tornado.ioloop import IOLoop
from server_db import ServerDB
import json

class InferenceHandler (RequestHandler):
	def get(self):
		self.write({'message': 'hello world'})

	def post(self):
		try:
			data = json.loads( self.request.body)
			id_ = data['id']
			link_ = data['video']
			data["processed"] = 0
			data["published"] = 0
			try:
				db.insert_record( data )
				self.write( data)
			except:
				raise HTTPError(2404,"Error in record insertion")
		except:
			raise HTTPError(2400,"Error in processing")

def make_app():
	urls = [("/process_video", InferenceHandler)]
	return Application(urls)

if __name__ == '__main__':

	# Init DB
	PORT = 3000
	db_path = "/home/paperspace/inference/DeepLabCut/test_db.sqlite3"
	db = ServerDB( db_path, "RECORD")
	print(" Initiating on Port : ", PORT)
	app = make_app()
	app.listen(PORT)
	IOLoop.instance().start()
