import os
from dotenv import load_dotenv
from src.agent import create_discovery_agent

def main():
    print("Loading environment variables...")
    load_dotenv()
    
    # Check for required API keys
    required_keys = ["GEMINI_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Error: Missing required environment variables: {', '.join(missing_keys)}")
        print("Please copy .env.example to .env and fill in your keys.")
        return

    print("Initializing Requirements Discovery Agent...")
    agent = create_discovery_agent()
    
    # Define the initial query/direction
    initial_topic = "软件开发者抱怨的工具, 痛点, 缺少的功能"
    print(f"Starting discovery process with topic: {initial_topic}")
    
    user_profile = (
        "- Expert in C++ and Python\n"
        "- Experience in 3D geometry modeling kernel algorithms (ZWSOFT)\n"
        "- Developed, published, and operated an independent C-end desktop application (Jigsaw Designer), familiar with 2D image algorithms, puzzle generation logic, and product operations.\n"
        "- Strong capability in high-performance computing and dealing with complex algorithms."
    )
    
    initial_state = {
        "search_query": initial_topic,
        "user_profile": user_profile,
        "raw_data": [],
        "identified_needs": [],
        "evaluated_ideas": [],
        "final_report": ""
    }
    
    # Run the graph
    print("Agent is running. This may take a while...")
    for output in agent.stream(initial_state):
        # Stream outputs as they complete each node
        for key, value in output.items():
            print(f"Finished node: '{key}'")
            # print(f"Current State update from {key}: {value}")
            print("-" * 40)
            
    print("\n=== FINAL DISCOVERY REPORT ===")
    final_state = output[list(output.keys())[0]] # Get the state from the last node
    # The actual final report string isn't printed here directly unless we extract it
    # We'll print it properly later once the state structure is fully populated.
    print("Check the generated report.")

if __name__ == "__main__":
    main()
