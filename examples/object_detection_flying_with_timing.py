#!/usr/bin/env python3

from time import time
import asyncio
import jetson.inference
from jetson_tello import H264DecoderAsync, decoded_frame_to_cuda, FrameDecodeError, get_coco_class_by_id
from tello_asyncio import Tello

object_detector = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

results = []

def decode_frame(frame):
    try:
        cuda, width, height = h264_frame_to_cuda(frame)

    except FrameDecodeError:
        print('(frame decode error)')
        pass    


def detect_objects_in_frame(frame_number, cuda):
        t0 = time()
        object_detections = object_detector.Detect(cuda)
        dt = time() - t0

        results.append([frame_number, dt, object_detections])


async def main():
    drone = Tello()

    print('[main] waiting for wifi...')
    await drone.wifi_wait_for_network()
    await drone.connect()
    await drone.start_video()
    decoder = H264DecoderAsync()

    async def fly():
        print('[flying] START')
        # await drone.takeoff()
        await asyncio.sleep(10)
        # await drone.land()
        print('[flying] END')

    async def watch_video():
        print('[watch video] START')
        await decoder.decode_frames(drone.video_stream)
        print('[watch video] END')

    async def detect_objects():
        print('[detect objects] START')
        while True:
            print('[detect objects] waiting for frame...')
            f = await decoder.decoded_frame
            print(f'[detect objects] frame {f.number}')
            try:
                cuda = decoded_frame_to_cuda(f)
                print('cuda:', cuda)
                detect_objects_in_frame(f.number, cuda)
            except Exception as e:
                print(f'error {e}')
                print('(no frame)')
        print('[detect objects] END')

    try:
        finished, unfinished = await asyncio.wait([fly(), watch_video(), detect_objects()], return_when=asyncio.FIRST_COMPLETED)
        for task in unfinished:
            task.cancel()
        await asyncio.wait(unfinished)
    finally:
        await drone.stop_video()
        await drone.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

def format_detections(ds):
    ss = []
    for d in ds:
        c = get_coco_class_by_id(d.ClassID)
        ss.append(c.name)
    return ', '.join(ss)

print('Results:')
for [i, t, ds] in results:
    print(f'frame #{i}, detection time {t:0.4}s, ' + format_detections(ds))



