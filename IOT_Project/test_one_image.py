import cv2
import numpy as np
import time

def load_pre_process():
	gray = cv2.imread("test_image1.jpg", 0)
	
	roi = gray[120:240, :]
	cv2.imshow('Image', roi)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	image_array = roi.reshape(1, 38400).astype(np.float32)
	
	

	return image_array

if __name__ == "__main__":
	image_array = load_pre_process()
	model = cv2.ml.ANN_MLP_load('mlp_xml/mlp_1521212184.xml')
	ret, resp = model.predict(image_array)
	prediction = resp.argmax(-1)
	print prediction


