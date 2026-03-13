import os
import requests
from typing import Dict, Any

def search_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node responsibility: Search the internet for user complaints, feature requests,
    and pain points. Uses DuckDuckGo (free, no API key needed) as the primary engine,
    with Gemini Grounding with Google Search as a fallback.
    """
    print("---SEARCHING FOR PAIN POINTS---")
    query = state.get("search_query", "")
    
    raw_data = []
    
    # --- Strategy 1: DuckDuckGo (Free, no API key needed) ---
    try:
        from ddgs import DDGS
        
        # Search multiple targeted queries to get diverse results
        search_queries = [
            f"{query} site:reddit.com",
            f"developer tools pain points frustrations site:reddit.com",
            f"I wish there was a tool software complaint site:reddit.com",
            f"what software tools are missing gap market site:news.ycombinator.com",
            f"underserved software niche opportunity",
        ]
        
        ddgs = DDGS()
        for sq in search_queries:
            try:
                results = ddgs.text(sq, max_results=5)
                for r in results:
                    raw_data.append({
                        "source": r.get("href", "DuckDuckGo"),
                        "title": r.get("title", ""),
                        "content": r.get("body", "")
                    })
            except Exception as inner_e:
                print(f"  Query failed: {inner_e}")
        
        # Deduplicate by title
        seen_titles = set()
        unique_data = []
        for item in raw_data:
            if item["title"] not in seen_titles:
                seen_titles.add(item["title"])
                unique_data.append(item)
        raw_data = unique_data
        
        print(f"[DuckDuckGo] Found {len(raw_data)} unique data points.")
        
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")
    
    # --- Strategy 2: Gemini Grounding with Google Search (Fallback) ---
    if not raw_data:
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        if gemini_api_key:
            try:
                url = f"https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash:generateContent?key={gemini_api_key}"

                search_prompt = (
                    f"Search for: {query} site:reddit.com OR site:news.ycombinator.com OR site:indiehackers.com\n\n"
                    "Find developer complaints, pain points, missing features, and unmet needs. "
                    "For each finding, provide the source URL, a title, and a summary of the complaint/pain point."
                )

                payload = {
                    "contents": [{"role": "user", "parts": [{"text": search_prompt}]}],
                    "tools": [{"googleSearch": {}}],
                    "generationConfig": {"temperature": 0.2},
                }

                resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
                resp.raise_for_status()
                data = resp.json()

                candidate = data.get("candidates", [{}])[0]

                # Extract grounding sources from metadata
                grounding = candidate.get("groundingMetadata", {})
                chunks = grounding.get("groundingChunks", [])
                for chunk in chunks:
                    web = chunk.get("web", {})
                    if web:
                        raw_data.append({
                            "source": web.get("uri", ""),
                            "title": web.get("title", ""),
                            "content": ""
                        })

                # Use the response text as content for the first result
                parts = candidate.get("content", {}).get("parts", [])
                response_text = parts[0].get("text", "") if parts else ""
                if response_text and raw_data:
                    raw_data[0]["content"] = response_text[:2000]
                elif response_text:
                    raw_data.append({
                        "source": "Gemini Google Search",
                        "title": "Search Results",
                        "content": response_text[:2000]
                    })

                # Deduplicate by title
                seen = set()
                unique = []
                for item in raw_data:
                    key = item["title"] or item["source"]
                    if key not in seen:
                        seen.add(key)
                        unique.append(item)
                raw_data = unique

                print(f"[Gemini Grounding Search] Found {len(raw_data)} data points.")

            except Exception as e:
                print(f"Gemini Grounding Search failed: {e}")
    
    # --- Strategy 3: Fallback dummy data ---
    if not raw_data:
        print("Warning: All search engines failed. Using dummy data.")
        raw_data = [
            {"source": "Dummy Reddit", "title": "Dummy Post", "content": "I wish there was a tool that could automatically generate 3D models from my 2D sketches. The current ones are too hard to use."}
        ]
    
    return {"raw_data": raw_data}

