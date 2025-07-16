import os
from dataclasses import dataclass, field
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from nodes.classify import classify_ticket_llm
from nodes.retrieve import retrieve_context
from nodes.draft import generate_draft_llm
from nodes.review import review_draft_llm
from nodes.escalation import escalate

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

def process_ticket(state: SupportState, llm: Any) -> SupportState:
    # I handle the classification step
    classifier = classify_ticket_llm(llm)
    result = classifier.invoke(state.to_dict())
    state.category = result["category"]
    print(f"\nClassifying ticket...\nCategory: {state.category}")
    
    # I fetch relevant context
    result = retrieve_context(state.to_dict())
    state.context = result["context"]
    print("Retrieving context...")
    
    # I generate an appropriate response
    drafter = generate_draft_llm(llm)
    result = drafter.invoke(state.to_dict())
    state.draft = result["draft"]
    state.drafts.append(state.draft)
    print("Generating response...")
    print(f"Draft #{len(state.drafts)}:")
    print(state.draft)
    
    # I review the generated response
    reviewer = review_draft_llm(llm)
    result = reviewer.invoke(state.to_dict())
    state.review = result["review"]
    print(f"Reviewing response...\nReview: {state.review}")
    
    if "Approved" in state.review:
        state.final_response = state.draft
    else:
        state.attempts += 1
        state.feedbacks.append(state.review)
        if state.attempts >= 2:
            result = escalate(state.to_dict())
            state.final_response = result["final_response"]
    
    return state

def main():
    print("\nInitializing Support Ticket Agent...")
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
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
            
            result = process_ticket(initial_state, llm)
            
            print("\nFINAL RESPONSE:")
            print("-" * 50)
            if result.final_response:
                print(result.final_response)
            else:
                print("NOTICE: No final response generated")
                print("\nLast Draft:", result.draft)
                print("\nReviewer Feedback:", result.review)
            
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
