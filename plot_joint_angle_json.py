import pdb 

import argparse as arg

import json

from matplotlib import pyplot as plt

def plot_joints( json_path_ia):
	with open( json_path_ia ) as file:
	  angle_data = json.load( file)

	fig, ax = plt.subplots()
	for key in angle_data.keys():
		ax.plot( angle_data[key], '-*',label=key)

	legend = ax.legend(loc='lower center', fontsize='small')
	plt.title( 'Angles')
	plt.show()

if __name__ == "__main__":
	# Input Processing
	argparser = arg.ArgumentParser(description="Process angle json")
	argparser.add_argument('-i', dest="json_path",help="path to the angle json file", required=True)
	args = argparser.parse_args()

	plot_joints( args.json_path )
