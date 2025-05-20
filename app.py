from fastapi import FastAPI, Form, Request, Depends, status, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import pandas as pd
import uvicorn
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

USERS = {
    "josemartinezcaparros42@gmail.com": "pmr2025"
}

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if USERS.get(email) == password:
        request.session["user"] = email
        return RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales incorrectas"})

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    if not request.session.get("user"):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not request.session.get("user"):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    df = pd.read_excel(file_location)
    table_html = df.to_html(classes="table", index=False)

    return templates.TemplateResponse("home.html", {"request": request, "table": table_html, "filename": file.filename})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8500, reload=True)