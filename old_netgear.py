from vidgear.gears import NetGear
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2.request import CompletedRequest
import libcamera
import pickle, cv2, time, os
from dotenv import load_dotenv
from datetime import datetime
import numpy as np

load_dotenv()

picam2 = Picamera2()

# netgear server setup

options = {
    "address": os.environ["CLIENT_IP"],
    "port": os.environ["CLIENT_PORT"],
    "protocol": "tcp",
    "logging": True,
    "pattern": 1
}
server = NetGear(**options)

# Define received data dictionary
data_dict = {}

# set and apply config

lsize = (320, 240)
half_resolution = [dim // 2 for dim in picam2.sensor_resolution]

config = {
    "main": {"size": half_resolution, "format": "RGB888"},
    "lores": {"size": lsize, "format": "YUV420"},
    "transform": libcamera.Transform(hflip=1, vflip=1),
    "encode": "lores",
    "controls": {
        # "FrameDurationLimits": (66666, 99999),
        "AwbEnable": 0
    }
}

video_config = picam2.video_configuration(**config)
picam2.configure(video_config)

# print on image via callback

colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

def apply_timestamp(request):
    # timestamp = time.strftime("%Y-%m-%d %X")
    timestamp="Hiiiiiiiiiiiiiiii"
    with MappedArray(request, "lores") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

# picam2.request_callback = apply_timestamp

# setup for image stills
w, h = lsize
prev = None 

# final setup - encodings, output, and start

encoder = H264Encoder(10000000)
output = FfmpegOutput('test.mp4')
picam2.start_recording(encoder, output)

while True:
    try:
        frame = picam2.capture_array("lores")

        if frame is None:
            break

        # 1. process frame to image and send
        timestamp = time.strftime("%Y-%m-%d %X")
        img = cv2.cvtColor(frame, cv2.COLOR_YUV420p2RGB)
        img = cv2.putText(img, timestamp, origin, font, scale, colour, thickness)
        # recv_data = server.send(frame)

        # 2. use frame to look for motion
        # see https://towardsdatascience.com/image-analysis-for-beginners-creating-a-motion-detector-with-opencv-4ca6faba4b42
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_YUV420p2GRAY)  #greyscale
        if prev is not None:
            diff_frame = cv2.absdiff(src1=processed_frame, src2=prev)
            
            # dilute the image to exagerate the differences
            kernel = np.ones((5, 5))
            diff_frame = cv2.dilate(diff_frame, kernel, 1)

            # Only take different areas that are different enough (>20 / 255)
            thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

            #TODO: replace below with conditional image write if number of pixels > certain threshold
            recv_data = server.send(cv2.cvtColor(thresh_frame, cv2.COLOR_GRAY2RGB))
        prev = processed_frame


        # cur = cur[:w*h].reshape(h, w)
        # if prev is not None:
        #     # Measure pixels differences between current and
        #     # previous frame
            
        #     prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        #     mse = np.square(np.subtract(frame, prev)).mean()
        #     if mse > 7:
        #         request = picam2.capture_request()
        #         request.save("main", f"snaps/{str(datetime.now())}.jpg")
        #         request.release()
        #         print("Still image captured!")

        # prev = frame

    except KeyboardInterrupt:
        break

# safely close video stream
picam2.stop()
# picam2.stop_recording()
# safely close server
server.close()