from pathlib import Path
import jetson.utils
from jetson_tello import h264_frame_to_cuda, FrameDecodeError

from ast import literal_eval
with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

Path("h264_frames_to_cuda").mkdir(exist_ok=True)

i = 1
for frame in frames:
    try:
        cuda, width, height = h264_frame_to_cuda(frame)

        file_path = f'h264_frames_to_cuda/frame-{i}.jpg'
        print(file_path)
        jetson.utils.saveImageRGBA(file_path, cuda, width, height)
        i += 1
    except FrameDecodeError:
        pass
