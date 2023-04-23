from starlette.exceptions import HTTPException as StarletteHTTPException

from app.main import app
from app.shortcuts import render, redirect
from app.users.exceptions import LoginRequiredException


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    context = {"status_code": status_code}
    template_name = "errors/404.html" if status_code == 404 else "errors/main.html"

    return render(request, template_name, context, status_code=status_code)


@app.exception_handler(LoginRequiredException)
async def login_required_exception_handler(request, exc):
    return redirect("/login", remove_session=True)