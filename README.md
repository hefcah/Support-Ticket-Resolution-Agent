
## Overview
I've developed an intelligent support ticket processing system that automatically handles customer inquiries through a multi-step workflow. My implementation uses a modular approach to classify, analyze, and respond to various types of support tickets.

## Features
- Interactive menu-driven interface
- Automated ticket classification (billing, technical, security, general)
- Context-aware response generation
- Quality review system
- Automatic escalation for complex cases
- Support for multiple response attempts
- Clean, formatted output

## File Structure and Purpose

### Main Files
- `demo.py` - I created this as the main entry point for the demo version, using mock implementations for reliable demonstrations.
- `main.py` - I implemented this as the production version that integrates with LangChain and OpenAI for intelligent processing.
- `README.md` - I wrote this to provide comprehensive documentation and setup instructions.

### Mock Implementation (`mock_nodes/`)
- `__init__.py` - I added this to make the mock_nodes directory a proper Python package.
- `classify.py` - I implemented keyword-based ticket classification for demo purposes.
- `retrieve.py` - I created simulated context retrieval for demonstration.
- `draft.py` - I wrote pre-defined response templates based on ticket categories.
- `review.py` - I added mock review logic that always approves responses.
- `escalation.py` - I implemented basic escalation handling for complex cases.

### Production Implementation (`nodes/`)
- `classify.py` - I integrated LLM-based classification using advanced language understanding.
- `retrieve.py` - I developed smart context retrieval based on ticket content.
- `draft.py` - I implemented AI-powered response generation using LangChain.
- `review.py` - I created intelligent response quality assessment using LLMs.
- `escalation.py` - I built advanced escalation logic with proper handling.
```

## How to Run

### Demo Version (No API Required)
```bash
python demo.py
```

### Full Version (Requires OpenAI API Key)
1. Set your OpenAI API key:
```bash
# Windows
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

2. Run the main script:
```bash
python main.py
```

## Sample Tickets
I've included four types of sample tickets:
1. Billing Issue - Refund Request
2. Technical Issue - App Crash
3. Security Issue - Suspicious Login
4. General Inquiry - Account Settings

## Technical Implementation
- I used Python's dataclass for state management
- I implemented a modular design pattern for separation of concerns
- I built a workflow system that handles multiple response attempts
- I included proper error handling and state tracking
- I created both mock and LLM-powered versions

## State Management
I designed the `SupportState` class to track:
- Ticket details (subject, description)
- Processing state (category, context)
- Response drafts and reviews
- Attempt tracking
- Final responses

## Dependencies
### Demo Version
- Python 3.8 or newer

### Full Version
- langchain
- langchain-openai
- langchain-core
- langgraph

## Note
The demo version (`demo.py`) uses mock implementations and requires no external dependencies. It's perfect for demonstrations and testing the workflow logic.

The full version (`main.py`) integrates with OpenAI's GPT-3.5 for enhanced capabilities but requires an API key and additional dependencies.

