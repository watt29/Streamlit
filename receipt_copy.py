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
import time
import string

# Register the font
pdfmetrics.registerFont(TTFont('THSarabunNew', 'https://raw.githubusercontent.com/watt29/Streamlit/main/THSarabunNew.ttf'))

# Function to generate receipt PDF
def generate_receipt(items, quantities, prices_per_liter, total_prices_before_vat, vat_values, total_prices_after_vat, grand_total, invoice_number, current_date):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=40, bottomMargin=40)

    # Styles
    style_normal = ParagraphStyle(
        'normal',
        fontName='THSarabunNew',  # Use THSarabunNew for all text
        fontSize=12,
        leading=14,
        alignment=0,
    )

    style_center = ParagraphStyle(
        'center',
        fontName='THSarabunNew',  # Use THSarabunNew for all text
        fontSize=12,
        leading=14,
        alignment=1,
    )

    # For bold text style (use regular THSarabunNew for bold as well)
    style_bold_center = ParagraphStyle(
        'bold_center',
        fontName='THSarabunNew',  # Use THSarabunNew for bold as well
        fontSize=14,
        leading=16,
        alignment=1,
        spaceAfter=12,
    )

    # Company and customer details
    company_info = '''
        <b>ห้างหุ้นส่วนจำกัด ภัณฑิรา ปิโตรเลียม</b><br />
        เลขที่ 70 หมู่ 4 ถนนบางปะหัน-ลพบุรี<br />
        ตำบลมหาราช อำเภอมหาราช จังหวัดพระนครศรีอยุธยา 13150<br />
        เลขประจำตัวผู้เสียภาษี: 0 1435 30000 17 4<br />
        โทรศัพท์: 081-8592375
    '''

    customer_info = '''
        <b>ชื่อลูกค้า: สภ.มหาราช</b><br />
        ที่อยู่: เลขที่ 59 หมู่ 2 ต.บ้านใหม่ อ.มหาราช, จ.พระนครศรีอยุธยา<br />
        โทรศัพท์: 035-389-153
    '''

    current_date_str = current_date.strftime('%d/%m/%Y')

    # Table data for items
    table_data = [["รายการ", "ปริมาณ (ลิตร)", "ราคาต่อลิตร (บาท)", "ยอดรวมก่อนภาษี (บาท)", "ภาษีมูลค่าเพิ่ม (บาท)", "ยอดรวมทั้งสิ้น (บาท)"]]
    for i in range(len(items)):
        table_data.append([items[i], f"{quantities[i]:.2f}", f"{prices_per_liter[i]:.2f}", f"{total_prices_before_vat[i]:.2f}", f"{vat_values[i]:.2f}", f"{total_prices_after_vat[i]:.2f}"])

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

    # PDF content
    elements = []
    elements.append(Paragraph('<b>ใบบันทึกรายการขาย (sales slip)</b>', style_center))
    elements.append(Spacer(1, 20))

    # Add company and customer information
    data = [[Paragraph(company_info, style_normal), Paragraph(customer_info, style_normal)]]
    table = Table(data, colWidths=[300, 300])
    table.setStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (0, -1), 50)])
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Invoice header
    invoice_header = f'<b>ใบเสร็จเลขที่: {invoice_number}</b> | วันที่: {current_date_str}'
    elements.append(Paragraph(invoice_header, style_center))
    elements.append(Spacer(1, 12))

    # Add table with items and totals
    invoice_table = Table(table_data, hAlign="LEFT")
    invoice_table.setStyle(table_style)
    elements.append(invoice_table)
    elements.append(Spacer(1, 4))

    # Summary section (with grand total only)
    summary_data = [
        ["ยอดรวมทั้งสิ้น (บาท)", f"{grand_total:.2f}"]
    ]
    summary_table = Table(summary_data, colWidths=[280, 100])
    summary_table.setStyle(TableStyle([ 
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'THSarabunNew'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 24))

    # Acknowledgment footer
    acknowledgment_footer = '''
        <b>หมายเหตุ:</b> "ได้รับมอบน้ำมันเชื้อเพลิงตามรายการข้างต้นไว้ครบถ้วนถูกต้องแล้ว"<br />
        <b>ลงชื่อ..............................................................</b><br />
        <b>ผู้จัดซื้อน้้ามันเชื้อเพลิง:</b> (ผู้ขับรถส่วนกลางหรือผู้ที่ได้รับมอบหมาย / คำสั่ง)<br />
        หมายเลขทะเบียน.................................................................    
    '''
    elements.append(Paragraph(acknowledgment_footer, style_normal))
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Streamlit interface
st.title("สร้างใบเสร็จ (Generate Receipt)")

# User inputs for number of items
item_options = ["ดีเซล B7", "แก๊สโซฮอล์ 91"]
selected_items = st.multiselect("เลือกสินค้าที่จะเติม", item_options)

# Price per liter input for each selected item
prices_per_liter = []
quantities = []

for item in selected_items:
    # ราคาต่อลิตรที่กรอกโดยผู้ใช้
    price = st.number_input(f"กรอกราคาต่อลิตรสำหรับ {item} (บาท)", min_value=0.0, format="%.2f", key=f"price_{item}")
    prices_per_liter.append(price)
    
    # กรอกจำนวนเงินที่เติมน้ำมัน รวมภาษีมูลค่าเพิ่ม
    total_money_with_vat = st.number_input(f"กรอกจำนวนเงินที่เติมสำหรับ {item} (รวมภาษี) (บาท)", min_value=0.0, format="%.2f", key=f"money_with_vat_{item}")
    
    # คำนวณจำนวนเงินก่อนภาษี (ราคาสินค้า) จากจำนวนเงินรวมภาษี
    total_money_before_vat = total_money_with_vat / (1 + 0.06525)  # 6.525% VAT
    
    # คำนวณจำนวนลิตรจากราคาก่อนภาษีและราคาต่อลิตร
    if price > 0:
        quantity = total_money_before_vat / price
    else:
        quantity = 0.0
    quantities.append(quantity)

# Date input
current_date = st.date_input("เลือกวันที่สำหรับใบเสร็จ")

# Generating receipt
if st.button("สร้างใบเสร็จ"):
    invoice_number = f"INV-{random.randint(1000, 9999)}"
    total_prices_before_vat = [quantities[i] * prices_per_liter[i] for i in range(len(selected_items))]
    vat_values = [total_prices_before_vat[i] * 0.06525 for i in range(len(selected_items))]
    total_prices_after_vat = [total_prices_before_vat[i] + vat_values[i] for i in range(len(selected_items))]
    grand_total = sum(total_prices_after_vat)
    
    # Generate receipt PDF
    buffer = generate_receipt(selected_items, quantities, prices_per_liter, total_prices_before_vat, vat_values, total_prices_after_vat, grand_total, invoice_number, current_date)
    
    # Create a download button with a unique filename
    filename = f"receipt_{invoice_number}_{int(time.time())}.pdf"
    st.download_button(
        label="ดาวน์โหลดใบเสร็จ",
        data=buffer,
        file_name=filename,
        mime="application/pdf",
    )
