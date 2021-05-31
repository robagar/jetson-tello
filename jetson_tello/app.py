#!/usr/bin/env python3

import asyncio
from inspect import isawaitable
from jetson_tello import H264DecoderAsync, decoded_frame_to_cuda
from tello_asyncio import Tello


def run_jetson_tello_app(fly, process_frame, drone=None, on_frame_decoded=None, wait_for_wifi=True):
    '''
    Fly and control a drone while analysing video frames using CUDA.

    This function takes two main arguments - an async function to control the 
    drone in whatever way you want, and a callback called with video frame data
    ready and loaded into CUDA memory for analysis.

    The `process_frame` callback always waits for the next available frame, 
    skipping any that arrive while processing the last.  Frame analysis can 
    take as long as it needs without falling behind the live video.

    There is also an optional `on_frame_decoded` callback which is called 
    for *every* frame.  This must be fast enough to not clog things up and
    cause latency.  

    :param fly: Awaitable function which controls the drone.  The app exits when complete.
    :type fly: Coroutine function which takes a :class:`tello_asyncio.tello.Tello` drone argument.
    :param process_frame: Callback called with frame data loaded into CUDA memory
    :type process_frame: Awaitable or plain function taking :class:`tello_asyncio.tello.Tello` drone, :class:`jetson_tello.types.DecodedFrame` frame, :class:`cudaImage` cuda
    :param drone: Optional drone instance. One will be created automatically if not provided
    :type drone: :class:`tello_asyncio.tello.Tello` 
    :param on_frame_decoded: Optional callback called for every decoded frame
    :type on_frame_decoded: Awaitable or plain function taking :class:`jetson_tello.types.DecodedFrame` frame
    :param wait_for_wifi: If true, wait for connection to the drone's WiFi network before proceeding (Linux only)
    :type wait_for_wifi: bool 
    '''

    if not drone:
        drone = Tello()

    async def main():
        if wait_for_wifi:
            print('[main] waiting for wifi...')
            await drone.wifi_wait_for_network()
    
        await drone.connect()

        # begin video stream
        await drone.start_video()
        decoder = H264DecoderAsync()

        async def watch_video():
            ''' 
            Receive and decode all frames from the drone. Decoding each frame
            often relies on previous frame data, so all frames must be decoded.
            '''
            print('[watch video] START')
            await decoder.decode_frames(drone.video_stream, on_frame_decoded)
            print('[watch video] END')

        async def process_frames():
            ''' 
            Process frames when available without falling behind
            '''
            print('[process frames] START')
            while True:
                # wait for next frame, skipping any that arrived during last iteration
                frame = await decoder.decoded_frame

                # load frame image into CUDA memory
                try:
                    cuda = decoded_frame_to_cuda(frame)
                except Exception as e:
                    continue

                # call callback
                if isawaitable(process_frame):
                    await process_frame(drone, frame, cuda)
                else:
                    process_frame(drone, frame, cuda)
            print('[process frames] END')

        try:
            # run all together until `fly` is complete
            finished, unfinished = await asyncio.wait(
                [fly(drone), watch_video(), process_frames()], 
                return_when=asyncio.FIRST_COMPLETED)

            # clean up
            for task in unfinished:
                task.cancel()
            await asyncio.wait(unfinished)
        finally:
            await drone.stop_video()
            await drone.disconnect()

    # run asyncio event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




