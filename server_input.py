from tornado.web import Application, RequestHandler
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
			db.insert_record( data )
			self.write( data)
		except:
			raise HTTPError(2400,"Error in processing")

def make_app():
	urls = [("/process_video", InferenceHandler)]
	return Application(urls)

if __name__ == '__main__':

	# Init DB
	db_path = "/home/anand/Music/DeepLabCut/test.sqlite3"
	db = ServerDB( db_path, "RECORD")
	app = make_app()
	app.listen(3000)
	IOLoop.instance().start()