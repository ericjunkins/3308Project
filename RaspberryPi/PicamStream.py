from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview(
raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264

for i in camera:
     
    v4l2-ctl --overlay=1 # enable viewfinder
    v4l2-ctl --overlay=0 # disable viewfinder
     # Record a video
    v4l2-ctl --set-fmt-video=width=1920,height=1088,pixelformat=4
    v4l2-ctl --stream-mmap=3 --stream-count=100 --stream-to=somefile.264

#camera.start_recording()
sleep(10)
#camera.stop_recording()
camera.stop_preview()


#**********************************************
#This needs to go to the command line
#raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 |cvlc -vvv stream:///dev/stdin --sout 
#**********************************************


'''
    # Load the sudo
    module modprobe bcm2835-v4l2

    # Control the viewfinder
    v4l2-ctl --overlay=1 # enable viewfinder
    v4l2-ctl --overlay=0 # disable viewfinder

    # Record a video
    v4l2-ctl --set-fmt-video=width=1920,height=1088,pixelformat=4
    v4l2-ctl --stream-mmap=3 --stream-count=100 --stream-to=somefile.264

    # Capture a JPEG image
    v4l2-ctl --set-fmt-video=width=2592,height=1944,pixelformat=3
    v4l2-ctl --stream-mmap=3 --stream-count=1 --stream-to=somefile.jpg

    # Set the video bitrate
    v4l2-ctl --set-ctrl video_bitrate=10000000

    # List the supported formats
    v4l2-ctl --list-formats
'''