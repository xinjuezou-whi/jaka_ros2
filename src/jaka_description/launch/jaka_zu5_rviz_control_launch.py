import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
# from launch.substitutions import LaunchConfiguration, FindPackageShare # Xinjue
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Declare launch arguments if needed (e.g., file paths)

    urdf_file = os.path.join(
        get_package_share_directory("jaka_description"),
        "urdf",
        "jaka_zu5.urdf"
    )
    with open(urdf_file, "r") as f:
        robot_desc = f.read()

    return LaunchDescription([
        # Declare the robot_description parameter using a URDF file
        DeclareLaunchArgument(
            'robot_description',
            # default_value=FindPackageShare('jaka_description') + '/urdf/jaka_zu5.urdf', # Xinjue
            default_value=PathJoinSubstitution(
                [FindPackageShare('jaka_description'), 'urdf', 'jaka_zu5.urdf']
            ),
            description='Path to the URDF file for the robot'
        ),

        # Start the robot_state_publisher node 
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            # remappings=[('/joint_states', 'robot_jog_command')],
            parameters=[
                {"robot_description": robot_desc}
            ],
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),
        
        # # Start the jaka_jog_panel node # Xinjue
        # Node(
        #     package='jaka_jog_panel',
        #     executable='jakajogpanel',
        #     name='jaka_jog_panel',
        # ),

        # Start rviz with the provided configuration file
        Node(
            package='rviz2',  # ROS 2 uses rviz2 instead of rviz
            executable='rviz2',
            name='rviz',
            # arguments=['-d', FindPackageShare('jaka_description') + '/config/jaka_zu5_urdf.rviz'], # Xinjue
            arguments=[
                '-d',
                PathJoinSubstitution([
                    FindPackageShare('jaka_description'),
                    'config',
                    'jaka_zu5_urdf.rviz',
                ]),
            ],
            # required=True # Xinjue
            output='screen',
        ),
    ])
