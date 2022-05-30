from picamera2 import Picamera2, Preview
from picamera2.encoders import Encoder, H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
import socket, time, pickle, struct
import cv2

try:
    picam2 = Picamera2()
    video_config = picam2.video_configuration({"size": (1280, 720)})
    picam2.configure(video_config)
    picam2.encoder = H264Encoder(1000000, False)
    picam2.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # localhost of the raspberry
        # sock.bind(("0.0.0.0", 10001))
        # address accessible to workstation
        sock.bind(("0.0.0.0", 10001))
        sock.listen(5)

        conn, addr = sock.accept()
        print(f"connection accepted, addr: {addr}, conn: {conn}")

        stream = conn.makefile("wb")
        # picam2.encoder.output = FfmpegOutput(stream)
        picam2.encoder.output = FfmpegOutput("test.mp4")
        picam2.start_encoder()
        picam2.start()

        print(sock.getsockname())
        time.sleep(60)
        # while True:
        #     time.sleep(1)

        picam2.stop()
        picam2.stop_encoder()
        conn.close()
        exit(0)

except Exception as e:
    print(f"\nError occured: {e}\n")