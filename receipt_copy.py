import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import random
import io

# Register the THSarabunNew font
pdfmetrics.registerFont(TTFont('THSarabunNew', 'D:/python/receipt/THSarabunNew.ttf'))

# Function to generate receipt PDF
def generate_receipt(items, unit_prices, quantities, total_prices, vat_values, total_with_vat, invoice_number, current_date):
    # Create a BytesIO buffer to save the PDF in memory
    buffer = io.BytesIO()

    # Create the PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=40)

    # Create styles for the text
    style_normal = ParagraphStyle(
        'normal',
        fontName='THSarabunNew',
        fontSize=12,
        leading=14,
        alignment=0,  # Align text to the left
    )

    style_center = ParagraphStyle(
        'center',
        fontName='THSarabunNew',
        fontSize=12,
        leading=14,
        alignment=1,  # Center the text
    )

    # Company (Seller) Information
    company_info = '''
        <b>ห้างหุ้นส่วนจำกัด ภัณฑิรา ปิโตรเลียม</b><br />
        เลขที่ 70 หมู่ 4 ถนนบางปะหัน-ลพบุรี<br />
        ตำบลมหาราช อำเภอมหาราช จังหวัดพระนครศรีอยุธยา 13150<br />
        เลขประจำตัวผู้เสียภาษี: 0 1435 30000 17 4<br />
        โทรศัพท์: 081-8592375
    '''

    # Customer Information
    customer_info = '''
        <b>ชื่อลูกค้า: สภ.มหาราช</b><br />
        ที่อยู่: เลขที่ 59 หมู่ 2 ต.บ้านใหม่ อ.มหาราช, จ.พระนครศรีอยุธยา<br />
        โทรศัพท์: 035-389-153
    '''

    # Format date
    current_date_str = current_date.strftime('%d/%m/%Y')

    # Creating the table data for the receipt
    table_data = [["รายการ", "ราคาต่อหน่วย (บาท)", "ปริมาณ (ลิตร)", "มูลค่าสินค้า (บาท)", "ภาษีมูลค่าเพิ่ม (บาท)", "รวมทั้งสิ้น (บาท)"]]  # Header row
    for i in range(len(items)):
        table_data.append([items[i], f"{unit_prices[i]:.2f}", f"{quantities[i]:.2f}", f"{total_prices[i]:.2f}", f"{vat_values[i]:.2f}", f"{total_with_vat[i]:.2f}"])

    # Table Style
    table_style = TableStyle([ 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'THSarabunNew'),
        ('FONTNAME', (0, 1), (-1, -1), 'THSarabunNew'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ])

    # Create elements for the PDF
    elements = []

    # Add the Sales Slip Title
    sales_slip_header = '<b>ใบบันทึกรายการขาย (Sales Slip)</b>'
    elements.append(Paragraph(sales_slip_header, style_center))

    # Add some space
    elements.append(Spacer(1, 12))

    # Company and Customer Information in 2 Columns
    data = [
        [Paragraph(company_info, style_normal), Paragraph(customer_info, style_normal)],
    ]
    table = Table(data, colWidths=[300, 300])
    table.setStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (0, -1), 50)])
    elements.append(table)

    # Add space
    elements.append(Spacer(1, 24))

    # Invoice Header with Invoice Number and Date
    invoice_header = f'<b>ใบเสร็จเลขที่: {invoice_number}</b> | วันที่: {current_date_str}'
    elements.append(Paragraph(invoice_header, style_center))

    # Add space
    elements.append(Spacer(1, 12))

    # Create the invoice table for the first receipt (top part of the page)
    invoice_table = Table(table_data)
    invoice_table.setStyle(table_style)
    elements.append(invoice_table)

    # Add space after the first receipt
    elements.append(Spacer(1, 24))

    # --- Second Part (Lower part of the page) ---
    # Add extra space before the second section (to move it further down)
    elements.append(Spacer(1, 80))  # 48 unit of space (about 2x the default)

    # Add the Sales Slip Title for the second receipt
    sales_slip_header2 = '<b>ใบบันทึกรายการขาย (Sales Slip)</b>'
    elements.append(Paragraph(sales_slip_header2, style_center))

    # Add some space
    elements.append(Spacer(1, 12))

    # Company and Customer Information in 2 Columns
    table = Table(data, colWidths=[300, 300])
    table.setStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (0, -1), 50)])
    elements.append(table)

    # Add space
    elements.append(Spacer(1, 24))

    # Invoice Header with Invoice Number and Date for the second receipt
    invoice_header2 = f'<b>ใบเสร็จเลขที่: {invoice_number}</b> | วันที่: {current_date_str}'
    elements.append(Paragraph(invoice_header2, style_center))

    # Add space
    elements.append(Spacer(1, 12))

    # Create the invoice table for the second receipt (bottom part of the page)
    invoice_table2 = Table(table_data)
    invoice_table2.setStyle(table_style)
    elements.append(invoice_table2)

    # Add acknowledgment footer for both receipts
    acknowledgment_footer = '''
        <b>หมายเหตุ:</b> "ได้รับมอบน้ำมันเชื้อเพลิงตามรายการข้างต้นไว้ครบถ้วนถูกต้องแล้ว"<br />
        <b>ลงชื่อ..................................</b>
        <b>ผู้จัดซื้อน้้ามันเชื้อเพลิง:</b> (ผู้ขับรถส่วนกลางหรือผู้ที่ได้รับมอบหมาย / คำสั่ง)<br />
        หมายเลขทะเบียน.................................................................    
    '''
    elements.append(Spacer(1, 24))  # Add space after the second receipt
    elements.append(Paragraph(acknowledgment_footer, style_normal))

    # Build the PDF
    doc.build(elements)

    # Seek to the beginning of the buffer
    buffer.seek(0)
    return buffer

# Streamlit interface
st.title("สร้างใบเสร็จ (Generate Receipt)")

# Fixed product list
fixed_items = ["ดีเซล B7", "แก๊สโซฮอล์ 91"]
unit_prices = []  # Prices will be filled based on user input
quantities = []
total_prices = []
vat_values = []
total_with_vat = []

# Add the fixed products to the form
for i, item in enumerate(fixed_items):
    # Input for price per liter (ราคาต่อลิตร)
    price_per_liter = st.number_input(f"ราคาต่อลิตรสำหรับ {item} (บาท)", min_value=0.0, format="%.2f")
    
    # Input for total amount spent (ยอดรวมทั้งสิ้น)
    total_amount = st.number_input(f"จำนวนเงินที่เติม {item} (บาท)", min_value=0.0, format="%.2f")
    
    # Calculate the quantities and VAT values
    quantity = total_amount / price_per_liter if price_per_liter != 0 else 0
    vat_value = total_amount * 0.065425
    total_price = total_amount - vat_value
    total_with_vat_value = total_amount
    
    unit_prices.append(price_per_liter)
    quantities.append(quantity)
    total_prices.append(total_price)
    vat_values.append(vat_value)
    total_with_vat.append(total_with_vat_value)

# Select the invoice date
selected_date = st.date_input("เลือกวันที่", value=datetime.today())

# Generate the invoice number
invoice_number = f"INV-{random.randint(1000, 9999)}"

# Generate the PDF
pdf_data = generate_receipt(fixed_items, unit_prices, quantities, total_prices, vat_values, total_with_vat, invoice_number, selected_date)

# Provide the download link for the PDF
st.download_button(
    label="ดาวน์โหลดใบเสร็จ (Download Receipt)",
    data=pdf_data,
    file_name=f"ใบเสร็จ_{invoice_number}.pdf",
    mime="application/pdf"
)
