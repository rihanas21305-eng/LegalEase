import os

from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import generate_legal_document
from backend.schemas import DocumentRequest

router = APIRouter()


@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:
        result = generate_legal_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

        return {
            "success": True,
            "document": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )