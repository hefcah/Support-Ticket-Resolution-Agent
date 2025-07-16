from typing import TypedDict
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

def generate_draft_llm(llm):
    prompt = PromptTemplate.from_template(
        """You are a helpful support assistant. Use the context to answer the ticket.

Subject: {subject}
Description: {description}
Context: {context}

Write a clear and polite response:"""
    )
    chain = prompt | llm | (lambda out: {"draft": out.content.strip()})
    
    def draft_wrapper(state):
        return chain.invoke({
            "subject": state["subject"],
            "description": state["description"],
            "context": state["context"]
        })
    
    return RunnableLambda(draft_wrapper)
