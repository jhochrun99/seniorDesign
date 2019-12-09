#file for setting up our library

#!/usr/bin/env python
from setuptools import setup
setup(name='compe',
  version='1.0',
  description='CompE Stub Library',
  author='Jess Hochrun',
  author_email='jh5367@nyu.edu',
  url='https://github.com/jhochrun99/seniorDesign',
  py_modules=['compe'],
  install_requires=['pyserial', 'Adafruit_BBIO'], #need to edit these with the libraries we installed and import
)
