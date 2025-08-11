from google import genai
from google.genai import types
from config.settings import settings
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import List, Dict

class AIAnalyzer:    
    def __init__(self):
        self.client = self.setup_client()
    
    def setup_client(self):
        api_key = settings.google_api_key.get_secret_value()
        if not api_key or api_key == 'API_KEY':
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
        return genai.Client(api_key=api_key)
    
    def chunk_text(self, text: str, max_chars: int = 8000) -> List[str]:
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + max_chars, len(text))
            
            if end < len(text):
                newline = text.rfind('\n', start, end)
                if newline > start + 100:
                    end = newline
            
            chunks.append(text[start:end])
            start = end
        
        return chunks
    
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def call_ai(self, prompt: str) -> str:
        """Call AI with retry logic - 3 attempts with exponential backoff"""
        try:
            print(f"🔄 Calling Gemini API...")
            response = self.client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.gemini_temperature,
                    max_output_tokens=settings.gemini_max_output_tokens,
                )
            )
            return response.text if hasattr(response, 'text') else str(response)
        
        except Exception as e:
            print(f"⚠️ API call failed: {str(e)}")
            raise 
    
    def analyze_with_genai(self, slides_content: List[Dict]) -> str:
        combined_text = ""
        for slide in slides_content:
            combined_text += f"\n--- SLIDE {slide['slide_number']} ---\n{slide['content']}\n"
        
        prompt_template = (
            "Find factual or logical inconsistencies in this presentation:\n\n"
            "Look for:\n"
            "1) Numerical conflicts (same metric, different values)\n"
            "2) Contradictory statements\n"
            "3) Timeline mismatches\n"
            "4) Logic problems\n\n"
            "Format response as:\n"
            "ANALYSIS RESULTS:\n"
            "Issues Found: [number]\n\n"
            "Issue 1: [Type]\n"
            "- Slides: [numbers]\n"
            "- Description: [explanation]\n"
            "- Details: [specifics]\n"
            "- Severity: [High/Medium/Low]\n\n"
            "If no issues: 'Issues Found: 0 - No significant inconsistencies detected.'\n\n"
            "Content:\n\n"
        )
        
        chunks = self.chunk_text(combined_text)
        results = []
        
        for i, chunk in enumerate(chunks, 1):
            print(f"📡 Analyzing chunk {i}/{len(chunks)} ({len(chunk)} chars)")
            try:
                prompt = prompt_template + chunk
                result = self.call_ai(prompt)
                results.append(result)
                print(f"✅ Chunk {i} completed successfully")
            except Exception as e:
                print(f"❌ Chunk {i} failed after 3 retries: {str(e)}")
                results.append(f"❌ Chunk {i} analysis failed: {str(e)}")
        
        if len(results) == 1:
            return results[0]
        else:
            return f"Analysis from {len(chunks)} chunks:\n\n" + "\n\n--- NEXT CHUNK ---\n\n".join(results)

def analyze_inconsistencies(slides_content: List[Dict]) -> str:
    try:
        analyzer = AIAnalyzer()
        return analyzer.analyze_with_genai(slides_content)
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"