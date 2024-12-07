import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os

# ระบุไฟล์ credentials (ไฟล์ Service Account ที่คุณดาวน์โหลด)
cred_file_path = r"D:\rescue\maharat-be0ae-f63b0350b7e1.json"

# กำหนดสิทธิ์ในการเข้าถึง (scopes)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# เชื่อมต่อกับ Google API โดยใช้ไฟล์ credentials
creds = Credentials.from_service_account_file(cred_file_path, scopes=scope)
client = gspread.authorize(creds)

# เชื่อมต่อกับ Google Sheet
spreadsheet_name = "rescue"  # ชื่อของ Google Sheet
sheet = client.open(spreadsheet_name).sheet1  # ใช้แผ่นงานแรก

# ฟอร์มการกรอกข้อมูล
st.title('แบบฟอร์มฐานข้อมูล')

# กรอกข้อมูลส่วนตัว
full_name = st.text_input("ชื่อเต็ม")
nickname = st.text_input("ชื่อเล่น")
id_card = st.text_input("หมายเลขบัตรประชาชน")
address = st.text_area("ที่อยู่")
phone_number = st.text_input("หมายเลขโทรศัพท์")

# ตัวเลือกมูลนิธิ
st.markdown('**ท่านเป็นเจ้าหน้าที่มูลนิธิ:**')
foundation_options = [
    "มูลนิธิกู้ภัยอยุธยา",
    "มูลนิธิร่วมกตัญญู",
    "มูลนิธิพุทไธสวรรค์",
]
foundation = st.selectbox("เลือกมูลนิธิ", foundation_options)

# อัปโหลดรูปภาพ
image = st.file_uploader("อัปโหลดรูปภาพ", type=["jpg", "png", "jpeg"])

# ฟังก์ชันบันทึกข้อมูลลงใน Google Sheets
def insert_data_to_google_sheet(full_name, nickname, id_card, address, phone_number, foundation, image_path):
    # เพิ่มข้อมูลลงในแผ่นงาน
    sheet.append_row([full_name, nickname, id_card, address, phone_number, foundation, image_path])

# ปุ่มส่งฟอร์ม
if st.button("ส่งข้อมูล"):
    # ตรวจสอบข้อมูล
    if all([full_name, nickname, id_card, address, phone_number, foundation]):
        # ตรวจสอบและบันทึกรูปภาพ
        image_path = None
        if image is not None:
            # ตั้งชื่อไฟล์ใหม่จากชื่อเต็มของผู้กรอกข้อมูล (แทนที่ช่องว่างด้วยเครื่องหมายขีด)
            image_name = full_name.replace(" ", "_") + os.path.splitext(image.name)[-1]
            
            # สร้างโฟลเดอร์สำหรับเก็บรูปภาพ (ถ้ายังไม่มี)
            if not os.path.exists('uploaded_images'):
                os.makedirs('uploaded_images')
            
            # บันทึกภาพลงในโฟลเดอร์
            image_path = f'uploaded_images/{image_name}'
            with open(image_path, 'wb') as f:
                f.write(image.getbuffer())
        
        # บันทึกข้อมูลลงใน Google Sheets
        insert_data_to_google_sheet(full_name, nickname, id_card, address, phone_number, foundation, image_path)
        st.success(f"ข้อมูลของคุณได้รับการบันทึกแล้ว\nมูลนิธิที่เลือก: {foundation}")
        if image_path:
            st.image(image_path, caption="ภาพที่อัปโหลด", use_column_width=True)
    else:
        st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

# เพิ่มส่วนที่แสดงข้อมูลที่บันทึกใน Google Sheets
st.subheader("ข้อมูลที่บันทึกไว้ในฐานข้อมูล")

# ดึงข้อมูลทั้งหมดจาก Google Sheets และแสดงในตาราง
users_data = sheet.get_all_records()

# ตรวจสอบว่ามีข้อมูลใน Google Sheets หรือไม่
if users_data:
    # แสดงข้อมูลในรูปแบบตาราง
    st.table(users_data)
else:
    st.warning("ยังไม่มีข้อมูลใน Google Sheets")
