import os
import time
from faster_whisper import WhisperModel
import torch

class Transcriber:
    def __init__(self, model_dir="./models"):
        self.model_dir = model_dir
        self.current_model = None
        self.current_model_name = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "int8"
        
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    def get_available_models(self):
        # List of models we support
        models = ["tiny", "base", "small", "medium", "large-v3"]
        result = []
        for m in models:
            # Check if model is downloaded
            # faster-whisper models are usually in subdirectories
            model_path = os.path.join(self.model_dir, f"models--systran--faster-whisper-{m}")
            is_local = os.path.exists(model_path)
            result.append({"name": m, "local": is_local})
        return result

    def load_model(self, model_name):
        if self.current_model_name == model_name and self.current_model is not None:
            return self.current_model
        
        print(f"Loading model {model_name} on {self.device} with {self.compute_type}...")
        self.current_model = WhisperModel(
            model_name, 
            device=self.device, 
            compute_type=self.compute_type,
            download_root=self.model_dir
        )
        self.current_model_name = model_name
        return self.current_model

    def transcribe(self, file_path, model_name="base", language=None, progress_callback=None):
        model = self.load_model(model_name)
        
        segments, info = model.transcribe(file_path, beam_size=5, language=language)
        
        print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")
        
        full_text = []
        # info.duration is the total duration in seconds
        total_duration = info.duration
        
        for segment in segments:
            full_text.append(segment.text.strip())
            if progress_callback:
                # Calculate progress based on segment end time
                progress = min(100, int((segment.end / total_duration) * 100))
                progress_callback(progress, segment.text)
                
        return {
            "text": " ".join(full_text),
            "language": info.language,
            "duration": info.duration,
            "model": model_name
        }
