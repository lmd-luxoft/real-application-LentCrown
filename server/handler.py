# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import json
import os
from aiohttp import web
from queue import Queue
from distutils.util import strtobool
from server.file_service import FileService, FileServiceSigned
from server.file_loader import FileLoader, QueuedLoader
from server.users import UsersAPI
from server.role_model import RoleModel
from server.users_sql import UsersSQLAPI
from server.role_model_sql import RoleModelSQL


def startFS(folder: str, encryption: str):
    encode = encryption.split(",")
    if (encode[0]=="on"):
        fs = FileServiceSigned(folder,encode[1])
    else:
        fs = FileService(folder,encode[1])
    os.chdir(folder)
    return fs

class Handler():
    """Aiohttp handler with coroutines.

    """

    def __init__(self, path: str, encryption: list):
        self._fs = startFS(path,encryption)

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.

        """
        return web.Response(text="OK",status=200)

    #@UsersAPI.authorized
    #@RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        """
        try:
            list = self._fs.get_files()
            status = 200
            response = {'state':'success','description':'File retrieval OK', "file_list": list}
        except Exception as e:
            status = 500
            response = {'state':'error','description':e}
        return web.Response(content_type="json",status=status,text=json.dumps(response))

    #@UsersAPI.authorized
    #@RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def get_file_info(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting full info about file in working directory.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """
        filename = request.rel_url.query["name"]
        try:
            file_info = self._fs.get_file_data(filename)
            status = 200
            response = {'state':'success','description':'File deletion OK', "data": file_info}
        except Exception as e:
            status = 400
            response = {'state':'error','description':e} 
        return web.Response(content_type="json",status=status,text=json.dumps(response))

    #@UsersAPI.authorized
    #@RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def create_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for creating file.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "content": "string. Content string. Optional",
                "security_level": "string. Security level. Optional. Default: low",
                "is_signed": "boolean. Sign or not created file. Optional. Default: false"
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """
        content = await request.content.read()
        content = content.decode("utf-8")
        directory = json.loads(content)
        try:
            if (directory.get("is_signed")=='false' and self._fs.__class__.__name__=="FileServiceSigned"):
                pass
            elif (directory.get("is_signed")=='true' and self._fs.__class__.__name__=="FileService"):
                pass
            else:
                file_info = self._fs.create_file(directory.get("content"),directory.get("security_level"),None)
            status = 200
            response = {'state':'success','description':'file created OK', "file_info": file_info}
        except Exception as e:
            status = 400
            response = {'state':'error','description':e}
        return web.Response(content_type="json",status=status, text=json.dumps(response))


    #@UsersAPI.authorized
    #@RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def delete_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting file.

        Args:
            request (Request): aiohttp request, contains filename.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """
        filename = request.rel_url.name
        try:
            self._fs.delete_file(filename)
            status = 200
            response = {'state':'success','description':'File deletion OK'}
        except Exception as e:
            status = 400
            response = {'state':'error','description':e} 
        return web.Response(content_type="json",status=status,text=json.dumps(response))

    #@UsersAPI.authorized
    #@RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def download_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for downloading files from working directory via threads.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    #@UsersAPI.authorized
    #@RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def download_file_queued(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for downloading files from working directory via queue.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    async def signup(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for signing up user.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "name": "string. User's first name. Required"
                "surname": "string. User's last name. Optional"
                "email": "string. User's email. Required",
                "password": "string. Required letters and numbers. Quantity of symbols > 8 and < 50. Required",
                "confirm_password": "string. Must match with password. Required"
            }.

        Returns:
            Response: JSON response with success status or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    async def signin(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for signing in user.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "email": "string. User's email. Required",
                "password": "string. User's password. Required",
            }.

        Returns:
            Response: JSON response with success status, success message user's session UUID or error status and error
            message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    async def logout(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for logout.

        Args:
            request (Request): aiohttp request, contains session_id.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPUnauthorized: 401 HTTP error, if user session is expired or not found.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def add_method(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for adding method into role model.

        Args:
            request (Request): aiohttp request, contains method name.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def delete_method(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting method from role model.

        Args:
            request (Request): aiohttp request, contains method name.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def add_role(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for adding role into role method.

        Args:
            request (Request): aiohttp request, contains role name.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def delete_role(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting role from role method.

        Args:
            request (Request): aiohttp request, contains role name.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def add_method_to_role(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for adding method to role.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "method": "string. Method name. Required",
                "role": "string. Role name. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def delete_method_from_role(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting method from role.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "method": "string. Method name. Required",
                "role": "string. Role name. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def change_shared_prop(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for changing shared property of method.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "method": "string. Method name. Required",
                "value": "boolean. Value of shared property. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    @UsersAPI.authorized
    @RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def change_user_role(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for setting new role to user.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "email": "string. User's email. Required",
                "role": "string. Role name. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        pass

    #@UsersAPI.authorized
    #@RoleModel.role_model
    # @UsersSQLAPI.authorized
    # @RoleModelSQL.role_model
    async def change_file_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for changing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """
        content = await request.content.read()
        content = content.decode("utf-8")
        directory = json.loads(content)
        try:
            self._fs.change_dir(directory.get("path"))
            status = 200
            response = {'state':'success','description':'directory changed', "path": directory}
        except Exception as e:
            status = 400
            response = {'state':'error','description':e}
        return web.Response(content_type="json",status=status, text=json.dumps(response))
