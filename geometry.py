import numpy as np
# import cv2


class Geometry:

	def __init__( self, DEBUG=False):
		self.pi = np.pi
		self.DEBUG = DEBUG

	
	class Point:

		def __init__( self, x_ia, y_ia):
			self.x = x_ia
			self.y = y_ia

		def get_x(self): return self.x
		def get_y(self): return self.y		


	def get_distance(self, p1,p2):
		return np.sqrt( np.square( p2.get_x() - p1.get_x() ) + np.square( p2.get_y() - p1.get_y()))

	def get_angles( self, p1, p2, p3):
		# let a,b,c are sides between p1-p2, p2-p3 and p3-p1 respectively
		# angle A faces to side a i.e. center at p3
		# angle B faces to side b i.e. center at p1
		# angle C faces to side c i.e. center at p2
        
#	        	p1
#	           /\
#	        a /B \ c
#			 /    \
#			/C   A \
#		  p2---------p3
# 			    b

		a = self.get_distance( p1, p2)
		b = self.get_distance( p2, p3)
		c = self.get_distance( p3, p1)

		if self.DEBUG:
			print("Distance between points %d,%d and %d,%d ---> %f" % ( p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y(), a))
			print("Distance between points %d,%d and %d,%d ---> %f" % ( p2.get_x(), p2.get_y(), p3.get_x(), p3.get_y(), b))
			print("Distance between points %d,%d and %d,%d ---> %f" % ( p3.get_x(), p3.get_y(), p1.get_x(), p1.get_y(), c))
		
		A = np.degrees( np.arccos( ( np.square(b) + np.square(c) - np.square(a) ) / ( 2 * b * c ) ) )
		B = np.degrees( np.arccos( ( np.square(a) + np.square(c) - np.square(b) ) / ( 2 * a * c ) ) )
		C = np.degrees( np.arccos( ( np.square(a) + np.square(b) - np.square(c) ) / ( 2 * a * b ) )	)	

		return [B,C,A]

if __name__=="__main__":
	test = Geometry(DEBUG=True)
	p1 = test.Point(0,0)
	p2 = test.Point(3,0)
	p3 = test.Point(0,4)
	print(test.get_angles(p1,p2,p3))

	p1 = test.Point(1,1)	
	p2 = test.Point(1,3)
	p3 = test.Point(1,4)
	print(test.get_angles(p1,p2,p3))