import cv2
import numpy as np
import sys
from fractions import Fraction
import random
import librosa
import math
from shutil import copyfile

class Video_sync():
	def __init__(self):
		pass
	def syncing(self,audio_file,v_file, output_file):
		cap = cv2.VideoCapture(v_file)
		frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		fps = int(cap.get(cv2.CAP_PROP_FPS))   

		buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

		fc = 0
		ret = True

		while (fc < frameCount  and ret):
		    ret, buf[fc] = cap.read()
		    fc += 1

		cap.release()

		# manipulation starts----------------
		
		original_length = librosa.get_duration(filename=v_file)  # t1
		new_length = librosa.get_duration(filename=audio_file)   # t2

		frameCount = int(fps*original_length)
		n_frameCount = int(fps*new_length)
		n_file = np.empty((n_frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

		if new_length == original_length:
			print("Already same length")
			i = 0
			while i < frameCount:
				try:
					n_file[i] = buf[i]
				except:
					print("Error in reading frame", i)
				i+=1
		elif original_length < new_length:  #frames to be added
			n = int((new_length-original_length)*fps)
			f_hop = Fraction(int(original_length*fps),int(n))
			every_frame = int(int(original_length*fps)/int(n))
			# to_be_added = f_hop.denominator
			i = 0
			idx = 0
			while i < frameCount && idx < n_frameCount:
				n_file[idx] = buf[i]
				idx+=1
				if i%every_frame==0:
					n_file[idx] = buf[i]
					idx+=1
				i+=1
		elif original_length > new_length: #frames to be dropped
			n = int((new_length-original_length)*fps)
			f_hop = Fraction(int(original_length*fps),int(n))
			every_frame = int(int(original_length*fps)/int(n))
			# to_be_added = f_hop.denominator
			i = 0
			idx = 0
			while i < frameCount && idx < n_frameCount:
				n_file[idx] = buf[i]
				if i%every_frame==0:
					i+=1
				idx+=1
				i+=1
			

		writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), fps, (frameWidth, frameHeight), True)
		for i in range(n_frameCount):
		    writer.write(n_file[i])

				

		# if f_hop > 1:
