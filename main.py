from pptx import Presentation

from extractors import extract_numbers

def analyze_file(filename):
    print(f"Analyzing file: {filename}")
    try:
        presentation = Presentation(filename)
        print(f"📊 Found {len(presentation.slides)} slides")
        
        slides_data = []
        for slide_num,slide in enumerate(presentation.slides):
            print(f"📄 Reading Slide {slide_num}:")
            slide_text = []

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    print(f"   • {shape.text}")
                    slide_text.append(shape.text.strip())
            
            all_text = " ".join(slide_text)
            numbers = extract_numbers(all_text)
            print(f"🔢 Numbers found: {numbers}")

            slides_data.append({
                "slide": slide_num,
                "text": all_text,
                "numbers": numbers
            })

            print(slides_data)
        return "File analyzed successfully"
    
    except Exception as error:
        print(f"❌ Error reading file: {error}")
        return "❌ Failed to read PowerPoint"

def main():
    print("🚀 Starting PowerPoint Analyzer")

    result = analyze_file("test.pptx")
    print(result)

    print("✅ Done!")

if __name__ == "__main__":
    main()