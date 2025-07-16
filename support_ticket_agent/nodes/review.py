from typing import TypedDict
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

def review_draft_llm(llm):
    prompt = PromptTemplate.from_template(
        """Review the following support reply for policy violations.

Draft: {draft}

If it's good, reply: Approved  
If not, reply: Rejected: <reason>"""
    )
    chain = prompt | llm | (lambda out: {"review": out.content.strip()})
    
    def review_wrapper(state):
        return chain.invoke({
            "draft": state["draft"]
        })
    
    return RunnableLambda(review_wrapper)
