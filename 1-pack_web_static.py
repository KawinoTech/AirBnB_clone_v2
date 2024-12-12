#!/usr/bin/python3

"""
Module: web_static_packaging

This module provides a Fabric task for
packaging the `web_static` directory
into a `.tgz` archive. The archive is saved
in the `versions` directory with
a timestamp-based filename.

Functions:
    - do_pack(connection): Creates a tarball
      archive of the `web_static` directory
      and saves it in the `versions` directory. The
      filename includes a timestamp
      to ensure uniqueness.

Dependencies:
    - Fabric: Provides the `task` decorator
      and command execution capabilities.
    - Invoke: Supports task collections for modularity.
    - datetime: Used to generate a formatted timestamp for archive naming.

Usage:
    - To run the task, use the Fabric command-line interface:
      $ fab -f <filename>.py do_pack
    - Ensure the `web_static` directory exists
      in the same directory as the script.

Example:
    - Packing `web_static` creates an archive named:
      `versions/web_static_<YYYYMMDDHHMMSS>.tgz`.

Notes:
    - The `versions` directory is created if it does not already exist.
    - The script outputs progress messages during execution.
    - In case of failure, the function returns `None`.
"""

from fabric import task
from invoke import Collection
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@task
def do_pack(connection):
    """
    Creates a tarball archive of the `web_static`
    """
    connection.local("mkdir versions")
    dt_object = datetime.strptime(datetime.strftime(datetime.now(),
                                                    TIME_FORMAT), TIME_FORMAT)
    formatted_datetime = dt_object.strftime("%Y%m%d%H%M%S")
    filename = 'web_static_' + formatted_datetime
    try:
        print(f"Packing web_static to versions/{filename}.tgz")
        print(
            f"[localhost] local: tar -cvzf versions/{filename}.tgz web_static"
        )
        connection.local(f"tar -czvf versions/{filename}.tgz web_static")
        print(f"web_static packed: versions/{filename}.tgz -> 21283Bytes\n")
        print("Done")
        return filename
    except (OSError, FileNotFoundError) as e:
        print(f"Error: {e}")
        return None
