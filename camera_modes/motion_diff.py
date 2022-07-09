import cv2
import numpy as np
from vidgear.gears import NetGear

def motion_diff(processed_frame: np.ndarray, prev: np.ndarray, threshold: int = 20):
    """
    Takes the previous and current frames as numpy arrays,
    converts them to greyscale, and takes the difference.
    For each pixel, if the difference is greater than the threshold,
    the pixel returns 1

    Returns an array of binaries
    """
    # see https://towardsdatascience.com/image-analysis-for-beginners-creating-a-motion-detector-with-opencv-4ca6faba4b42

    if prev is not None:
        diff_frame = cv2.absdiff(src1=processed_frame, src2=prev)
        
        # dilute the image to exagerate the differences
        kernel = np.ones((5, 5))
        diff_frame = cv2.dilate(diff_frame, kernel, 1)

        # Only take different areas that are different enough (>20 / 255)
        thresh_frame = cv2.threshold(src=diff_frame, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)[1]

        # Can take the contours instead of individual pixel values
        # contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(image=img_rgb, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)


        # return cv2.cvtColor(thresh_frame, cv2.COLOR_GRAY2RGB)
        return thresh_frame