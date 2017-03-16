from setuptools import setup

setup(
    name='Devpi cloud test trigger',
    author='Oliver Bestwalter',
    description='Trigger tests for devpi packages on CI services',
    install_requires=['fire', 'plumbum', 'devpy'],
    entry_points={'console_scripts': ['dctt = dctt:main']},
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
