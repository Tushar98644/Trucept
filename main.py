from pptx import Presentation

def say_hello():
    print("Hello from a function!")

def analyze_file(filename):
    print(f"Analyzing file: {filename}")
    return f"Analysis complete for {filename}"

def create_ppt():
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Hello, World!"
    subtitle.text = "python-pptx was here!"
    prs.save("test.pptx")

def main():
    print("🚀 Starting PowerPoint Analyzer")

    say_hello()

    print("🚀 Creating PowerPoint")

    create_ppt()

    print("✅ Done!")

    result = analyze_file("sample.pptx")
    print(result)

    print("✅ Done!")

if __name__ == "__main__":
    main()