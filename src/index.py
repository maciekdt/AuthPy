import os
import aiofiles
from sanic import Sanic, response
from sanic.response import json, empty, html, text, file
import src.repos.auth_repo as auth
from src.exceptions.UnauthorizedException import UnauthorizedException
from src.exceptions.NotFoundException import NotFoundException
from utils import get_project_root
import src.repos.files_repo as files_repo

app = Sanic("AuthPy")


async def get_page(page_relative_path):
    page_path = os.path.join(get_project_root(), page_relative_path)
    async with aiofiles.open(page_path, 'r') as file:
        page = await file.read()
        return page.replace('\n', '')


@app.post("/auth/login")
async def login(request):
    name = request.form['name'][0]
    password = request.form["pass"][0]
    token, expire_time = await auth.login(name, password)
    response = text("Logged in", status=200)
    response.cookies["token"] = token
    return response


@app.get("/auth/check")
async def check(request):
    token = request.cookies.get("token")
    user = await auth.verify_token(token)
    return json({"user": user}, status=200)


@app.post("/auth/register")
async def register(request):
    name = request.form['name'][0]
    password = request.form["pass"][0]
    await auth.register(name, password)
    return text("User registered", status=200)


@app.post("/file")
async def register(request):
    file_bytes = request.files.get("uploaded_file").body
    file_name = request.files.get("uploaded_file").name
    file_id_name = files_repo.add_new_file(file_name, file_bytes)
    return await response.file('C:\\Users\\maciek\\Documents\\Semestr_4\\JezykiSkryptowe_lab\\AuthPy\\src\\res/files/cde2e833-7fec-4bd0-a4ea-8bed22f9fda0.txt', filename=file_name)










@app.get("/page/auth/login")
async def get_login_page(request):
    page = await get_page('res/pages/login_page.html')
    return html(page, status=200)


@app.get("/page/auth/register")
async def get_register_page(request):
    page = await get_page('res/pages/register_page.html')
    return html(page, status=200)


@app.get("/page/upload")
async def get_register_page(request):
    page = await get_page('res/pages/upload_page.html')
    return html(page, status=200)


@app.exception(UnauthorizedException)
async def raise_401s(request, exception):
    page = await get_page('res/pages/login_page.html')
    return html(page, status=401)


@app.exception(NotFoundException)
async def raise_404s(request, exception):
    return text("Not found, try again", status=404)


# @app.exception(Exception)
# async def raise_500s(request, exception):
# return text("Server error", status=500)


if __name__ == "__main__":
    app.run(dev=True)
