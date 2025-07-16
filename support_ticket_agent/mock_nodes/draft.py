def mock_draft(state_dict):
    category = state_dict["category"]
    if category == "billing":
        return {"draft": "I understand your concern about the refund. I'll help you track down the status of your refund right away."}
    elif category == "technical":
        return {"draft": "I see you're experiencing technical difficulties. Let's resolve this with some troubleshooting steps."}
    elif category == "security":
        return {"draft": "I understand your security concerns. Let's secure your account immediately with some preventive measures."}
    return {"draft": "Thank you for reaching out. I'll guide you through this process step by step."}
