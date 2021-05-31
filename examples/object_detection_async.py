#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import decoded_frame_to_cuda, H264DecoderAsync

from ast import literal_eval
with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

async def async_frames():
    for f in frames:
        yield f
        await asyncio.sleep(1/30)

object_detector = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

async def main():
    decoder = H264DecoderAsync()

    async def watch_video():
        print('[watch video] START')
        await decoder.decode_frames(async_frames())
        print('[watch video] END')

    async def detect_objects():
        print('[detect objects] START')
        while True:
            # print('[detect objects] waiting for frame...')
            f = await decoder.decoded_frame
            # print(f'[detect objects] frame {f.number}')
            try:
                cuda = decoded_frame_to_cuda(f)
                detections = object_detector.Detect(cuda)
                print(f'frame {f.number} detections:')
                for d in  detections:
                    print(d)
            except Exception as e:
                print(f'error {e}')
                print('(no frame)')
        print('[detect objects] END')

    finished, unfinished = await asyncio.wait([watch_video(), detect_objects()], return_when=asyncio.FIRST_COMPLETED)
    for task in unfinished:
        task.cancel()
    await asyncio.wait(unfinished)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
