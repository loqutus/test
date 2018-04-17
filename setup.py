from setuptools import setup

setup(
    name='test',
    packages=['master', 'slave'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pytest'
    ],
)