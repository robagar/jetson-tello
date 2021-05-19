#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import h264_frame_to_cuda, FrameDecodeError #, World, get_coco_class
from tello_asyncio import Tello

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

next_frame = None
frame_available = asyncio.Condition()

# world = World()

def on_video_frame(frame):
    global next_frame
    async with frame_available:
        next_frame = frame
        frame_available.notify()


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
    try:
        await drone.connect()
        await drone.start_video(on_video_frame)
        # await drone.takeoff()
        # await drone.turn_clockwise(360)
        # await drone.land()

        while True:
            async with frame_available:
                await frame_available.wait()
                frame = next_frame
                next_frame = None

            process_frame(frame)

    finally:
        await drone.stop_video()
        await drone.disconnect()

# Python 3.7+
#asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())