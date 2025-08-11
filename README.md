# Trucept

**AI-Powered PowerPoint Inconsistency Detector**

Trucept is a command-line Python tool (and agent) that analyzes PowerPoint (.pptx) presentations to automatically detect factual, numerical, logical, or temporal inconsistencies across slides — powered by Google Gemini (GenAI).

##  Features

- **Numerical consistency checks** (e.g., mismatched revenue figures, percentages)
- **Textual contradiction detection** (e.g., conflicting claims across slides)
- **Timeline mismatch analysis** (dates or sequences that don't align)
- Leverages **Google Gemini-2.5-Flash** for intelligent content analysis  
- **Modular design**: Integrates clean extraction, AI interaction, and tooling
- **Structured Reports** - Markdown output with severity classification and extraction data

## Installation

Clone the repository:
```bash
git clone https://github.com/Tushar98644/Trucept.git .
```

Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Copy the .env.example to .env:
```bash
cp .env.example .env
```

Add your Google GenAI API Key to the .env file:
```bash
GOOGLE_API_KEY=your_api_key_here
```
Get your API key: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

To analyze the default test.pptx:
```bash
python main.py
```

To analyze a custom PowerPoint file:
```bash
python main.py path/to/presentation
```

## Environment Variables:

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `GOOGLE_API_KEY` | Your Google GenAI API key | **Required** |
| `GEMINI_MODEL` | Model version | `gemini-2.5-flash` |
| `GEMINI_TEMPERATURE` | Sampling temperature | `0` |
| `GEMINI_MAX_OUTPUT_TOKENS` | Maximum output tokens | `20000` |

## Sample Output
```yaml
ANALYSIS RESULTS:
Issues Found: 1

Issue 1: Numerical Conflict
- Slides: 2, 3
- Description: Conflicting revenue data for Q1 appears across slides.
- Details: Slide 2 shows "$2M", while slide 3 indicates "$2.5M".
- Severity: Medium
```

Analysis results are automatically saved as structured markdown reports in the `results/` directory.

## Documentation

> **For developers**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete system design details and extension points.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch `git checkout -b feat/amazing-feature`
3. Commit using [Conventional Commits](https://conventionalcommits.org/) `git commit -m 'feat: add amazing feature'`
4. Submit a pull request `git push origin feat/amazing-feature`

## License

This project is under the GPL-3.0 License - see the [LICENSE](https://github.com/Tushar98644/Trucept/blob/main/LICENSE) file for details.
