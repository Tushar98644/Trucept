import sys
from extractors import extract_presentation
from analyzers import analyze_inconsistencies
from config.settings import settings

def main():
    print("🚀 AI-Powered PowerPoint Inconsistency Detector")
    print("🤖 Using Google Gemini Flash")
    print("="*60)
    
    try:
        api_key = settings.google_api_key.get_secret_value()
        print(f"🔑 API Key status: {'✅ Set' if api_key and api_key != 'YOUR_API_KEY_HERE' else '❌ Missing'}")
        if api_key:
            print(f"🔑 API Key preview: {api_key[:10]}...{api_key[-4:]}")
    except Exception as e:
        print(f"❌ API Key error: {e}")
        return
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "test.pptx"
        print(f"💡 No file specified, using default: {filename}")
    
    try:
        print(f"📁 Extracting content from {filename}...")
        slides_content = extract_presentation(filename)
        
        print("\n🤖 Analyzing with Google Gemini...")
        ai_results = analyze_inconsistencies(slides_content)  # Now works correctly!
        print(ai_results)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Set your API key: export GOOGLE_API_KEY='api-key'")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
