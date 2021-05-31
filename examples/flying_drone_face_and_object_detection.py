#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import run_jetson_tello_app


face_detector = jetson.inference.detectNet("facenet", threshold=0.5)
object_detector = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)


def detect_faces_and_objects(drone, frame, cuda):
    face_detections = face_detector.Detect(cuda)
    object_detections = object_detector.Detect(cuda)

    print('faces:')
    for d in face_detections:
        print(d)

    print('objects:')
    for d in object_detections:
        print(d)


async def fly(drone):
    await drone.takeoff()
    for i in range(4):
        await drone.turn_clockwise(90)
        await asyncio.sleep(3)
    await drone.land()


run_jetson_tello_app(fly, process_frame=detect_faces_and_objects)