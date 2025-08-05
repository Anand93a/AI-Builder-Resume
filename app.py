import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os
from io import BytesIO


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("Arial", "", 12)

    def header(self):
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, "Resume", ln=True, align='C')
        self.ln(10)

    def section(self, title, content):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 12)
        if isinstance(content, list):
            for item in content:
                self.multi_cell(0, 10, f"- {item}")
        else:
            self.multi_cell(0, 10, content)
        self.ln(2)

def create_pdf(data):
    pdf = PDF()

    def clean_text(text):
        if isinstance(text, str):
            return text.encode('latin-1', errors='replace').decode('latin-1')
        elif isinstance(text, list):
            return [clean_text(item) for item in text]
        return text

    if data.get('profile_pic'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(data['profile_pic'].read())
            tmp_file_path = tmp_file.name
        pdf.image(tmp_file_path, x=160, y=10, w=33)
        os.remove(tmp_file_path)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, clean_text(data['name']), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, clean_text(f"{data['email']} | {data['phone']} | {data['linkedin']}"), ln=True)
    pdf.ln(5)

    pdf.section("Professional Summary", clean_text(data['summary']))
    pdf.section("Education", clean_text(data['education']))
    pdf.section("Experience", clean_text(data['experience']))
    pdf.section("Skills", clean_text(data['skills']))
    pdf.section("Projects", clean_text(data['projects']))
    pdf.section("Certifications", clean_text(data['certifications']))
    pdf.section("Languages", clean_text(data['languages']))
    pdf.section("Hobbies", clean_text(data['hobbies']))
    pdf.section("References", clean_text(data['references']))

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_bytes)


st.set_page_config(page_title=" Resume Builder Application", page_icon="🧠")
st.title("📄 Resume Builder Application")

with st.sidebar:
    st.header("Upload Profile Image (Optional)")
    uploaded_img = st.file_uploader("Upload your image", type=["png", "jpg", "jpeg"])

st.subheader("Basic Information")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
linkedin = st.text_input("LinkedIn Profile")

st.subheader("Summary")
summary = st.text_area("Professional Summary", max_chars=500)

st.subheader("Education")
education = st.text_area("Education (degrees, universities, dates)")

st.subheader("Experience")
experience = st.text_area("Work Experience (roles, responsibilities, duration)")

st.subheader("Projects")
projects = st.text_area("List projects with tech and role")

st.subheader("Certifications")
certifications = st.text_area("List certifications")

st.subheader("Skills, Languages & Hobbies")
skills = [s.strip() for s in st.text_input("Skills (comma-separated)").split(',') if s.strip()]
languages = [l.strip() for l in st.text_input("Languages (comma-separated)").split(',') if l.strip()]
hobbies = [h.strip() for h in st.text_input("Hobbies (comma-separated)").split(',') if h.strip()]

st.subheader("References")
references = st.text_area("References (optional)")

if st.button("Generate Resume"):
    if not all([name, email, phone]):
        st.warning("Please fill in all mandatory fields.")
    else:
        data = {
            'profile_pic': uploaded_img,
            'name': name,
            'email': email,
            'phone': phone,
            'linkedin': linkedin,
            'summary': summary,
            'education': education,
            'experience': experience,
            'projects': [p.strip() for p in projects.split('\n') if p.strip()],
            'certifications': [c.strip() for c in certifications.split('\n') if c.strip()],
            'skills': skills,
            'languages': languages,
            'hobbies': hobbies,
            'references': references
        }

        pdf_stream = create_pdf(data)
        st.success("Resume generated successfully!")
        st.download_button("Download Resume PDF", data=pdf_stream, file_name="My_Resume.pdf", mime="application/pdf")
