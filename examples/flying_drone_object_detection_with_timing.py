#!/usr/bin/env python3

from time import time
import asyncio
import jetson.inference
from jetson_tello import run_jetson_tello_app, get_coco_class


object_detector = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

results = []

def detect_objects(drone, frame, cuda):
    object_detections = object_detector.Detect(cuda)

    t0 = time()
    object_detections = object_detector.Detect(cuda)
    dt = time() - t0

    results.append([frame.number, dt, object_detections])


async def fly(drone):
    await drone.takeoff()
    for i in range(4):
        await drone.turn_clockwise(90)
        await asyncio.sleep(3)
    await drone.land()


run_jetson_tello_app(fly, process_frame=detect_objects)


#####################################################################
# output results

def format_detections(ds):
    ss = []
    for d in ds:
        c = get_coco_class(d)
        confidence_percent = round(100 * d.Confidence)
        ss.append(f'{c.name} {confidence_percent}%')
    if ss:
        return ', '.join(ss)
    else:
        return '(none)'

print('Results:')
total_detection_time = 0
for [i, t, ds] in results:
    print(f'  frame #{i}, detection time {t:0.4}s, ' + format_detections(ds))
    total_detection_time += t

num_results = len(results)
print(f'total results: {num_results}')

average_detection_time = total_detection_time / num_results
print(f'average detection time: {average_detection_time:0.4}s')