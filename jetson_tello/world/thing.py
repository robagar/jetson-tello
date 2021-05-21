from time import time
from ..coco import get_coco_class
from ..video import video_x_to_local_azimuth, video_y_to_local_altitude


class Thing:
    def __init__(self, detected_object):
        self.link_detected_object(detected_object)

    def link_detected_object(self, detected_object):
        self._last_seen_at_time = time()
        self._most_recent_detected_object = detected_object
        self._coco_class = get_coco_class(detected_object.ClassId)
        self._confidence - detected_object.Confidence
        x,y = detected_object.Center
        self._local_azimuth = video_x_to_local_azimuth(x)
        self._local_altitude = video_y_to_local_altitude(y)

    @property
    def last_seen_at_time(self):
        return self._last_seen_at_time

    @property
    def coco_class(self):
        return self._coco_class

    @property
    def confidence(self):
        return self._confidence

    @property
    def local_azimuth(self):
        return self._local_azimuth    

    @property
    def local_altitude(self):
        return self._local_altitude    
