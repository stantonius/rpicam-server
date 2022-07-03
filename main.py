from vidgear.gears.asyncio import NetGear_Async
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import cv2, time, asyncio
from datetime import datetime
from settings import netgear_options, picam_config, text_config

server = NetGear_Async(**netgear_options)

picam2 = Picamera2()
cam_config = picam_config(picam=picam2)
video_config = picam2.video_configuration(**cam_config)
picam2.configure(video_config)

encoder = H264Encoder(10000000)
output = FfmpegOutput('test.mp4')
picam2.start_recording(encoder, output)

async def main():
    # always start with prev = None, so the first frame is never sent
    prev = None
    while True:
        frame = picam2.capture_array("lores")

        if frame is None:
            break

        # 1. process frame to image and send
        timestamp = time.strftime("%Y-%m-%d %X")
        img = cv2.cvtColor(frame, cv2.COLOR_YUV420p2RGB)
        img = cv2.putText(img, timestamp, **text_config)

        # do some more stuff with the frame here

        yield frame
        # yield img
        # sleep for sometime
        await asyncio.sleep(0)


if __name__ == "__main__":
    # set event loop
    asyncio.set_event_loop(server.loop)
    # Add your custom source generator to Server configuration
    server.config["generator"] = main()
    # Launch the Server
    server.launch()
    try:
        # run your main function task until it is complete
        server.loop.run_until_complete(server.task)
    except (KeyboardInterrupt, SystemExit):
        # wait for interrupts
        pass
    finally:
        # close stream
        picam2.stop()
        # finally close the server
        server.close()


# def main():
#     # always start with prev = None, so the first frame is never sent
#     prev = None
#     while True:
#         try:
#             frame = picam2.capture_array("lores")

#             if frame is None:
#                 break

#             # 1. process frame to image and send
#             timestamp = time.strftime("%Y-%m-%d %X")
#             img = cv2.cvtColor(frame, cv2.COLOR_YUV420p2RGB)
#             img = cv2.putText(img, timestamp, **text_config)
#             server.send(img)

#             # prev = processed_frame

#             # server.send


#             # cur = cur[:w*h].reshape(h, w)
#             # if prev is not None:
#             #     # Measure pixels differences between current and
#             #     # previous frame
                
#             #     prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

#             #     mse = np.square(np.subtract(frame, prev)).mean()
#             #     if mse > 7:
#             #         request = picam2.capture_request()
#             #         request.save("main", f"snaps/{str(datetime.now())}.jpg")
#             #         request.release()
#             #         print("Still image captured!")

#             # prev = frame

#         except KeyboardInterrupt:
#             break

#     # safely close video stream
#     picam2.stop()
#     # picam2.stop_recording()
#     # safely close server
#     server.close()


# if __name__ == "__main__":
#     main()