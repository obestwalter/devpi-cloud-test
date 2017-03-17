# Could this be something for me?

If you are not using [devpi](http://doc.devpi.net) to test, share and store packages and test results you can probably stop reading now.

**devpi-cloud-test** provides a `dct` cli tool that manipulates repositories which in turn trigger CI tests of packages from your devpi index on CI services like Travis CI and Appveyor.

To make it clear: it triggers tests for the package hosted on devpi that you configured in the repository - not the source code in that repository.

This is just a thin convenience wrapper around a [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester) by [@nicoddemus](https://github.com/nicoddemus).

# How it works

Install this small cli tool (not yet on pypi):

    $ pip install git+git://github.com/obestwalter/devpi-cloud-test.git@master

To create a new cloud test repo you can get started by creating  the necessary files in a directory `devpi-cloud-test-<package name>` by calling

    $ dct create <package name>

e.g. if you are in `~/home/work` and call `dct create tuxy` a directory `devpi-cloud-test-tuxy` gets created with `dct.ini` prepopulated with the package name - you could also pass devpi user and index right away or add it later.

Create a new repo on Github or wherever you push to and add it as origin to the new repository.

Activate the CI services that are used in the test repo (e.g. Travis and Appveyor).

Copy the appropriate CI badge codes into `tpl/README.md`.

If you did not pass all values on creation add the missing settings in `dct.ini`.

    $ cd </path/to/your/dct/repo>
    $ dct trigger <version>  # version of package on devpi

sample output:

    dct trigger 2.6.1
    
    INFO:dct:## rendered tpl/README.md ##
    # Results for [tox==2.6.1](https://devpi.net/obestwalter/dev/tox/2.6.1)
    
    [![Build Status](https://travis-ci.org/obestwalter/devpi-cloud-test-tox.svg?branch=master)](https://travis-ci.org/obestwalter/devpi-cloud-test-tox)
    
    [![Build status](https://ci.appveyor.com/api/projects/status/98yyno2u5fpnds4l/branch/master?svg=true)](https://ci.appveyor.com/project/obestwalter/devpi-cloud-test-tox/branch/master)
    
    Test triggered at: Thu Mar 16 20:50:14 2017
    
    ## -> README.md ##
    
    INFO:dct:## rendered tpl/appveyor.yml ##
    install:
      - echo Installed Pythons
      - dir c:\Python*
      - choco install python.pypy > pypy-inst.log 2>&1 || (type pypy-inst.log & exit /b 1)
      - set PATH=C:\tools\pypy\pypy;%PATH% # so tox can find pypy
      - echo PyPy installed
      - pypy --version
      - C:\Python36\python -m pip install devpi
    build: false  # Not a C# project, build stuff at the test step instead.
    test_script:
      - C:\Python36\python -m devpi use https://devpi.net/obestwalter/dev
      - C:\Python36\python -m devpi test tox==2.6.1
    
    ## -> appveyor.yml ##
    
    INFO:dct:## rendered tpl/.travis.yml ##
    sudo: false
    language: python
    python:
      - 3.5
    install: "pip install -U devpi"
    script:
      - devpi use https://devpi.net/obestwalter/dev
      - devpi test tox==2.6.1
    
    ## -> .travis.yml ##
    
    INFO:dct:triggered test by pushing /home/oliver/Dropbox/projects/tox/devpi-cloud-test-tox

# Used by

* [tox-dev/tox](https://github.com/obestwalter/devpi-cloud-test-tox)
* that's it - nothing else - it's just an idea I am playing with
