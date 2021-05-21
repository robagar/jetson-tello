#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import h264_frame_to_cuda, FrameDecodeError #, World, get_coco_class
from tello_asyncio import Tello

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# world = World()

def process_frame(frame):
    try:
        cuda, width, height = h264_frame_to_cuda(frame)

        detections = net.Detect(cuda)

        print(f'detections:')
        for d in  detections:
            print(d)

    except FrameDecodeError:
        pass    

async def main():
    global next_frame

    drone = Tello()
    await drone.connect()
    await drone.start_video()
    await drone.connect_video()

    async def fly():
        pass

    async def process_video():
        async for frame in drone.video_stream:
            process_frame(frame)

    try:
        await asyncio.wait([fly(), process_video()])
    finally:
        await drone.stop_video()
        await drone.disconnect()

# Python 3.7+
#asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
