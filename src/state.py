from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """
    State of the Requirements Discovery Agent.
    This state will be passed around and updated by each node in the LangGraph.
    """
    search_query: str
    user_profile: str
    raw_data: List[Dict[str, Any]]
    identified_needs: List[Dict[str, Any]]
    evaluated_ideas: List[Dict[str, Any]]
    final_report: str
