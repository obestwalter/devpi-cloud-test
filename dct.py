import logging
import os
import sys
from datetime import datetime
from string import Template

import fire
from plumbum import local, LocalPath

import settings

log = logging.getLogger('DCT')


class Runner:
    def __init__(self, project, version):
        self.project = project
        self.version = version
        self.user = settings.USER
        self.repoName = settings.REPO_NAME
        self.devpiIndex = settings.DEVPI_INDEX
        self.withLogin = settings.WITH_LOGIN
        self.projectPath = LocalPath(settings.PROJECTS_ROOT) / self.project
        self.devpiPackageUrl = "%s/%s/%s" % (
            self.project, self.version, self.devpiIndex)

    def prepare_new_version(self):
        self.render_files()
        self._tag_new_version()
        self._devpi_upload()

    def trigger_tests(self):
        self._push_changes()

    def retract(self):
        """remove tag and remove build from devpi"""
        with local.cwd(self.projectPath):
            cmd.git('tag', '-d', self.version)
            cmd.devpi('remove', '-y', '%s==%s', self.project, self.version)

    def release(self):
        """paranoia level: advanced beginner - not automated ... yet"""
        log.info(
            '\nrelease the package to pypi:\n'
            'cd %s\n'
            'git push upstream %s\n'
            'devpi push %s==%s pypi:pypi',
            self.projectPath, self.version, self.project, self.version)

    def render_files(self):
        for file in os.listdir('tpl'):
            with open(os.path.join('tpl', file)) as tpl:
                tpl = Template(tpl.read())
            with open(file, 'w') as result:
                result.write(tpl.safe_substitute(
                    PROJECT=self.project, VERSION=self.version,
                    DEVPI_INDEX=self.devpiIndex, REPO_NAME=self.repoName))

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
        timestamp = datetime.now().isoformat()
        self._write_timestamp(timestamp)
        cmd.git('add', '.')
        cmd.git('commit', '-m', '"trigger %s==%s at %s"' % (
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
        if not cls.path.exists():
            log.error("no current test set")
            sys.exit(1)

        memory = [e.strip() for e in cls.path.read('utf-8').split()]
        log.info("working with %s", memory)
        return memory

    @classmethod
    def set(cls, project, version, which=path):
        which.write(project + "\n" + version, encoding='utf-8')


class Cli:
    """Little cloud test and release helper thing"""

    def set(self, project, version):
        Memory.set(project, version)

    def info(self):
        """Show which build is configured"""
        Memory.get()

    def test(self):
        """Trigger CI tests for configured build"""
        runner = Runner(*Memory.get())
        runner.trigger_tests()

    def release(self):
        """Release the current build (still a NOP)"""
        runner = Runner(*Memory.get())
        runner.release()

    def retract(self):
        """Release the current build (still a NOP)"""
        runner = Runner(*Memory.get())
        runner.retract()

    def render_only(self):
        """Update files from templates only"""
        runner = Runner(*Memory.get())
        runner.render_files()


def main():
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(Cli)

if __name__ == '__main__':
    sys.exit(main)
