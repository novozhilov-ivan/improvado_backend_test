import requests
from flask import redirect, request, jsonify, url_for, render_template

from api.config import app
from api.utils import VkontakteApp


@app.route('/')
def redirect_to_allow_application_access():
    link = VkontakteApp.link_to_generate_code()
    # print(f'Для авторизации перейдите по ссылке {link}')
    # return redirect(link)
    return f'<p>Авторизуйтесь в приложении с помощью вашего аккаунта VK по <a href={link}>ссылке</a>.</p>'


@app.route('/auth/')
def check_auth_in_app():
    code = request.args['code']
    link = VkontakteApp.link_to_get_access_token(code)
    response = requests.get(url=link)

    if response.status_code == 200:
        response_info = response.json()
        return redirect(
            url_for(
                'parameter_selection_page',
                access_token=response_info['access_token'],
                user_id=response_info['user_id']
            )
        )
    else:
        return '<p>Произошла ошибка</p>'


@app.route('/friends/', methods=['GET'])
def parameter_selection_page():
    access_token = request.values.get('access_token')
    user_id = request.values.get('user_id')
    default_file_path = "../"
    default_file_name = "report"

    return render_template(
        "select_parameters.html",
        access_token=access_token,
        user_id=user_id,
        default_file_path_and_name=f"{default_file_path}{default_file_name}"
    )


@app.route('/friends/', methods=['POST'])
def form_data():
    access_token = request.form.get("assess_token")
    user_id = request.form.get("user_id")
    file_format = request.form.get("file_format")
    file_name_and_path = request.form.get("file_name_and_path")
    if access_token and user_id and file_format and file_name_and_path:
        # my_dict = {
        #     "assess_token": f'{access_token}',
        #     "user_id": f'{user_id}',
        #     "file_path_name_format": f'{file_name_and_path}.{file_format}'
        # }
        data = VkontakteApp.get_all_friends(access_token, '121696444')
        return jsonify(data)
    else:
        return '<p>Произошла ошибка</p>'

