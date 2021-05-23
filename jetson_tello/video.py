import jetson.utils
import h264decoder # see https://github.com/DaWelter/h264decoder for installation instructions
import numpy as np

class FrameDecodeError(Exception):
    pass

decoder = h264decoder.H264Decoder()

def h264_frame_to_numpy_array(frame):
    '''
    Decodes raw h.264 frame data and copies it into a NumPy array ready for analysis.

    :param frame: The raw frame data
    :type frame: bytes
    :rtype: :class:`numpy.ndarray`
    :throws: :class:`jetson_tello.video.FrameDecodeError`
    '''
    try:
        (frame_info, num_bytes) = decoder.decode_frame(frame)
    except:
        raise FrameDecodeError()

    (frame_data, width, height, row_size) = frame_info
    if width and height:
        flat_array = np.frombuffer(frame_data, dtype=np.ubyte)
        array = np.reshape(flat_array, (height, width, 3))
        return array, width, height
    else:
        raise FrameDecodeError()

def h264_frame_to_cuda(frame):
    '''
    Decodes raw h.264 frame data and copies it into CUDA memory.

    :param frame: The raw frame data
    :type frame: bytes
    :rtype: :class:`cudaImage`
    :throws: :class:`jetson_tello.video.FrameDecodeError`
    '''
    array, width, height = h264_frame_to_numpy_array(frame)
    cuda = jetson.utils.cudaFromNumpy(array)
    return cuda, width, height

