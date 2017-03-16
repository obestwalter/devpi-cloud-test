# Could this be something for me?

If you are not using [devpi](http://doc.devpi.net) to test, share and store packages and test results you can probably stop reading now.

**devpi-cloud-test** provides a `dct` cli tool that manipulates repositories which in turn trigger CI tests of packages from your devpi index on CI services like Travis CI and Appveyor.

To make it clear: it triggers tests for the package hosted on devpi that you configured in the repository - not the source code in that repository.

This is just a thin convenience wrapper around a [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester) by [@nicoddemus](https://github.com/nicoddemus).

# How it works

Install this small cli tool (not yet on pypi):

    $ pip install git+git://github.com/obestwalter/devpi-cloud-test.git@master

Fork an existing devpi-cloud-test-repo, e.g. https://github.com/obestwalter/devpi-cloud-test-tox and clone it.

Activate the CI services that are used in the test repo (e.g. Travis and Appveyor).

Copy the appropriate CI badge codes into `tpl/README.md`.

Adjust settings in `dct.ini`

    $ cd </path/to/your/dct/repo>
    $ dct trigger <version>  # version of package on devpi

# Used by

* [tox-dev/tox](https://github.com/tox-dev/tox)
* that's it - nothing else - it's just an idea I am playing with
