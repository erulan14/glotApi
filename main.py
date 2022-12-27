import uvicorn
from glot import Glot
from glot.response import HTMLResponse
from glot.templating import Jinja2Templates
from datetime import datetime

app = Glot()
templates = Jinja2Templates(directory="templates")


@app.route("/")
def start(request):
    params = request.query_params
    print(params)
    return templates.TemplateResponse("index.html", {"request": request, "datetime": datetime.now()})


@app.route("/test/{name}")
def test(request, name):
    return HTMLResponse(f"<h1>{name}</h1>")


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)