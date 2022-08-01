# from https://github.com/raspberrypi/picamera2

sudo apt update
sudo apt upgrade -y

# headless install (no GUI needed)
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-prctl libatlas-base-dev ffmpeg libopenjp2-7 python3-pip
pip3 install numpy --upgrade
NOGUI=1 pip3 install picamera2

# require opencv
sudo apt install -y python3-opencv
sudo apt install -y opencv-data


# dependencies for the camera setup
pip install flask, RPi.GPIO