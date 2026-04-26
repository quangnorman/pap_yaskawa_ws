from setuptools import find_packages, setup

setup(
    name="gp7_gui",
    version="0.1.0",
    packages=find_packages(include=["gp7_gui", "gp7_gui.*"]),
    install_requires=["setuptools"],
    zip_safe=True,
    data_files=[
        ("share/ament_index/resource_index/packages", []),
        ("share/gp7_gui", ["package.xml"]),
        ("share/gp7_gui/launch", ["launch/gui.launch.py"]),
        ("share/gp7_gui/config", ["config/gui_modes.yaml"]),
        ("share/gp7_gui/resource", ["resource/gp7_gui"]),
    ],
    entry_points={
        "console_scripts": [
            "gp7_gui = gp7_gui.gui_main:main",
        ],
    },
)
