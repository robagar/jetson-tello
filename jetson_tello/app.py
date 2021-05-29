#!/usr/bin/env python3

import asyncio
from jetson_tello import H264DecoderAsync, decoded_frame_to_cuda
from tello_asyncio import Tello


def run_jetson_tello_app(fly, process_frame):
    drone = Tello()

    async def main():
        print('[main] waiting for wifi...')
        await drone.wifi_wait_for_network()
        await drone.connect()
        await drone.start_video()
        decoder = H264DecoderAsync()

        async def watch_video():
            print('[watch video] START')
            await decoder.decode_frames(drone.video_stream)
            print('[watch video] END')

        async def process_frames():
            print('[process frames] START')
            while True:
                frame = await decoder.decoded_frame
                try:
                    cuda = decoded_frame_to_cuda(frame)
                except Exception as e:
                    continue

                await process_frame(drone, frame, cuda)
            print('[process frames] END')

        try:
            finished, unfinished = await asyncio.wait([fly(drone), watch_video(), process_frames()], return_when=asyncio.FIRST_COMPLETED)
            for task in unfinished:
                task.cancel()
            await asyncio.wait(unfinished)
        finally:
            await drone.stop_video()
            await drone.disconnect()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




