from typing import Dict
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

def classify_ticket_llm(llm):
    prompt = PromptTemplate.from_template(
        """Analyze this support ticket and classify it into one of these categories: Billing, Technical, Security, General.

Guidelines:
- Billing: Anything related to payments, refunds, subscriptions, or invoices
- Technical: Software issues, bugs, errors, or functionality problems
- Security: Account security, unauthorized access, or data privacy concerns
- General: General inquiries about services, features, or account management

Subject: {subject}
Description: {description}

Provide ONLY the category name, nothing else.
Category:"""
    )
    
    chain = prompt | llm | (lambda out: {"category": out.content.strip()})
    
    def classify_wrapper(state):
        return chain.invoke({
            "subject": state["subject"],
            "description": state["description"]
        })
    
    return RunnableLambda(classify_wrapper)
