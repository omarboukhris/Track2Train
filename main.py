
from VideoProcessor import *

import sys

if __name__ == "__main__" :
	vr = VideoReader(sys.argv[1], ".")
	vr.run()


