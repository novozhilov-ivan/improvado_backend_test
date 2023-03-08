import math

import requests

from app.working_with_report_file import create_report


class VkApp:
    APP_ID = '51571106'  # идентификатор приложения.
    VK_API_VERSION = '5.131'  # версия API VK.
    SCHEME = 'https'
    AUTH_AUTHORITY = 'oauth.vk.com'
    API_AUTHORITY = "api.vk.com"
    AUTH_REDIRECT_URI = "http://127.0.0.1:8000/auth/"
    FRIENDS_REDIRECT_URI = "http://127.0.0.1:8000/friends/"
    VK_REDIRECT_URI = "https://oauth.vk.com/blank.html"
    DEFAULT_REDIRECT_URI = AUTH_REDIRECT_URI
    VK_METHOD_AUTHORIZE = 'authorize'
    VK_API_METHOD_GET_FRIENDS = 'friends.get'
    VK_API_METHOD_ACCESS_TOKEN = 'access_token'
    # url = "https://api.vk.com/method/<METHOD>?<PARAM>&<PARAM>"
    MAX_FRIENDS_AMOUNT_IN_RESPONSE = 5000
    DEFAULT_FIELDS = ('country', 'city', 'bdate', 'sex')
    NAME_CASE_NOM = 'nom'  # имена и фамилии пользователей vk.com в именительном падеже
    DEFAULT_NAME_CASE = NAME_CASE_NOM
    DEFAULT_REVOKE = 1
    # revoke - параметр (1 или 0), указывающий, что необходимо не пропускать этап подтверждения
    # прав, даже если пользователь уже выдавал права приложению.
    # 0 - пропустить повторное подтверждение; 1 - всегда запрашивать подтверждение.
    ORDER_BY_HINTS = 'hints'  # Получение друзей отсортированных сайтом по рейтингу пользователя - можно 2 стр. по 5000
    ORDER_BY_RANDOM = 'random'  # Получение не отсортированных сайтом друзей - можно 2 страницы по 5000, но с повторами
    ORDER_BY_NAME = 'name'  # Получение друзей отсортированных сайтом по имени - можно только первую страницу с 5000
    DEFAULT_APP_SCOPE = ('friends', 'offline')
    # scope - права доступа приложения, запрашиваемые при авторизации в приложении.
    # friends - получение доступа к друзьям пользователя;
    # offline - получение доступа к данным пользователя, даже если он не в сети.
    # При добавлении параметра offline - access_token становится бессрочным
    DISPLAY_AS_PAGE = 'page'
    DISPLAY_AS_POPUP = 'popup'
    DEFAULT_DISPLAY = DISPLAY_AS_PAGE
    FRIENDS_PER_PAGE = 500

    # Implicit Flow для получения ключа доступа пользователя
    @classmethod
    def get_url_to_generate_code_or_token(cls, response_type: str, redirect_uri: str = DEFAULT_REDIRECT_URI,
                                          display: str = DEFAULT_DISPLAY, scope: tuple = DEFAULT_APP_SCOPE,
                                          revoke: int = DEFAULT_REVOKE) -> str:
        # response_type = 'token' или 'code', Implicit Flow код или Authorization Code Flow соответственно.
        # response_type — Тип ответа, который вы хотите получить:
        # code — если вы хотите делать запросы со стороннего сервера (по умолчанию);
        # token — если вы хотите делать запросы с клиента.
        url = f'{cls.SCHEME}://{cls.AUTH_AUTHORITY}/{cls.VK_METHOD_AUTHORIZE}'
        params = {
         'client_id': cls.APP_ID,
         'redirect_uri': redirect_uri,
         'display': display,
         'scope': ",".join(scope),
         'response_type': response_type,
         'revoke': revoke,
         'v': cls.VK_API_VERSION
        }
        generated_url = requests.request('get', url=url, params=params).url
        return generated_url

    # может быть задействован при реализации клиент-серверного приложения
    # Authorization Code Flow для получения ключа доступа пользователя
    # @classmethod
    # def get_url_for_create_access_token(cls, code: str):
    #     access_token_url = f"{cls.SCHEME}://{cls.AUTHORITY}/{cls.VK_API_METHOD_ACCESS_TOKEN}?" \
    #                        f"client_id={cls.APP_ID}&" \
    #                        f"redirect_uri={cls.FRIENDS_REDIRECT_URI}&" \
    #                        f"code={code}"
    #     return access_token_url

    @classmethod
    def get_friends(cls, access_token: str, user_id: str,
                    order: str = ORDER_BY_HINTS, count: int = None, offset: int = None,
                    fields: tuple = DEFAULT_FIELDS, name_case: str = DEFAULT_NAME_CASE):
        url = f"{cls.SCHEME}://{cls.API_AUTHORITY}/method/{cls.VK_API_METHOD_GET_FRIENDS}"
        params = {
            'user_id': user_id,
            'order': order,
            'count': count,  # url параметр: количество друзей на странице
            'offset': offset,  # url параметр: смещение после которого нужно взять count друзей
            'fields': ','.join(fields),
            'name_case': name_case,
            'access_token': access_token,
            'v': cls.VK_API_VERSION
        }

        response = requests.get(url, params=params)
        return response.json()

    @classmethod
    def get_friends_amount(cls, access_token: str, user_id: str):
        friends = cls.get_friends(access_token, user_id, fields=(), order=cls.ORDER_BY_RANDOM)
        return friends

    @classmethod
    def create_vk_friends_report(cls, access_token: str, user_id: str,
                                 friends_amount_in_report: int,
                                 page_number: int,
                                 file_path_and_name: str, file_format: str):
        # page_number: номер страницы полученных на входе.
        # amount_pages: если нужно получить больше 5000 друзей, то amount_pages = 2, иначе 1.
        # friends_amount_in_report: количество запрашиваемых друзей в запросе. Не больше 5000 для каждого запроса.
        all_friends = []
        if page_number == 0:
            amount_pages = math.ceil(friends_amount_in_report / cls.MAX_FRIENDS_AMOUNT_IN_RESPONSE)
            friends_amount_in_report = cls.MAX_FRIENDS_AMOUNT_IN_RESPONSE
        else:
            amount_pages = 1
        offset = (page_number - 1) * friends_amount_in_report
        for page in range(amount_pages):
            if page_number == 0:
                offset = page * friends_amount_in_report
            friends = cls.get_friends(access_token, user_id, count=friends_amount_in_report, offset=offset)
            all_friends.extend(friends['response']['items'])

        create_report(all_friends, file_path_and_name, file_format)
