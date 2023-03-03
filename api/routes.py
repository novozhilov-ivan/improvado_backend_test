from flask import redirect, render_template

from api import app


@app.route('/')
def auth():
    client_id = '51571106'  # id приложения или client_id
    vk_api_version = '5.131'
    redirect_page = "127.0.0.1:8000/api/"
    display = 'page'
    scope = ['friends', 'offline']
    # response_type = 'token'
    response_type = 'code'
    url_implicit_code = f'https://oauth.vk.com/authorize?' \
                        f'client_id={client_id}&' \
                        f'display={display}&' \
                        f'redirect_uri={redirect_page}&' \
                        f'scope={scope}&' \
                        f'response_type={response_type}&' \
                        f'v={vk_api_version}&' \
                        f'state=123456'
    url_authorization_code = f'https://oauth.vk.com/authorize?' \
                             f'client_id={client_id}&' \
                             f'display={display}&' \
                             f'redirect_uri={redirect_page}&' \
                             f'scope={",".join(scope)}&' \
                             f'response_type={response_type}&' \
                             f'revoke=1&' \
                             f'v={vk_api_version}'
    # f'redirect_uri={redirect_page}' \
    print(f'Для авторизации перейдите по ссылке {url_authorization_code}')
    # return redirect(url_authorization_code)
    return f'<p>Для авторизации перейдите по <a href={url_authorization_code}>ссылке</a>.</p>'



implicit_code = 'https://oauth.vk.com/authorize?client_id=1&display=page&redirect_uri=https://example.com/callback&' \
                'scope=friends&response_type=token&v=5.131&state=123456'
authorization_code = 'https://oauth.vk.com/authorize?client_id=1&display=pag' \
                     'e&redirect_uri=https://example.com/callback&scope=friends&response_type=code&v=5.131'



