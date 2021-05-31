try:
    import jetson.utils
except ImportError:
    print('ImportError - failed to import jetson.utils')
    print('Please visit https://github.com/dusty-nv/jetson-inference and follow the instructions to build and install')

try:
    import h264decoder
except ImportError:
    print('ImportError - failed to import h264decoder')
    print('h264decoder requires manual building and installation - please see https://github.com/robagar/h264decoder for installation instructions')

import numpy as np
from .exceptions import NoFrameData
from .types import DecodedFrame


def decode_h264_frame(h264_frame):
    '''
    Attempt to decode an h.264 encoded frame.

    :param bytes h624_frame: The encoded frame data
    :rtype: :class:`jetson_tello.types.DecodedFrame`
    :throws: :class:`jetson_tello.exceptions.NoFrameData`
    '''
    fn = decode_h264_frame
    if not hasattr(fn, 'decoder'):
        fn.decoder = h264decoder.H264Decoder()
    if not hasattr(fn, 'frame_number'):
        fn.frame_number = 0

    (frame_info, num_bytes) = fn.decoder.decode_frame(h264_frame)
    (data, width, height, row_size) = frame_info
    if width and height:
        fn.frame_number += 1
        return DecodedFrame(fn.frame_number, width, height, data)
    else:
        raise NoFrameData()


def decoded_frame_to_numpy_array(decoded_frame):
    '''
    Takes a decoded frame and returns a NumPy array of the RGB values.

    :param decoded_frame:
    :type decoded_frame: :class:`jetson_tello.types.DecodedFrame`
    :rtype: :class:`numpy.array`
    '''

    (frame_number, width, height, data) = decoded_frame
    flat_array = np.frombuffer(data, dtype=np.ubyte)
    return np.reshape(flat_array, (height, width, 3))


def decoded_frame_to_cuda(decoded_frame):
    '''
    Loads frame data into CUDA memory.

    :param decoded_frame:
    :type decoded_frame: :class:`jetson_tello.types.DecodedFrame`
    :rtype: :class:`cudaImage`
    '''
    numpy_array = decoded_frame_to_numpy_array(decoded_frame)
    return jetson.utils.cudaFromNumpy(numpy_array)


def h264_frame_to_numpy_array(h264_frame):
    '''
    Decodes raw h.264 frame data and copies it into a NumPy array ready for analysis.

    :param h264_frame: The h.264 encoded frame data
    :type frame: bytes
    :rtype: (:class:`jetson_tello.types.DecodedFrame`, :class:`numpy.ndarray`)
    :throws: :class:`jetson_tello.video.NoFrameData`
    '''
    decoded_frame = decode_h264_frame(h264_frame)
    numpy_array = decoded_frame_to_numpy_array(decoded_frame)
    return decoded_frame, numpy_array


def h264_frame_to_cuda(h264_frame):
    '''
    Decodes raw h.264 frame data and copies it into CUDA memory.

    :param frame: The raw frame data
    :type frame: bytes
    :rtype: (:class:`jetson_tello.types.DecodedFrame`, :class:`cudaImage`)
    :throws: :class:`jetson_tello.video.NoFrameData`
    '''
    decoded_frame, numpy_array = h264_frame_to_numpy_array(h264_frame)
    cuda = jetson.utils.cudaFromNumpy(numpy_array)
    return decoded_frame, cuda


