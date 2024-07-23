import cv2 as cv
import numpy as np
from cam.helper.algorithms import ImageProcessingAlgorithms
from cam.helper.functions import Functions
from cam.helper.draw import Draw
from PIL import Image
#import config
#from lobe import ImageModel


class WBCs:
    def GetWBCExternalContours(image, minContourArea:int):
        #image = cv.watershed(image, markers=np.zeros(image.shape, dtype=np.int32))
        cmyk = ImageProcessingAlgorithms.ToCMYK(image)
        # cv2.imshow("c", cmyk[0])
        # cv2.imshow("m", cmyk[1])
        # cv2.imshow("y", cmyk[2])
        # cv2.imshow("k", cmyk[3])
        ei = cv.equalizeHist(cmyk[2])
        ei = cmyk[2]
        ei = cv.erode(ei, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)))
        ei = cv.medianBlur(ei, 3)
        #ei = cv.GaussianBlur(ei, (3, 3), 20)
        #cv.imshow("ei", ei)
        ei = cv.threshold(ei, ImageProcessingAlgorithms.Get_ostou_threshold(ei, True), 200, cv.THRESH_OTSU)[1]

        #cv.imshow("ei_thread", ei)

        # morphological operations
        # morph = cv2.morphologyEx(ei, cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))
        # morph = cv2.

        # get border
        ctn, heirarchy = cv.findContours(ei, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        ctn_selected = []
        for contour in ctn:
            if cv.contourArea(contour) >= minContourArea:
                ctn_selected.append(contour)

        return ctn_selected

    def DrawWBCContour(image, ctn):
        mask = np.zeros(image.shape, np.uint8)
        cv.drawContours(mask, ctn, -1, (255, 255, 255), 1)
        image = Functions.Draw_Mask(image, mask, 0.4)
        return image

    
    def Predict_xception(cellimage):
        pass

    def predict_resnet50(cellimage):
        pass

    def predict_yoloc5(cellimage):
        pass






