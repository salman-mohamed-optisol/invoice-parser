import streamlit as st
import os
from backend import ocr_extraction, get_pezzo_prompt, get_response
from dotenv import load_dotenv

load_dotenv()


def process_invoice(file_path):
    file_content = ocr_extraction(file_path)
    prompt = get_pezzo_prompt("InvoicePrompt", file_content)
    response = get_response(prompt)
    invoice_dict = response.dict()
    printer(invoice_dict)

def printer(invoice_dict):
    st.divider()
    st.markdown("## Invoice Details")
    invoice_data = {
        "Invoice Id": invoice_dict.get('invoice_id'),
        "Vendor Name": invoice_dict.get('Vendor_name'),
        "Invoice Number": invoice_dict.get('invoice_number'),
        "Invoice Date": invoice_dict.get('invoice_date'),
        "Due Date": invoice_dict.get('due_date'),
        "Total Amount": invoice_dict.get('total_amount'),
        "Invoice Status": invoice_dict.get('invoice_status'),
        "Payment Terms": invoice_dict.get('payment_terms'),
        "PO Number": invoice_dict.get('po_number')
    }
    st.table(invoice_data)
    items = invoice_dict.get('items')
    if items:
        st.write("**Line Items:**")
        item_data = {
            "Description": [item.get('description') for item in items],
            "Quantity": [item.get('quantity') for item in items],
            "SKU Price": [item.get('SKU_Price') for item in items]
        }
        st.table(item_data)

def main():
    st.title("Invoice Parser")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if st.button("OK"):
        if uploaded_file is not None:
            process_invoice(uploaded_file)
        else:
            st.write("Please upload a PDF file first.")

if __name__ == "__main__":
    main()