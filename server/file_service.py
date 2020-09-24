# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import os
import typing
#import server.utils as utils
from collections import OrderedDict
from server.crypto import BaseCipher, AESCipher, RSACipher, HashAPI
import platform
import time
import string
import random
import sys


class FileService:
    """Singleton class with methods for working with file system.

    """
    # def __new__(cls, *args, **kwargs):
    #     pass 

    def __init__(self, path: str):
        self.__path = path

    def __call__(self, cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(FileService, cls).__call__(*args, **kwargs)
            return cls.__instance

    @property
    def path(self) -> str:
        """Working directory path getter.

        Returns:
            Str with working directory path.

        """
        return self.__path

    @path.setter
    def path(self, value: str):
        """Working directory path setter.

        Args:
            value (str): Working directory path.

        """
        self.__path=value

    @staticmethod
    def change_dir(path: str):
        """Change current directory of app.

        Args:
            path (str): Path to working directory with files.

        Raises:
            AssertionError: if directory does not exist.

        """
        if not(os.path.isdir(path)):
            raise AssertionError("directory does not exist")
        else:
            os.chdir(path)

    def get_file_data(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.

        """
        filename = os.getcwd() + "\\" + filename + ".txt"
        if not(os.path.isfile(filename)):
            raise AssertionError("File does not exist or filename format is invalid")
        else:
            try:
                with open(filename, "r") as file:
                    data = file.read()
            except ValueError:
                raise ValueError("Security level is invalid")
            file_info=dict(name=os.path.relpath(filename),content=data,create_date=time.ctime(os.path.getctime(filename)),edit_date=time.ctime(os.path.getmtime(filename)),size=os.path.getsize(filename),user_id=user_id)
        return file_info

    async def get_file_data_async(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file. Asynchronous version.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.

        """
        pass

    def get_files(self) -> typing.List[typing.Dict[str, str]]:
        """Get info about all files in working directory.

        Returns:
            List of dicts, which contains info about each file. Keys:
                name (str): name of file with .txt extension.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (str): size of file in bytes.

        """
        file_list_info=[]
        files = [file for file in os.listdir(os.getcwd()) if os.path.isfile(file)]
        for file in files:
            file = dict(name=file,create_date=time.ctime(os.path.getctime(file)),edit_date=time.ctime(os.path.getmtime(file)),size=os.path.getsize(file))
            file_list_info.append(file)
        return file_list_info

    async def create_file(
            self, content: str = None, security_level: str = None, user_id: int = None) -> typing.Dict[str, str]:
        """Create new .txt file.

        Method generates name of file from random string with digits and latin letters.

        Args:
            content (str): String with file content,
            security_level (str): String with security level,
            user_id (int): User Id.

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
        modes=[
        "r", #read-only
        "rb", #read-only binary
        "r+", #reading/writing
        "w", #write-only
        "wb", #write-only binary
        "w+", #writing/reading
        "wb+", #writing/reading binary
        "a", #appending
        "ab", #appending binary
        "a+", #appending/reading
        "ab+" #appending/reading binary
        ]
        if not(security_level in modes):
            raise ValueError("Security level is invalid")
        filename = os.getcwd() + "\\" + ''.join(random.choice(string.ascii_letters) for i in range(15)) + ".txt"
        with open(filename, security_level) as file:
            file.write(content)
        file_info=dict(name=os.path.relpath(filename),content=content,create_date=time.ctime(os.path.getctime(filename)),size=os.path.getsize(filename),user_id=user_id)
        return file_info

    def delete_file(self, filename: str):
        """Delete file.

        Args:
            filename (str): Filename without .txt file extension.

        Returns:
            Str with filename with .txt file extension.

        Raises:
            AssertionError: if file does not exist.

        """
        filename = os.getcwd() + "\\" + filename + ".txt"
        if not(os.access(filename,os.F_OK)):
            raise AssertionError("File does not exist")
        else:
            os.remove(filename)
        return os.path.relpath(filename)

class FileServiceSigned(FileService):
    """Singleton class with methods for working with file system and file signatures.

    """

    def get_file_data(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid, signatures are not match,
            signature file does not exist,
            ValueError: if security level is invalid.

        """

        pass

    async def get_file_data_async(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file. Asynchronous version.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid, signatures are not match,
            signature file does not exist,
            ValueError: if security level is invalid.

        """

        pass

    async def create_file(
            self, content: str = None, security_level: str = None, user_id: int = None) -> typing.Dict[str, str]:
        """Create new .txt file with signature file.

        Method generates name of file from random string with digits and latin letters.

        Args:
            content (str): String with file content,
            security_level (str): String with security level,
            user_id (int): User Id.

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
