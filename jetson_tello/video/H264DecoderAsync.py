import asyncio
from inspect import iscoroutinefunction

try:
    from h264decoder import H264Decoder
except ImportError:
    print('ImportError - failed to import h264decoder.H264Decoder')
    print('h264decoder requires manual building and installation - please see https://github.com/robagar/h264decoder for installation instructions')

from .types import DecodedFrame


class H264DecoderAsync:
    '''
    Decodes a stream of h.264 encoded video frames, making them available for
    analysis.
    '''

    def __init__(self):
        self._decoder = H264Decoder()
        self._frame_available = asyncio.Condition()
        self._decoded_frame = None
        self._frame_number = 0

    async def decode_frames(self, video_stream, on_frame_decoded=None):
        '''
        Begin decoding video frames.

        :param video_stream: The video stream
        :type video_stream: Asynchronous iterator of h.264 frames
        :param on_frame_decoded: Optional callback called  for each successfully decoded frame. Must be fast!
        :type on_frame_decoded: Awaitable or plain function taking :class:`jetson_tello.types.DecodedFrame` 
        '''
        async for frame in video_stream:
            # print(f'[H264DecoderAsync] frame, acquiring lock...')
            await self._frame_available.acquire()
            # print(f'[H264DecoderAsync] frame {self._frame_number}')
            try:
                (frame_info, num_bytes) = self._decoder.decode_frame(frame)
                (frame_data, width, height, row_size) = frame_info
                if width and height:
                    self._frame_number += 1
                    self._decoded_frame = DecodedFrame(self._frame_number, width, height, frame_data)
                    if on_frame_decoded:
                        if iscoroutinefunction(on_frame_decoded):
                            await on_frame_decoded(self._decoded_frame)
                        else:
                            on_frame_decoded(self._decoded_frame)
                    self._frame_available.notify()
            except Exception as e:
                # print(f'[H264DecoderAsync] error: {e}')
                self._decoded_frame = None
            self._frame_available.release()

    @property
    async def decoded_frame(self):
        '''
        The most recently decoded frame.
        :rtype: :class:`jetson_tello.types.DecodedFrame`
        '''
        # print(f'[H264DecoderAsync] decoded frame, acquiring lock...')
        await self._frame_available.acquire()
        # print(f'[H264DecoderAsync] decoded frame, waiting...')
        await self._frame_available.wait()
        f = self._decoded_frame
        self._frame_available.release()
        return f
