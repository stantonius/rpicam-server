from vidgear.gears import NetGear
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2.request import CompletedRequest
import libcamera
import pickle, cv2, time, os, dotenv
from datetime import datetime
import numpy as np
from settings import netgear_options


server = NetGear(**netgear_options)
picam2 = Picamera2()


def main():
    pass
