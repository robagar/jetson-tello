import asyncio
from h264decoder import H264Decoder # see https://github.com/DaWelter/h264decoder for installation instructions
from .types import DecodedFrame


class H264DecoderAsync:
    def __init__(self):
        self._decoder = H264Decoder()
        self._frame_available = asyncio.Condition()
        self._decoded_frame = None
        self._frame_number = 0

    async def decode_frames(self, video_stream):
        async for frame in video_stream:
            # print(f'[H264DecoderAsync] frame, acquiring lock...')
            await self._frame_available.acquire()
            self._frame_number += 1
            # print(f'[H264DecoderAsync] frame {self._frame_number}')
            try:
                (frame_info, num_bytes) = self._decoder.decode_frame(frame)
                (frame_data, width, height, row_size) = frame_info
                print(width, height, len(frame_data))
                self._decoded_frame = DecodedFrame(self._frame_number, width, height, frame_data)
                self._frame_available.notify()
            except Exception as e:
                print(f'[H264DecoderAsync] error {e}')
                self._decoded_frame = None
            self._frame_available.release()

    @property
    async def decoded_frame(self):
        # print(f'[H264DecoderAsync] decoded frame, acquiring lock...')
        await self._frame_available.acquire()
        # print(f'[H264DecoderAsync] decoded frame, waiting...')
        await self._frame_available.wait()
        f = self._decoded_frame
        self._frame_available.release()
        return f
