from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'krotov'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'params'), glob(os.path.join('params', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ldps-06',
    maintainer_email='ldps-06@example.com',
    description='ROS2 package for even numbers',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'even_pub = krotov.even_number_publisher:main',
            'overflow_listener = krotov.overflow_listener:main',
        ],
    },
)