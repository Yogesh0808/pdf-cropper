from fastapi import FastAPI, Request, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uuid
import io
from convert import convert_pdf_to_tiff

app = FastAPI()

# Folder for temporary uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Clean up function after conversion
def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)


# Homepage with web upload form
@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route for web upload via HTML form
@app.post("/upload/")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    filename = file.filename
    base_name = os.path.splitext(filename)[0]
    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Convert PDF to TIFF
    tiff_bytes = convert_pdf_to_tiff(input_path)

    # Schedule cleanup
    background_tasks.add_task(remove_file, input_path)

    return StreamingResponse(
        io.BytesIO(tiff_bytes),
        media_type="image/tiff",
        headers={"Content-Disposition": f"attachment; filename={base_name}.tiff"}
    )


# API endpoint for external/bot-based PDF uploads
@app.post("/api/convert/")
async def api_convert_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    filename = file.filename
    base_name = os.path.splitext(filename)[0]
    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Convert PDF to TIFF
    tiff_bytes = convert_pdf_to_tiff(input_path)

    # Schedule cleanup
    background_tasks.add_task(remove_file, input_path)

    return StreamingResponse(
        io.BytesIO(tiff_bytes),
        media_type="image/tiff",
        headers={"Content-Disposition": f"attachment; filename={base_name}.tiff"}
    )
