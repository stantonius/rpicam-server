# RPi Camera Server

Sends Raspberry Pi image data to home lab server.

Currently is configured to do some processing locally before sending image data to the server, but this can change in the future.

The main loop is in `camserver.py`.

I have been using watchmedo using the following command: `watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM python camserver.py`
