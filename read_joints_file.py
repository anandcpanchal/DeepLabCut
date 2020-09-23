class Joints:

	def __init__(self, joint_file):
		self.file = joint_file

	def get_joints_dictionary(self):
		joint_dict = {}
		joint_file = open( self.file, 'r')
		lines = joint_file.readlines()
		for i,line in enumerate(lines):
			line = line.replace('\n','').split(',')
			if len(line) == 3:
				joint_dict[i] = line 
		return joint_dict

if __name__== "__main__":
	file_path = '/home/anand/Music/DeepLabCut/test_joint_list.txt'
	joints = Joints( file_path )
	print(joints.get_joints_dictionary())