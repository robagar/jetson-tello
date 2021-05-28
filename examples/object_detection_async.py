#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import decoded_frame_to_cuda, FrameDecodeError, H264DecoderAsync

from ast import literal_eval
with open("frames.txt", "r") as f:
    frames = [literal_eval(l) for l in f]

async def async_frames():
    for f in frames:
        yield f
        await asyncio.sleep(0.1)

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
            print('[detect objects] waiting for frame...')
            f = await decoder.decoded_frame
            print(f'[detect objects] frame {f.number}')
            try:
                cuda = decoded_frame_to_cuda(f)
                print('cuda:', cuda)
                object_detections = object_detector.Detect(cuda)
                print(object_detections)
            except Exception as e:
                print(f'error {e}')
                print('(no frame)')
        print('[detect objects] END')

    await asyncio.wait([watch_video(), detect_objects()], return_when=asyncio.FIRST_COMPLETED)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
