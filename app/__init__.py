from app.routes import (
    render_page_with_link_for_auth,
    get_page_to_copy_and_send_full_url,
    authorization,
    parameters_on_selection_pages,
    get_form_data,
    download_report
)
from app.config import app

__all__ = [
    'render_page_with_link_for_auth',
    'get_page_to_copy_and_send_full_url',
    'authorization',
    'parameters_on_selection_pages',
    'get_form_data',
    'download_report',
    'app'
]

