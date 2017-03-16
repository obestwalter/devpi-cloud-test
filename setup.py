from setuptools import setup

setup(
    name='devpi-cloud-test',
    author='Oliver Bestwalter',
    description='CLI tool to manipulate cloud test repos and trigger tests',
    install_requires=['fire', 'plumbum', 'devpy'],
    entry_points={'console_scripts': ['dct = dct:main']},
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
