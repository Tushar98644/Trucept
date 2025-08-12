from typing import Dict, Any
from .state import AnalysisState
from analyzers import AIAnalyzer

def chunk_content_node(state: AnalysisState) -> Dict[str, Any]:
    analyzer = AIAnalyzer()
    
    combined_text = ""
    for slide in state["slides_content"]:
        combined_text += f"\n--- SLIDE {slide['slide_number']} ---\n{slide['content']}\n"
    
    chunks = analyzer.chunk_text(combined_text)
    print(f"📦 Created {len(chunks)} chunks for processing")
    
    return {"chunks": chunks}

def analyze_chunk_node(state: AnalysisState) -> Dict[str, Any]:
    analyzer = AIAnalyzer()
    chunk_analyses = []
    
    for i, chunk in enumerate(state["chunks"], 1):
        print(f"🔍 Analyzing chunk {i}/{len(state['chunks'])}")
        
        prompt = (
            "Analyze this presentation content for inconsistencies:\n\n"
            "Look for:\n"
            "1) Numerical conflicts (same metric, different values)\n"
            "2) Contradictory statements\n"
            "3) Timeline mismatches\n"
            "4) Mathematical errors\n\n"
            "Extract and list ANY inconsistencies you find with specific slide references.\n"
            "If no issues in this chunk, respond: 'No inconsistencies found in this chunk.'\n\n"
            f"Content:\n{chunk}"
        )
        
        analysis = analyzer.call_ai(prompt)
        chunk_analyses.append(f"Chunk {i} Analysis:\n{analysis}")
    
    return {"chunk_analyses": chunk_analyses}

def cross_chunk_analysis_node(state: AnalysisState) -> Dict[str, Any]:    
    if len(state["chunks"]) == 1:
        print("✅ Single chunk - no cross-chunk analysis needed")
        analysis = state["chunk_analyses"][0].replace("Chunk 1 Analysis:\n", "")
        return {"final_analysis": analysis}
    
    analyzer = AIAnalyzer()
    all_analyses = "\n\n".join(state["chunk_analyses"])
    
    print(f"🔗 Cross-chunk analysis for {len(state['chunks'])} chunks...")
    
    analyzer = AIAnalyzer()
    
    all_analyses = "\n\n".join(state["chunk_analyses"])
    
    print(f"🔗 Performing cross-chunk conflict analysis...")
    
    prompt = (
        "Review these individual chunk analyses and identify any cross-chunk inconsistencies:\n\n"
        "Focus on:\n"
        "1) Same metrics with different values across different chunks/slides\n"
        "2) Contradictory facts mentioned in different parts\n"
        "3) Timeline conflicts across the presentation\n"
        "4) Any patterns of inconsistency\n\n"
        "Provide a final summary in this format:\n"
        "ANALYSIS RESULTS:\n"
        "Issues Found: [number]\n\n"
        "Issue 1: [Type]\n"
        "- Slides: [numbers]\n"
        "- Description: [explanation]\n"
        "- Details: [specifics]\n"
        "- Severity: [High/Medium/Low]\n\n"
        "If no cross-chunk issues: 'Issues Found: 0 - No significant inconsistencies detected.'\n\n"
        f"Chunk Analyses:\n{all_analyses}"
    )
    
    final_analysis = analyzer.call_ai(prompt)
    return {"final_analysis": final_analysis}