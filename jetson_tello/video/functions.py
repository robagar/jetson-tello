try:
    import jetson.utils
except ImportError:
    print('ImportError - failed to import jetson.utils')
    print('Please visit https://github.com/dusty-nv/jetson-inference and follow the instructions to build and install')

from tello_asyncio_video import decoded_frame_to_numpy_array, h264_frame_to_numpy_array


def decoded_frame_to_cuda(decoded_frame):
    '''
    Loads frame data into CUDA memory.

    :param decoded_frame:
    :type decoded_frame: :class:`tello_asyncio_video.DecodedFrame`
    :rtype: :class:`cudaImage`
    '''
    numpy_array = decoded_frame_to_numpy_array(decoded_frame)
    return jetson.utils.cudaFromNumpy(numpy_array)


def h264_frame_to_cuda(h264_frame):
    '''
    Decodes raw h.264 frame data and copies it into CUDA memory.

    :param frame: The raw frame data
    :type frame: bytes
    :rtype: (:class:`tello_asyncio_video.DecodedFrame`, :class:`cudaImage`)
    :throws: :class:`tello_asyncio_video.NoFrameData`
    '''
    decoded_frame, numpy_array = h264_frame_to_numpy_array(h264_frame)
    cuda = jetson.utils.cudaFromNumpy(numpy_array)
    return decoded_frame, cuda


