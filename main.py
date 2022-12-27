import uvicorn
from glot import Glot
from glot.response import HTMLResponse
from glot.staticfiles import StaticFiles
from glot.templating import Jinja2Templates

app = Glot()

templates = Jinja2Templates(directory="templates")

@app.route("/")
def start(request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.route("/test/{name}")
def test(request, name):
    return f"<h1>{name}</h1>"


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)