import numpy as np
import numpy.linalg 
import cv2
import pandas as pd
from collections import OrderedDict as odict
#todo : write export data

class TrackedMarker :
	def __init__ (self, frame, imagepath) :
		self.frame = frame
		self.imagepath = imagepath + ".png"
		self.markers = []

	def add (self, p) :
		self.markers.append(p)

	def remove (self, p) :
		i = self.getClosest(p)
		if i == None : return 
		self.markers.pop(i)
	
	def replace (self, p) :
		self.remove(p)
		self.markers.append(p)

	def getClosest (self, p) :
		if len(self.markers) < 1 :
			return None
		min_point = numpy.linalg.norm (np.array(p)-np.array(self.markers[0]))
		min_ind = 0
		for i in range (1, len(self.markers)) :
			marker = self.markers[i]
			actual_min = np.linalg.norm(np.array(p)-np.array(marker))
			if actual_min < min_point :
				min_point = actual_min
				min_ind = i
		return min_ind
	
	def get (self) :
		return (self.imagepath, self.markers)
	
	def get_str (self) :
		return "{} : {}".format(self.imagepath, self.markers)
	
	def export (self) :
		if type(self.frame) == type(None) :
			return
		cv2.imwrite (self.imagepath, self.frame)
		#export image path and markers in csv
		#generate appropriate binarized frame during training 


class TrackedMarkersDataSet :
	def __init__ (self, outfolder="mydata", imagepath="images/image_{}") :
		self.tracked_markers = []
		self.count = 0
		self.imagepath = "{}/{}".format(outfolder, imagepath)
		self.outfolder = outfolder

	def add (self, frame, points2d) :
		tr_markers_byframe = TrackedMarker(frame, self.imagepath.format(self.count))

		for p in points2d :
			tr_markers_byframe.add(p)
		self.tracked_markers.append(
			tr_markers_byframe
		)
		self.count += 1

	def getCurrent (self) :
		if len(self.tracked_markers) == 0 :
			self.add (None, [])
		return self.tracked_markers[-1]

	def pop (self) :
		self.tracked_markers.pop()
		self.count -= 1

	def export(self): 
		#define export to csv or whatever fileformat is suitable
		d = odict()
		for trm in self.tracked_markers :
			k, v = trm.get()
			d[k] = v
			trm.export ()
		df = pd.DataFrame.from_dict(d, orient="index")
		df.to_csv("{}/dataset.csv".format(self.outfolder))

	def __str__ (self): 
		ss = ""
		for it in self.tracked_markers :
			ss += it.get_str() + "\n"
		return ss

