from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from convert import convert_pdf_to_tiff
import io

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    filename = file.filename
    base_name = os.path.splitext(filename)[0]

    # Save uploaded PDF
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Convert to TIFF and read from file
    tiff_path = convert_pdf_to_tiff(input_path)  # this returns path now

    # Stream it back
    return StreamingResponse(
        open(tiff_path, "rb"),
        media_type="image/tiff",
        headers={"Content-Disposition": f"attachment; filename={base_name}.tiff"}
    )
