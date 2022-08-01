import os
from dotenv import load_dotenv
from picamera2 import Picamera2
from picamera2.controls import Controls
import libcamera
import cv2

load_dotenv()


def picam_config(picam: Picamera2) -> dict:
    # lsize = (320, 240)
    lsize = (720,480)
    half_resolution = [dim // 2 for dim in picam.sensor_resolution]

    return {
        "main": {"size": half_resolution, "format": "RGB888"},
        "lores": {"size": lsize, "format": "YUV420"},
        "transform": libcamera.Transform(hflip=0, vflip=0),
        "encode": "lores",
    }

def picam_controls(picam: Picamera2) -> None:
    with picam.controls as ctrls:
        # ctrls.Brightness = 0.5
        # ctrls.Contrast = 1.5
        # ctrls.AeConstraintMode = 2
        # ctrls.FrameDurationLimits = (125000, 150000)
        ctrls.AwbEnable = 1
        # ctrls.AwbMode = 0
        # ctrls.ExposureTime = 100000

# Image text settings

text_config = {
    "color": (0, 255, 0),
    "org": (0, 30),  # origin
    "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
    "fontScale": 1,
    "thickness": 2
}