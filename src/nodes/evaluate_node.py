import os
import json
from typing import Dict, Any
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    idea: str = Field(description="The core idea or pain point being evaluated.")
    match_score: int = Field(description="A score from 0 to 100 on how well this matches the user's resources.")
    reason: str = Field(description="Detailed explanation of why it matches (or doesn't match) the user's profile.")
    profitability: str = Field(description="Estimation of profitability (High/Medium/Low) and market reasoning.")

class BatchEvaluation(BaseModel):
    evaluations: list[EvaluationResult]

def evaluate_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node responsibility: Evaluate the identified_needs against the user's specific resources
    """
    print("---EVALUATING BUSINESS VALUE & RESOURCE MATCH---")
    needs = state.get("identified_needs", [])
    
    if not needs:
        print("No needs to evaluate.")
        return {"evaluated_ideas": []}
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not set. Using dummy data for evaluation.")
        return {"evaluated_ideas": [
            {"idea": "Dummy Idea", "match_score": 90, "reason": "Dummy reason", "profitability": "High"}
        ]}

    # Prepare data for LLM
    needs_str = "\n".join([f"- Need: {n['need']}\n  Context: {n['context']}" for n in needs])

    user_profile = (
        "- Expert in C++ and Python\n"
        "- Experience in 3D geometry modeling kernel algorithms (ZWSOFT)\n"
        "- Developed, published, and operated an independent C-end desktop application (Jigsaw Designer), familiar with 2D image algorithms, puzzle generation logic, and product operations.\n"
        "- Strong capability in high-performance computing and dealing with complex algorithms."
    )

    prompt = (
        "You are a strategic business advisor and technical co-founder.\n"
        "Evaluate the following list of user needs/pain points against my exact technical profile.\n"
        f"My Profile:\n{user_profile}\n\n"
        f"The Needs:\n{needs_str}\n\n"
        "For each need, evaluate its business potential and calculate a 'match_score' (0-100).\n"
        "Give high scores (80+) ONLY to ideas where my specific background (C++, 3D Geometry, Image Processing) gives me an unfair advantage and builds a strong moat against typical web developers.\n"
        "Give low scores to generic SaaS ideas (like basic CRUD apps or auth systems).\n"
        "Extract the evaluations."
    )

    try:
        # Using latest available model: gemini-2.5-flash on v1beta
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        schema = {
            "type": "OBJECT",
            "properties": {
                "evaluations": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "idea": {"type": "STRING", "description": "The core idea or pain point being evaluated."},
                            "match_score": {"type": "INTEGER", "description": "A score from 0 to 100 on how well this matches the user's resources."},
                            "reason": {"type": "STRING", "description": "Detailed explanation of why it matches (or doesn't match) the user's profile."},
                            "profitability": {"type": "STRING", "description": "Estimation of profitability (High/Medium/Low) and market reasoning."}
                        },
                        "required": ["idea", "match_score", "reason", "profitability"]
                    }
                }
            },
            "required": ["evaluations"]
        }
        
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
                "responseSchema": schema
            }
        }
        
        import requests
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
        if response.status_code != 200:
            print(f"Gemini API Error ({response.status_code}): {response.text}")
        response.raise_for_status()
        
        resp_data = response.json()
        if "candidates" in resp_data and len(resp_data["candidates"]) > 0:
            content_text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
            result_json = json.loads(content_text)
            evaluations_list = result_json.get("evaluations", [])
            
            # Filter for high match scores (e.g., >= 75) to keep the report focused
            good_ideas = [idea for idea in evaluations_list if idea.get("match_score", 0) >= 75]
            
            print(f"Evaluated {len(evaluations_list)} ideas. Found {len(good_ideas)} high-match ideas.")
            return {"evaluated_ideas": good_ideas}
        else:
            print("No candidates returned from Gemini.")
            return {"evaluated_ideas": []}
        
    except Exception as e:
        print(f"Error during Gemini Evaluation: {e}")
        return {"evaluated_ideas": []}
