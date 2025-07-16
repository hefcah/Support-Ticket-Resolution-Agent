def mock_classify(state_dict):
    subject = state_dict["subject"].lower()
    if "refund" in subject or "billing" in subject:
        return {"category": "billing"}
    elif "crash" in subject or "error" in subject:
        return {"category": "technical"}
    elif "security" in subject or "suspicious" in subject:
        return {"category": "security"}
    return {"category": "general"}
