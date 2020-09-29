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
cd <path> - change folder
ls - get file list
cat <filename> - get file content
rm <filename> - delete file
h - display command list
q - exit
""")

def startFS(folder: str, encode: str):
    if (encode=="on"):
        fs = FileServiceSigned(folder,encode)
    else:
        fs = FileService(folder,encode)
    os.chdir(folder)
    return fs

def init_logger(log_level: str):
    """Funtion that initialise logger

        Args:
            log_level (str): string that contains logger write level

        Returns:
            Logger object
        """
    log_types={"debug":logging.DEBUG,"info":logging.INFO,"warning":logging.WARNING,"error":logging.ERROR,"critical":logging.CRITICAL}
    logging.basicConfig(level=log_types.get(log_level), filename="main.log", format='%(asctime)s - %(name)s - %(levelname)s : %(message)s')
    return logging.getLogger("main")

def start_server(args, logger):
    """Funtion that starts web-server

        Args:
            args: array of parsed command line arguments
            logger: logger object
        """
    app = web.Application()
    handler = Handler(args.folder,args.enc)
    app.add_routes([
        web.get('/', handler.handle),
        web.get('/files/list', handler.get_files),
        web.get('/files',handler.get_file_info),
        web.post('/files',handler.create_file),
        web.delete('/files/{name}',handler.delete_file),
        web.post('/change_file_dir',handler.change_file_dir)
    ])
    web.run_app(app, host='localhost', port=args.port, access_log = logger)

def cmd_Args_Parse():
    """Command line parser.

    Parse port and working directory parameters from command line.

    """
    parser = argparse.ArgumentParser(description='Short argument description')
    parser.add_argument('-p', '--port', dest='port', default=8080, help='port')
    parser.add_argument('-f', '--folder', dest='folder', default=os.getcwd(), help='working directory (absolute or relative path)')
    parser.add_argument('-i', '--init', dest='init', help='initialize database')
    parser.add_argument('-l', '--log', dest='log', default='info', help='specify logger mode')
    parser.add_argument('-s', '--security', dest='sec', help='specify security level to file (default: w+)')
    parser.add_argument('-e', '--encrypt', dest='enc', default='md5', help='disable or enable encryption (default: "on,md5"')
    array = parser.parse_args()
    return array


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
    -l --log - specify logger mode
    -s --security - specify security level to file (default: w+)
    -e --encrypt - disable or enable encryption (default: "on,md5"
    -h --help - help.

    """
    args = cmd_Args_Parse()
    logger = init_logger(args.log)
    start_server(args, logger)
    logger.info("Server started")

if __name__ == '__main__':
    main()
