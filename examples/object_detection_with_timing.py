#!/usr/bin/env python3

from time import time
import jetson.inference
from jetson_tello import h264_frame_to_cuda, FrameDecodeError

from ast import literal_eval
with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

i = 1
times = []
for frame in frames:
    try:
        cuda, width, height = h264_frame_to_cuda(frame)

        t0 = time()
        detections = net.Detect(cuda)
        times.append([i, time() - t0])

        print(f'frame {i} detections:')
        for d in  detections:
            print(d)

        i += 1
    except FrameDecodeError:
        pass

print('detection times (seconds):')
for i,t in times:
    print(f'  {i}: {t:0.4}')  
