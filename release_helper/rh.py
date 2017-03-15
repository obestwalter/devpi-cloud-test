import sys
from configparser import ConfigParser
from datetime import datetime
from string import Template

import devpy
import fire
from devpi_common.types import cached_property
from plumbum import local, LocalPath
from plumbum.commands.processes import ProcessExecutionError

log = devpy.autolog(level='DEBUG')


class Runner:
    def __init__(self, version):
        self.version = version
        self._init()

    def __str__(self):
        return '\n'.join(
            ["%s: %s" % (a, getattr(self, a)) for a in dir(self) if
             not a.startswith('_') and not callable(getattr(self, a))])

    def _init(self):
        self.dcttPath = local.cwd
        self.project = self.cnf['project']
        self.user = self.cnf['user']
        self.devpiIndex = self.cnf['devpi_index']
        self.projectPath = LocalPath(self.cnf['root_path']) / self.project
        log.info("working with:\n%s" % self)

    @cached_property
    def cnf(self):
        config = ConfigParser()
        config.read('dctt.ini')
        return config['dctt']

    def prepare(self):
        self.render_files()
        self._tag_new_version()
        self._devpi_upload()

    def devpi_test(self):
        self._push_changes()

    def retract(self, radical):
        """remove tag and remove build from devpi"""
        with local.cwd(self.projectPath):
            cmd.git('tag', '-d', self.version)
            if radical:
                cmd.devpi('remove', '-y', '%s==%s', self.project, self.version)

    def release(self):
        """paranoia level: advanced beginner - not automated ... yet"""
        log.warning("not doing anything - just jogging your memory")
        log.info(
            '\nrelease the package to pypi:\n'
            'cd %s\n'
            'git push upstream %s\n'
            'devpi push %s==%s pypi:pypi',
            self.projectPath, self.version, self.project, self.version)

    def render_files(self):
        for file in (self.dcttPath / 'tpl').list():
            tpl = Template(file.read(encoding='utf-8'))
            renderResult = tpl.safe_substitute(
                PROJECT=self.project, VERSION=self.version,
                USER=self.user, DEVPI_INDEX=self.devpiIndex,
                TIMESTAMP=datetime.now().ctime())
            LocalPath(file.name).write(renderResult, encoding='utf-8')

    def _tag_new_version(self):
        """set git version tag for the new build"""
        with local.cwd(self.projectPath):
            cmd.git('tag', '-fam', self.version, self.version)

    def _devpi_upload(self):
        """upload new version to devpi"""
        with local.cwd(self.projectPath):
            cmd.devpi('use', self.devpiIndex)
            try:
                cmd.devpi('upload')
            except ProcessExecutionError as e:
                if 'devpi login' in e.stdout:
                    log.warning("logging you in to devpi ...")
                    cmd.devpi('login', self.user)
                    cmd.devpi('upload')
            log.info("uploaded package to %s", self.devpiIndex)

    def _push_changes(self):
        """If anything in this repo changes, new tests are triggered"""
        with local.cwd(self.dcttPath):
            cmd.git('add', '.')
            cmd.git('commit', '-m', '%s==%s' % (self.project, self.version))
            cmd.git('push', 'origin', 'master')


class cmd:
    devpi = local['devpi']
    git = local['git']


class Memory:
    path = LocalPath('version')

    @classmethod
    def get(cls):
        return cls.path.read(encoding='utf-8').strip()

    @classmethod
    def set(cls, version):
        cls.path.write(version, encoding='utf-8')


def read_only_memory(func):
    def _with_memory(self, *args, **kwargs):
        if not hasattr(self, '_runner'):
            log.warning("no version. Call 'rh set <version>' first")
            sys.exit(1)

        log.info("%s", self._runner.version)
        func(self, *args, **kwargs)
    return _with_memory


class Cli():
    """Little cloud test and release helper thing"""
    def __init__(self):
        try:
            self._runner = Runner(Memory.get())
        except FileNotFoundError:
            pass

    def set(self, version):
        Memory.set(version)
        if version != Memory.get():
            self._runner = Runner(Memory.get())

    @read_only_memory
    def prepare(self):
        """Trigger CI tests for configured build"""
        self._runner.prepare()

    @read_only_memory
    def test(self):
        """Trigger CI tests for configured build"""
        self._runner.devpi_test()

    @read_only_memory
    def retract(self, radical=False):
        """Retract the build (tag and optional devpi build)"""
        self._runner.retract(radical)

    @read_only_memory
    def release(self):
        """Release the current build (still a NOP)"""
        self._runner.release()


def main():
    fire.Fire(Cli())
