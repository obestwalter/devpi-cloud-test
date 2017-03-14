from setuptools import setup

setup(
    name='release-helper',
    install_requires=['fire', 'plumbum', 'devpy'],
    entry_points={'console_scripts': ['dct = dct:main']},
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
