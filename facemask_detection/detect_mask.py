# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os

from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}


def detect_and_predict_mask(frame, faceNet, maskNet,args):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

def detectmask():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--face", type=str,
		default="face_detector",
		help="path to face detector model directory")
	ap.add_argument("-m", "--model", type=str,
		default="mask_detector.model",
		help="path to trained face mask detector model")
	ap.add_argument("-c", "--confidence", type=float, default=0.5,
		help="minimum probability to filter weak detections")
	args = vars(ap.parse_args())

	print("")
	print("Loading the face mask detector...")
	print("")
	# load our serialized face detector model from disk
	# print("[INFO] loading face detector model...")
	prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
	weightsPath = os.path.sep.join([args["face"],
		"res10_300x300_ssd_iter_140000.caffemodel"])
	faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

	# load the face mask detector model from disk
	# print("[INFO] loading face mask detector model...")
	maskNet = load_model(args["model"])

	# initialize the video stream and allow the camera sensor to warm up
	# print("[INFO] starting video stream...")
	#vs = VideoStream(src=0).start()
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	hasMask = False

	# loop over the frames from the video stream
	#kimmy - turn off completely after 3 confirmations that the mask is on
	#if not wearing a mask for 3 confirmations turn off and say go away
	#but time for no mask takes longer incase they move or is not detected
	#maybe have a buffer time before turning on so the person in front of you can leave?

	has_mask_counter = 0
	no_mask_counter = 0
	mask_on = False

	#if they have a mask for 3 cycles you can confirm that they have a mask
	#if they dont have a mask for 10 cycles then ask them to leave
	while True:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=500)

		# detect faces in the frame and determine if they are wearing a
		# face mask or not
		(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet,args)


		# loop over the detected face locations and their corresponding
		# locations
		for (box, pred) in zip(locs, preds):
			# unpack the bounding box and predictions
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred

			# determine the class label and color we'll use to draw
			# the bounding box and text
			if mask > withoutMask:
				label = "Thank You. Mask On."
				color = (0, 255, 0)
				hasMask = True
				has_mask_counter += 1
				# print("has mask", has_mask_counter)
			else:
				label = "No Face Mask Detected"
				color = (0, 0, 255)
				hasMask = False
				no_mask_counter += 1
				# print ("has no mask", no_mask_counter)
			
			#if (not) wearing a mask is confirmed, break the for
			if has_mask_counter > 1:
				break
			elif no_mask_counter >2:
				break
			
			# display the label and bounding box rectangle on the output
			# frame
			cv2.putText(frame, label, (startX-50, startY - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		
		if has_mask_counter > 1:
			mask_on = True
			# print("the has_mask_counter has exeeded > 1")
			# print("we will break this loop")
			break
		elif no_mask_counter >2:
			mask_on = False
			# print("no_mask_counter has exeeded > 2")
			print("Please wear a mask properly")
			break


		# show the output frame
		cv2.imshow("Face Mask Detector", frame)
		key = cv2.waitKey(1) & 0xFF
		
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	#do we need to return the hasMask value to the main function?

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	return mask_on
