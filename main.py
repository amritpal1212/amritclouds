from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime
import aiofiles
import json
from models import File as FileModel
from database import SessionLocal, engine, Base
import hashlib
import uuid
from sqlalchemy import func

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudSync API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://amritclouds.web.app",
        "https://amritclouds.firebaseapp.com",
        "http://localhost:3000"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Store file metadata
files = []

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

async def save_upload_file(upload_file: UploadFile, destination: str):
    """Save uploaded file asynchronously"""
    async with aiofiles.open(destination, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)

@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """Upload multiple files"""
    uploaded_files = []
    
    for file in files:
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
            
            # Calculate file hash
            file_hash = calculate_file_hash(file_path)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create database entry
            db_file = FileModel(
                filename=file.filename,
                file_path=file_path,
                file_type=file.content_type,
                file_size=file_size,
                upload_date=datetime.now(),
                file_hash=file_hash
            )
            
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            
            uploaded_files.append({
                "id": db_file.id,
                "filename": db_file.filename,
                "file_type": db_file.file_type,
                "file_size": db_file.file_size,
                "upload_date": db_file.upload_date.isoformat()
            })
            
        except Exception as e:
            # If there's an error, delete the file if it was created
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Files uploaded successfully", "files": uploaded_files}

@app.get("/api/files")
def get_files(db: Session = Depends(get_db)):
    """Get all files"""
    files = db.query(FileModel).all()
    return [
        {
            "id": file.id,
            "filename": file.filename,
            "file_type": file.file_type,
            "file_size": file.file_size,
            "upload_date": file.upload_date.isoformat()
        }
        for file in files
    ]

@app.get("/api/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """Download a file by ID"""
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        file.file_path,
        filename=file.filename,
        media_type=file.file_type
    )

@app.delete("/api/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """Delete a file by ID"""
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Delete file from storage
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
        
        # Delete from database
        db.delete(file)
        db.commit()
        
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/storage")
def get_storage_info(db: Session = Depends(get_db)):
    """Get storage information"""
    total_files = db.query(FileModel).count()
    total_size = db.query(FileModel).with_entities(func.sum(FileModel.file_size)).scalar() or 0
    
    # Get storage limits (you can modify these values)
    storage_limit = 1024 * 1024 * 1024  # 1 GB
    max_file_size = 100 * 1024 * 1024  # 100 MB
    
    return {
        "total_files": total_files,
        "total_size": total_size,
        "storage_limit": storage_limit,
        "max_file_size": max_file_size,
        "used_percentage": (total_size / storage_limit) * 100 if storage_limit > 0 else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 