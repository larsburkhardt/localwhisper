import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import json

from .transcribe import Transcriber
from .markdown_export import generate_markdown, save_markdown

app = FastAPI(title="LocalWhisper Transcriber")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

for d in [MODELS_DIR, EXPORTS_DIR, UPLOAD_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

transcriber = Transcriber(model_dir=MODELS_DIR)

# Transcription status storage (in-memory for now)
transcription_status = {}

class ModelInfo(BaseModel):
    name: str
    local: bool

@app.get("/api/models", response_model=List[ModelInfo])
async def get_models():
    return transcriber.get_available_models()

@app.post("/api/transcribe")
async def start_transcription(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model: str = Form("base"),
    language: Optional[str] = Form(None)
):
    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    transcription_status[job_id] = {
        "status": "pending",
        "progress": 0,
        "filename": file.filename,
        "model": model,
        "language": language,
        "result": None
    }
    
    background_tasks.add_task(run_transcription, job_id, file_path, model, language)
    
    return {"job_id": job_id}

async def run_transcription(job_id, file_path, model, language):
    try:
        transcription_status[job_id]["status"] = "processing"
        
        def progress_callback(progress, text):
            transcription_status[job_id]["progress"] = progress
            transcription_status[job_id]["current_text"] = text

        result = transcriber.transcribe(
            file_path, 
            model_name=model, 
            language=language, 
            progress_callback=progress_callback
        )
        
        transcription_status[job_id]["status"] = "completed"
        transcription_status[job_id]["progress"] = 100
        transcription_status[job_id]["result"] = result
        
        # Clean up uploaded file
        # os.remove(file_path)
        
    except Exception as e:
        print(f"Transcription error: {e}")
        transcription_status[job_id]["status"] = "failed"
        transcription_status[job_id]["error"] = str(e)

@app.get("/api/transcribe/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in transcription_status:
        raise HTTPException(status_code=404, detail="Job not found")
    return transcription_status[job_id]

@app.post("/api/export")
async def export_transcription(job_id: str = Form(...), edited_text: Optional[str] = Form(None)):
    if job_id not in transcription_status or transcription_status[job_id]["status"] != "completed":
        raise HTTPException(status_code=400, detail="Transcription not completed")
    
    job_data = transcription_status[job_id]
    result = job_data["result"]
    
    if edited_text:
        result["text"] = edited_text
        
    md_content = generate_markdown(result, job_data["filename"])
    
    filename_no_ext = os.path.splitext(job_data["filename"])[0]
    export_filename = f"{filename_no_ext}_transkript.md"
    export_path = os.path.join(EXPORTS_DIR, export_filename)
    
    save_markdown(md_content, export_path)
    
    return {"filename": export_filename, "content": md_content, "path": export_path}

@app.get("/api/system")
async def get_system_info():
    import torch
    import multiprocessing
    import psutil
    
    gpu_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if gpu_available else None
    
    return {
        "gpu_detected": gpu_available,
        "gpu_name": gpu_name,
        "cpu_cores": multiprocessing.cpu_count(),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2)
    }

# Serve frontend
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
