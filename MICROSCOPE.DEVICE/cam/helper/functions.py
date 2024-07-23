import numpy as np
import cv2 as cv
from cam.helper.draw import Draw

class Functions:
    def Crop(img, rect):
        x, y, w, h = rect
        return img[y:y + h, x:x + w]

    def Get_BoundingRect(img, contour, space_coef):
        x, y, w, h = cv.boundingRect(contour)
        x -= space_coef
        y -= space_coef
        w += space_coef
        h += space_coef
        return (x,y,w,h)

    def Draw_BoundingRectangles(img, ctn, space_coef, color, thickness):
        for contour in ctn:
            Functions.Draw_Rectangle(img, cv.boundingRect(contour), space_coef, color, thickness)

    def Draw_SeparateContours(img, ctn):
        contour_images = []
        for i, contour in enumerate(ctn):
            contour_image = np.zeros_like(img)
            cv.drawContours(contour_image, [contour], -1, (255, 255, 255), thickness=cv.FILLED)
            masked_image = cv.bitwise_and(img, contour_image)
            contour_images.append(masked_image)
        return contour_images
    
    def Draw_SeparateContours_AsRectangle(img,ctn,space_coef):
        result=[]
        for contour in ctn:
            x, y, w, h = cv.boundingRect(contour)
            margin = space_coef
            x -= margin
            y -= margin
            w += margin
            h += margin
            cropped_rectangle = img[y:y+h, x:x+w]
            result.append(cropped_rectangle)
        return result




    def Put_Text(image, text, ctn, color, thickness):
        for contour in ctn:
            x, y, w, h = cv.boundingRect(contour)
            cv.putText(image, text, (x, y), fontFace= 1, fontScale= 3, color= color, thickness= thickness)


    def Draw_Rectangle(img, rect, space_coef, color, thickness):
        x, y, w, h = rect
        cv.rectangle(img, (x - space_coef, y - space_coef), (x + w + space_coef, y + h + space_coef),
                            color, thickness)

    def Draw_Mask(img, mask, alpha):
        return cv.addWeighted(img, 1, mask, alpha, 0)

    def Draw_Text(image, text, ctn, color, thickness):
        x, y, w, h = cv.boundingRect(ctn)
        cv.putText(image, (x, y), "Arial", 23, color, thickness)

    def encodeBytesAsJPG(buf, width, height, quality):
        img_np = np.frombuffer(buf, dtype=np.uint8)
        img_np = img_np.reshape((height, width, 3))

        encode_params = [int(cv.IMWRITE_JPEG_QUALITY), quality]
        _, img_encoded = cv.imencode(".jpg", img_np, encode_params)
        return img_encoded

    def encodeBytes(buf, width, height, extension = '.png'):
        img_np = np.frombuffer(buf, dtype=np.uint8)
        img_np = img_np.reshape((height, width, 3))

        success, img_encoded = cv.imencode(extension, img_np)
        if success:
            return img_encoded
        else:
            return None