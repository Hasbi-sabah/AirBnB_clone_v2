#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import *
from datetime import datetime
import os

env.hosts = ["100.27.4.102", "54.165.197.71"]


@task
def deploy():
    """ Fabric script that creates and distributes an archive """
    file_name = do_pack()
    if not os.path.isfile('versions/{}'.format(file_name)):
        return False
    return do_deploy('versions/{}'.format(file_name))


def do_deploy(archive_path):
    """Fabric script that distributes an archive to web servers"""
    if not os.path.isfile(archive_path):
        return False
    with_ext = archive_path.split("/")[-1]
    without_ext = archive_path.split("/")[-1].split(".")[0]
    put(archive_path, "/tmp")
    run("mkdir -p /data/web_static/releases/{}".format(without_ext))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}\
".format(with_ext, without_ext))
    run("rm /tmp/{}".format(with_ext))
    run("mv /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}".format(without_ext, without_ext))
    run("rm -rf /data/web_static/releases/{}/web_static\
".format(without_ext))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ \
/data/web_static/current".format(without_ext))
    return True


@runs_once
def do_pack():
    """generates a .tgz archive from web_static"""
    file_name = "web_static_{}.tgz\
".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    local(
        "mkdir versions ; tar -cvzf \
versions/{} web_static/".format(file_name)
    )
    return file_name
