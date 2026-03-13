import os
import sys
import json
from dotenv import load_dotenv

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agent import create_discovery_agent

def main():
    load_dotenv()
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No topic provided"}))
        return

    topic = sys.argv[1]
    user_profile = sys.argv[2] if len(sys.argv) > 2 else "Experienced software developer."
    
    try:
        agent = create_discovery_agent()
        
        initial_state = {
            "search_query": topic,
            "user_profile": user_profile,
            "raw_data": [],
            "identified_needs": [],
            "evaluated_ideas": [],
            "final_report": ""
        }
        
        # Use invoke to get final result
        result = agent.invoke(initial_state)
        
        # Output clean JSON for the web bridge
        output = {
            "identified_needs": result.get("identified_needs", []),
            "evaluated_ideas": result.get("evaluated_ideas", []),
            "final_report": result.get("final_report", "")
        }
        print(json.dumps(output))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
