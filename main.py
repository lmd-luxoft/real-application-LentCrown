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
from prettytable import PrettyTable

def displayCLI():
    print("""Options:

touch - create text file
cd - change folder
ls - get file list
cat - get file content
rm - delete file
h - display command list
q - exit
""")

def clear():
    os.system('cls')

def commandline_parser() -> argparse.ArgumentParser:
    """Command line parser.

    Parse port and working directory parameters from command line.

    """
    parser = argparse.ArgumentParser(description='Short argument description')
    parser.add_argument('-p', '--port', dest='port', default=8080, help='port')
    parser.add_argument('-f', '--folder', dest='folder', default=os.getcwd(), help='working directory (absolute or relative path)')
    parser.add_argument('-i', '--init', dest='init', help='initialize database')
    parser.add_argument('-l', '--log', dest='log', default='info', help='specify logger mode')
    parser.add_argument('-s', '--security', dest='sec', help='specify security level to file (default: w+)')
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
    -f --folder - working directory (absolute or relative path, default: current app folder FileServer)
    -i --init - initialize database.
    -h --help - help.

    """
    args = commandline_parser().parse_args()
    log_types={"debug":logging.DEBUG,"info":logging.INFO,"warning":logging.WARNING,"error":logging.ERROR,"critical":logging.CRITICAL}
    logging.basicConfig(level=log_types.get(args.log), filename="main.log", format='%(asctime)s - %(name)s - %(levelname)s : %(message)s')
    logger = logging.getLogger("main")

    logger.info("##############################")
    logger.info("Program started")
    fs = FileService(args.folder)
    clear()
    displayCLI()
    while True:
        action = input(f'{fs.path}>').lower()
        clear()
        try:
            if action == 'touch':
                if not(args.sec):
                    args.sec = "w+"
                content = input("""File content:
""")
                clear()
                dict = fs.create_file(content,args.sec,None)
                table = PrettyTable(['Filename', "Size", "Created", "UserID"])
                table.add_row([dict.get('name'), dict.get('size'), dict.get('create_date'), dict.get('user_id')])
                print(f'File info:\n{table}\nFile content:\n\n{dict.get("content")}\n')
            elif action == 'cd':
                path = input("path>")
                fs.change_dir(path)
                clear()
            elif action == 'ls':
                # list = fs.get_files()
                table = PrettyTable(['Filename', 'Weight', "Created", "Modified"])
                for dict in fs.get_files():
                    table.add_row([dict.get('name'), dict.get('size'), dict.get('create_date'), dict.get('edit_date')])
                print(f'File list:\n{table}\n\n')
            elif action == 'cat':
                filename = input("Filename:")
                clear()
                dict = fs.get_file_data(filename)
                print(f"Content:\n{dict.get('content')}\n\n")
            elif action == 'rm':
                filename = input("Filename:")
                print(f"File {fs.delete_file(filename)} deleted successfully")
            elif action == 'h':
                displayCLI()
            elif action == 'q':
                break
        except Exception as e:
            print(e)
            logger.error(e)
    logger.info("Program finished")

if __name__ == '__main__':
    main()
