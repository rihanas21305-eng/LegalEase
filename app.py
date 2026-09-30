import requests
import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# -----------------------------
# Session State
# -----------------------------
if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""


# -----------------------------
# Header
# -----------------------------
st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write("Create professional legal documents quickly using AI.")

st.divider()


# -----------------------------
# Inputs
# -----------------------------
document_type = st.selectbox(
    "Select Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement",
        "Freelance Work Contract",
        "Service Agreement",
        "Partnership Agreement"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder="Example: Jane Doe (Employee), ABC Technologies (Employer)"
)

terms = st.text_area(
    "Key Terms",
    placeholder=(
        "Example: Payment within 30 days; "
        "Confidentiality must be maintained; "
        "Either party may terminate with 15 days notice"
    )
)

effective_date = st.date_input("Effective Date")

st.divider()


# -----------------------------
# Generate Document
# -----------------------------
if st.button("Generate Legal Document"):

    if not parties:
        st.warning("Please enter the parties.")

    elif not terms:
        st.warning("Please enter the key terms.")

    else:

        data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": str(effective_date)
        }

        try:

            response = requests.post(
                "https://legalease-11.onrender.com/generate",
                json=data,
                timeout=60
            )

            if response.status_code == 200:

                result = response.json()

                st.session_state.generated_document = result["document"]

                st.success("Document generated successfully!")

            else:

                st.error("Error: " + response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "Backend is not running. "
                "Please start FastAPI first."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timed out. "
                "Please check the backend."
            )


# -----------------------------
# Generated Document
# -----------------------------
if st.session_state.generated_document:

    st.subheader("Generated Document")

    document = st.session_state.generated_document

    # -----------------------------
    # TXT Download
    # -----------------------------
    st.download_button(
        label="📄 Download as .TXT",
        data=document,
        file_name="legal_document.txt",
        mime="text/plain"
    )


    # -----------------------------
    # DOCX Creation
    # -----------------------------
    doc = Document()

    for line in document.split("\n"):
        doc.add_paragraph(line)

    docx_buffer = BytesIO()
    doc.save(docx_buffer)
    docx_buffer.seek(0)


    # -----------------------------
    # DOCX Download
    # -----------------------------
    st.download_button(
        label="📝 Download as .DOCX",
        data=docx_buffer,
        file_name="legal_document.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


    # -----------------------------
    # PDF Creation
    # -----------------------------
    pdf_buffer = BytesIO()

    pdf = SimpleDocTemplate(pdf_buffer)

    styles = getSampleStyleSheet()

    story = []

    for line in document.split("\n"):

        if line.strip():

            story.append(
                Paragraph(
                    line.replace("&", "&amp;"),
                    styles["Normal"]
                )
            )

            story.append(Spacer(1, 8))

    pdf.build(story)

    pdf_buffer.seek(0)


    # -----------------------------
    # PDF Download
    # -----------------------------
    st.download_button(
        label="📕 Download as .PDF",
        data=pdf_buffer,
        file_name="legal_document.pdf",
        mime="application/pdf"
    )
