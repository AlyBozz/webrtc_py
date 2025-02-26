import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rtc_py_demo',#double check if this is the actual package name
            executable='rtc_pi_demo', #the node inside the folder
            name='raspicam_device_node', #name
            output='screen',
            parameters=[{
                "host": "0.0.0.0",
                "port": 8080
            }]
        )
    ])