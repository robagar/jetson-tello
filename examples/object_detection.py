import jetson.inference
from jetson_tello import h264_frame_to_cuda, FrameDecodeError

from ast import literal_eval
with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

i = 1
for frame in frames:
    try:
        cuda, width, height = h264_frame_to_cuda(frame)

        detections = net.Detect(cuda)

        print(f'frame {i} detections:')
        for d in  detections:
            print(d)

        i += 1
    except FrameDecodeError:
        pass    
