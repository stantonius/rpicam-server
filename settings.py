import os
from dotenv import load_dotenv
from picamera2 import Picamera2
import libcamera
import cv2

load_dotenv()

# NETGEAR CONFIG

netgear_options = {
    "address": os.environ["CLIENT_IP"],
    "port": os.environ["CLIENT_PORT"],
    "protocol": "tcp",
    "logging": True,
    "pattern": 1,
    "source": None,
    "timeout": 10
}

# PICAM CONFIG

def picam_config(picam: Picamera2) -> dict:
    lsize = (320, 240)
    half_resolution = [dim // 2 for dim in picam.sensor_resolution]

    return {
        "main": {"size": half_resolution, "format": "RGB888"},
        "lores": {"size": lsize, "format": "YUV420"},
        "transform": libcamera.Transform(hflip=1, vflip=1),
        "encode": "lores",
        "controls": {
            # "FrameDurationLimits": (66666, 99999),
            "AwbEnable": 0
        }
    }

# Image text settings

text_config = {
    "color": (0, 255, 0),
    "org": (0, 30),  # origin
    "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
    "fontScale": 1,
    "thickness": 2
}


# def apply_timestamp(request):
#     # timestamp = time.strftime("%Y-%m-%d %X")
#     timestamp="Hiiiiiiiiiiiiiiii"
#     with MappedArray(request, "lores") as m:
#         cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

# picam2.request_callback = apply_timestamp

# setup for image stills
# w, h = lsize