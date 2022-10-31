import numpy as np
import cv2 as cv
from PIL import Image
class img_carct(object):

    def __init__(self, boss, set_img):
        self.boss = boss
        self.set_img = set_img
    # reglage de la luminosité
    def update_eclair(self, value):
        value = (float(value) / 5) * 255
        self.boss.eclair = value
        self.regl_caract(value, self.boss.contrast, self.boss.gamma)


    # reglage du contrast
    def update_contrast(self, value):
        value = (float(value) / 5) * 127
        self.boss.contrast = value
        self.regl_caract(self.boss.eclair, value, self.boss.gamma)

    # reglage du gamma
    def update_gamma(self, value):
        value = (float(value) / 5) * 255
        self.boss.gamma = value
        self.regl_caract(self.boss.eclair, self.boss.contrast, value)

    # reglage des propriétés de l'image
    def regl_caract(self, brigth, contraste, gamma_):
        image_matrix = np.array(self.boss.img_bef)
        image_matrix = cv.cvtColor(image_matrix, cv.COLOR_RGB2BGR)

        if brigth > 0:
            shadow = brigth
            highlight = 255
        else:
            shadow = 0
            highlight = brigth + 255

        alpha = (highlight - shadow) / 255
        gamma = shadow
        image_matrix = cv.addWeighted(image_matrix, alpha, image_matrix, 0, gamma)

        f = 131 * (contraste + 127) / (127 * (131 - contraste))
        alpha = f
        gamma = 127 * (1 - f)

        image_matrix = cv.addWeighted(image_matrix, alpha, image_matrix, 0, gamma)

        image_matrix = cv.addWeighted(image_matrix, 1, image_matrix, 0, gamma_)

        image_matrix = cv.cvtColor(image_matrix, cv.COLOR_BGR2RGB)
        self.boss.img_f = Image.fromarray(image_matrix)
        self.set_img.update_img()
