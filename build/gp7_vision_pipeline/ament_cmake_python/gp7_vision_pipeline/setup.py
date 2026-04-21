from setuptools import find_packages
from setuptools import setup

setup(
    name='gp7_vision_pipeline',
    version='0.1.0',
    packages=find_packages(
        include=('gp7_vision_pipeline', 'gp7_vision_pipeline.*')),
)
