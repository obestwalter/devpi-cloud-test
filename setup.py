from setuptools import setup, find_packages

setup(
    name='devpi-cloud-test',
    author='Oliver Bestwalter',
    url='https://github.com/obestwalter/devpi-cloud-test',
    use_scm_version=True,
    description='CLI tool to manipulate cloud test repos and trigger tests',
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['fire', 'plumbum', 'devpi'],
    entry_points={'console_scripts': ['dct = dct.cli:main']},
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
