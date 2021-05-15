import jetson.utils
from jetson_tello import h264_frame_to_cuda

frame = b''

cuda, width, height = h264_frame_to_cuda(frame)

jetson.utils.saveImageRGBA('h264_frame_to_cuda.jpg', cuda, width, height)