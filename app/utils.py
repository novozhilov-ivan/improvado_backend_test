from http import HTTPStatus

from flask import url_for, redirect
from werkzeug import Response

from app.vk_api_requests import VkApp


def get_report_params_selection_page_for_user(access_token: str, app_user_id,
                                              user_id_for_get_friends: str) -> tuple[str, HTTPStatus] | str | Response:
    response = VkApp().get_friends_amount(access_token, user_id_for_get_friends)
    try:
        user_friends_amount = response['response']['count']

        redirect_uri = f"{url_for('parameter_selection_page')}?" \
                       f"access_token={access_token}&" \
                       f"app_user_id={app_user_id}&" \
                       f"user_friends_amount={user_friends_amount}&" \
                       f"user_id_for_get_friends={user_id_for_get_friends}&" \
                       f"friends_per_page={VkApp.FRIENDS_PER_PAGE}"
    except KeyError:
        error_message = response['error']['error_msg']
        return f"<p>Произошла ошибка. {error_message}</p>", HTTPStatus(403)
    except (Exception, ):
        return f"<p>Произошла ошибка. Неизвестная ошибка</p>", HTTPStatus(500)
    else:
        return redirect(redirect_uri)
