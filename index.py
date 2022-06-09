from sanic import Sanic
from sanic.response import text
import endpoints.mongo_service as db_service

app = Sanic("AuthPy")


@app.get("/")
async def hello_world(request):
    x = db_service.get_user_by_email("maciek.fi88@gmail.com")
    for item in x:
        print(item)
    return text("ELO")

if __name__ == "__main__":
    app.run(dev=True)
