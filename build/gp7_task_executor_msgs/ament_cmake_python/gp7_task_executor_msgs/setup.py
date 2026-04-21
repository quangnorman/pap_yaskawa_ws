from setuptools import find_packages
from setuptools import setup

setup(
    name='gp7_task_executor_msgs',
    version='1.0.0',
    packages=find_packages(
        include=('gp7_task_executor_msgs', 'gp7_task_executor_msgs.*')),
)
