import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_share = get_package_share_directory('tricept_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'tricept.urdf.xacro')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'tricept.rviz')

    # Forzamos la lectura como string para evitar el error de parsing YAML en ROS 2 Jazzy
    robot_description_content = ParameterValue(
        Command(['xacro ', xacro_file]), 
        value_type=str
    )

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            parameters=[{'robot_description': robot_description_content}]  # <--- Esta línea era necesaria
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file] if os.path.exists(rviz_config_file) else []
        )
    ])
