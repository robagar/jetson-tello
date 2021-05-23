Code examples
=============

H.264 frames to NumPy arrays
----------------------------

Demonstrates the decoding of pre-captured video frames (of my cat, Marble) and loading into `NumPy arrays<https://numpy.org/doc/stable/reference/arrays.html>`_ suitable for analysis.

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


