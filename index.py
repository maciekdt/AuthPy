from sanic import Sanic
from sanic.response import text
import endpoints.mongo_service as db_service

app = Sanic("AuthPy")


@app.get("/")
async def hello_world(request):
    db_service.get_database()
    return text("ELO")

if __name__ == "__main__":
    app.run(dev=True)
