import os
from dataclasses import dataclass, field
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from mock_nodes.classify import mock_classify
from mock_nodes.retrieve import mock_retrieve
from mock_nodes.draft import mock_draft
from mock_nodes.review import mock_review
from mock_nodes.escalation import mock_escalate

@dataclass
class SupportState:
    ticket: Dict[str, str]
    subject: str
    description: str
    category: str = ""
    context: str = ""
    draft: str = ""
    review: str = ""
    attempts: int = 0
    drafts: List[str] = field(default_factory=list)
    feedbacks: List[str] = field(default_factory=list)
    final_response: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket": self.ticket,
            "subject": self.subject,
            "description": self.description,
            "category": self.category,
            "context": self.context,
            "draft": self.draft,
            "review": self.review,
            "attempts": self.attempts,
            "drafts": self.drafts,
            "feedbacks": self.feedbacks,
            "final_response": self.final_response
        }

def mock_classify(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    subject = state_dict["subject"].lower()
    if "refund" in subject or "billing" in subject:
        return {"category": "billing"}
    elif "crash" in subject or "error" in subject:
        return {"category": "technical"}
    elif "security" in subject or "suspicious" in subject:
        return {"category": "security"}
    return {"category": "general"}

def mock_retrieve(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {"context": "Retrieved relevant knowledge base articles."}

def mock_draft(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    category = state_dict["category"]
    if category == "billing":
        return {"draft": "I understand your concern about the refund. I'll help you track down the status of your refund right away."}
    elif category == "technical":
        return {"draft": "I see you're experiencing technical difficulties. Let's resolve this with some troubleshooting steps."}
    elif category == "security":
        return {"draft": "I understand your security concerns. Let's secure your account immediately with some preventive measures."}
    return {"draft": "Thank you for reaching out. I'll guide you through this process step by step."}

def mock_review(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {"review": "Approved: Clear and helpful response."}

def mock_escalate(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {"final_response": "[ESCALATED] This ticket requires specialist attention."}

def process_ticket(state: SupportState) -> SupportState:
    # Classification
    result = mock_classify(state.to_dict())
    state.category = result["category"]
    print(f"\nClassifying ticket...\nCategory: {state.category}")
    
    # Context retrieval
    result = mock_retrieve(state.to_dict())
    state.context = result["context"]
    print("Retrieving context...")
    
    # Generate response
    result = mock_draft(state.to_dict())
    state.draft = result["draft"]
    state.drafts.append(state.draft)
    print("Generating response...")
    print(f"Draft #{len(state.drafts)}:")
    print(state.draft)
    
    # Review
    result = mock_review(state.to_dict())
    state.review = result["review"]
    print(f"Reviewing response...\nReview: {state.review}")
    
    if "Approved" in state.review:
        state.final_response = state.draft
    else:
        state.attempts += 1
        state.feedbacks.append(state.review)
        if state.attempts >= 2:
            result = mock_escalate(state.to_dict())
            state.final_response = result["final_response"]
    
    return state

def main():
    print("\nInitializing Support Ticket Agent...")
    
    # Sample tickets for different categories
    sample_tickets = {
        "1": {
            "name": "Billing Issue - Refund Request",
            "ticket": {
                "subject": "Refund not processed",
                "description": "I canceled my subscription but haven't received my refund yet. Please check."
            }
        },
        "2": {
            "name": "Technical Issue - App Crash",
            "ticket": {
                "subject": "App keeps crashing",
                "description": "Every time I try to open the app, it crashes after a few seconds. Using version 2.1.0 on iPhone."
            }
        },
        "3": {
            "name": "Security Issue - Suspicious Login",
            "ticket": {
                "subject": "Suspicious login attempts",
                "description": "Getting email notifications about login attempts from different countries. Worried my account is compromised."
            }
        },
        "4": {
            "name": "General Inquiry - Account Settings",
            "ticket": {
                "subject": "How to change account settings",
                "description": "I want to update my notification preferences but can't find where to do this."
            }
        }
    }

    while True:
        print("\n" + "="*40)
        print("Support Ticket Agent Demo")
        print("="*40)
        print("\nSelect a ticket to process:")
        print("-"*40)
        for key, value in sample_tickets.items():
            print(f"  {key}. {value['name']}")
        print("-"*40)
        print("  5. Exit")
        print("-"*40)

        choice = input("\nEnter choice (1-5): ")

        if choice == "5":
            print("Thank you for using the Support Agent!")
            break
        elif choice in sample_tickets:
            print(f"\nProcessing: {sample_tickets[choice]['name']}")
            print("-" * 50)
            
            initial_state = SupportState(
                ticket=sample_tickets[choice]['ticket'],
                subject=sample_tickets[choice]['ticket']['subject'],
                description=sample_tickets[choice]['ticket']['description']
            )
            
            result = process_ticket(initial_state)
            
            print("\nFINAL RESPONSE:")
            print("-" * 50)
            if result.final_response:
                print("[FINAL] " + result.final_response)
            elif "Approved" in result.review:
                print("[APPROVED] " + result.draft)
            else:
                print("[NOTICE] No final response generated")
                print("\nLast Draft:", result.draft)
                print("\nReviewer Feedback:", result.review)
            
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
