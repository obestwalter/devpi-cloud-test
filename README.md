# Could this be something for me?

If you are not a Python developer maintaining an open source project you can probably stop reading now.

If you are not using [devpi](http://doc.devpi.net) to test, share and store packages and test results you can probably stop reading now.

# What does this do?

dctt configures a special trigger repository to run tests on Travis CI and Appveyor.

# How it works

Install this small cli tool (not yet on pypi):

    $ pip install git+git://github.com/obestwalter/devpi-cloud-test.git@master

Fork an existing devpi-cloud-test-repo, e.g. https://github.com/obestwalter/devpi-cloud-test-tox and clone it.

Activate the CI services that are used in the test repo (e.g. Travis and Appveyor).

Copy the appropriate CI badge codes into `tpl/README.md`.

Adjust settings in `dctt.ini`

    $ cd </path/to/your/dctt/repo>
    $ dctt trigger <version>  # version of package on devpi

# Used by

* [tox-dev/tox](https://github.com/tox-dev/tox)
* that's it - nothing else - it's just an idea I am playing with

# Acknowledgements

This is just a thin convenience wrapper around [@nicoddemus](https://github.com/nicoddemus) [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester).

> Talent hits a target no one else can hit; Genius hits a target no one else can see.
>
> -- Arthur Schopenhauer
