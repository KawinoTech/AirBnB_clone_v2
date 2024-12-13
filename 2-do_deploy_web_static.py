#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static.

import os
from datetime import datetime

from fabric.api import run, put, settings, cd, local, env

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

env.hosts = ['ubuntu@54.173.70.151', 'ubuntu@18.207.236.53']


def do_pack():
    """
    Creates a tarball archive of the `web_static` directory and stores it
    in the `versions` folder. The filename includes a timestamp for uniqueness.

    Returns:
        str: The name of the created archive, or None if an error occurs.
    """
    local("mkdir -p versions")  # Creates the directory if it doesn't exist

    dt_object = datetime.strptime(datetime.strftime(datetime.now(), TIME_FORMAT), TIME_FORMAT)
    formatted_datetime = dt_object.strftime("%Y%m%d%H%M%S")
    filename = f'web_static_{formatted_datetime}'

    try:
        print(f"Packing web_static to versions/{filename}.tgz")
        local(f"tar -czvf versions/{filename}.tgz web_static")
        print(f"web_static packed: versions/{filename}.tgz -> {os.path.getsize(f'./versions/{filename}.tgz')} Bytes")

        return filename
    except (OSError, FileNotFoundError) as e:
        print(f"Error: {e}")
        return None


def do_deploy(archive_path):
    """
    Deploys the specified archive to the server and sets up the symbolic
    link for the current web_static directory.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        with settings(user="root"):
            with cd("/tmp"):
                put(archive_path, ".")

            filename = os.path.basename(archive_path)
            filename_no_extension = filename.replace(".tgz", "")

            run(f"mkdir -p /data/web_static/releases/{filename_no_extension} "
                f"&& tar -xvzf /tmp/{filename} -C /data/web_static/releases/{filename_no_extension} "
                f"--strip-components=1")

            run(f"rm /tmp/{filename}")
            run(f"rm /data/web_static/current")
            run(f"ln -s /data/web_static/releases/{filename_no_extension} /data/web_static/current")

        print("New version deployed")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
