#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import run_jetson_tello_app, get_coco_class

object_detector = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)


async def fly(drone):
    await drone.takeoff()
    for i in range(4):
        await drone.turn_clockwise(90)
        await asyncio.sleep(3)
    await drone.land()

def detect_objects(drone, frame, cuda):
    object_detections = object_detector.Detect(cuda)

    objects = []
    for d in object_detections:
        c = get_coco_class(d)
        confidence_percent = round(100 * d.Confidence)
        objects.append(f'{c.name} {confidence_percent}%')
    if objects:
        print(f'frame {frame.number}: {", ".join(objects)}')

run_jetson_tello_app(fly, process_frame=detect_objects)