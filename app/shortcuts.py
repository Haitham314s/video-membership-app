from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .config import get_settings

settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def redirect(path, cookies: dict = None, remove_session=False):
    if cookies is None:
        cookies = {}

    response = RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(key=k, value=v, httponly=True)

    if remove_session:
        response.set_cookie(key="session_ended", value="1", httponly=True)
        response.delete_cookie("session_id")
    return response


def render(
        request, template_name, context=None, status_code: int = 200, cookies=None
):
    if cookies is None:
        cookies = {}
    if context is None:
        context = {}

    ctx = context.copy()
    ctx.update({"request": request})

    t = templates.get_template(template_name)
    html_str = t.render(ctx)

    response = HTMLResponse(html_str, status_code=status_code)
    # Set httponly cookies
    if len(cookies.keys()) > 0:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)

    # # Delete cookies
    # for key in request.cookies.keys():
    #     response.delete_cookie(key)
    return response
