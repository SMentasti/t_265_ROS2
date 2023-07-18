import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    
    
    t265 = Node(
        package='t265',
        executable='publisher',
    )
    
        
    return LaunchDescription([
        t265,
    ])
