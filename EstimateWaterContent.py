import sys
DEBUG_SYS = True

try:
	import numpy as np
	import cv2
except:
	print "Please install following dependencies"
	print "1. numpy"
	print "2. cv2"
	sys.exit()
try:
	from matplotlib import pyplot as plt
except:
	print "Import Error: The program will run but you will not be able to see output images"
	DEBUG_SYS = False

def read_image(filename=None):
	if filename != None:
		try:
			img = cv2.imread(filename)
			return img
		except:
			print "Error reading input file [%s]"%filename

	else:
		print "Capturing from default camera"
		try:
			cap = cv2.VideoCapture(0)
			ret, frame = cap.read()
			cap.release()
			return frame
		except:
			print "Error reading image from default webcam"
	return None

def show_image(image):
	plt.imshow(image, interpolation='bicubic')
	plt.xticks([]), plt.yticks([])
	plt.show()

def get_grayscale_image(image_rgb):
	rows, cols, channels = image_rgb.shape
	gray_array = np.random.random((rows, cols))
	gray_image = np.array(gray_array, dtype=np.uint8)
	for i in range(rows):
		for j in range(cols):
			pixel_value = 0.2989*image_rgb[i, j , 2 ] + 0.5870*image_rgb[i, j, 1] + 0.1140*image_rgb[i, j , 0]
			gray_image[i,j] = pixel_value
	return gray_image

def count_dark_pixels(image_mat, threshold):
	rows, cols = image_mat.shape
	count = 0
	for i in range(rows):
		for j in range(cols):
			if image_mat[i][j] > threshold:
				count += 1
	return count

def get_total_pixels(image_mat):
	rows, cols = image_mat.shape
	return rows*cols

def calculate_rws(image, threshold):
	dark = count_dark_pixels(image, threshold)
	total = get_total_pixels(image)
	percent = int((dark*100)/total)
	if percent == 0 or percent == 100:
		print "Image in not clear. Try with some better images"
	return percent

def generate_histograms(gray_image):
	global DEBUG, DEBUG_SYS
	if DEBUG_SYS == True and DEBUG == True:
		try:
			plt.hist(gray_image.ravel(), 256, [0,256])
			plt.show()
		except:
			print "No display found"
	else:
		print """Please make sure that matplotlib is installed
				and DEBUG flag is set to true"""

def main(threshold=200):
	bgr_image = read_image()
	gray_image = get_grayscale_image(bgr_image)
	generate_histograms(gray_image)
	rws = calculate_rws(gray_image, threshold)
	print "RWS is %d%%"%rws

if __name__ == "__main__":
	DEBUG = True 		# Set this flag to True to see histograms(This will not work if beaglenone is not connected to any display)
	threshold = 200		# Vary the limit of threshold between 0 and 255 to get accurate results
	main(threshold)	