class NoFrameData(Exception):
    '''
    Exception raised when no frame data is available, either because the frame
    is corrupted, or intentionally for reasons known only to the h.264 encoder.
    '''
    pass
