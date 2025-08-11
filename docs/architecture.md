# System Architecture

## Table of Contents

- [Design Philosophy](#design-philosophy)
- [Component Architecture](#component-architecture)
- [Processing Pipeline](#processing-pipeline)
- [Scalability Strategy](#scalability-strategy)
- [Error Handling](#error-handling)
- [Configuration Management](#configuration-management)
- [Content Handler Architecture](#content-handler-architecture)
- [Data Flow Architecture](#data-flow-architecture)
- [Development Architecture](#development-architecture)
- [Limitations](#limitations)
- [Extension Points](#extension-points)

## Design Philosophy

### Core Principles

- **Modularity** - Each component has single, well-defined responsibility
- **Scalability** - Handles presentations from 1 to 100+ slides efficiently
- **Robustness** - Graceful error handling and recovery
- **Extensibility** - Easy to add new content types and analysis features

### COMPONENT ARCHITECTURE

```bash
powerpoint-inconsistency-detector/
├── main.py                    # Entry point and orchestration
├── config/
│   ├── __init__.py
│   └── settings.py           # Environment configuration
├── extractors/
│   ├── __init__.py
│   ├── content_extractor.py  # Main extraction orchestrator
│   ├── content_handlers.py   # Individual content type handlers
│   └── utils.py              # Extraction utilities
├── analyzers/
│   ├── __init__.py
│   └── ai_analyzer.py        # AI-powered inconsistency detection
├── results/                  # Generated analysis reports
└── docs/                     # Project documentation
```

### PROCESSING PIPELINE

1. Content Extraction Phase

   Shape Detection & Classification

   ```python
   for shape in slide.shapes:
       content_type = identify_shape_type(shape)  # Table, Chart, Text, etc.
       handler = get_handler(content_type)
       content = handler.extract(shape)
   ```

   Key Features:

   - Priority-based processing - Tables and charts processed before text
   - Structure preservation - Maintains formatting context
   - Error isolation - Individual shape failures don't break slide processing

2. Content Aggregation

   Combine extracted content with type prefixes

   ```python
   combined_text = combine_content([
       {"type": "text", "content": "Revenue Summary"},
       {"type": "table", "content": "Q1 | $2.5M\nQ2 | $2.2M"}
   ])
   ```

3. AI Analysis Phase

   Intelligent chunking for large presentations

   ```python
   chunks = chunk_text_by_chars(combined_content, max_chars=8000)
   for chunk in chunks:
       result = call_ai_with_retry(chunk)
       results.append(result)
   ```

### SCALABILITY STRATEGY

Memory Management

- Incremental Processing - Slides processed one at a time
- Object Cleanup - Presentation objects released after extraction
- Streaming Approach - Large content streamed through chunking pipeline

API Efficiency

- Connection Reuse - Single client instance across all requests
- Intelligent Chunking - Respects sentence boundaries to preserve context
- Batch Optimization - Multiple chunks processed in sequence

Chunking Algorithm

```python
def chunk_text_by_chars(text: str, max_chars: int = 8000):
    """
    Smart chunking that:
    1. Respects sentence boundaries
    2. Maintains context across chunks
    3. Prevents mid-word splitting
    4. Handles large presentations efficiently
    """
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
```

### ERROR HANDLING

Multi-Level Error Handling

Shape Level:

- Individual shape extraction failures don't stop slide processing
- Detailed error logging for debugging
- Fallback content for unsupported shapes

Slide Level:

- Slide processing failures don't stop presentation analysis
- Graceful degradation with partial results
- Continue processing remaining slides

**Example error handling pattern:**

```python
try:
    content = extract_shape_content(shape)
except Exception as e:
    log_error(f"Shape extraction failed: {e}")
    content = f"[Error: Could not extract {shape.shape_type}]"
```

### CONFIGURATION MANAGEMENT

Environment-Based Settings

```python
class Settings(BaseSettings):
    google_api_key: SecretStr
    gemini_model: str = 'gemini-1.5-flash'
    temperature: float = 0.1
    max_output_tokens: int = 1500

    class Config:
        env_file = ".env"
```

### CONTENT HANDLER ARCHITECTURE

Handler Registry Pattern

```python
CONTENT_HANDLERS = {
    'text': extract_text,
    'table': extract_table,
    'chart': extract_chart,
    'image': extract_image,
    'smartart': extract_smartart,
    'textbox': extract_textbox
}

def get_handler(content_type: str):
    return CONTENT_HANDLERS.get(content_type, extract_text)
```

Handler Characteristics

- Stateless - No shared state between extractions
- Focused - Single content type per handler
- Extensible - Easy to add new content types

### DATA FLOW ARCHITECTURE

```bash
PowerPoint File (.pptx)
         ↓
   File Validation
         ↓
   Slide Iteration
         ↓
   Shape Detection
         ↓
   Content Extraction
         ↓
   Content Aggregation
         ↓
   Text Chunking
         ↓
   AI Analysis (Multiple API Calls)
         ↓
   Result Aggregation
         ↓
   Markdown Report Generation
         ↓
   File Output (results/*.md)
```

### DEVELOPMENT ARCHITECTURE

Code Organization Principles

- Single Responsibility - Each function/class has one job
- Dependency Injection - Configuration passed in, not hardcoded
- Error Boundaries - Failures contained to specific components
- Logging Strategy - Structured logging for debugging

### Limitations

- No Video/Audio Support - Cannot extract content from embedded videos or audio files
- Embedded Object Limitations - Cannot process PDFs, Excel files, or other embedded documents
- Cross-Chunk Context Loss - Each chunk analyzed independently, may miss inconsistencies spanning multiple chunks (e.g., slide 1 vs slide 49)
- Single-Threaded Processing - Cannot process multiple presentations or chunks concurrently
- No Caching - Repeated analysis of same content makes full API calls each time
- Memory Limitations - Large presentations (100+ slides) may consume significant memory
- No Partial Results - Complete analysis failure if any chunk processing fails
- Network Timeout - No handling for slow network connections or timeouts

### EXTENSION POINTS

Adding New Content Types

1. Add handler function

```python
def extract_video(shape) -> str:
    return f"[Video: {shape.name}]"
```

2. Register in CONTENT_HANDLERS

```python
CONTENT_HANDLERS['video'] = extract_video
```

3. Update shape detection logic

```python
elif hasattr(shape, 'media_type') and 'video' in shape.media_type:
    return 'video'
```

**Custom Analysis Rules**

Extend AI Analyzer for domain-specific rules
class CustomAnalyzer(AI Analyzer):

```python
    def add_custom_prompt(self, domain_rules: str):
        self.base_prompt += f"\nAdditional Rules:\n{domain_rules}"
```