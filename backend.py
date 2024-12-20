import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from langchain_openai import ChatOpenAI
from pezzo.client import pezzo

from pydantic import BaseModel
from typing import List

class InvoiceItem(BaseModel):
    SKU_Price: float
    description: str
    quantity: int

class Invoice(BaseModel):
    invoice_id: str
    Vendor_name: str
    invoice_number: str
    invoice_date: str
    due_date: str
    total_amount: float
    items: List[InvoiceItem]
    invoice_status: str
    payment_terms: str
    po_number: str


def ocr_extraction(file_content):
    print(f"INFO: OCR extraction started for the file")
    key = os.environ["VISION_KEY"]
    endpoint = os.environ["VISION_ENDPOINT"]

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=file_content,
            content_type="application/octet-stream"
    )
    result = poller.result()
    ocr_output = result.as_dict() 
    return ocr_output['content']

def get_pezzo_prompt(prompt_name, file_content):
    prompt_template = pezzo.get_prompt(prompt_name)
    prompt = prompt_template.content['prompt']
    return prompt.format(invoice_content=file_content)

def get_response(prompt):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.environ["OPENAI_API_KEY"]
    )
    response = llm.with_structured_output(Invoice).invoke(prompt)
    return response
