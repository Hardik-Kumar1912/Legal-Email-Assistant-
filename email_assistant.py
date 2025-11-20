import os
import json
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

MODEL_NAME = "gemini-2.5-flash"

# --- Data Models ---

class AgreementReference(BaseModel):
    type: str = Field(description="Type of the agreement")
    date: str = Field(description="Date of the agreement")

class Parties(BaseModel):
    client: str = Field(description="Client company name")
    counterparty: str = Field(description="Counterparty company name")

class EmailAnalysis(BaseModel):
    intent: str = Field(description="Main intent (e.g., legal_advice_request)")
    primary_topic: str = Field(description="Primary legal topic")
    parties: Parties
    agreement_reference: AgreementReference
    questions: List[str] = Field(description="Specific questions asked")
    requested_due_date: str = Field(description="Requested advice deadline")
    urgency_level: str = Field(description="Inferred urgency (low, medium, high)")

# --- Core Functions ---

def get_llm(temperature=0.0):
    return ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=temperature)

def analyze_email(email_text: str) -> dict:
    llm = get_llm().with_structured_output(EmailAnalysis)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Legal Assistant. Extract key details into structured JSON."),
        ("human", "Email Content:\n{email_text}")
    ])

    chain = prompt | llm
    return chain.invoke({"email_text": email_text}).model_dump()

def draft_reply(email_text: str, analysis: dict, contract_text: str) -> str:
    llm = get_llm()

    system_instruction = (
        "You are Senior Legal Counsel. Draft a professional reply based strictly on the provided "
        "contract text. Address the sender by name, cite specific clauses (e.g., 9.1), and avoid "
        "guaranteeing outcomes. Use terms like 'appears to' or 'indicates'. "
        "Sign the email as 'Hardik Kumar'."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "Email:\n{email_text}\n\nAnalysis:\n{analysis}\n\nContract:\n{contract_text}\n\nDraft:")
    ])

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "email_text": email_text,
        "analysis": analysis,
        "contract_text": contract_text
    })

if __name__ == "__main__":
    sample_email = """Subject: Termination of Services under MSA
Dear Counsel,
We refer to the Master Services Agreement dated 10 March 2023 between Acme Technologies Pvt. Ltd. (“Acme”) and Brightwave Solutions LLP (“Brightwave”).
Due to ongoing performance issues and repeated delays in delivery, we are considering termination of the Agreement for cause with effect from 1 December 2025.
Please confirm:
1. Whether we are contractually entitled to terminate for cause on the basis of repeated delays in delivery;
2. The minimum notice period required.
We would appreciate your advice by 18 November 2025.

Regards,
Priya Sharma
Legal Manager, Acme Technologies Pvt. Ltd."""

    contract_snippet = """Clause 9 – Termination for Cause
9.1 Either Party may terminate this Agreement for cause upon thirty (30) days’ written notice if the other Party commits a material breach.
9.2 Repeated failure to meet delivery timelines constitutes a material breach.
Clause 10 – Notice
10.1 All notices shall be given in writing and shall be effective upon receipt.
10.2 For termination, minimum thirty (30) days’ prior written notice is required."""

    print("--- Analyzed Data (JSON) ---")
    data = analyze_email(sample_email)
    print(json.dumps(data, indent=2))

    print("\n--- Drafted Reply ---")
    response = draft_reply(sample_email, data, contract_snippet)
    print(response)