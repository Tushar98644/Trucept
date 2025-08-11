import os
from typing import List, Dict

def validate_file(filename: str, supported_formats: List[str]):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' not found")
    
    _, ext = os.path.splitext(filename)
    if ext.lower() not in supported_formats:
        raise ValueError(f"Unsupported format: {ext}")

def combine_content(extracted_content: List[Dict]) -> str:
    combined = []
    
    for item in extracted_content:
        content_type = item['type']
        content = item['content']
        
        if content and content.strip():
            if content_type == 'table':
                combined.append(f"[TABLE]\n{content}")
            elif content_type == 'chart':
                combined.append(f"[CHART]\n{content}")
            else:
                combined.append(content)
    
    return '\n\n'.join(combined)

def identify_shape_type(shape) -> str:
    if hasattr(shape, 'has_table') and shape.has_table:
        return 'table'
    
    elif hasattr(shape, 'has_chart') and shape.has_chart:
        return 'chart'
    
    elif hasattr(shape, 'shape_type') and 'SMART_ART' in str(shape.shape_type):
        return 'smartart'
    
    elif hasattr(shape, 'text') and shape.text.strip():
        return 'text'
    
    elif hasattr(shape, 'text_frame') and shape.text_frame.text.strip():
        return 'textbox'
    
    elif hasattr(shape, 'image'):
        return 'image'
    
    else:
        return 'unknown'