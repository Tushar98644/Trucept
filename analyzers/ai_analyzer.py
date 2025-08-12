from google import genai
from google.genai import types
from config.settings import settings
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import List

class AIAnalyzer:
    def __init__(self):
        self.client = self.setup_client()

    def setup_client(self):
        api_key = settings.google_api_key.get_secret_value()
        if not api_key or api_key == "API_KEY":
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
        return genai.Client(api_key=api_key)

    def chunk_text(self, text: str, max_chars: int = None) -> List[str]:
        max_chars = max_chars or settings.max_chunk_size
    
        if len(text) <= max_chars:
            print(f"✅ Content fits in single chunk ({len(text)}/{max_chars} chars)")
            return [text]
        
        print(f"⚠️ Content too large ({len(text)} chars), splitting into chunks...")
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
        reraise=True,
    )
    def call_ai(self, prompt: str) -> str:
        try:
            if settings.enable_workflow_logging:
                print(f"🤖 Calling Gemini API ({len(prompt)} chars)...")

            response = self.client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.gemini_temperature,
                    max_output_tokens=settings.gemini_max_output_tokens,
                ),
            )
            result = response.text if hasattr(response, "text") else str(response)

            if settings.enable_workflow_logging:
                print(f"✅ API call successful ({len(result)} chars returned)")

            return result

        except Exception as e:
            print(f"⚠️ API call failed: {str(e)}")
            raise
