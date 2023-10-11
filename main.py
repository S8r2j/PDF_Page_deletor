from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import FileResponse
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

app = FastAPI()

@app.post("/uploadpdf/")
async def upload_pdf(file: UploadFile, page_number: int = Query(..., description="Page number to delete")):
    # Check if the uploaded file is a PDF
    if not file.filename.endswith('.pdf'):
        return {"error": "Only PDF files are allowed."}

    # Save the uploaded file
    with open(file.filename, "wb") as pdf_file:
        pdf_file.write(file.file.read())

    # Validate the provided page number
    if page_number < 1:
        return {"error": "Invalid page number. Must be greater than or equal to 1."}

    pdf_reader = PdfReader(file.filename)

    # Check if the specified page number exists
    if page_number <= len(pdf_reader.pages):
        pdf_writer = PdfWriter()
        for page_num, page in enumerate(pdf_reader.pages, start=1):
            if page_num != page_number:
                pdf_writer.add_page(page)

        # Save the modified PDF to a new file
        new_pdf_filename = f"modified_{file.filename}"
        with open(new_pdf_filename, 'wb') as new_pdf_file:
            pdf_writer.write(new_pdf_file)

        return FileResponse(new_pdf_filename, headers={"Content-Disposition": "attachment; filename=modified.pdf"})
    else:
        return {"error": "Page number exceeds the number of pages in the PDF."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
