# Could this be something for me?

If you are not a Python developer maintaining an open source project you can probably stop reading now.

If you are not using [devpi](http://doc.devpi.net) to test, share and store packages and test results you can probably stop reading now.

# What does this do?

dctt configures a special trigger repository to run tests on Travis CI and Appveyor.

# How it works

Install this tool (not yet on pypi):

    $ pip install git+git://github.com/obestwalter/release-helper.git@master 

Fork an existing dctt-repo, e.g. https://github.com/obestwalter/dctt-tox and clone it.

Activate Travis and Appveyor for your fork.

Copy the badge info for Travis and Appveyor into the README.

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

This is just a thin convenience wrapper around [@nicoddemus](https://github.com/nicoddemus) [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester).

> Talent hits a target no one else can hit; Genius hits a target no one else can see.
>
> -- Arthur Schopenhauer

