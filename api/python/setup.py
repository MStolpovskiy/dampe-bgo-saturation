import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dampe_bgo_sat_api",
    version = "1.0",
    author = "M. Stolpovskiy",
    author_email = "mikhail.stolpovskiy@unige.ch",
    description = "Python API to apply the CNN models for the BGO saturation",
    long_description=read('README'),
)
