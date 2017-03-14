# Latest package cloud test results for $

Visit package: [tox==2.6.1](https://devpi.net/obestwalter/dev/tox/2.6.1)

Travis: [![Build Status](https://travis-ci.org/$USER/devpi-cloud-tester.svg?branch=master)](https://travis-ci.org/$USER/devpi-cloud-tester)

AppVeyor: [![Build status](https://ci.appveyor.com/api/projects/status/i8uvwxe6gxwkir5g?svg=true)](https://ci.appveyor.com/project/$USER/devpi-cloud-tester)

# What is this?

Test and release helper for packages that:

* create version numbers from tags (e.g. with [setuptools_scm](https://pypi.python.org/pypi/setuptools_scm))
* are pushed to devpi
* are released to pypi by pushing from devpi

# Usage

1. Fork this repository and enable Travis and AppVeyor for your fork.
2. adjust `settings.py` to your needs
3. If necessary: edit `.travis.yml` and `appveyor.yml`

    $ </path/to/your/clone>
    $ pip install -e .
    $ dct -- --help

# Used by

* [tox-dev/tox](https://github.com/tox-dev/tox)
* that's it - nothing else

# Acknowledgements

Based on [@nicoddemus](https://github.com/nicoddemus) [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester).

