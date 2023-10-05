#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import *
from datetime import datetime
import os

env.hosts = ["100.27.4.102", "54.165.197.71"]


@task
def do_clean(number=0):
    """formats input and cleans remote"""
    n = 1
    if int(number) != 0:
        n = int(number)
    local("ls -dt ./versions/* | head -n -{} | xargs rm -fr".format(n))
    run("ls -dt /data/web_static/releases/* | head -n \
-{} | xargs rm -fr".format(n))
