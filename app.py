from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.sentence_analyzer import analyze

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_form(
    request: Request,
    sentence: str = Form(...)
):
    result = analyze(sentence)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result
        }
    )
