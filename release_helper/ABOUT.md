# What is this?

It's a cli tool that by creating and pushing changes to this repository triggers CI builds and helps releasing projects that ...

* create version numbers from tags (e.g. with [setuptools_scm](https://pypi.python.org/pypi/setuptools_scm))
* are pushed to [devpi](http://doc.devpi.net)
* are released to [pypi](https://pypi.org/) by pushing from devpi

# Used by

* [tox-dev/tox](https://github.com/tox-dev/tox)
* that's it - nothing else - it's just an idea I am playing with

# Usage

Find out more from cli help or [the source luke](rh.py).

1. Fork this repository and enable Travis and Appveyor for your fork.
2. adjust `settings.py` to your needs
3. If necessary: edit `.travis.yml` and `appveyor.yml`

```bash
$ </path/to/your/clone>
$ pip install -e .
$ rh -- --help
```

# Acknowledgements

> Talent hits a target no one else can hit; Genius hits a target no one else can see.

-- Arthur Schopenhauer

The cloud testing bit is based on [@nicoddemus](https://github.com/nicoddemus) [nifty idea](https://github.com/nicoddemus/devpi-cloud-tester).
