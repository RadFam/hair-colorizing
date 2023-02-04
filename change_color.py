import numpy as np
import cv2
from sklearn.cluster import KMeans

class ColorChanger():

    def __init__(self, image=None, mask=None, pref_color=None, old_color=None):
        self._init_img = image
        self._mask_img = mask
        self._color = pref_color
        self._clr = old_color

    @property
    def init_img(self):
        return self._init_img

    @init_img.setter
    def init_img(self, img):
        self._init_img = img

    @property
    def mask_img(self):
        return self._mask_img
    
    @mask_img.setter
    def mask_img(self, img):
        self._mask_img = img

    @property
    def pref_color(self):
        return self._color

    @pref_color.setter
    def pref_color(self, color):
        self._color = color

    @property
    def old_color(self):
        return self._clr

    @old_color.setter
    def old_color(self, color):
        self._clr = color

    def __blur_mask(self, img_bkgrd, mask_zero, mask_color):
        mask = cv2.GaussianBlur(mask_zero, (9,9), 0)
        mask = mask / 255.0
        mask = np.clip(mask, 0.0, 255.0)

        val_1 = np.where(mask > 0.99)
        val_2 = np.where((mask <= 0.99) & (mask > 0.7))
        val_3 = np.where(mask <= 0.7)

        result = np.zeros_like(img_bkgrd)
        result[val_1[0], val_1[1], :] = mask_color[val_1[0], val_1[1], :]
        result[val_3[0], val_3[1], :] = img_bkgrd[val_3[0], val_3[1], :]
        result[val_2[0], val_2[1], :] = (1-mask[val_2[0], val_2[1], :])*img_bkgrd[val_2[0], val_2[1], :] + mask[val_2[0], val_2[1], :]*mask_color[val_2[0], val_2[1], :]

        return result
        

    def __seed_union(self, img_1, img_2):
        var = np.where(img_2 > 0)
        
        sub_mask = np.zeros_like(img_1)
        sub_mask[var[0], var[1], :] = 255

        result = np.zeros_like(img_1)

        result[var[0], var[1], :] = img_1[var[0], var[1], :] + img_2[var[0], var[1], :] - 128
        result = np.clip(result, 0, 255)

        img_1 = self.__blur_mask(img_1, sub_mask, result)
        return img_1

    def __change_tone(self, img_1, img_2):
        var = np.where(img_2 > 0)

        sub_mask = np.zeros_like(img_1)
        sub_mask[var[0], var[1], :] = 255

        result = np.zeros_like(img_1)

        result[var[0], var[1], 0] = img_2[var[0], var[1], 0]
        result[var[0], var[1], 1] = img_1[var[0], var[1], 1]
        result[var[0], var[1], 2] = img_1[var[0], var[1], 2]

        img_1 = self.__blur_mask(img_1, sub_mask, result)

        return img_1

    def __diffuse_light(self, img_1, img_2):
        val = np.where(img_2 > 0)
        
        sub_img = np.zeros_like(img_1)
        sub_mask = np.zeros_like(img_1)
        sub_img[val[0], val[1], :] = img_1[val[0], val[1], :]
        sub_mask[val[0], val[1], :] = 255

        rs = 255 - (255 - sub_img) * (255 - img_2) / 255
        result = sub_img * (rs + img_2 * (255 - sub_img) / 255)
        result = (result - np.min(result)) / (np.max(result) - np.min(result)) * 255

        img_1 = self.__blur_mask(img_1, sub_mask, result)
        return img_1

    def __twice_diffuse_light(self, img_1, img_2):
        val = np.where(img_2 > 0)
        
        sub_img = np.zeros_like(img_1)
        sub_mask = np.zeros_like(img_1)
        sub_img[val[0], val[1], :] = img_1[val[0], val[1], :]
        sub_mask[val[0], val[1], :] = 255

        rs = 255 - (255 - sub_img) * (255 - img_2) / 255
        result = sub_img * (rs + img_2 * (255 - sub_img) / 255)
        result = (result - np.min(result)) / (np.max(result) - np.min(result)) * 255

        rs = 255 - (255 - result) * (255 - img_2) / 255
        result = result * (rs + img_2 * (255 - result) / 255)
        result = (result - np.min(result)) / (np.max(result) - np.min(result)) * 255

        img_1 = self.__blur_mask(img_1, sub_mask, result)
        return img_1

    
    def __light_light_algo(self, final_image):
        final_image = cv2.cvtColor(final_image, cv2.COLOR_HSV2RGB)
        self._mask_img_color = cv2.cvtColor(self._mask_img_color, cv2.COLOR_HSV2RGB)

        final_image = final_image.astype('float32')
        self._mask_img_color = self._mask_img_color.astype('float32')

        final_image = self.__diffuse_light(final_image, self._mask_img_color)

        final_image = final_image.astype('uint8')
        self._mask_img_color = self._mask_img_color.astype('uint8')

        final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)

        return final_image

    def __dark_light_algo(self, final_image):
        # seed union
        final_image = cv2.cvtColor(final_image, cv2.COLOR_HSV2RGB)
        self._mask_img_color = cv2.cvtColor(self._mask_img_color, cv2.COLOR_HSV2RGB)

        final_image = final_image.astype('float32')
        self._mask_img_color = self._mask_img_color.astype('float32')

        final_image = self.__seed_union(final_image, self._mask_img_color)

        final_image = final_image.astype('uint8')
        self._mask_img_color = self._mask_img_color.astype('uint8')

        # change tone
        final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)
        self._mask_img_color = cv2.cvtColor(self._mask_img_color, cv2.COLOR_RGB2HSV)

        final_image = self.__change_tone(final_image, self._mask_img_color)

        return final_image

    def __light_dark_algo(self, final_image):
        final_image = cv2.cvtColor(final_image, cv2.COLOR_HSV2RGB)
        self._mask_img_color = cv2.cvtColor(self._mask_img_color, cv2.COLOR_HSV2RGB)
        final_image = final_image.astype('float32')
        self._mask_img_color = self._mask_img_color.astype('float32')

        final_image = self.__twice_diffuse_light(final_image, self._mask_img_color)
        
        final_image = final_image.astype('uint8')
        self._mask_img_color = self._mask_img_color.astype('uint8')

        final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)

        return final_image

    def __dark_dark_algo(self, final_image):
        final_image = cv2.cvtColor(final_image, cv2.COLOR_HSV2RGB)
        self._mask_img_color = cv2.cvtColor(self._mask_img_color, cv2.COLOR_HSV2RGB)
        final_image = final_image.astype('float32')
        self._mask_img_color = self._mask_img_color.astype('float32')

        final_image = self.__diffuse_light(final_image, self._mask_img_color)
        
        final_image = final_image.astype('uint8')
        self._mask_img_color = self._mask_img_color.astype('uint8')

        final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)

        return final_image

    def BalancedAlgorithm(self):
        self._init_img = cv2.cvtColor(self._init_img, cv2.COLOR_BGR2HSV)

        final_img = self._init_img.copy()
        val = np.where(self._mask_img > 0)

        if self._clr is None:
            pix = self._init_img[val[0], val[1], :]
            clustering = KMeans(n_clusters=3, max_iter=50, tol=0.1, init='k-means++')
            clustering.fit(pix)

            labels = clustering.labels_
            labs = list(set(labels))

            # check, how mush pixels in each cluster
            vols = []
            for k in labs:
                vols.append(len([x for x in labels if x == k]))

            srt_labs = [l for _,l in sorted(zip(vols, labs))]

            # get_centroid
            pix_main = pix[labels == srt_labs[-1], :]
            self._clr = np.mean(pix_main, axis=0)
            self._clr = self._clr.astype('uint8')

        self._mask_img_color = np.zeros_like(self._init_img)
        self._mask_img_color[val[0], val[1], :] = self._color

        # check if the old_color is light/dark and new_color is light_dark
        if self._color[2] >= 130 and self._clr[2] >= 130: # light on light
            return self.__light_light_algo(final_img)

        if self._color[2] >= 130 and self._clr[2] < 130: # light on dark
            return self.__light_dark_algo(final_img)

        if self._color[2] < 130 and self._clr[2] >= 130: # dark on light
            return self.__dark_light_algo(final_img)

        if self._color[2] < 130 and self._clr[2] < 130: # dark on dark
            return self.__dark_dark_algo(final_img)