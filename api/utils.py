import requests


class VkontakteApp:
    VK_APP_ID = '51571106'  # идентификатор приложения.
    VK_API_VERSION = '5.131'  # версия API VK.
    SCHEME = 'https'
    AUTHORITY = 'oauth.vk.com'
    VK_APP_SECRET_KEY = 'mfIyix9k0DcrdiyOiuVC'
    REDIRECT_URI = "http://127.0.0.1:8000/auth/"

    @staticmethod
    def link_to_generate_code(path: str = 'authorize', scheme: str = SCHEME, authority: str = AUTHORITY,
                              v: str | float = VK_API_VERSION, client_id: str = VK_APP_ID,
                              redirect_uri: str = REDIRECT_URI, display: str = 'page',
                              scope: tuple = ('friends', 'offline'), response_type: str = 'code',
                              revoke: str | int = 1):
        # display: page - тип отображения страницы авторизации.
        # scope - настройки доступа приложения. Перечисляются через запятую.
        # friends - получение доступа к друзьям;
        # offline - получение доступа к данным пользователя, даже если он не в сети.
        # Если указать scope=offline, при response_type = 'token', то access_token будет бессрочный.
        # response_type = 'token'
        # revoke - параметр, указывающий, что необходимо не пропускать этап подтверждения прав,
        # даже если пользователь уже авторизован.
        # 0 - пропустить повторное подтверждение; 1 - всегда запрашивать подтверждение.
        generate_code_link = f'{scheme}://{authority}/{path}?' \
                             f'client_id={client_id}&' \
                             f'redirect_uri={redirect_uri}&' \
                             f'display={display}&' \
                             f'scope={",".join(scope)}&' \
                             f'response_type={response_type}&' \
                             f'revoke={revoke}&' \
                             f'v={v}'
        return generate_code_link

    @staticmethod
    def link_to_get_access_token(code: str, path: str = "access_token", scheme: str = SCHEME,
                                 authority: str = AUTHORITY, client_id: str = VK_APP_ID,
                                 redirect_uri: str = REDIRECT_URI,
                                 client_secret_key: str = VK_APP_SECRET_KEY):
        access_token_link = f"{scheme}://{authority}/{path}?" \
                            f"client_id={client_id}&" \
                            f"redirect_uri={redirect_uri}&" \
                            f"client_secret={client_secret_key}&" \
                            f"code={code}"
        return access_token_link

    @staticmethod
    def get_all_friends(access_token: str, user_id: str, order: str = 'name',
                        count: None | int = None, offset: None | int = None,
                        fields: tuple = ('country', 'city', 'bdate', 'sex'), name_case: str = 'nom',
                        v: str = VK_API_VERSION):
        VK_API_METHOD = 'friends.get'
        # url = "https://api.vk.com/method/<METHOD>?<PARAMS>"
        url = f"https://api.vk.com/method/{VK_API_METHOD}?" \
              f"user_id={user_id}&order={order}&" \
              f"fields={','.join(fields)}&" \
              f"name_case={name_case}&access_token={access_token}&v={v}"
        response = requests.get(url=url)
        return response.json()
