"""
Utility functions for the BrandTone application.
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(
    prompt: str, 
    model: str = "gpt-4o", 
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    Call OpenAI API with a prompt and return the response.
    
    Args:
        prompt: The prompt to send to OpenAI.
        model: The model to use.
        temperature: The sampling temperature.
        max_tokens: The maximum number of tokens to generate.
        
    Returns:
        The generated text.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional writer specializing in brand voice adaptation."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

def save_result(content: str, format_type: str = "txt", file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Save the result to a file.
    
    Args:
        content: The content to save.
        format_type: The format to save in (txt or json).
        file_path: The path to save to. If None, a default path will be used.
        
    Returns:
        Dictionary containing status and file path.
    """
    if file_path is None:
        # Create a timestamped filename
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"brandtone_result_{timestamp}.{format_type}"
    
    try:
        path = Path(file_path)
        
        if format_type.lower() == "json":
            with open(path, 'w') as f:
                json.dump({"content": content}, f, indent=2)
        else:
            with open(path, 'w') as f:
                f.write(content)
                
        return {"status": "success", "file_path": str(path.absolute())}
    except Exception as e:
        return {"status": "error", "message": str(e)}
