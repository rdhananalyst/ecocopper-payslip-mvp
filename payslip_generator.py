# filename: payslip_generator.py
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(page_title="EcoCopper Payroll - Payslip Generator", layout="centered")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Copper_element_symbol_Cu.svg/120px-Copper_element_symbol_Cu.svg.png", width=100)
st.title("EcoCopper Payroll – 🇦🇺 Payslip Generator (MVP)")
st.caption("Generate an ATO-style payslip with automatic tax and super calculations.")

with st.form("payslip_form"):
    emp_name = st.text_input("Employee Name")
    pay_period = st.text_input("Pay Period (e.g., 01 Oct – 15 Oct 2025)")
    hours = st.number_input("Hours Worked", min_value=0.0, value=38.0)
    rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=35.0)
    super_rate = st.slider("Superannuation Rate (%)", 9.5, 15.0, 11.0)
    extra_super = st.number_input("Extra Employee Super (%)", min_value=0.0, value=0.0)
    tax_rate = st.slider("Tax Withholding Estimate (%)", 0.0, 40.0, 18.0)
    uploaded_logo = st.file_uploader("Upload Clinic Logo (optional)", type=["png", "jpg"])
    submit = st.form_submit_button("Generate Payslip")

if submit:
    gross = hours * rate
    super_amt = gross * (super_rate + extra_super) / 100
    tax = gross * tax_rate / 100
    net = gross - tax

    pdf_buffer = BytesIO()
    p = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    # Logo
    if uploaded_logo is not None:
        from PIL import Image
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img = Image.open(uploaded_logo)
        img.save(temp_file.name)
        p.drawImage(temp_file.name, 50, 780, width=50, height=50)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 800, "PAYSLIP")

    p.setFont("Helvetica", 11)
    y = 760
    details = [
        f"Employee Name: {emp_name}",
        f"Pay Period: {pay_period}",
        f"Hours Worked: {hours}",
        f"Hourly Rate: ${rate:.2f}",
        f"Gross Pay: ${gross:.2f}",
        f"Tax Withheld ({tax_rate}%): ${tax:.2f}",
        f"Net Pay: ${net:.2f}",
        f"Superannuation ({super_rate + extra_super}%): ${super_amt:.2f}",
        f"Total Employer Cost: ${(gross + super_amt):.2f}",
    ]
    for d in details:
        p.drawString(50, y, d)
        y -= 15

    p.drawString(50, 620, "Generated via EcoCopper Payroll MVP (Demo Only)")
    p.showPage()
    p.save()

    pdf_buffer.seek(0)
    st.download_button(
        label="📥 Download Payslip PDF",
        data=pdf_buffer,
        file_name=f"{emp_name}_Payslip.pdf",
        mime="application/pdf"
    )

    st.success("Payslip generated successfully ✅")