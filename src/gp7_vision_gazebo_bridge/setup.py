from setuptools import find_packages, setup

package_name = "gp7_vision_gazebo_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="norman",
    maintainer_email="norman@todo.todo",
    description="Vision-to-Gazebo bridge for box spawn/update.",
    license="Apache-2.0",
    tests_require=["pytest"],
)

