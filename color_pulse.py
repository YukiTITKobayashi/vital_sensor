import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import os
from pprint import pprint
import json
import ffmpeg
import csv

cap_path = os.path.join('.', 'data', 'IMG_7177.MOV')
cap_file = cv.VideoCapture(cap_path)


video_info = ffmpeg.probe(cap_path)

with open("output.txt",'w') as f:

    for stream in video_info['streams']:
        f.write('stream {0}: {1}'.format(stream['index'],stream['codec_type']))
        f.write("\n")
        #pprint(stream)     #Stream dictionary
        f.write(json.dumps(stream))
        f.write("\n")

    f.write("Video captured time (GMT):")
    f.write(video_info['streams'][0]['tags']['creation_time'])    #Read datetime when the video captured by FFmpeg
    f.write("\n")

    if cap_file.isOpened():
        f.write("Frame counts:"+str(cap_file.get(cv.CAP_PROP_FRAME_COUNT))+"\n")
        f.write("FPS:"+str(cap_file.get(cv.CAP_PROP_FPS))+"\n")
        f.write("Seconds:"+str(cap_file.get(cv.CAP_PROP_FRAME_COUNT)/cap_file.get(cv.CAP_PROP_FPS))+"\n")
        f.write("\n")

    else:
        
        print("File is not opened.\n")


    i = 0
    
    while (cap_file.isOpened()):

        ret, frame = cap_file.read()
        if not ret: #If the frame is not read anymore,
            break

        f_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        f_gray1d = np.array(f_gray).flatten()
        color_mean = f_gray1d.mean()

        #if i>3000:
        #    print(i)

        #if np.mod(i,100)==0 :
        f.write(str(color_mean)+"\n")

        i = i + 1


cap_file.release()
cv.destroyAllWindows()