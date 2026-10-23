import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_share = get_package_share_directory('tricept_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'tricept.urdf.xacro')
    
    # Procesamos el XACRO directamente en Python
    robot_description_config = xacro.process_file(xacro_file).toxml()

    # Nodo para arrancar el simulador Gazebo (con un mundo vacío y la física activa)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # Nodo para "spawnear" (generar) el robot en el simulador
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-string', robot_description_config, '-name', 'tricept', '-z', '1.5'],
        output='screen'
    )

    return LaunchDescription([gazebo, spawn])