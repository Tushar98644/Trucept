from pptx import Presentation
from typing import List, Dict
import os

class PowerPointExtractor:
    """Efficient PowerPoint content extractor"""
    
    def __init__(self):
        self.supported_formats = ['.pptx']
    
    def validate_file(self, filename: str) -> bool:
        """Validate file exists and is supported format"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found")
        
        _, ext = os.path.splitext(filename)
        if ext.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported format: {ext}")
        
        return True
    
    def extract_content(self, filename: str) -> List[Dict]:
        """Extract content from PowerPoint slides"""
        self.validate_file(filename)
        
        presentation = Presentation(filename)
        slides_content = []
        
        for slide_num, slide in enumerate(presentation.slides, 1):
            slide_text = []
            
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text.strip())
            
            content = '\n'.join(slide_text) if slide_text else "[No text content]"
            
            slides_content.append({
                'slide_number': slide_num,
                'content': content,
                'text_elements': len(slide_text)
            })

        print(f"✅ Extracted content from {len(slides_content)} slides: {slides_content}") 
        return slides_content

def extract_presentation(filename: str) -> List[Dict]:
    """Simple function to extract PowerPoint content"""
    extractor = PowerPointExtractor()
    return extractor.extract_content(filename)