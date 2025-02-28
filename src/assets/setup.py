# ~/ros2_ws/src/assets/setup.py

from setuptools import setup, find_packages
import os

package_name = 'assets'

def find_data_files():
    data_files = []
    for root, dirs, files in os.walk('share/assets/p1'):
        for file in files:
            filepath = os.path.join(root, file)
            install_dir = os.path.relpath(root, 'share')
            data_files.append((os.path.join('share', install_dir), [filepath]))
    return data_files

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(include=[package_name, f'{package_name}.*']),
    include_package_data=True,  # 确保包含包内数据
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wbb',
    maintainer_email='wbb@example.com',
    description='Assets package containing robot configurations',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 如果有需要，可以在这里添加脚本入口
        ],
    },
    data_files=find_data_files() + [('share/' + package_name, ['package.xml'])],  # 安装 package.xml

)

