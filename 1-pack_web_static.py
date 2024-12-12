#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static.

import os
from fabric.api import local
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


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
    filename = 'web_static_' + formatted_datetime

    try:
        print(f"Packing web_static to versions/{filename}.tgz")
        local(f"tar -czvf versions/{filename}.tgz web_static")
        print(f"web_static packed: versions/{filename}.tgz -> {os.path.getsize(f'./versions/{filename}.tgz')} Bytes")

        return filename
    except (OSError, FileNotFoundError) as e:
        print(f"Error: {e}")
        return None
