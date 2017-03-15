# Could this be something for me?

If you are not a Python developer maintaining an open source project you can probably stop reading now.

If you are not maintaining a project that uses [setuptools_scm](https://pypi.python.org/pypi/setuptools_scm) or some other mechanism that determines the version number of a build from source control (specifically git) you can probably stop reading now.

If you are not using [devpi](http://doc.devpi.net) test test, share and store packages and test results you can probably stop reading now.

If you do not release your projects to [devpi](http://doc.devpi.net) or [pypi](https://pypi.org/) by pushing the package from your devpi index you can probably stop reading now.

If you did not stop reading although all this does not really fit, check out [zest.releaser](https://pypi.python.org/pypi/zest.releaser).

# What does this do?

* It tags the source code of your project with the version number you pass on the command line, creates a package and uploads it to your configured devpi index for testing.
* It configures a special trigger repository to run tests on Travis CI and Appveyor.
* (not yet, but would be easy) it releases the version to pypi and pushes the release tag to the repository

# How it works

* pip install release-helper
* create a repo for the project you want to test and release that way
* store the configuration in settings.py of that repo (TODO create a template for creating one of those repos)
* the release helper will operate on your project (setting and removing tags, creating builds) and on the trigger/result repo (rendering the files for the changing builds and updating the history)


# Used by

* [tox-dev/tox](https://github.com/tox-dev/tox)
* that's it - nothing else - it's just an idea I am playing with

```bash
$ </path/to/your/clone>
$ pip install -e .
$ rh -- --help
```

# Acknowledgements

> Talent hits a target no one else can hit; Genius hits a target no one else can see.

-- Arthur Schopenhauer

The cloud testing bit is based on [@nicoddemus](https://github.com/nicoddemus) [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester).
