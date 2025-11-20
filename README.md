# Legal Email Assistant

This project is a prototype for a legal assistant tool designed to analyze incoming client emails and draft appropriate legal responses. It utilizes Google's Gemini models (via LangChain) to extract structured data and generate professional legal correspondence based on contract clauses.

## Features
- **Email Analysis:** Extracts intent, parties, agreement references, and specific questions into a structured JSON format.
- **Drafting Module:** Generates a formal legal reply citing specific contract clauses (e.g., Termination for Cause).
- **Schema Validation:** Uses Pydantic to ensure consistent data output.

## Dependencies
- Python 3.9+
- langchain-google-genai
- langchain-core
- pydantic
- python-dotenv

## Setup Instructions

1. **Clone or download** the repository to your local machine.

2. **Install required packages**:
   ```bash
   pip install langchain-google-genai langchain-core pydantic python-dotenv

3. **Configure Environment**:
    Create a file named .env in the root directory and add your Google Gemini API key
    GOOGLE_API_KEY=your_api_key_here

## Usage

    python email_assistant.py
    
    
