from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes.search_node import search_node
from src.nodes.analyze_node import analyze_node
from src.nodes.evaluate_node import evaluate_node
from src.nodes.report_node import report_node

def create_discovery_agent():
    """
    Creates and compiles the LangGraph StateGraph for the Requirements Discovery Agent.
    """
    # 1. Initialize the graph with our custom state
    workflow = StateGraph(AgentState)
    
    # 2. Add nodes to the graph
    workflow.add_node("search", search_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("evaluate", evaluate_node)
    workflow.add_node("report", report_node)
    
    # 3. Define the edges (the flow of the application)
    workflow.add_edge(START, "search")
    workflow.add_edge("search", "analyze")
    workflow.add_edge("analyze", "evaluate")
    workflow.add_edge("evaluate", "report")
    workflow.add_edge("report", END)
    
    # 4. Compile the graph
    app = workflow.compile()
    
    return app
