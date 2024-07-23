import numpy as np
import cv2 as cv

class ImageProcessingAlgorithms:
    def ToCMYK(img):
        # Create float
        bgr = img.astype(float) / 255.

        # Extract channels
        with np.errstate(invalid='ignore', divide='ignore'):
            K = 1 - np.max(bgr, axis=2)
            C = (1 - bgr[..., 2] - K) / (1 - K)
            M = (1 - bgr[..., 1] - K) / (1 - K)
            Y = (1 - bgr[..., 0] - K) / (1 - K)

        # Convert the input BGR image to CMYK colorspace
        CMYK = (np.dstack((C, M, Y, K)) * 255).astype(np.uint8)

        # Split CMYK channels
        Y, M, C, K = cv.split(CMYK)

        np.isfinite(C).all()
        np.isfinite(M).all()
        np.isfinite(K).all()
        np.isfinite(Y).all()

        return C, M, Y, K

    def Get_ostou_threshold(image, is_normalized):
        # Set total number of bins in the histogram
        bins_num = 256

        # Get the image histogram
        hist, bin_edges = np.histogram(image, bins=bins_num)

        # Get normalized histogram if it is required
        if is_normalized:
            hist = np.divide(hist.ravel(), hist.max())

        # Calculate centers of bins
        bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.

        # Iterate over all thresholds (indices) and get the probabilities w1(t), w2(t)
        weight1 = np.cumsum(hist)
        weight2 = np.cumsum(hist[::-1])[::-1]

        # Get the class means mu0(t)
        mean1 = np.cumsum(hist * bin_mids) / weight1
        # Get the class means mu1(t)
        mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]

        inter_class_variance = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

        # Maximize the inter_class_variance function val
        index_of_max_val = np.argmax(inter_class_variance)

        threshold = bin_mids[:-1][index_of_max_val]
        return threshold


class ImageProcessingActions:
    def DrawBoundingBox(image, ctn, text):
        for c in ctn:
            rect = cv.boundingRect(c)
            if rect[2] < 100 or rect[3] < 100: continue
            x, y, w, h = rect
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(image, text, (x + w + 10, y + h), 0, 0.3, (0, 255, 0))

    def Show(image, blackBackground:bool):
        width, height, channels = image.shape
        if blackBackground:
            cv.imshow(np.zeros((width, height, channels), np.uint8))
        else: pass

class ContourCalculations:
    def Get_Area(ctn):
        return cv.contourArea(ctn)

    def Get_Diameter(ctn):
        return np.sqrt(4* cv.contourArea(ctn) /np.pi)

    def Get_Perimeter(ctn):
        return cv.arcLength(ctn, True)