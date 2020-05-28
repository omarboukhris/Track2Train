import numpy as np
import cv2

class PyrLKTracker :
	def __init__ (self) :
		# params for ShiTomasi corner detection
		self.feature_params = dict( 
			maxCorners = 100,
			qualityLevel = 0.3,
			minDistance = 7,
			blockSize = 7 )

		# Parameters for lucas kanade optical flow
		self.lk_params = dict( 
			winSize  = (15,15),
			maxLevel = 2,
			criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
		self.old_gray = None
		self.frame_gray = None
		self.p0 = None
		self.issetup = False

	def setSetup (self, val) :
		self.issetup = val
	def isSetup (self) :
		return self.issetup

	#setup tracker with frame and initial points
	def setup (self, frame, p0) :
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		self.update_old (frame) 
		self.p0 = np.array(p0).astype(np.float32)
		self.issetup = True

	#update old frame (frame must be gray)
	def update_old (self, frame) :
		self.old_gray = frame.copy()

	#set current frame (colored)
	def set_frame (self, frame) :
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		self.frame_gray = frame.copy()

	def track_frame (self) :
		if len(self.p0) == 0 :
			return []
		p1, st, err = cv2.calcOpticalFlowPyrLK(
			self.old_gray, 
			self.frame_gray, 
			self.p0, 
			None, 
			**self.lk_params)

		out = []
		for point in p1 :
			out.append((point[0], point[1]))

		self.p0 = p1
		return out
