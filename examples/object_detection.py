#!/usr/bin/env python3

import jetson.inference
from jetson_tello import h264_frame_to_cuda, NoFrameData

from ast import literal_eval
with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

for frame in frames:
    try:
        decoded_frame, cuda = h264_frame_to_cuda(frame)

        detections = net.Detect(cuda)

        i = decoded_frame.number
        print(f'frame {i} detections:')
        for d in  detections:
            print(d)
    except NoFrameData:
        pass    
