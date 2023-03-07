import math

import requests

from app.working_with_report_file import create_report


class VkontakteApp:
    VK_APP_ID = '51571106'  # идентификатор приложения.
    VK_API_VERSION = '5.131'  # версия API VK.
    SCHEME = 'https'
    AUTHORITY = 'oauth.vk.com'
    REDIRECT_URI = "http://127.0.0.1:8000/auth/"
    VK_METHOD_AUTHORIZE = 'authorize'
    VK_API_METHOD_GET_FRIENDS = 'friends.get'
    VK_API_METHOD_ACCESS_TOKEN = 'access_token'
    # url = "https://api.vk.com/method/<METHOD>?<PARAM>&<PARAM>"
    MAX_FRIENDS_AMOUNT_IN_RESPONSE = 5000

    def link_to_generate_code_or_token(self, response_type: str,
                                       redirect_uri: str | None = REDIRECT_URI, display: str = 'page',
                                       scope: tuple = ('friends', 'offline'), revoke: str | int = 1):
        # display: page - тип отображения страницы авторизации.
        # scope - настройки доступа приложения. Перечисляются через запятую.
        # friends - получение доступа к друзьям;
        # offline - получение доступа к данным пользователя, даже если он не в сети.
        # Если указать scope=offline, при response_type = 'token', то access_token будет бессрочный.
        # response_type = 'token' или 'code'
        # revoke - параметр, указывающий, что необходимо не пропускать этап подтверждения прав,
        # даже если пользователь уже авторизован.
        # 0 - пропустить повторное подтверждение; 1 - всегда запрашивать подтверждение.
        redirect_uri = f'redirect_uri={redirect_uri}&' if redirect_uri is not None else ''
        generate_code_link = f'{self.SCHEME}://{self.AUTHORITY}/{self.VK_METHOD_AUTHORIZE}?' \
                             f'client_id={self.VK_APP_ID}&' \
                             f'{redirect_uri}' \
                             f'display={display}&' \
                             f'scope={",".join(scope)}&' \
                             f'response_type={response_type}&' \
                             f'revoke={revoke}&' \
                             f'v={self.VK_API_VERSION}'
        return generate_code_link

    # может быть задействован при реализации клиент-серверного приложения
    # @staticmethod
    # def link_to_get_access_token(code: str, path: str = "access_token", scheme: str = SCHEME,
    #                              authority: str = AUTHORITY, client_id: str = VK_APP_ID,
    #                              redirect_uri: str = REDIRECT_URI):
    #     access_token_link = f"{scheme}://{authority}/{path}?" \
    #                         f"client_id={client_id}&" \
    #                         f"redirect_uri={redirect_uri}&" \
    #                         f"code={code}"
    #     return access_token_link

    def get_friends(self, access_token: str, user_id: str, order: str = 'hints',
                    count: int = None, offset: int | None = None,
                    fields: tuple = ('country', 'city', 'bdate', 'sex'), name_case: str = 'nom'):
        param_count = f'count={count}&' if count is not None else ''
        # url параметр: количество друзей на странице
        param_offset = f'offset={count * offset}&' if offset is not None else ''
        # url параметр: смещение после которого нужно взять count друзей
        url = f"https://api.vk.com/method/{self.VK_API_METHOD_GET_FRIENDS}?" \
              f"user_id={user_id}&" \
              f"order={order}&" \
              f"{param_count}" \
              f"{param_offset}" \
              f"fields={','.join(fields)}&" \
              f"name_case={name_case}&" \
              f"access_token={access_token}&" \
              f"v={self.VK_API_VERSION}"
        response = requests.get(url=url)

        return response.json()

    def get_friends_amount(self, access_token: str, user_id: str):
        friends = self.get_friends(access_token, user_id, fields=())
        return friends['response']['count']

    def create_vk_friends_report(self, access_token: str, user_id: str,
                                 friends_amount_in_report: int, page_number: int | None,
                                 file_path_and_name: str, file_format: str):
        all_friends = []
        if not page_number:
            amount_pages = math.ceil(friends_amount_in_report / self.MAX_FRIENDS_AMOUNT_IN_RESPONSE)
            friends_amount_in_report = self.MAX_FRIENDS_AMOUNT_IN_RESPONSE
        else:
            amount_pages = 1

        for page in range(amount_pages):
            if page_number:
                offset_page = page_number - 1
            else:
                offset_page = page
            friends = self.get_friends(access_token, user_id, count=friends_amount_in_report,
                                       offset=offset_page)
            all_friends.extend(friends['response']['items'])
        create_report(all_friends, file_path_and_name, file_format)
