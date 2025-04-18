import fitz  # PyMuPDF
from PIL import Image
import os

def convert_pdf_to_tiff(input_pdf_path):
    doc = fitz.open(input_pdf_path)
    page = doc[0]

    zoom = 300 / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    bw_img = img.convert("L").point(lambda x: 0 if x < 128 else 255, mode='1')

    # Save TIFF temporarily
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    output_path = os.path.join("uploads", f"{base_name}.tiff")
    bw_img.save(output_path, format="TIFF", compression="tiff_lzw")

    return output_path
