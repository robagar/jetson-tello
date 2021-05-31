#!/usr/bin/env python3

from pathlib import Path
import jetson.utils
from jetson_tello import h264_frame_to_cuda, NoFrame

from ast import literal_eval
with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

Path("h264_frames_to_cuda").mkdir(exist_ok=True)

for frame in frames:
    try:
        decoded_frame, cuda = h264_frame_to_cuda(frame)

        i = decoded_frame.number
        print(f'frame {i}:')
        print(cuda)

        file_path = f'h264_frames_to_cuda/frame-{i}.jpg'
        jetson.utils.saveImageRGBA(file_path, cuda, decoded_frame.width, decoded_frame.height)
        print(f'saved as {file_path}')
        i += 1
    except NoFrame:
        print('(no frame data, skipped)')
    print('-----------------------------------------------------------------')