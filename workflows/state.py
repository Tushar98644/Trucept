from typing import TypedDict, List, Dict

class AnalysisState(TypedDict):
    slides_content: List[Dict]          
    chunks: List[str]
    chunk_analyses: List[str]
    final_analysis: str
