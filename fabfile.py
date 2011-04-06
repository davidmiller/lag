"""
Fabric functions for Sysadmin and Ops
"""
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['david@larapel.com']

def apache_reload():
    """
    Get the apache status from all machines
    """
    sudo("/etc/init.d/apache2 restart")

def celery_reload():
    """
    Reload our celery stuff
    """
    sudo("/etc/init.d/celeryd restart")
    sudo("/etc/init.d/celerybeat restart")

def buildout():
    """
    Re - run the buildout
    """
    with cd("/home/web/lag"):
        run("./bin/buildout")

def restart_app():
    """
    Restart all the app components
    """
    apache_reload()

def pull_new_changes():
    """
    Get the new changes and then mv them to the app directory
    """
    with cd("/home/web/lag"):
        run("git pull origin master")

def syncdb():
    "run syncdb"
    with cd("/home/web/lag"):
        run("./bin/django syncdb")

def deploy():
    """
    Deploy most recent changes to application
    """
    pull_new_changes()
    buildout()
    restart_app()


