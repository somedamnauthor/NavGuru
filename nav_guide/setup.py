from setuptools import setup

package_name = 'nav_guide'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ramakrishnan Ramakrishnan',
    maintainer_email='Parthipan Ramakrishnan',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_controller = nav_guide.robot_controller:main',
            'astar = nav_guide.astar:main',
            'dijkstra = nav_guide.dijkstra:main',
            'qlearning = nav_guide.qlearning:main',
        ],
    },
)
