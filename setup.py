from setuptools import setup

setup(
    name='release-helper',
    author='Oliver Bestwalter',
    description='A little cli helper for my kind of release flow',
    install_requires=['fire', 'plumbum', 'devpy'],
    packages=['release_helper'],
    entry_points={'console_scripts': ['rh = release_helper.rh:main']},
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
