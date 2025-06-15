from fastapi import FastAPI
from pydantic import BaseModel
from correct_code import correct_code

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all frontend domains (you can restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

@app.post("/correct")
def fix_code(data: CodeInput):
    corrected_code, corrections = correct_code(data.code)
    return {
        "corrected_code": corrected_code,
        "corrections": corrections
    }
