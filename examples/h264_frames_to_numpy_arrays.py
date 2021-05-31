#!/usr/bin/env python3

from ast import literal_eval
from jetson_tello import h264_frame_to_numpy_array, NoFrameData

with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

for frame in frames:
    try:
        decoded_frame, numpy_array = h264_frame_to_numpy_array(frame)
        print(f'frame {decoded_frame.number} size: {decoded_frame.width} x {decoded_frame.height}')
        print(numpy_array)
    except NoFrameData:
        print(f'(no frame data - skipped)')
      
