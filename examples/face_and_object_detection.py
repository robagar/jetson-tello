#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import h264_frame_to_cuda, FrameDecodeError
from tello_asyncio import Tello

face_detector = jetson.inference.detectNet("facenet", threshold=0.5)
object_detector = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)


async def process_frame(frame):
    try:
        cuda, width, height = h264_frame_to_cuda(frame)

        face_detections = face_detector.Detect(cuda)
        object_detections = object_detector.Detect(cuda)

        print('faces:')
        for d in face_detections:
            print(d)

        print('objects:')
        for d in object_detections:
            print(d)

    except FrameDecodeError:
        pass    

async def main():
    global next_frame

    drone = Tello()

    await drone.wifi_wait_for_network()
    await drone.connect()
    await drone.start_video()

    async def fly():
        await drone.takeoff()

    async def process_video():
        async for frame in drone.video_stream:
            await process_frame(frame)

    try:
        await asyncio.wait([fly(), process_video()])
    finally:
        await drone.stop_video()
        await drone.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
