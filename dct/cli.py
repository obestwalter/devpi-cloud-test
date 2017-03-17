import logging
from configparser import ConfigParser
from datetime import datetime
from string import Template

import fire
from plumbum import local, LocalPath

log = logging.getLogger(__name__)


class Config:
    rel_ini_path = LocalPath('dct.ini')

    def __init__(self):
        config = ConfigParser()
        config.read(self.rel_ini_path)
        dct = config['dct']
        self.package = dct['package']
        self.devpi_user = dct['devpi_user']
        self.devpi_index = dct['devpi_index']


# TODO Use `from plumbum.cli import Application` for cli
class Dct:
    """Normal usage:

    dct trigger <version>

    Advanced usage see:
    https://github.com/google/python-fire/blob/master/doc/using-cli.md
    """
    _tpl_path = LocalPath('tpl')

    def trigger(self, version):
        """Trigger tests by rendering file and pushing changes"""
        self._render(version)
        self._push(version)

    def create(self, package, devpi_user='', devpi_index=''):
        parent = local.cwd / ('devpi-cloud-test-' + package)
        if parent.exists():
            log.error("%s already exists - aborting", parent)
            exit(1)

        log.info("create new cloud test in %s", parent)
        try:
            blueprint_path = LocalPath(__file__).dirname.up() / 'blueprint'
            blueprint_path.copy(parent)
            with local.cwd(parent):
                self.__render(Config.rel_ini_path,
                              PACKAGE=package, DEVPI_USER=devpi_user,
                              DEVPI_INDEX=devpi_index)
        except Exception:
            log.exception("creation failed")
            parent.delete()
            exit(1)

        if not all((devpi_user, devpi_index)):
            log.warning("not all options set, please add later in dct.ini")

    def _render(self, version):
        """only render the files for the trigger."""
        config = Config()
        for src in LocalPath('tpl').list():
            self.__render(
                src, PACKAGE=config.package, VERSION=version,
                DEVPI_USER=config.devpi_user, DEVPI_INDEX=config.devpi_index,
                TIMESTAMP=datetime.now().ctime())

    @staticmethod
    def __render(path, **kwargs):
        tpl = Template(path.read(encoding='utf-8'))
        result = tpl.safe_substitute(**kwargs)
        dst = LocalPath(path.name)
        log.info("## rendered %s ##\n%s\n## -> %s ##\n", path, result, dst)
        dst.write(result, encoding='utf-8')

    def _push(self, version):
        """only push the changes to origin"""
        git = local['git']
        git('add', '.')
        git('commit', '-m', '%s==%s' % (Config().package, version))
        git('push', 'origin', 'master')
        log.info("triggered test by pushing %s", local.cwd)


def main():
    logging.basicConfig(level=logging.INFO)
    fire.Fire(Dct())
