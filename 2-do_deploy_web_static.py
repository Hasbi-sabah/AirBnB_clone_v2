#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import *

env.hosts = ["100.27.4.102", "54.165.197.71"]


@task
def do_deploy(archive_path):
    """Fabric script that distributes an archive to web servers"""
    try:
        with_ext = archive_path.split("/")[-1]
        without_ext = archive_path.split("/")[-1].split(".")[0]
        put(archive_path, "/tmp")
        run("mkdir -p /data/web_static/releases/" + without_ext)
        run("tar -xzf /tmp/{} -C /data/web_static/releases/\
{}".format(with_ext, without_ext))
        run("rm /tmp/{}".format(with_ext))
        run("mv /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}".format(without_ext, without_ext))
        run("rm -rf /data/web_static/releases/{}/web_static\
".format(without_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ \
/data/web_static/current".format(without_ext))
        return True
    except Exception:
        return False


@task
def do_pack():
    """generates a .tgz archive from web_static"""
    local(
        "mkdir versions ; tar -cvzf \
versions/web_static_$(date +%Y%m%d%H%M%S).tgz web_static/"
    )
