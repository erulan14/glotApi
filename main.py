import uvicorn
from glot import Glot
from glot.response import HTMLResponse
from glot.templating import Jinja2Templates
from datetime import datetime

from pydantic import BaseModel

app = Glot()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    username: str
    password: str


users = [User(username=f"test{i}", password="").dict() for i in range(10)]


@app.route("/")
def start(request):
    params = request.query_params
    return templates.TemplateResponse("index.html", {"request": request, "datetime": datetime.now()})


@app.route("/test/{name}")
def test(request, name):
    return HTMLResponse(f"<h1>{name}</h1>")


@app.route("/api/v1/", methods=["POST"])
def api(request):
    test = request.query_params.get("test")
    return users


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)