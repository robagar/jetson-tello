from collections import namedtuple

DecodedFrame = namedtuple('DecodedFrame', 'number width height data')
DecodedFrame.__doc__ = 'Video frame data and information'
DecodedFrame.number.__doc__ = 'Position in the sequence of successfully decoded frames'
DecodedFrame.width.__doc__ = 'Frame image width in pixels'
DecodedFrame.height.__doc__ = 'Frame image height in pixels'
DecodedFrame.data.__doc__ = 'Decoded frame data as `bytes`'
