import pdb 

# Input Processing
import os
import argparse as arg

# Deeplabcut
import deeplabcut

# Output CSV postprocessing
import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d

# angle processing
from geometry import Geometry 
from read_joints_file import Joints
import json

# Input Processing
argparser = arg.ArgumentParser(description="Process video repetition count with DeepLabCut")
argparser.add_argument('-c', dest="config",help="config_yaml_path", required=True)
argparser.add_argument('-i', dest="video_path",help="path to the video file", required=True)
argparser.add_argument('-o', dest="output_video",help="output video file", default=True)
argparser.add_argument('-j', dest="joints",help="joint list file", default=None)
args = argparser.parse_args()

path_, extension_ = os.path.splitext( args.video_path)

# Deeplabcut Inference
try:
	o_DLCScorer = deeplabcut.analyze_videos( args.config, [ args.video_path ], videotype= extension_, save_as_csv= True)
	o_result_path = path_ + o_DLCScorer + '.csv'

	print("Result path : ",  o_result_path)
except:
	print(" DeepLabCut Inference Failed - Exiting ")
	exit()


# Output CSV postprocessing
csv_result = pd.read_csv( o_result_path )

# Preprocess result
def preprocess_result( csv_result_pd_frame_ioa ):
	pre_header = csv_result_pd_frame_ioa.iloc[0]
	post_header = csv_result_pd_frame_ioa.iloc[1]
	header = pre_header.str.cat( post_header, sep='_' )
	csv_result_pd_frame_ioa = csv_result_pd_frame_ioa[2:]
	csv_result_pd_frame_ioa.columns = header
	return csv_result_pd_frame_ioa

csv_result = preprocess_result( csv_result )

csv_columns = csv_result.columns.tolist()[1:] # extracting column names

# Convert results to dict
def init_result_dict( columns_ia):
    result_dict_oa = {}
    for column_ in columns_ia:
        result_dict_oa[ column_ ] = list()
    return result_dict_oa

csv_result_dict = init_result_dict( csv_columns )

for column_ in csv_columns:
    csv_result_dict[ column_ ] = csv_result[ column_ ].tolist()

# Convert coordinates list to numpy array
for key_ in csv_result_dict.keys():
    csv_result_dict[ key_ ] = np.array( csv_result_dict[ key_ ], dtype='float')

# Convert to Polar form
def convert2Polar(x,y):
    r = np.sqrt( x**2 + y**2)
    t = np.arctan2( y, x)
    return r,t

csv_result_keys = list( csv_result_dict.keys() )
polar_result_dict = {}
i = 0
while i < len( csv_result_keys ):
    polar_result_dict[ csv_result_keys[i].replace('_x','') ] = convert2Polar( csv_result_dict[ csv_result_keys[i] ], csv_result_dict[ csv_result_keys[i+1] ] )
    i = i + 3

polar_keys = list( polar_result_dict.keys() )


# Counter
def on_segment( p, q, r):
    if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
        return True
    return False

def orientation( p, q, r):
    val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
    if val == 0 : return 0
    return 1 if val > 0 else -1

def intersects( seg1, seg2):
    p1, q1 = seg1
    p2, q2 = seg2
    
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    
    if o1 != o2 and o3 != o4:
        return True
    
    if o1 == 0 and on_segment(p1, q1, p2) : return True
    if o2 == 0 and on_segment(p1, q1, q2) : return True
    if o3 == 0 and on_segment(p2, q2, p1) : return True
    if o4 == 0 and on_segment(p2, q2, p1) : return True
    
    return False

def count_data( filter_data_ia ):
    ref_line = ( ( 0,filter_data_ia.mean() ), ( filter_data_ia.shape[0],filter_data_ia.mean()) )
    result = []
    for i,point in enumerate( filter_data_ia ):
        if i < len( filter_data_ia )-1:
            segment = ( (i,filter_data_ia[i]),((i+1,filter_data_ia[i+1])) )
            result.append( intersects(ref_line, segment) )
    return int( result.count(True) / 2 )


MAGNITUDE = 0
ANGLE = 1

counter_data_dict = {}
for key in polar_keys:
    counter_data_dict[key] = count_data(gaussian_filter1d( polar_result_dict[key][MAGNITUDE],7))

for key_ in counter_data_dict.keys():
	print( key_ , '	:	', counter_data_dict[ key_ ] )

if args.output_video:
	deeplabcut.create_labeled_video( args.config, [ args.video_path ], videotype= extension_, draw_skeleton=True)


# Joint Angle Analysis
if args.joints:
    path = o_result_path

    # Joint Angle Analysis
    joints = Joints( args.joints )
    joint_dict = joints.get_joints_dictionary()
    print("Joint to analyze : ")
    print( joint_dict )
    coord_dict = {}
    for key in joint_dict.keys():
        coord_dict[key] = {}
        for item in joint_dict[key]:
            coord_dict[key][item] = {}
            for i,value in enumerate(csv_result_dict[ item+'_x']):
                coord_dict[key][item][i] = (csv_result_dict[ item+'_x'][i], csv_result_dict[ item+'_y'][i])


    angle_dict = {}
    angle = Geometry()

    for key in coord_dict.keys():
        angle_dict[key] = list()
        joints = list(coord_dict[key].keys())
        for i,_ in enumerate(coord_dict[key][joints[0]].keys()):
            p1 = angle.Point( coord_dict[key][joints[0]][i][0], coord_dict[key][joints[0]][i][1] )
            p2 = angle.Point( coord_dict[key][joints[1]][i][0], coord_dict[key][joints[1]][i][1] )
            p3 = angle.Point( coord_dict[key][joints[2]][i][0], coord_dict[key][joints[2]][i][1] )
            angle_dict[key].append( angle.get_angles(p1,p2,p3)[1]) # Saving only central angle
    
    with open( path.replace('.csv','.json'),'w') as out_file:
        json.dump( angle_dict, out_file) 