import sys
from datetime import datetime
from string import Template

import devpy
import fire
from plumbum import local, LocalPath

from release_helper import settings

log = devpy.autolog()


class Runner:
    HERE = LocalPath(__file__).dirname
    ROOT = HERE.up()
    TPL_PATH = HERE / 'tpl'

    def __init__(self, project, version):
        self.project = project
        self.version = version
        self.user = settings.USER
        self.repoName = settings.REPO_NAME
        self.devpiIndex = settings.DEVPI_INDEX
        self.withLogin = settings.WITH_LOGIN
        self.projectPath = LocalPath(settings.PROJECTS_ROOT) / self.project
        self.devpiPackageUrl = "%s/%s/%s" % (
            self.devpiIndex, self.project, self.version)
        log.info("working with:\n%s" % self)

    def __str__(self):
        return '\n'.join(
            ["%s: %s" % (a, getattr(self, a)) for a in dir(self) if
             not a.startswith('_') and not callable(getattr(self, a))])

    def prepare_new_version(self):
        self.render_files()
        self._tag_new_version()
        self._devpi_upload()

    def trigger_tests(self):
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
        for file in self.TPL_PATH.list():
            content = file.read()
            tpl = Template(content)
            dstPath = self.ROOT / file.basename
            renderResult = tpl.safe_substitute(
                PROJECT=self.project, VERSION=self.version,
                USER=settings.USER, DEVPI_INDEX=self.devpiIndex,
                REPO_NAME=self.repoName)
            dstPath.write(renderResult)

    def _tag_new_version(self):
        """set git version tag for the new build"""
        with local.cwd(self.projectPath):
            cmd.git('tag', '-fam', self.version, self.version)

    def _devpi_upload(self):
        """upload new version to devpi"""
        with local.cwd(self.projectPath):
            cmd.devpi('use', self.devpiIndex)
            if self.withLogin:
                cmd.devpi('login', self.user)
            cmd.devpi('upload')
            log.info("uploaded package to %s", self.devpiIndex)

    @staticmethod
    def _write_timestamp(timestamp):
        """Always changing timestamp ensures a new build every time.

        Needed if you want to test a new package with the same version
        """
        LocalPath('TIMESTAMP').write(timestamp)

    def _push_changes(self):
        """If anything in this repo changes, new tests are triggered"""
        timestamp = datetime.now().ctime()
        self._write_timestamp(timestamp)
        cmd.git('add', '.')
        cmd.git('commit', '-m', 'trigger %s==%s (%s)' % (
            self.project, self.version, timestamp))
        cmd.git('push', 'origin', 'master')

    def _set_last_test_info(self):
        pass


class cmd:
    devpi = local['devpi']
    git = local['git']


class Memory:
    path = LocalPath('memory')

    @classmethod
    def get(cls):
        return [e.strip() for e in cls.path.read('utf-8').split()]

    @classmethod
    def set(cls, project, version, which=path):
        which.write(project + "\n" + version, encoding='utf-8')


def read_only_memory(func):
    def _with_memory(self, *args, **kwargs):
        if not hasattr(self, '_runner'):
            log.warning("nothing to work with. Call 'dct set' to get started")
            sys.exit(1)

        log.info("%s==%s", self._runner.project, self._runner.version)
        func(self, *args, **kwargs)
    return _with_memory


class Cli():
    """Little cloud test and release helper thing"""
    def __init__(self):
        try:
            self._runner = Runner(*Memory.get())
        except FileNotFoundError:
            pass

    def set(self, project, version):
        Memory.set(project, version)
        if [project, version] != Memory.get():
            self._runner = Runner(*Memory.get())

    @read_only_memory
    def test(self):
        """Trigger CI tests for configured build"""
        self._runner.trigger_tests()

    @read_only_memory
    def release(self):
        """Release the current build (still a NOP)"""
        self._runner.release()

    @read_only_memory
    def retract(self, radical=False):
        """Retract the build (tag and optional devpi build)"""
        self._runner.retract(radical)

    @read_only_memory
    def render_only(self):
        """Update files from templates only"""
        self._runner.render_files()


def main():
    with local.cwd(LocalPath(__file__).dirname):
        fire.Fire(Cli())
