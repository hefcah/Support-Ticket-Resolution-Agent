from typing import Dict, Any

def retrieve_context(state: Dict[str, Any]) -> Dict[str, str]:
    """
    Retrieves relevant context based on the ticket category.
    This is a simplified version that returns predefined context.
    """
    category = state["category"].lower()
    
    context_database = {
        "billing": """
        Billing Process:
        1. Refunds are processed within 5-7 business days
        2. Subscription cancellations are immediate
        3. Pro-rated refunds are available for unused time
        """,
        
        "technical": """
        Troubleshooting Steps:
        1. Force close and restart the app
        2. Check for updates
        3. Clear cache and data
        4. Reinstall if needed
        """,
        
        "security": """
        Security Protocols:
        1. Force password reset on suspicious activity
        2. Enable two-factor authentication
        3. Review recent login history
        4. Lock account if necessary
        """,
        
        "general": """
        General Support Info:
        1. Account settings are in user profile
        2. Self-service guides available
        3. 24/7 support for premium users
        """
    }
    
    # Get context based on category, default to empty string if category not found
    context = context_database.get(category, "No specific context available for this category.")
    
    return {"context": context}
