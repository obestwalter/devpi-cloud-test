from setuptools import setup

setup(
    name='release-helper',
    install_requires=['fire', 'plumbum', 'devpy'],
    entry_points={'console_scripts': ['dct = dct:main']}
)
