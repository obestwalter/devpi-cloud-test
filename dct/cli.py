import logging
from configparser import ConfigParser
from datetime import datetime
from string import Template

import fire
from plumbum import local, LocalPath

log = logging.getLogger(__name__)


def with_sanity(func):
    def _with_sanity(*args, **kwargs):
        if not LocalPath(Dct._iniName).exists():
            log.error("no %s in '%s'" % (Dct._iniName, local.cwd))
            exit(1)

        return func(*args, **kwargs)
    return _with_sanity


class Dct:
    """Normal usage:

    dct trigger <version>

    Advanced usage see:
    https://github.com/google/python-fire/blob/master/doc/using-cli.md
    """
    _iniName = 'dct.ini'

    @with_sanity
    def __init__(self):
        config = ConfigParser()
        config.read(self._iniName)
        dct = config['dct']
        self._package = dct['package']
        self._devpiUser = dct['devpi_user']
        self._devpiIndex = dct['devpi_index']

    def trigger(self, version):
        """Trigger tests by rendering file and pushing changes"""
        self.render(version)
        self.push(version)

    def create(self, package):
        for src in LocalPath('tpl').list():
            tpl = Template(src.read(encoding='utf-8'))


    def render(self, version):
        """only render the files for the trigger."""
        for src in LocalPath('tpl').list():
            tpl = Template(src.read(encoding='utf-8'))
            result = tpl.safe_substitute(
                PACKAGE=self._package, VERSION=version,
                USER=self._devpiUser, DEVPI_INDEX=self._devpiIndex,
                TIMESTAMP=datetime.now().ctime())
            dst = LocalPath(src.name)
            log.info("## rendered %s ##\n%s\n## -> %s ##\n", src, result, dst)
            dst.write(result, encoding='utf-8')

    def push(self, version):
        """only push the changes to origin"""
        git = local['git']
        git('add', '.')
        git('commit', '-m', '%s==%s' % (self._package, version))
        git('push', 'origin', 'master')
        log.info("triggered test by pushing %s", local.cwd)


def main():
    logging.basicConfig(level=logging.INFO)
    fire.Fire(Dct())
