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
    local("mkdir -p versions")  # Create the directory if it doesn't exist

    dt_object = datetime.strptime(
        datetime.strftime(datetime.now(), TIME_FORMAT), TIME_FORMAT)
    formatted_datetime = dt_object.strftime("%Y%m%d%H%M%S")
    filename = f'web_static_{formatted_datetime}'

    try:
        print(f"Packing web_static to versions/{filename}.tgz")
        local(f"tar -czvf versions/{filename}.tgz web_static")
        file_size = os.path.getsize(f'./versions/{filename}.tgz')
        print(f"web_static packed: versions/{filename}.tgz -> {file_size} Bytes")
        return filename
    except (OSError, FileNotFoundError) as error:
        print(f"Error occurred during packing: {error}")
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
        print(f"Archive not found: {archive_path}")
        return False

    try:
        with settings(user="root"):
            with cd("/tmp"):
                put(archive_path, ".")  # Upload archive to remote server

            filename = os.path.basename(archive_path)
            filename_no_ext = filename.replace(".tgz", "")

            # Unpack the archive and handle it on the remote server
            run(
                f"mkdir -p /data/web_static/releases/{filename_no_ext} && "
                f"tar -xvzf /tmp/{filename} -C "
                f"/data/web_static/releases/{filename_no_ext} "
                f"--strip-components=1"
            )

            # Cleanup and symbolic link
            run(f"rm /tmp/{filename}")
            run(f"rm -rf /data/web_static/current")
            run(f"ln -s /data/web_static/releases/{filename_no_ext} "
                f"/data/web_static/current")

        print("New version deployed successfully")
        return True

    except Exception as error:
        print(f"Deployment failed: {error}")
        return False


def deploy():
    """
    Creates and deploys an archive.
    """
    filename = do_pack()
    if filename:
        archive_path = f'versions/{filename}.tgz'
        return do_deploy(archive_path)
    print("Failed to create archive for deployment")
    return False
