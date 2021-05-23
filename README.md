# jetson-tello

Utility code for using the NVIDIA [Jetson](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) and [tello-asyncio](https://tello-asyncio.readthedocs.io/en/latest/) to interact with the [Tello EDU](https://www.ryzerobotics.com/tello-edu) drone.

The primary function so far is to pipe video frame data from the drone through to neural networks running on the Jetson, typically for object or face detection.

Created for my autonomous drone project, [drone-braain](https://github.com/robagar/drone-braain). 

## Prerequisites

There are two prerequisites that require manual installation:

* NVIDIA's [jetson-inference](https://github.com/dusty-nv/jetson-inference) project, following these [instructions](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md) to build from source and install.

* My fork of [h264decoder](https://github.com/robagar/h264decoder). This is identical to the [original repo](https://github.com/DaWelter/h264decoder) apart from building with the slightly old version of CMake (3.10) available on the Jetson.

## Example code

The [face_and_object_detection.py](./examples/face_and_object_detection.py) example demonstrates feeding video frames to object and face detection neural nets


``` python
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
```

Which typically outputs a stream of results like this (along with a fair amount of spam from the h.264 decoder):

```
    faces:
    <detectNet.Detection object>
       -- ClassID: 0
       -- Confidence: 0.809878
       -- Left:    434.667
       -- Top:     0
       -- Right:   702.267
       -- Bottom:  302.5
       -- Width:   267.6
       -- Height:  302.5
       -- Area:    80949
       -- Center:  (568.467, 151.25)
    objects:
    <detectNet.Detection object>
       -- ClassID: 7
       -- Confidence: 0.500977
       -- Left:    0
       -- Top:     7.30054
       -- Right:   959
       -- Bottom:  719.04
       -- Width:   959
       -- Height:  711.74
       -- Area:    682559
       -- Center:  (479.5, 363.171)
```