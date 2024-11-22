import streamlit as st
import pandas as pd
import csv
from datetime import datetime

# ฟังก์ชันในการตรวจสอบข้อมูล
def validate_data(name, id_card, phone_number):
    if not name or not id_card or not phone_number:
        st.warning("กรุณากรอกข้อมูลให้ครบถ้วน!")
        return False
    return True

# ฟังก์ชันในการบันทึกข้อมูลลงไฟล์ CSV
def save_data_to_csv(name, position, room_type, address, relationships, reason, marital_status, children_count, id_card, house_rights, phone_number):
    if not validate_data(name, id_card, phone_number):
        return

    # บันทึกข้อมูลลงในไฟล์ CSV
    with open("form_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # ตรวจสอบว่าไฟล์ว่างหรือไม่
            writer.writerow([
                "ชื่อ-นามสกุล", "ตำแหน่ง", "ประเภทที่พักอาศัย", "ที่อยู่", "ความสัมพันธ์ในบ้าน", "เหตุผลการยื่นคำร้อง", 
                "สถานภาพ", "จำนวนบุตร", "หมายเลขบัตรประชาชน", "หมายเลขโทรศัพท์ติดต่อ", "สิทธิในการเบิกค่าบ้าน", "วันที่บันทึก"
            ])
        writer.writerow([
            name, position, room_type, address, relationships, reason, marital_status, children_count, id_card, phone_number, house_rights, 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
    st.success("ข้อมูลถูกบันทึกเรียบร้อยแล้ว!")

# ฟังก์ชันในการลบข้อมูลจากไฟล์ CSV
def delete_data_from_csv(delete_rows):
    try:
        # อ่านข้อมูลเดิมจากไฟล์ CSV
        with open("form_data.csv", mode="r", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        # ตรวจสอบว่ามีข้อมูลหรือไม่
        if len(rows) <= 1:
            st.warning("ไม่มีข้อมูลในไฟล์เพื่อให้ลบ")
            return

        # ลบแถวที่เลือก
        new_rows = [row for index, row in enumerate(rows) if index not in delete_rows]

        # เขียนข้อมูลใหม่กลับไปที่ไฟล์
        with open("form_data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(new_rows)
        
        st.success("ข้อมูลที่เลือกถูกลบออกจากไฟล์เรียบร้อยแล้ว!")
    except FileNotFoundError:
        st.warning("ไม่พบไฟล์ข้อมูลเพื่อทำการลบ")

# ฟังก์ชันตรวจสอบรหัสผ่าน
def authenticate_password():
    # รหัสผ่านที่กำหนดให้ผู้ใช้กรอก
    correct_password = "1234"  # คุณสามารถเปลี่ยนรหัสผ่านนี้ได้ตามต้องการ
    password = st.text_input("กรุณากรอกรหัสผ่านเพื่อยืนยันการลบข้อมูล:", type="password")
    if password == correct_password:
        return True
    else:
        return False

# UI ด้วย Streamlit
st.set_page_config(page_title="บ้านพักของทางราชการ", layout="centered")

# เพิ่ม header และคำแนะนำ
# ใช้ st.markdown และกำหนดขนาดข้อความด้วย HTML
st.markdown("<h2 style='font-size: 20px;'>ฟอร์มสำรวจข้าราชการที่เข้าพักอาศัยในที่พักของทางราชการ</h2>", unsafe_allow_html=True)
st.markdown("กรุณากรอกข้อมูลในฟอร์มด้านล่างนี้")

# ข้อมูลส่วนตัว
name = st.text_input("ยศ-ชื่อ-นามสกุล:")
id_card = st.text_input("หมายเลขบัตรประชาชน:")
phone_number = st.text_input("หมายเลขโทรศัพท์ติดต่อ:")

position = st.selectbox("ตำแหน่ง:", [
    "รอง สวป.สภ.มหาราช", "รอง สว.(สอบสวน)สภ.มหาราช", "รอง สว.(ป.)สภ.มหาราช", "รอง สว.สส.สภ.มหาราช", 
    "ผบ.หมู่.(ป.)สภ.มหาราช", "ผบ.หมู่.(จร.)สภ.มหาราช", "ผบ.หมู่.(สส.)สภ.มหาราช", "ผบ.หมู่.ผช.พงส.สภ.มหาราช"
])
room_type = st.selectbox("ประเภทที่พักอาศัย:", ["บ้านพักอิสระ"])

# เพิ่มฟิลด์ที่อยู่ในฟิลด์เดียว
address = st.text_area("กรอกที่อยู่ตามบัตร ปชช. (บ้านเลขที่, หมู่/ซอย, ถนน, ตำบล/แขวง, อำเภอ/เขต, จังหวัด):", height=150)

# ความสัมพันธ์ในบ้าน
relationship_choices = ["บิดา", "มารดา", "บุตร", "พี่/น้อง", "บิดามารดา", "คนเดียว", "คู่สมรส"]
relationships = st.multiselect("พักอาศัยกับ:", relationship_choices)

# เหตุผลการยื่นคำร้อง
reason = st.text_area("เหตุผลการยื่นคำร้อง:เช่น ไม่มีที่พักอาศัย")

# ข้อมูลสถานภาพสมรส
marital_status = st.selectbox("สถานภาพ:", ["โสด", "สมรส", "หย่า"])
children_count = ""
if marital_status in ["สมรส", "หม้าย", "หย่า"]:
    children_count = st.text_input("จำนวนบุตร:")

# สิทธิในการเบิกค่าบ้าน
house_rights = st.selectbox("สิทธิในการเบิกค่าบ้าน:", ["มีสิทธิ", "ไม่มีสิทธิ"])

# บันทึกข้อมูลลงไฟล์ CSV
st.markdown("---")  # เพิ่มเส้นแบ่ง
if st.button("บันทึกข้อมูล", use_container_width=True):
    save_data_to_csv(name, position, room_type, address, ", ".join(relationships), reason, marital_status, children_count, id_card, house_rights, phone_number)

# การแสดงข้อมูลที่บันทึกแล้ว
st.markdown("### ข้อมูลที่บันทึกไว้:")
try:
    # อ่านข้อมูลจากไฟล์ CSV
    with open("form_data.csv", mode="r", encoding="utf-8") as file:
        rows = list(csv.reader(file))
    
    # ตรวจสอบว่า rows มีข้อมูลหรือไม่
    if rows:
        # แปลงข้อมูลเป็น DataFrame
        df = pd.DataFrame(rows[1:], columns=rows[0])
        st.dataframe(df)  # แสดงข้อมูลในรูปแบบตาราง
        
        # ตัวเลือกในการลบข้อมูล
        delete_rows = st.multiselect("เลือกแถวที่ต้องการลบ", options=range(1, len(rows)), format_func=lambda x: str(rows[x][0]))
        
        # เมื่อผู้ใช้ต้องการลบข้อมูล
        if st.button("ลบข้อมูลที่เลือก"):
            if authenticate_password():  # ตรวจสอบรหัสผ่าน
                delete_data_from_csv(delete_rows)
            else:
                st.warning("รหัสผ่านไม่ถูกต้อง!")
    else:
        st.warning("ไม่มีข้อมูลในไฟล์.")
except FileNotFoundError:
    st.warning("ไม่พบไฟล์ข้อมูลเพื่อแสดงผล")

# การปรับแต่ง CSS ให้เหมาะสมกับมือถือ
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 16px 24px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextArea>textarea, .stTextInput>input, .stSelectbox select {
        font-size: 16px;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)
