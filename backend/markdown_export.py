import os
from datetime import datetime

def generate_markdown(transcription_data, original_filename):
    """
    Generates a Markdown string with YAML frontmatter.
    """
    title = os.path.splitext(original_filename)[0]
    date_iso = datetime.now().isoformat()
    language = transcription_data.get("language", "unknown")
    model = transcription_data.get("model", "unknown")
    text = transcription_data.get("text", "")
    
    # Structure the text into paragraphs
    # For now, we'll just split by common sentence endings and group them
    # In a more advanced version, we could use NLP or Whisper's segment info
    paragraphs = []
    current_paragraph = []
    sentences = text.split(". ")
    
    for i, sentence in enumerate(sentences):
        current_paragraph.append(sentence)
        # Every 5 sentences or so, start a new paragraph
        if (i + 1) % 5 == 0:
            paragraphs.append(". ".join(current_paragraph) + ".")
            current_paragraph = []
            
    if current_paragraph:
        paragraphs.append(". ".join(current_paragraph) + ".")
        
    formatted_text = "\n\n".join(paragraphs)
    
    # Build the Markdown content
    md_content = f"""---
title: "{title}"
date: "{date_iso}"
source: "{original_filename}"
language: "{language}"
model: "{model}"
tags: [transkription]
---

{formatted_text}
"""
    return md_content

def save_markdown(md_content, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    return output_path
