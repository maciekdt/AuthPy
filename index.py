from sanic import Sanic
from sanic.response import text, json
import endpoints.mongo_service as db_service
import model.auth_repo as auth

app = Sanic("AuthPy")


@app.get("/login")
async def login(request):
    return json()


@app.get("/register")
async def register(request):
    await db_service.add_new_user("jacek", "key123")


if __name__ == "__main__":
    app.run(dev=True)
