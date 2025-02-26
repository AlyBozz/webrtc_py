
from setuptools import setup

package_name = 'rtc_py_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/rtc_py_demo_launch.py']),
    ],
    install_requires=['setuptools', 'rclpy', 'aiortc', 'aiohttp', 'picamera2', 'av', 'numpy'],
    zip_safe=True,
    author='Aly Soliman',
    #author_email='your.email@example.com',
    description='ROS 2 package for WebRTC streaming on Raspberry Pi using libcamera.',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'rtc_pi_node = rtc_py_demo.rtc_pi_node:main'
        ],
    },
)