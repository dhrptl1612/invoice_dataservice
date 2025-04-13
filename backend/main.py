from typing import Union

from fastapi import FastAPI,UploadFile,File,HTTPException 
from fastapi.responses import JSONResponse
import os



app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload/")
async def upload_invoice(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the file
    with open(file_location, "wb") as f:
        contents = await file.read()
        f.write(contents)

    return JSONResponse(content={"message": "File uploaded successfully!", "filename": file.filename})