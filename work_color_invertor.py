import cv2

from unet.network import network
from colors import COLORS
from change_color import ColorChanger

class ColorInvertor():

    def __init__(self):
        self.net = network()
        self.centroid = None
        self.changer = ColorChanger()

        self.__load_unet()

    def __load_unet(self):
        self.net.load_network()
    
    def __recalculate_color(self):
        self.changer.init_img = self.init_img
        self.changer.mask_img = self.mask_img
        self.changer.pref_color = COLORS[self.recolor]

        self.final_img = self.changer.BalancedAlgorithm()

        self.final_img = cv2.cvtColor(self.final_img, cv2.COLOR_HSV2BGR)


    def recolor_hair_image(self, img_name, color):
        self.init_img = cv2.imread(img_name)
        self.recolor = color

        # start network
        self.mask_img = self.net.proceed_image(self.init_img)

        self.__recalculate_color()

        cv2.imshow('Result', self.final_img)
        cv2.waitKey(0)

    def recolor_hair_video(self, color):
        self.recolor = color
        cap = cv2.VideoCapture(0)

        while True:
            _, frame = cap.read()
            self.init_img = cv2.resize(frame, (600,400))

            # start network
            self.mask_img = self.net.proceed_image(self.init_img)

            self.__recalculate_color()
            cv2.imshow('a', self.final_img)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
