#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import local


@task
def do_pack():
    local("tar -cvzf web_static_$(date +%Y%m%d%H%M%S).tgz web_static/")
