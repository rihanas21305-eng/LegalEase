import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

client = None

if api_key:
    client = genai.Client(api_key=api_key)


def generate_legal_document(
    document_type,
    parties,
    terms,
    effective_date
):

    # Try Gemini first
    if client:
        try:

            prompt = f"""
Create a professional draft legal document.

Document Type:
{document_type}

Parties:
{parties}

Key Terms:
{terms}

Effective Date:
{effective_date}

Create a clear document with headings and clauses.
Do not invent important facts.
Return only the document text.
"""

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception:
            # If Gemini is unavailable, use fallback below
            pass


    # Fallback document
    return f"""
LEGAL DOCUMENT

Document Type: {document_type}

PARTIES

{parties}


TERMS AND CONDITIONS

{terms}


EFFECTIVE DATE

{effective_date}


GENERAL PROVISION

This document is prepared based on the information provided by
the user and is intended as a draft for review.


SIGNATURES

Party 1: ______________________________

Party 2: ______________________________

Date: _________________________________
"""
