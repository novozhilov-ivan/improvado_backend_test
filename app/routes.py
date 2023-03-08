from http import HTTPStatus
import math
import os

from flask import redirect, request, url_for, render_template, send_file

from app.config import app
from app.vk_api_requests import VkApp
from app.utils import get_report_params_selection_page_for_user


@app.route('/')
def render_page_with_link_for_auth():
    url = VkApp().get_url_to_generate_code_or_token(response_type='token')
    return f'<p>Авторизуйтесь в приложении с помощью вашего аккаунта VK по <a href={url}>ссылке</a></p>'


@app.route('/auth/', methods=['GET'])
def get_page_to_copy_and_send_full_url():
    return render_template('get_access_token.html')


@app.route('/auth/', methods=['POST'])
def authorization():
    full_url = request.form.get("full_url")
    if 'access_token' in full_url and 'user_id' in full_url:
        url_params = full_url.split('#')[1].split('&')
        access_token = url_params[0].split('=')[1]
        app_user_id = url_params[2].split('=')[1]
        if len(access_token) != 220:
            return "<p>Произошла ошибка. Вернитесь назад и убедитесь, " \
                   "что полностью скопировали URL из адресной строки.</p>", HTTPStatus(400)
        response = get_report_params_selection_page_for_user(access_token,
                                                             app_user_id=app_user_id,
                                                             user_id_for_get_friends=app_user_id)
        return response


# может быть задействован при реализации клиент-серверного приложения
# @app.route('/auth/')
# def check_auth_in_app():
#     code = request.args['code']
#     url = VkApp().get_url_for_create_access_token(code)
#     response = requests.get(url=url)


@app.route('/friends/', methods=['GET'])
def parameters_on_selection_pages():
    access_token = request.values.get('access_token')
    app_user_id = request.values.get('app_user_id')
    user_friends_amount = request.values.get('user_friends_amount')
    user_id_for_get_friends = request.values.get('user_id_for_get_friends')

    if access_token and app_user_id and user_friends_amount:
        default_file_path = "./"
        default_file_name = "report"
        user_friends_amount = int(user_friends_amount)
        friends_per_page = int(request.values.get('friends_per_page'))
        if user_friends_amount:
            amount_of_pages_with_friends = math.ceil(user_friends_amount / friends_per_page)
        else:
            amount_of_pages_with_friends = 0
        return render_template(
            "select_parameters.html",
            access_token=access_token,
            app_user_id=app_user_id,
            user_id_for_get_friends=user_id_for_get_friends,
            user_friends_amount=user_friends_amount,
            amount_of_pages_with_friends=amount_of_pages_with_friends,
            friends_per_page=friends_per_page,
            default_file_path=default_file_path,
            default_file_name=default_file_name
        )
    return '<p>Произошла ошибка. ' \
           'Вернитесь назад, обновите страницу, проверьте заполняемые поля и попробуйте еще раз.</p>'


@app.route('/friends/', methods=['POST'])
def get_form_data():
    user_friends_amount = int(request.values.get('user_friends_amount'))
    new_user_id_for_get_friends = request.form.get("user_id_for_get_friends")
    user_id_for_get_friends = request.values.get("user_id_for_get_friends")
    app_user_id = request.values.get("app_user_id")
    access_token = request.form.get("assess_token")
    friends_amount_type = request.form.get("friends_amount_type")
    file_format = request.form.get("file_format")
    file_path_and_name = request.form.get("file_name_and_path")
    friends_per_page = int(request.values.get('friends_per_page'))
    page_number = int(request.form.get("page_number"))

    # Если у пользователя нет друзей - создание отчета для него недоступно
    if not user_friends_amount and new_user_id_for_get_friends == user_id_for_get_friends:
        return '<p>У вас нет друзей.</p>'

    # Если пользователь приложения указывает не свой ID, а ID прочего пользователя, то страница обновляется и
    # приводится количество друзей для искомого пользователя.
    if new_user_id_for_get_friends not in (app_user_id, user_id_for_get_friends):
        response = get_report_params_selection_page_for_user(access_token,
                                                             app_user_id=app_user_id,
                                                             user_id_for_get_friends=new_user_id_for_get_friends)
        return response

    if friends_amount_type == "page":
        friends_amount_in_report = friends_per_page
    else:
        friends_amount_in_report = user_friends_amount
        page_number = 0
    if access_token and user_id_for_get_friends and file_format and file_path_and_name:
        VkApp().create_vk_friends_report(access_token, user_id_for_get_friends,
                                         friends_amount_in_report=friends_amount_in_report,
                                         page_number=page_number,
                                         file_path_and_name=file_path_and_name,
                                         file_format=file_format)
        file_source = f"{file_path_and_name}.{file_format}"

        return redirect(url_for('download_report', file_source=file_source))
    return '<p>Произошла ошибка. ' \
           'Вернитесь назад, обновите страницу, проверьте заполняемые поля и попробуйте еще раз.</p>'


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
