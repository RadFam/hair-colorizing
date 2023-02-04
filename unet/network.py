import cv2
import numpy as np
from keras.models import load_model
from keras.utils import CustomObjectScope

from unet.utils.custom_objects import custom_objects

class network():
    
    def __init__(self) -> None:
        pass

    def load_network(self):
        with CustomObjectScope(custom_objects()):
            self.model = load_model('./unet/models/CelebA_DeeplabV3plus_256_hair_seg_model.h5')

    def proceed_image(self, image_in):
        image = image_in.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype('float32')
        img_shape = image.shape
        image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_NEAREST)
        image = image / 255.0
        image = (image - np.mean(image)) / np.std(image)
        image = np.expand_dims(image, axis=0)
        output = self.model.predict(image)

        mask = cv2.resize(output[0,:,:,0], (img_shape[1], img_shape[0]), interpolation=cv2.INTER_NEAREST)
        mask[mask >= 0.99] = 255
        mask[mask < 0.99] = 0
        mask = mask.astype('uint8')
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.erode(mask, kernel, iterations=1)
        return mask