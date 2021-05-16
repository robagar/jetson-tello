import jetson.utils
import h264decoder # see https://github.com/DaWelter/h264decoder for installation instructions
import numpy as np
from tello_asyncio import VIDEO_WIDTH, VIDEO_HEIGHT

class FrameDecodeError(Exception):
    pass

decoder = h264decoder.H264Decoder()

def h264_frame_to_numpy_array(frame):
    (frame_info, num_bytes) = decoder.decode_frame(frame)
    (frame_data, width, height, row_size) = frame_info
    if width and height:
        flat_array = np.frombuffer(frame_data, dtype=np.ubyte)
        array = np.reshape(flat_array, (height, width, 3))
        return array, width, height
    else:
        raise FrameDecodeError()

def h264_frame_to_cuda(frame):
    array, width, height = h264_frame_to_numpy_array(frame)
    cuda = jetson.utils.cudaFromNumpy(array)
    return cuda, width, height

# Tello camera field of view measured (roughly) in degrees
CAMERA_HORIZONTAL_HALF_FOV = 26.9
CAMERA_VERTICAL_HALF_FOV = 20.2

HALF_VIDEO_WIDTH = VIDEO_WIDTH / 2
HALF_VIDEO_HEIGHT = VIDEO_HEIGHT / 2

def video_x_to_local_azimuth(x, y):
    return CAMERA_HORIZONTAL_HALF_FOV * (y - HALF_VIDEO_WIDTH) / HALF_VIDEO_WIDTH

def video_y_to_local_altitude(x, y):
    return -CAMERA_VERTICAL_HALF_FOV * (y - HALF_VIDEO_HEIGHT) / HALF_VIDEO_HEIGHT
