import logging
from configparser import ConfigParser
from datetime import datetime
from string import Template

import fire
from plumbum import local, LocalPath

log = logging.getLogger(__name__)
git = local['git']
config = None


class Config:
    rel_ini_path = LocalPath('dct.ini')

    def __init__(self):
        config = ConfigParser()
        config.read(self.rel_ini_path)
        dct = config['dct']
        if not all(dct.values()):
            log.error('please complete the settings in %s', self.rel_ini_path)
            exit(1)

        self.package = dct['package']
        self.devpi_user = dct['devpi_user']
        self.devpi_index = dct['devpi_index']

    @classmethod
    def necessary(cls, func):
        def _necessary(*args, **kwargs):
            if not cls.rel_ini_path.exists():
                log.error("no %s in '%s'" % (cls.rel_ini_path, local.cwd))
                exit(1)

            return func(*args, **kwargs)
        return _necessary


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
        self._render_files(version)
        self._git_push(version)

    def create(self, package, devpi_user='', devpi_index=''):
        parent = local.cwd / ('devpi-cloud-test-' + package)
        if parent.exists():
            log.error("%s already exists - aborting", parent)
            exit(1)

        log.info("create new cloud test in %s", parent)
        try:
            blueprint_path = LocalPath(__file__).dirname / 'blueprint'
            blueprint_path.copy(parent)
            with local.cwd(parent):
                self.__render(Config.rel_ini_path,
                              PACKAGE=package, DEVPI_USER=devpi_user,
                              DEVPI_INDEX=devpi_index)
            self._init_repository(parent)
        except Exception:
            log.exception("creation failed")
            parent.delete()
            exit(1)

    @Config.necessary
    def _render_files(self, version):
        """only render the files for the trigger."""
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

    @Config.necessary
    def _git_push(self, version):
        """only push the changes to origin"""
        self._git_commit('%s==%s' % (config.package, version))
        git('push', 'origin', 'master')
        log.info("triggered test by pushing %s", local.cwd)

    def _init_repository(self, parent):
        with local.cwd(parent):
            git('init')
            self._git_commit('init')
            log.info("initialized. You can add your remote and push.")

    def _git_commit(self, msg):
        git('add', '.')
        git('commit', '-m', msg)


def main():
    logging.basicConfig(level=logging.DEBUG)
    global config
    config = Config()
    fire.Fire(Dct())
