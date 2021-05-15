import jetson.utils
import h264decoder # see https://github.com/DaWelter/h264decoder for installation instructions
import numpy as np

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
    array, width, height = frame_to_numpy_array(frame)
    cuda = jetson.utils.cudaFromNumpy(array)
    return cuda, width, height
