from pptx import Presentation

def analyze_file(filename):
    print(f"Analyzing file: {filename}")
    try:
        presentation = Presentation(filename)
        print(f"📊 Found {len(presentation.slides)} slides")

        for slide_num,slide in enumerate(presentation.slides):
            print(f"📄 Reading Slide {slide_num}:")

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    print(f"   • {shape.text}")

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