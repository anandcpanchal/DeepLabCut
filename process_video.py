import deeplabcut

import pdb 
import os
import argparse as arg

argparser = arg.ArgumentParser(description="Process video repetition count with DeepLabCut")
argparser.add_argument('-c', dest="config",help="config_yaml_path", required=True)
argparser.add_argument('-i', dest="video_path",help="path to the video file", required=True)
argparser.add_argument('-s', dest="save_csv",help="save csv results", default=True)
args = argparser.parse_args()

_, extension_ = os.path.splittext( args.video_path)

deeplabcut.analyze_videos( args.config, [ args.video_path ], videotype= extension_, save_as_csv= args.save_csv)
