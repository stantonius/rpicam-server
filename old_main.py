from vidgear.gears.asyncio import NetGear_Async
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import cv2, time, asyncio
import numpy as np
from settings import netgear_options, picam_config, text_config
from camera_modes.motion_diff import motion_diff

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

        # 0. Process the frame to greyscale
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_YUV420p2GRAY)  #greyscale 

        # 1. Gather pixel change
        if prev is not None:
            pixel_diffs = motion_diff(processed_frame=processed_frame, prev=prev)

            # 2. Calculate the pixel difference ratio vs the total number of pixels
            diff_ratio = round(np.sum(pixel_diffs) / np.product(pixel_diffs.shape), 2)


        # process frame to image and send
        timestamp = time.strftime("%Y-%m-%d %X")
        img = cv2.cvtColor(frame, cv2.COLOR_YUV420p2RGB)
        if prev is not None:
            img = cv2.putText(img, str(diff_ratio), **text_config)
        else:
            img = cv2.putText(img, timestamp, **text_config)
        

        # do some more stuff with the frame here

        # yield frame
        yield img
        
        # assign frame as prev
        prev = processed_frame

        # sleep for sometime
        await asyncio.sleep(0)



if __name__ == "__main__":
    # set event loop
    asyncio.set_event_loop(server.loop)
    # Add your custom source generator to Server configuration
    server.config["generator"] = main()

    # Launch the Server
    server.launch()

    # sleep time in seconds 
    sleep = 0

    # while pt < 86400:
    while True:
        if sleep <10:
            try:
                a = server.loop.run_until_complete(server.task)  # type: ignore

            except Exception as e:
                print(e.args)
                # wait for interrupts
                print("This gets triggered when there is no client")
                sleep+=2
        else:
            break


    # close stream
    picam2.stop()
    # finally close the server
    server.close(skip_loop=True)
