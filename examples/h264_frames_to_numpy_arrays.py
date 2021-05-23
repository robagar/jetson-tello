#!/usr/bin/env python3

from ast import literal_eval
from jetson_tello import h264_frame_to_numpy_array, FrameDecodeError

with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

i = 1
for frame in frames:
    try:
        array, width, height = h264_frame_to_numpy_array(frame)

        print(f'frame {i} size: {width} x {height}')
        print(array)
    except FrameDecodeError:
        print(f'frame {i} - (decode error)')
    i += 1
      
