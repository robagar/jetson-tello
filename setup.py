from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='jetson_tello',
      version='1.1.8',
      description='Tello drone integration with Jetson',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/robagar/jetson-tello',
      project_urls={
        'Documentation': 'https://jetson-tello.readthedocs.io/en/latest/'
      },
      author='Rob Agar',
      author_email='tello_asyncio@fastmail.net',
      license='LGPL',
      packages=['jetson_tello'],
      zip_safe=False,
      python_requires=">=3.6",
      install_requires=[
        'tello-asyncio >= 2.0.0',
        'tello-asyncio-video>=1.0.0',
        'numpy >= 1.13.3'
      ])