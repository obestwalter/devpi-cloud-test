# Could this be something for me?

If you are not a Python developer maintaining an open source project you can probably stop reading now.

If you are not maintaining a project that uses [setuptools_scm](https://pypi.python.org/pypi/setuptools_scm) or some other mechanism that determines the version number of a build from source control (specifically git) you can probably stop reading now.

If you are not using [devpi](http://doc.devpi.net) to test, share and store packages and test results you can probably stop reading now.

If you do not release your projects to [devpi](http://doc.devpi.net) or [pypi](https://pypi.org/) by pushing the package from your devpi index you can probably stop reading now.

If you did not stop reading although all this does not really fit, check out [zest.releaser](https://pypi.python.org/pypi/zest.releaser).

# What does this do?

* It tags the source code of your project with the version number you pass on the command line, creates a package and uploads it to your configured devpi index for testing.
* It configures a special trigger repository to run tests on Travis CI and Appveyor.
* (not yet, but would be easy) it releases the version to pypi and pushes the release tag to the repository

# How it works

Install this tool (not yet on pypi):

    $ pip install git+git://github.com/obestwalter/release-helper.git@master 

Fork an existing dctt-repo, e.g. https://github.com/obestwalter/dctt-tox and clone it.

Activate Travis and Appveyor for your fork.

Adjust settings in `dctt.ini`

    $ cd </path/to/your/dctt/repo>
    $ rh set <version>
    $ rh prepare
    $ rh test
    $ rh release  # (still a NOP)

# Used by

* [tox-dev/tox](https://github.com/tox-dev/tox)
* that's it - nothing else - it's just an idea I am playing with

# Acknowledgements

> Talent hits a target no one else can hit; Genius hits a target no one else can see.

-- Arthur Schopenhauer

The cloud testing bit is based on [@nicoddemus](https://github.com/nicoddemus) [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester).
