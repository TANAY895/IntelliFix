import sys
import os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from correct_code import correct_code  # ✅ your logic

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class CodeRequest(BaseModel):
    code: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/correct")
async def correct_code_api(request: CodeRequest):
    corrected_code, corrections = correct_code(request.code)
    return {
        "corrected_code": corrected_code,
        "corrections": corrections
    }
