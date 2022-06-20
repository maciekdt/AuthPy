from bson import ObjectId
from sanic import Sanic, response
from sanic.response import json, empty, html, text, file, redirect
import src.repos.auth_repo as auth
from src.exceptions.UnauthorizedException import UnauthorizedException
from src.exceptions.NotFoundException import NotFoundException
import src.repos.files_repo as files_repo
import src.repos.html_repo as html_repo
import src.endpoints.mongo_service as mongo_service
from src.utils import get_random_object_id

app = Sanic("AuthPy")


@app.middleware("request")
async def extract_user(request):
    if "/auth/" not in request.url:
        token = request.cookies.get("token")
        request.ctx.user_id = ObjectId(await auth.verify_token(token))


@app.get("/file/<folder_id>/<file_id>")
async def get_file(request, folder_id, file_id):
    folder = await mongo_service.get_folder(ObjectId(folder_id))
    if auth.check_owner(request, folder):
        file_path, file_name = await files_repo.get_file(ObjectId(file_id), ObjectId(folder_id))
        return await file(file_path, filename=file_name)


@app.post("/file/<folder_id>")
async def upload_file(request, folder_id):
    folder = await mongo_service.get_folder(ObjectId(folder_id))
    if auth.check_owner(request, folder):
        file_bytes = request.files.get("uploaded_file").body
        file_name = request.files.get("uploaded_file").name
        await files_repo.add_new_file(file_name, file_bytes, ObjectId(folder_id))
        return redirect("/folder/"+folder_id)


@app.get("folder/<folder_id>")
async def get_folder_page(request, folder_id):
    folder = await mongo_service.get_folder(ObjectId(folder_id))
    if auth.check_owner(request, folder):
        page = await html_repo.get_folders_page(folder)
        return html(page)


@app.post("folder/<folder_id>")
async def upload_folder(request, folder_id):
    folder_parent = await mongo_service.get_folder(ObjectId(folder_id))
    if auth.check_owner(request, folder_parent):
        folder_name = request.form['folder_name'][0]
        folder_id = get_random_object_id()
        await mongo_service.add_new_folder(folder_name, folder_id, folder_parent.owners)
        await mongo_service.add_folder_to_folder(folder_name, folder_id, folder_parent._id)
        return redirect("/folder/"+str(folder_parent._id))


@app.get("/page/auth/login")
async def get_login_page(request):
    page = await html_repo.get_page('res/pages/login_page.html')
    return html(page, status=200)


@app.post("/page/auth/login")
async def login(request):
    name = request.form['name'][0]
    password = request.form["pass"][0]
    token, user = await auth.login(name, password)
    return_response = redirect('/page/main')
    return_response.cookies["token"] = token
    return return_response


@app.get("/page/auth/register")
async def get_register_page(request):
    page = await html_repo.get_page('res/pages/register_page.html')
    return html(page, status=200)


@app.post("/page/auth/register")
async def register(request):
    name = request.form['name'][0]
    password = request.form["pass"][0]
    await auth.register(name, password)
    token, user = await auth.login(name, password)
    return_response = redirect('/page/main')
    return_response.cookies["token"] = token
    return return_response


@app.get("page/main")
async def page_main(request):
    user = await mongo_service.get_user_by_id(ObjectId(request.ctx.user_id))
    page = await html_repo.get_main_page(user.main_folder, user.shared_folder)
    return html(page, status=200)


@app.get("page/auth/unauthorized")
async def page_main(request):
    page = await html_repo.get_page('res/pages/unauthorized_page.html')
    return html(page, status=200)


@app.exception(UnauthorizedException)
async def raise_401s(request, exception):
    return redirect("/page/auth/unauthorized")


@app.exception(NotFoundException)
async def raise_404s(request, exception):
    return text("Not found, try again", status=404)


# @app.exception(Exception)
# async def raise_500s(request, exception):
# return text("Server error", status=500)


if __name__ == "__main__":
    app.run(dev=True)
