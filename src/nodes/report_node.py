from typing import Dict, Any

def report_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node responsibility: Format the final evaluated_ideas into a comprehensive
    Markdown report for the user.
    """
    print("---GENERATING FINAL REPORT---")
    ideas = state.get("evaluated_ideas", [])
    
    report = "# Requirements Discovery Report\n\n"
    report += "Here are the top business opportunities that match your specific technical profile and expertise:\n\n"
    
    for idx, idea in enumerate(ideas, 1):
        report += f"## {idx}. {idea['idea']}\n"
        report += f"- **Match Score:** {idea['match_score']}/100\n"
        report += f"- **Why you:** {idea['reason']}\n"
        report += f"- **Profitability:** {idea['profitability']}\n\n"
    
    # Save report to a file eventually, but for now just return it
    
    with open("final_report.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print("Report saved to final_report.md")
    
    return {"final_report": report}
