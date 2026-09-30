from pydantic import BaseModel


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str