Code examples
=============

H.264 frames to NumPy arrays
----------------------------

Demonstrates the decoding of pre-captured video frames (of my cat, Marble) and loading into `NumPy arrays <https://numpy.org/doc/stable/reference/arrays.html>`_ suitable for analysis.

.. literalinclude:: ../examples/h264_frames_to_numpy_arrays.py
   :language: python 


H.264 frames to CUDA
--------------------

The same video frames, but this time loaded into CUDA memory for GPU processing.  The images are saved back out to JPEG files just so you can see that they are valid. 

.. literalinclude:: ../examples/h264_frames_to_cuda.py
   :language: python 


Object detection
-----------------

Runs the frames through the *ssd-mobilenet-v2* detector and (hopefully) finds the cat.

.. literalinclude:: ../examples/object_detection.py
   :language: python 


Face detection
--------------

Pipes video frames captured from the flying Tello drone through the *facenet* detector and reports any human faces it sees.

.. literalinclude:: ../examples/face_detection.py
   :language: python 


Face and object detection
-------------------------

As face detection above, but also detecting objects in view at the same time.

.. literalinclude:: ../examples/face_and_object_detection.py
   :language: python 

Example output::

    faces:
    <detectNet.Detection object>
       -- ClassID: 0
       -- Confidence: 0.809878
       -- Left:    434.667
       -- Top:     0
       -- Right:   702.267
       -- Bottom:  302.5
       -- Width:   267.6
       -- Height:  302.5
       -- Area:    80949
       -- Center:  (568.467, 151.25)
    objects:
    <detectNet.Detection object>
       -- ClassID: 7
       -- Confidence: 0.500977
       -- Left:    0
       -- Top:     7.30054
       -- Right:   959
       -- Bottom:  719.04
       -- Width:   959
       -- Height:  711.74
       -- Area:    682559
       -- Center:  (479.5, 363.171)