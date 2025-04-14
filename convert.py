import fitz  # PyMuPDF
from PIL import Image
import io

def convert_pdf_to_tiff(input_pdf_path):
    doc = fitz.open(input_pdf_path)
    page = doc[0]  # Single-page PDF

    zoom = 300 / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    bw_img = img.convert("L").point(lambda x: 0 if x < 128 else 255, mode='1')

    # Save to in-memory buffer
    buffer = io.BytesIO()
    bw_img.save(buffer, format="TIFF", compression="tiff_lzw")
    buffer.seek(0)

    return buffer.read()
