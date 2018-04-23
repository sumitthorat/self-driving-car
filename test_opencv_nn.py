import cv2
import numpy as np
#from matplotlib import pyplot as plt

class NeuralNetwork():
    def __init__(self):
        self.model = cv2.ml.ANN_MLP_load('IOT_Project/mlp_xml/mlp_1522002066.xml')

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)

def test_image():
    model = NeuralNetwork()
    img = cv2.imread('IOT_Project/training_images_raw/fwd/frame00082.jpg', 0)
    cv2.imshow('image', img)
    k = cv2.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'):  # wait for 's' key to save and exit
        cv2.imwrite('messigray.png', img)
        cv2.destroyAllWindows()
    roi = img[120:240, :]
    image_array = roi.reshape(1, 38400).astype(np.float32)
    prediction = model.predict(image_array)
    print(prediction)

if __name__ == "__main__":
    test_image()
