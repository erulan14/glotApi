import uvicorn
from glot import Glot
from glot.response import HTMLResponse
from glot.templating import Jinja2Templates
from glot.staticfiles import StaticFiles
from pydantic import BaseModel
import datetime

app = Glot()
templates = Jinja2Templates(directory="templates")
static_file = StaticFiles(directory="static")


class User(BaseModel):
    username: str
    password: str


users = [User(username=f"test{i}", password="").dict() for i in range(10)]


@app.route("/static/{path}")
async def static(request, path):
    if static_file.lookup_path(path)[1] is None:
        return HTMLResponse("Not Found", status_code=404)

    res = await static_file.get_response(path, request.scope)
    return res


@app.route("/")
async def start(request):
    return templates.TemplateResponse("index.html", {"request": request, "time": datetime.datetime.now()})


@app.route("/test/{name:d}")
async def test(request, name):
    return HTMLResponse(f"<h1>{name}</h1>")


@app.route("/api/v1/", methods=["GET", "POST"])
async def api(request):
    if request.method == "GET":
        return users
    else:
        form = await request.form()
        file = form.get("file")
        if file is not None:
            file.save()
        return users


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)