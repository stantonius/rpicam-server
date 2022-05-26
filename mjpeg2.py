from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import io
import logging
import socketserver
from threading import Condition, Thread


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class HandleStreamRequest(socketserver.StreamRequestHandler):
    def handle(self):
        srcaddr, srcport = self.request.getpeername()
        print("Connection from {}:{}".format(srcaddr, srcport))
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                self.wfile.write(frame)
        except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))


class StreamingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


picam2 = Picamera2()
picam2.configure(picam2.video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    server = StreamingServer(("0.0.0.0", 10001), HandleStreamRequest)
    server.serve_forever()
finally:
    picam2.stop_recording()
