#!/usr/bin/python3
# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

# Import Fabric's API module
from fabric import task

@task
def hostname(c, branch="main"):
    c.run(f"hostname")
    c.run("pwd")

@task
def update(c):
    c.sudo("apt update")
    c.get("ps aux")