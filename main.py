def say_hello():
    print("Hello from a function!")

def analyze_file(filename):
    print(f"Analyzing file: {filename}")
    return f"Analysis complete for {filename}"

def main():
    print("🚀 Starting PowerPoint Analyzer")
    
    say_hello()
    
    result = analyze_file("sample.pptx")
    print(result)
    
    print("✅ Done!")

if __name__ == "__main__":
    main()
