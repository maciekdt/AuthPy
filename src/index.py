from bson import ObjectId
from sanic import Sanic, response
from sanic.response import json, empty, html, text, file
import src.repos.auth_repo as auth
from src.exceptions.UnauthorizedException import UnauthorizedException
from src.exceptions.NotFoundException import NotFoundException
import src.repos.files_repo as files_repo
import src.repos.html_repo as html_repo
import src.endpoints.mongo_service as mongo_service
from src.utils import get_random_object_id

app = Sanic("AuthPy")


@app.post("/auth/login")
async def login(request):
    name = request.form['name'][0]
    password = request.form["pass"][0]
    token, expire_time = await auth.login(name, password)
    return_response = text("Logged in", status=200)
    return_response.cookies["token"] = token
    return return_response


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
    await files_repo.add_new_file(file_name, file_bytes, ObjectId("b8618258485a3f412d1732a9"))
    return text("XDD")


@app.get("/")
async def test(request):
    f = await mongo_service.get_folder(ObjectId("c4d99b313444aebf743130df"))
    return text("XDD")










@app.get("/page/auth/login")
async def get_login_page(request):
    page = await html_repo.get_page('res/pages/login_page.html')
    return html(page, status=200)


@app.get("/page/auth/register")
async def get_register_page(request):
    page = await html_repo.get_page('res/pages/register_page.html')
    return html(page, status=200)


@app.get("/page/upload")
async def get_register_page(request):
    page = await html_repo.get_page('res/pages/upload_page.html')
    return html(page, status=200)


@app.exception(UnauthorizedException)
async def raise_401s(request, exception):
    page = await html_repo.get_page('res/pages/login_page.html')
    return html(page, status=401)


@app.exception(NotFoundException)
async def raise_404s(request, exception):
    return text("Not found, try again", status=404)


# @app.exception(Exception)
# async def raise_500s(request, exception):
# return text("Server error", status=500)


if __name__ == "__main__":
    app.run(dev=True)
