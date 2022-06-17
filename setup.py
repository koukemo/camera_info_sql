from setuptools import setup

package_name = 'camera_info_sql'
sql_package_name = 'camera_info_sql.sql_operations'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, sql_package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='koukemo',
    maintainer_email='java.sparrow22.surface@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_info_sub = camera_info_sql.camera_info_sql_node:main',
        ],
    },
)
