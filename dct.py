from configparser import ConfigParser
from datetime import datetime
from string import Template

import devpy
import fire
from plumbum import local, LocalPath

log = devpy.autolog(level='DEBUG', log_filename=False)


class Dct:
    def __init__(self):
        config = ConfigParser()
        config.read('dct.ini')
        dct = config['dct']
        self._package = dct['package']
        self._devpiUser = dct['devpi_user']
        self._devpiIndex = dct['devpi_index']

    def __str__(self):
        return ' | '.join(
            ["%s: %s" % (a, getattr(self, a)) for a in dir(self) if
             not a.startswith('_') and not callable(getattr(self, a))])

    def trigger(self, version):
        self._render_files(version)
        self._push_repo(version)

    def _render_files(self, version):
        for src in LocalPath('tpl').list():
            tpl = Template(src.read(encoding='utf-8'))
            result = tpl.safe_substitute(
                PACKAGE=self._package, VERSION=version,
                USER=self._devpiUser, DEVPI_INDEX=self._devpiIndex,
                TIMESTAMP=datetime.now().ctime())
            dst = LocalPath(src.name)
            log.debug("## rendered %s ##\n%s\n## -> %s ##\n", src, result, dst)
            dst.write(result, encoding='utf-8')

    def _push_repo(self, version):
        git = local['git']
        git('add', '.')
        git('commit', '-m', '%s==%s' % (self._package, version))
        git('push', 'origin', 'master')
        log.info("triggered test by pushing %s", local.cwd)


def main():
    fire.Fire(Dct())
