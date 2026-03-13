import os
import json
from typing import Dict, Any
from pydantic import BaseModel, Field

class NeedItem(BaseModel):
    need: str = Field(description="A concise description of the unmet need or pain point.")
    context: str = Field(description="The context or quote explaining why this is a pain point.")

class NeedsExtraction(BaseModel):
    needs: list[NeedItem]

def analyze_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node responsibility: Use Google GenAI SDK to analyze the raw_data and extract
    clear, unmet needs and business pain points.
    """
    print("---ANALYZING RAW DATA---")
    raw_data = state.get("raw_data", [])
    
    if not raw_data:
        print("No raw data to analyze.")
        return {"identified_needs": []}
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not set. Using dummy data for analysis.")
        return {"identified_needs": [
            {"need": "Easy 2D sketch to 3D model generation", "context": "Dummy context for missing API key."}
        ]}
    print(f"DEBUG: Using API Key starting with: {api_key[:5]}...")

    # Prepare data for LLM
    content_str = "\n".join([f"Source: {item.get('source', '')}\nContent: {item.get('content', item.get('title', ''))}\n---" for item in raw_data])

    prompt = (
        "You are an expert product manager and business analyst.\n"
        "Analyze the following raw data scraped from the internet (forums, social media, etc.).\n"
        "Identify distinct, unsolved problems, user pain points, or feature requests.\n"
        "Focus on things people are complaining about or wishing they had.\n\n"
        f"Raw Data:\n{content_str}\n\n"
        "Extract the top needs."
    )

    try:
        # Using stable model name: gemini-1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        schema = {
            "type": "OBJECT",
            "properties": {
                "needs": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "need": {"type": "STRING", "description": "A concise description of the unmet need or pain point."},
                            "context": {"type": "STRING", "description": "The context or quote explaining why this is a pain point."}
                        },
                        "required": ["need", "context"]
                    }
                }
            },
            "required": ["needs"]
        }
        
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
                "responseSchema": schema
            }
        }
        
        # We must import requests if it's not imported at the top
        import requests
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
        if response.status_code != 200:
            print(f"Gemini API Error ({response.status_code}): {response.text}")
        response.raise_for_status()
        
        # Parse JSON
        resp_data = response.json()
        if "candidates" in resp_data and len(resp_data["candidates"]) > 0:
            content_text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
            result_json = json.loads(content_text)
            needs_list = result_json.get("needs", [])
            
            print(f"Extracted {len(needs_list)} structured needs.")
            return {"identified_needs": needs_list}
        else:
            print("No candidates returned from Gemini.")
            return {"identified_needs": []}
        
    except Exception as e:
        print(f"Error during Gemini Analysis: {e}")
        return {"identified_needs": []}
