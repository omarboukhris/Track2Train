import cv2
import numpy as np

from MarkersData import * 
import opktracker as opk

"""
should have an event handler
right mouse click :
	remove closest
left mouse click :
	add/rectify point

save result each 10 frames in :
	imageFolder/image_%id%
	tracked_markers.csv or .pkl
"""
class VideoReader : 
	markers = TrackedMarkersDataSet()
	tracker = opk.PyrLKTracker()
	frame = None

	def __init__ (self, filename, outputfolder) :
		self.filename = filename
		self.outfolder = outputfolder
		self.cap = None
		self.frame = None

	@staticmethod
	def draw_points_on_frame () :
		frame = np.copy(VideoReader.frame)
		for point in  VideoReader.markers.getCurrent().markers :
			cv2.circle(frame, point, radius=4, color=(255, 0, 0), thickness=4)
		return frame

	@staticmethod
	def fn_call_back (event, x, y, flags, param) :
		#todo : show points state after update (size or something)
		
		if event == cv2.EVENT_LBUTTONDOWN:
			#left mouse click :
			#add point
			VideoReader.markers.getCurrent().add(p=(x,y))
			#draw it on frame
			frame = VideoReader.draw_points_on_frame()
			cv2.imshow('Frame',frame)
			VideoReader.tracker.setSetup(False)
		elif event == cv2.EVENT_RBUTTONDOWN:
			#right mouse click :
			#remove closest
			VideoReader.markers.getCurrent().remove(p=(x,y))
			#draw on frame
			frame = VideoReader.draw_points_on_frame()
			cv2.imshow('Frame',frame)
			VideoReader.tracker.setSetup(False)
		elif event == cv2.EVENT_RBUTTONDBLCLK :
			#double rclick :
			#replace point
			#VideoReader.markers.getCurrent().replace(p=(x,y))
			##draw on frame
			#frame = VideoReader.draw_points_on_frame()
			#cv2.imshow('Frame',frame)
			pass
		elif event == cv2.EVENT_LBUTTONDBLCLK :
			print ("mousecallback dbl : {}".format(VideoReader.markers))
			pass

	#loads video
	def run (self) :
		# Create a VideoCapture object and read from input file
		# If the input is the camera, pass 0 instead of the video file name
		self.cap = cv2.VideoCapture(self.filename)
		cv2.namedWindow("Frame")
		cv2.setMouseCallback("Frame", VideoReader.fn_call_back) 

		# Check if camera opened successfully
		if (self.cap.isOpened()== False): 
			print("Error opening video stream or file")

		# process video 
		self.process_stream()

		# Closes all the frames
		cv2.destroyAllWindows()

	def trackOnFrame(self, frame) :
		#setup tracker if needed
		if VideoReader.markers.getCurrent().markers == [] :
			return 
		if not VideoReader.tracker.isSetup () :
			VideoReader.tracker.setup (
				VideoReader.frame,
				VideoReader.markers.getCurrent().markers)
		
		#apply tracker here
		VideoReader.tracker.set_frame (VideoReader.frame)
		p1 = VideoReader.tracker.track_frame()
		VideoReader.markers.add (VideoReader.frame, p1)
		frame = VideoReader.draw_points_on_frame()
		cv2.imshow('Frame',frame)

	def fastforward (self) :
		n = 10
		print("fforward")
		while True :
			if not self.pause :
				for i in range (n) :
					self.cap.grab()
				ret, self.frame = self.cap.read()
				if ret == True :
					VideoReader.frame = np.copy(self.frame)
					cv2.imshow('Frame',VideoReader.frame)
				else : break

			pressed_key = cv2.waitKey(25) & 0xFF
			if pressed_key == ord('q') :
				break
			if pressed_key == ord(' ') :
				self.pause = not self.pause
			if pressed_key == ord('+'):
				n += 5
			if pressed_key == ord('-'):
				n -= 5

	def process_stream (self) :
		# Read until video is completed
		self.pause = False
		VideoReader.tracker = opk.PyrLKTracker()
		while(self.cap.isOpened()):
			# Capture frame-by-frame
			if not self.pause :
				ret, self.frame = self.cap.read()
				if ret == True:

					# Display the resulting frame
					VideoReader.frame = np.copy(self.frame)
					cv2.imshow('Frame',VideoReader.frame)
					self.trackOnFrame (self.frame)

				# Break the loop
				else: 
					break
			# Press Q on keyboard to  exit
			pressed_key = cv2.waitKey(25) & 0xFF
			if pressed_key == ord('q'):
				break
			elif pressed_key == ord(' '):
				self.pause = not self.pause
			elif pressed_key == ord('+'):
				self.fastforward()

		# When everything done, release the video capture object
		self.cap.release()
		VideoReader.markers.export()
