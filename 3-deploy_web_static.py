#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import *
from datetime import datetime
import os

env.hosts = ["100.27.4.102", "54.165.197.71"]


@task
def deploy():
    file_name = execute(do_pack)
    print('------------', file_name)
    if not os.path.isfile('versions/' + file_name[env.host]):
        return False
    return execute(do_deploy, 'versions/' + file_name[env.host])


@task
def do_deploy(archive_path):
    """Fabric script that distributes an archive to web servers"""
    if not os.path.isfile(archive_path):
        return False
    with_ext = archive_path.split("/")[-1]
    without_ext = archive_path.split("/")[-1].split(".")[0]
    put(archive_path, "/tmp")
    run("mkdir -p /data/web_static/releases/" + without_ext)
    run(
        "tar -xzf /tmp/"
        + with_ext + " -C /data/web_static/releases/"
        + without_ext
    )
    run("rm /tmp/" + with_ext)
    run(
        "mv /data/web_static/releases/"
        + without_ext
        + "/web_static/* /data/web_static/releases/"
        + without_ext
    )
    run("rm -rf /data/web_static/releases/"
        + without_ext + "/web_static")
    run("rm -rf /data/web_static/current")
    run(
        "ln -s /data/web_static/releases/"
        + without_ext
        + "/ /data/web_static/current"
    )
    return True


@task
def do_pack():
    """generates a .tgz archive from web_static"""
    file_name = "web_static_{}.tgz\
".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    local(
        "mkdir versions ; tar -cvzf \
versions/{} web_static/".format(file_name)
    )
    return file_name
