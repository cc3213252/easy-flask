# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'

import os
import json

from fabric.api import (
    lcd,
    cd,
    env,
    local,
    run,
    task,
    put,
)

from fabric.contrib.files import exists


PYPI_ADDR = os.environ.get("PYPI_INDEX", "http://mirrors.aliyun.com/pypi/simple/")
PYPI_TRUST = os.environ.get("PYPI_TRUST", "mirrors.aliyun.com")
FIX_PIP_VERSION = "7.1.2"

# fix env settings
env.use_ssh_config = True
env.keepalive = 60

env.deploying_commit = local('git rev-parse HEAD', capture=True)


def notify_print(msg):
    print("#" * 42)
    print(msg)
    print("#" * 42)


def python_deploy(app_name, local_dir, remote_dir,
                  virtualenv, stop_service_cmd="true", validate_cmd="true",
                  start_service_cmd="true"):

    remote_deploy_dir = remote_dir + ".deploy/"
    remote_old_dir = remote_dir + ".old/"

    if exists(remote_deploy_dir):
        run("rm -rf {}".format(remote_deploy_dir))
    if exists(remote_old_dir):
        run("rm -rf {}".format(remote_old_dir))

    _copy_source(local_git_dir=local_dir, remote_deploy_dir=remote_deploy_dir, app_name=app_name)

    # make sure virtualenv exists
    if not exists(virtualenv):
        _virtualenv_init(virtualenv)

    _virtualenv_install(virtualenv, remote_deploy_dir)

    notify_print("stoping service")
    with cd(remote_deploy_dir):
        run(stop_service_cmd)

    notify_print("moving directory")
    if exists(remote_dir):
        run("mv {} {}".format(remote_dir, remote_old_dir))
    run("mv {} {}".format(remote_deploy_dir, remote_dir))

    # start service
    notify_print("starting service")
    with cd(remote_dir):
        run(start_service_cmd)

    # validate
    notify_print("validating service")
    with cd(remote_dir):
        run(validate_cmd)

    # remove old version
    if exists(remote_old_dir):
        if exists(os.path.join(remote_old_dir, "git_version")):
            notify_print("old git version: " + run("cat {}".format(os.path.join(remote_old_dir, "git_version"))))
        notify_print("removing old dir")
        run("rm -rf {}/".format(remote_old_dir))


def _copy_source(local_git_dir, remote_deploy_dir, app_name):
    notify_print("copying source code")
    git_version = local("git rev-parse HEAD", capture=True)
    archive_name = '{}.tar.gz'.format(app_name)
    with lcd(local_git_dir):
        local("git archive -o {} HEAD".format(archive_name))
        run("mkdir -p {}".format(remote_deploy_dir))
        put(os.path.join(local_git_dir, archive_name), remote_deploy_dir)
        with cd(remote_deploy_dir):
            run("tar -xavf {}".format(archive_name))
            run("echo {} > git_version".format(git_version))
            run("rm {}".format(archive_name))
        local("rm {}".format(archive_name))


def _virtualenv_install(virtualenv, remote_dir):
    notify_print("pip installing")
    run("{}/bin/pip install -i {} -r {}/requirements.txt --trusted-host={}".format(virtualenv, PYPI_ADDR,
                                                                                   remote_dir, PYPI_TRUST))


def _virtualenv_init(virtualenv):
    notify_print("virtualenv initing")
    run("virtualenv {}".format(virtualenv))
    run("{0}/bin/pip install -i {1} -q -U distribute pip --trusted-host={}".format(
        virtualenv, PYPI_ADDR, PYPI_TRUST))


@task
def dev():
    with open("appspec.json") as in_:
        appspec = json.load(in_)
    env.hosts = appspec['dev-hosts']


@task
def pro():
    with open("appspec.json") as in_:
        appspec = json.load(in_)
    env.hosts = appspec['pro-hosts']


@task
def deploy():
    with open("appspec.json") as in_:
        appspec = json.load(in_)
    python_deploy(app_name=appspec['app_name'], local_dir=os.getcwd(), remote_dir=appspec['remote_dir'],
                  virtualenv=appspec['virtualenv'], stop_service_cmd=appspec['stop_service_cmd'],
                  validate_cmd=appspec['validate_service_cmd'], start_service_cmd=appspec['start_service_cmd'])
