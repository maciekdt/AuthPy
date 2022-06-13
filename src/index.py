import os
import aiofiles
from sanic import Sanic
from sanic.response import json, empty, html
import src.repos.auth_repo as auth
from utils import get_project_root

app = Sanic("AuthPy")


@app.post("/auth/login")
async def login(request):
    token = await auth.login("damian", "key123")
    if token:
        return json({"token": token}, status=200)
    else:
        return empty(status=401)


@app.post("/auth/register")
async def register(request):
    await auth.register("damian", "key123")
    return empty(status=200)


@app.get("/page/login")
async def get_login_page(request):
    page_path = os.path.join(get_project_root(), 'res/pages/login_page.html')
    async with aiofiles.open(page_path, 'r') as file:
        page = await file.read()
        page.replace('\n', '')
        return html(page, status=200)


if __name__ == "__main__":
    app.run(dev=True)
