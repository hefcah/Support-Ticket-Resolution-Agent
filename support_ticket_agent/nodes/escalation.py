import csv
from datetime import datetime
from typing import Dict, Any
from langchain_core.runnables import RunnableLambda

def log_to_csv(state: Dict[str, Any]) -> None:
    """Log escalated tickets to a CSV file."""
    filename = "escalation_log.csv"
    headers = ["timestamp", "category", "subject", "description", "drafts", "feedbacks"]
    
    # Create file with headers if it doesn't exist
    try:
        with open(filename, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    except FileExistsError:
        pass
    
    # Append the escalation
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            state["category"],
            state["ticket"]["subject"],
            state["ticket"]["description"],
            ";".join(state["drafts"]),
            ";".join(state["feedbacks"])
        ])

def escalate(state: Dict[str, Any]) -> Dict[str, str]:
    """Handles escalation when multiple draft attempts have failed."""
    # Log to CSV
    log_to_csv(state)
    
    escalation_message = f"""
     ESCALATED TO HUMAN AGENT 
    
    Ticket could not be automatically resolved after {state["attempts"]} attempts.
    
    Category: {state["category"]}
    Subject: {state["ticket"]["subject"]}
    Description: {state["ticket"]["description"]}
    
    Draft Attempts: {len(state["drafts"])}
    Last Draft: {state["drafts"][-1]}
    
    Review Feedback:
    {chr(10).join(f'- {feedback}' for feedback in state["feedbacks"])}
    
    This ticket requires human review and intervention.
    """
    
    return {"final_response": escalation_message}
