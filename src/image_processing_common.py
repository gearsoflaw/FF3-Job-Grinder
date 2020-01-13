# This mess has been created by GearsOfLaw https://github.com/gearsoflaw
# Adapted from the works of Sentdex https://github.com/Sentdex/pygta5
""" This module contains common image processing functions """
import numpy as np
import cv2

class ImageProcessing:
    """ This class contains common image processing functions """
    @staticmethod
    def region_of_interest(image, vertices):
        """ Using the vertices only the Region of Interest will be returned from the given image
        i.e. A mask"""
        #blank mask:
        mask = np.zeros_like(image)

        #filling pixels inside the polygon defined by "vertices" with the fill colour
        cv2.fillPoly(mask, vertices, 255)

        #returning the image only where mask pixels are nonzero
        masked = cv2.bitwise_and(image, mask)
        return masked
