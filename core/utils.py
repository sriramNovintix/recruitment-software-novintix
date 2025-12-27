import io
import pdfplumber
import docx


def extract_text(uploaded_file) -> str:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif uploaded_file.type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")
