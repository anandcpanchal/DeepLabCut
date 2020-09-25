from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

import json

class InferenceHandler (RequestHandler):
	def get(self):
		self.write({'message': 'hello world'})

	def post(self):
		try:
			data = json.loads( self.request.body)
			id_ = data['id']
			link_ = data['video']
			self.write( data)
		except:
			raise HTTPError(2400,"Error in processing")
			
def make_app():
	urls = [("/process_video", InferenceHandler)]
	return Application(urls)

if __name__ == '__main__':
	app = make_app()
	app.listen(3000)
	IOLoop.instance().start()