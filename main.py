# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import argparse
import os
import sys
import logging
import json
from aiohttp import web
from server.handler import Handler
#from server.database import DataBase
from server.file_service import FileService, FileServiceSigned
import server.file_service_no_class as FileServiceNoClass
from prettytable import PrettyTable

def commandline_parser() -> argparse.ArgumentParser:
    """Command line parser.

    Parse port and working directory parameters from command line.

    """
    parser = argparse.ArgumentParser(description='Short argument description')
    parser.add_argument('-p', '--port', dest='port', default=8080, help='port')
    parser.add_argument('-f', '--folder', dest='folder', help='working directory (absolute or relative path)')
    parser.add_argument('-i', '--init', dest='init', help='initialize database')
    parser.add_argument('-l', '--log', dest='log', help='logger mode')
    return parser


def get_file_data(path):
    """Get full info about file.

    Args:
        path (str): Working directory path.

    Returns:
        Dict, which contains full info about file. Keys:
            name (str): name of file with .txt extension.
            content (str): file content.
            create_date (str): date of file creation.
            edit_date (str): date of last file modification.
            size (int): size of file in bytes.

    Raises:
        AssertionError: if file does not exist, filename format is invalid,
        ValueError: if security level is invalid.

    """

    pass


def create_file(path):
    """Create new .txt file.

    Method generates name of file from random string with digits and latin letters.

    Args:
        path (str): Working directory path.

    Returns:
        Dict, which contains name of created file. Keys:
            name (str): name of file with .txt extension.
            content (str): file content.
            create_date (str): date of file creation.
            size (int): size of file in bytes,
            user_id (int): user Id.

    Raises:
        AssertionError: if user_id is not set,
        ValueError: if security level is invalid.

    """

    pass


def delete_file(path):
    """Delete file.

    Args:
        path (str): Working directory path.

    Returns:
        Str with filename with .txt file extension.

    Raises:
        AssertionError: if file does not exist.

    """

    pass


def change_dir(path):
    """Change working directory.

    Args:
        path (str): Working directory path.

    Returns:
        Str with successfully result.

    """

    pass


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.
    Command line options:
    -p --port - port (default: 8080).
    -f --folder - working directory (absolute or relative path, default: current app folder FileServer).
    -i --init - initialize database.
    -h --help - help.

    """
    logging.basicConfig(filename="main.log", level=logging.INFO)
    logging.info("Program started")
    args = commandline_parser().parse_args()
    FileServiceNoClass.change_dir(args.folder)
    while True:
        if (args.folder):
            action = input("""Options:
c - create text file
ch - change folder
l - get file list
g - get file content
d - delete file
q - exit
Action:""").lower()
            try:
                if action == 'c':
                    security_level = input("""SecLvl:
""")
                    if not(security_level):
                        security_level = "w+"
                    content = input("""Content:
""")
                    dict = FileServiceNoClass.create_file(content,security_level)
                    table = PrettyTable(['Filename', "Size", "Created", "UserID"])
                    table.add_row([dict.get('name'), dict.get('size'), dict.get('create_date'), dict.get('user_id')])
                    print(table)
                    print(dict.get('content'))
                elif action == 'ch':
                    path = input("""New directory path:
""")
                    FileServiceNoClass.change_dir(path)
                elif action == 'l':
                    table = PrettyTable(['Filename', 'Weight', "Created", "Modified"])
                    for dict in FileServiceNoClass.get_files():
                        table.add_row([dict.get('name'), dict.get('size'), dict.get('create_date'), dict.get('edit_date')])
                    print(table)
                elif action == 'g':
                    filename = input("""Filename:
""")
                    dict = FileServiceNoClass.get_file_data(filename)
                    print("Content:")
                    print(f"{dict.get('content')}")
                elif action == 'd':
                    filename = input("""Filename:
""")
                    print(f"File {FileServiceNoClass.delete_file(filename)} deleted successfully")
                elif action == 'q':
                    break
            except Exception as e:
                print(e)

if __name__ == '__main__':
    main()
