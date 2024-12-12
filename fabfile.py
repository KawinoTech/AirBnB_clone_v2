#!/usr/bin/python3
# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

# Import Fabric's API module
from fabric import task

@task
def do_pack(c):
    c.local("echo 'This is a local command'")
    c.local("ls -la")
