import math
import os

from flask import redirect, request, url_for, render_template, send_file

from app.config import app
from app.utils import VkontakteApp


# TODO Добавить функционал обрабатывающий потенциальные ошибки
# TODO Добавить docstrings
# TODO Добавить логирование
# TODO Добавить тесты функций

@app.route('/')
def redirect_to_allow_application_access():
    link = VkontakteApp()
    link = link.link_to_generate_code_or_token(response_type='token')
    return f'<p>Авторизуйтесь в приложении с помощью вашего аккаунта VK по <a href={link}>ссылке</a>.</p>'


@app.route('/auth/', methods=['GET'])
def copy_and_send_access_token():
    return render_template('get_access_token.html')


@app.route('/auth/', methods=['POST'])
def get_access_token():
    full_url = request.form.get("full_url")
    # TODO добавить обработку ошибки если пользователь скопировать full_url с изменением
    if 'access_token' in full_url and 'user_id' in full_url:
        url_params = full_url.split('#')[1].split('&')
        access_token = url_params[0].split('=')[1]
        user_id = url_params[2].split('=')[1]

        friends_amount = VkontakteApp().get_friends_amount(access_token, user_id)

        redirect_uri = f"{url_for('parameter_selection_page')}?" \
                       f"access_token={access_token}&" \
                       f"user_id={user_id}&" \
                       f"friends_amount={friends_amount}"
        return redirect(redirect_uri)

    return "<p>Произошла ошибка. Попробуйте еще раз.</p>"


# может быть задействован при реализации клиент-серверного приложения
# @app.route('/auth/')
# def check_auth_in_app():
#     code = request.args['code']
#     link = VkontakteApp.link_to_get_access_token(code)
#     response = requests.get(url=link)
#
#     if response.status_code == 200:
#         response_info = response.json()
#         return redirect(
#             url_for(
#                 'parameter_selection_page',
#                 access_token=response_info['access_token'],
#                 user_id=response_info['user_id']
#             )
#         )
#     else:
#         return '<p>Произошла ошибка</p>'


@app.route('/friends/', methods=['GET'])
def parameter_selection_page():
    access_token = request.values.get('access_token')
    user_id = request.values.get('user_id')
    friends_amount = request.values.get('friends_amount')
    # TODO добавить обработку ошибки если не все values получены (если хотя бы 1 не None)
    if access_token and user_id and friends_amount:
        default_file_path = "./"
        default_file_name = "report"
        friends_amount = int(friends_amount)
        amount_friends_pages = friends_amount
        if friends_amount:
            amount_friends_pages = math.ceil(friends_amount / 100)

        return render_template(
            "select_parameters.html",
            access_token=access_token,
            user_id=user_id,
            friends_amount=friends_amount,
            amount_friends_pages=amount_friends_pages,
            default_file_path_and_name=f"{default_file_path}{default_file_name}"
        )
    return "<p>Произошла ошибка. Попробуйте еще раз.</p>"


@app.route('/friends/', methods=['POST'])
def get_form_data():
    access_token = request.form.get("assess_token")
    user_id = request.form.get("user_id")

    friends_amount = request.form.get("friends_amount")
    friends_amount = 100 if friends_amount == "page" else None

    page_number = request.form.get("page_number")
    page_number = int(page_number) if friends_amount else None

    file_format = request.form.get("file_format")
    file_path_and_name = request.form.get("file_name_and_path")
    if access_token and user_id and file_format and file_path_and_name:
        VkontakteApp().create_vk_friends_report(access_token, user_id,
                                                friends_amount=friends_amount,
                                                page_number=page_number,
                                                file_path_and_name=file_path_and_name,
                                                file_format=file_format)
        file_source = f"{file_path_and_name}.{file_format}"

        return redirect(url_for('download_report', file_source=file_source))
    return '<p>Произошла ошибка. Попробуйте еще раз.</p>'


@app.route('/download/', methods=['GET', 'POST'])
def download_report():
    file_source = request.values.get('file_source')
    absolute_path = os.path.abspath(file_source)
    if request.method == "GET":
        page = f'<form method="POST">Отчет успешно создан. Полный путь к файлу: {absolute_path}' \
               f'<p><button type="submit">Скачать отчет</button></p>' \
               f'</form>'
        return page
    return send_file(path_or_file=absolute_path, as_attachment=True)
