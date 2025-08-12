from langgraph.graph import StateGraph, END
from .state import AnalysisState
from .nodes import chunk_content_node, analyze_chunk_node, cross_chunk_analysis_node

def create_analysis_workflow():    
    workflow = StateGraph(AnalysisState)
    
    workflow.add_node("chunk_content", chunk_content_node)
    workflow.add_node("analyze_chunks", analyze_chunk_node)
    workflow.add_node("cross_chunk_analysis", cross_chunk_analysis_node)
    
    workflow.set_entry_point("chunk_content")
    workflow.add_edge("chunk_content", "analyze_chunks")
    workflow.add_edge("analyze_chunks", "cross_chunk_analysis")
    workflow.add_edge("cross_chunk_analysis", END)
    
    return workflow.compile()

def analyze_with_langgraph(slides_content):
    app = create_analysis_workflow()
    
    initial_state = {
        "slides_content": slides_content,
        "chunks": [],
        "chunk_analyses": [],
        "final_analysis": ""
    }
    
    print("🚀 Starting LangGraph analysis...")
    result = app.invoke(initial_state)
    
    if len(result["chunks"]) == 1:
        print("✅ Single chunk detected - using direct analysis result")
        return result["chunk_analyses"][0].replace("Chunk 1 Analysis:\n", "")
    
    return result["final_analysis"]