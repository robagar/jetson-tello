
jetson-tello
============

.. image:: images/jetson_plus_tello.png

Utility code for using the NVIDIA `Jetson <https://developer.nvidia.com/embedded/jetson-nano-developer-kit>`_ and `tello\-asyncio <https://tello-asyncio.readthedocs.io/en/latest/>`_ to interact with the `Tello EDU <https://www.ryzerobotics.com/tello-edu>`_ drone.

The primary function so far is to pipe video frame data from the drone through to neural networks running on the Jetson, typically for object or face detection.  

Most importantly, the frame data analysis can take as much time as it needs.  Frames are skipped if needed to keep up with the live video stream. 

Created for my autonomous drone hobby project, `drone\-braain <https://github.com/robagar/drone-braain>`_, which is very much in its infancy. 

Package `jetson\-tello <https://pypi.org/project/jetson-tello/>`_ on PyPi. 


Prerequisites
-------------

There are two prerequisites that require manual installation:

* NVIDIA's `jetson\-inference <https://github.com/dusty-nv/jetson-inference>`_ project, following these `instructions <https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md>`_ to build from source and install.

* My fork of `h264decoder <https://github.com/robagar/h264decoder>`_. This is identical to the `original repo <https://github.com/DaWelter/h264decoder>`_ apart from building with the slightly old version of CMake (3.10) available on the Jetson.

.. toctree::
   :maxdepth: 3

   modules
   examples

