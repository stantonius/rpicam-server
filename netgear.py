from vidgear.gears import NetGear
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import libcamera
import pickle, cv2, time

picam2 = Picamera2()

# netgear server setup

options = {
    "address": "10.0.0.226",
    "port": "5454",
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
    timestamp = time.strftime("%Y-%m-%d %X")
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

picam2.request_callback = apply_timestamp



# final setup - encodings, output, and start

encoder = H264Encoder(10000000)
output = FfmpegOutput('test.mp4')
picam2.start_recording(encoder, output)

while True:
    try:
        frame = picam2.capture_array()[:,:,:3]
        


        if frame is None:
            break

        recv_data = server.send(frame)

        # cur = picam2.capture_buffer("lores")
        # cur = cur[:w*h].reshape(h, w)
        # if prev is not None:
        #     # Measure pixels differences between current and
        #     # previous frame
        #     mse = np.square(np.subtract(cur, prev)).mean()
        #     if mse > 7:
        #         if not encoding:
        #             encoder.output = FileOutput("{}.h264".format(int(time.time())))
        #             picam2.start_encoder()
        #             encoding = True
        #             print("New Motion", mse)
        #         ltime = time.time()
        #     else:
        #         if encoding and time.time() - ltime > 2.0:
        #             picam2.stop_encoder()
        #             encoding = False
        # prev = cur

        # check if valid data recieved
        if not (recv_data is None):
            # extract unique port address and its respective data
            unique_address, data = recv_data
            # update the extracted data in the data dictionary
            data_dict[unique_address] = data

        if data_dict:
            # print data just received from Client(s)
            for key, value in data_dict.items():
                print("Client at port {} said: {}".format(key, value))

    except KeyboardInterrupt:
        break

# safely close video stream
picam2.stop()
# picam2.stop_recording()
# safely close server
server.close()