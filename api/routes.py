import requests
from flask import redirect, request, jsonify

from api.config import app
from api.keys import client_secret_key

# def create_url():
#     return True


scheme = 'https'
authority = 'oauth.vk.com'


client_id = '51571106'  # идентификатор приложения.
vk_api_version = '5.131'  # версия API VK.
# redirect_page = "127.0.0.1:8000/auth/"
redirect_page = "http://127.0.0.1:8000/auth/"


@app.route('/')
def redirect_to_allow_application_access():
    path = 'authorize'
    display = 'page'  # page - тип отображения страницы авторизации.
    scope = ','.join(['friends', 'offline'])  # scope - настройки доступа приложения. Перечисляются через запятую
    # friends - получение доступа к друзьям;
    # offline - получение доступа к данным пользователя, даже если он не в сети.
    # Если указать scope=offline, при response_type = 'token', то access_token будет бессрочный.
    # response_type = 'token'
    response_type = 'code'
    revoke = 1
    # revoke - параметр, указывающий, что необходимо не пропускать этап подтверждения прав,
    # даже если пользователь уже авторизован.
    # 0 - пропустить повторное подтверждение; 1 - всегда запрашивать подтверждение.
    url_give_access = f'{scheme}://{authority}/{path}?' \
                      f'client_id={client_id}&' \
                      f'redirect_uri={redirect_page}&' \
                      f'display={display}&' \
                      f'scope={scope}&' \
                      f'response_type={response_type}&' \
                      f'revoke={revoke}&' \
                      f'v={vk_api_version}'

    print(f'Для авторизации перейдите по ссылке {url_give_access}')
    return redirect(url_give_access)
    # return f'<p>Для авторизации перейдите по <a href={url_give_access}>ссылке</a>.</p>'


@app.route('/auth/')
def get_code():
    code = request.args['code']
    path = "access_token"
    url_get_access_token = f"{scheme}://{authority}/{path}?" \
                           f"client_id={client_id}&" \
                           f"redirect_uri={redirect_page}&" \
                           f"client_secret={client_secret_key}&" \
                           f"code={code}"
    response = requests.get(url=url_get_access_token)
    # print(response.text)
    # print(f'Для авторизации перейдите по ссылке {url_get_access_token}')
    return response.json()



