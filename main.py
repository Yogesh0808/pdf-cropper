from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uuid
from convert import convert_pdf_to_tiff
import io

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    filename = file.filename
    base_name = os.path.splitext(filename)[0]

    # Save uploaded PDF to disk
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Convert PDF to TIFF and get BytesIO buffer
    tiff_bytes = convert_pdf_to_tiff(input_path)

    # Return as a streaming response (no saving)
    return StreamingResponse(
        io.BytesIO(tiff_bytes),
        media_type="image/tiff",
        headers={
            "Content-Disposition": f"attachment; filename={base_name}.tiff"
        }
    )