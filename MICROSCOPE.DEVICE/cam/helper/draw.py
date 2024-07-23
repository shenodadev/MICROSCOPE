import cv2 as cv
import numpy as np

class Draw:
    def DrawRBCContour(image, ctn):
        cv.drawContours(image, ctn, -1, (240, 0, 0), 2)
        return  image

    def DrawPlateletContour(image, ctn):
        cv.drawContours(image, ctn, -1, (0, 0, 240), 2)
        return  image

    def Draw_Text(image, text, ctn, color, thickness):
        x, y, w, h = cv.boundingRect(ctn)
        cv.putText(image, (x, y), "Arial", 23, color, thickness)




