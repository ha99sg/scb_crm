import json
from typing import Dict, Union
from urllib.parse import urlparse

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE_IDM


class ServiceIDM:
    def __init__(self, init_service):
        self.session = None
        self.HOST = init_service['idm']['host']
        self.headers = init_service['idm']['headers']
        self.cdn = {
            'thumb': '/cdn-profile/thumb',
            'avatar': '/cdn-profile',
        }

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()

    @staticmethod
    async def response_service(response):
        if response.status == status.HTTP_200_OK:
            return True, await response.json()
        if status.HTTP_400_BAD_REQUEST <= response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
            return False, await response.json()
        return False, {
            "message": ERROR_CALL_SERVICE_IDM,
            "detail": "STATUS " + str(response.status)
        }

    def replace_with_cdn(self, file_url: str, avatar_type: str = 'thumb') -> str:
        file_url_parse_result = urlparse(file_url)

        if file_url_parse_result.netloc and file_url_parse_result.scheme:
            file_url = file_url.replace(f'{file_url_parse_result.scheme}://{file_url_parse_result.netloc}{self.cdn["avatar"]}', self.cdn[avatar_type])
        elif self.cdn:
            # Thay thế link tải file từ service bằng CDN config theo dự án
            file_url = self.cdn.get(avatar_type) + file_url if file_url.startswith('/') else self.cdn.get(avatar_type) + '/' + file_url
        return file_url

    async def login(self, username, password) -> (bool, Union[str, Dict]):
        """
        Input: username,password, app_code từ login của CRM
        Output: Thông tin user từ IDM
        """
        headers = self.headers
        path = "/api/v1/staff/login"
        url = f'{self.HOST}{path}'

        data_user_login = {
            "username": username,
            "password": password,
            "app_code": SERVICE["idm"]['service_name']
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method='post',
                        url=url,
                        data=json.dumps(data_user_login),
                        headers=headers,
                        verify_ssl=False
                ) as response:
                    logger.log("SERVICE", f"[LOGIN] {response.status} : {url}")
                    return await self.response_service(response)
        except Exception as ex:
            logger.exception(ex)
            return False, {"message": str(ex)}

    async def check_token(self, username, bearer_token) -> (bool, Union[str, Dict]):
        """
        Input: username,token, app_code từ login của CRM
        Output: Thông tin user từ IDM
        """
        headers = self.headers
        path = "/api/v1/staff/check_token"
        url = f'{self.HOST}{path}'

        body = {
            "username": username,
            "token": bearer_token,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method='post',
                        url=url,
                        data=json.dumps(body),
                        headers=headers
                ) as response:
                    logger.log("SERVICE", f"[CHECK TOKEN] {response.status} : {url}")
                    return await self.response_service(response)

        except Exception as ex:
            logger.exception(ex)
            return False, {"message": str(ex)}

    async def banner_list(self):
        """
        Input: app_code từ login của CRM
        Output: Thông tin banner từ IDM
        """
        headers = self.headers
        path = "/api/v1/staff/banner_list"
        url = f'{self.HOST}{path}'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method='get',
                        url=url,
                        params={'app_code': SERVICE["idm"]['service_name']},
                        headers=headers,
                        verify_ssl=False
                ) as response:
                    logger.log("SERVICE", f"[BANNER] {response.status} : {url}")
                    return await self.response_service(response)

        except Exception as ex:
            logger.exception(ex)
            return False, {"message": str(ex)}
