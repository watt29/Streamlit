import streamlit as st
import csv
import requests
import base64
from datetime import datetime

# ฟังก์ชันในการตรวจสอบข้อมูล
def validate_data(name, id_card, phone_number):
    if not name or not id_card or not phone_number:
        st.warning("กรุณากรอกข้อมูลให้ครบถ้วน!")
        return False
    return True

# ฟังก์ชันในการบันทึกข้อมูลลงไฟล์ CSV บน GitHub
def upload_to_github(name, position, room_type, address, relationships, reason, marital_status, children_count, id_card, house_rights, phone_number):
    if not validate_data(name, id_card, phone_number):
        return

    # สร้างข้อมูลที่จะบันทึกใน CSV
    data = [
        ["ชื่อ-นามสกุล", "ตำแหน่ง", "ประเภทที่พักอาศัย", "ที่อยู่", "ความสัมพันธ์ในบ้าน", "เหตุผลการยื่นคำร้อง", "สถานภาพ", "จำนวนบุตร", "หมายเลขบัตรประชาชน", "หมายเลขโทรศัพท์ติดต่อ", "สิทธิในการเบิกค่าบ้าน", "วันที่บันทึก"],
        [name, position, room_type, address, relationships, reason, marital_status, children_count, id_card, phone_number, house_rights, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    # แปลงข้อมูลเป็น CSV string
    csv_data = "\n".join([",".join(row) for row in data])

    # GitHub repository URL และ API endpoint สำหรับบันทึกไฟล์
    github_repo = "watt29/Streamlit"
    github_file_path = "form_data.csv"
    github_api_url = f"https://api.github.com/repos/{github_repo}/contents/{github_file_path}"

    # GitHub Token (ให้เปลี่ยนเป็น token ของคุณ)
    github_token = "YOUR_GITHUB_TOKEN"

    # การเข้าถึงข้อมูลใน GitHub repository
    headers = {
        "Authorization": f"token {github_token}",
        "Content-Type": "application/json"
    }

    # อ่านไฟล์ที่มีอยู่ใน GitHub เพื่อตรวจสอบ hash (การอัปเดตไฟล์)
    response = requests.get(github_api_url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]
    else:
        sha = None  # หากไฟล์ไม่มีอยู่ จะไม่ใช้ SHA

    # ข้อมูลสำหรับการอัปโหลดไฟล์
    json_data = {
        "message": "เพิ่มข้อมูลจากฟอร์ม",
        "content": base64.b64encode(csv_data.encode()).decode("utf-8"),
        "sha": sha if sha else ""  # ใช้ SHA หากไฟล์มีอยู่แล้ว
    }

    # อัปโหลดไฟล์ไปยัง GitHub
    upload_response = requests.put(github_api_url, headers=headers, json=json_data)

    if upload_response.status_code == 201:
        st.success("ข้อมูลถูกบันทึกใน GitHub เรียบร้อยแล้ว!")
    else:
        st.error(f"เกิดข้อผิดพลาดในการอัปโหลดไฟล์: {upload_response.text}")

# UI ด้วย Streamlit
st.set_page_config(page_title="บ้านพักของทางราชการ", layout="centered")

# เพิ่ม header และคำแนะนำ
st.title("ฟอร์มสำรวจข้าราชการที่เข้าพักอาศัยในที่พักของทางราชการ")
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
address = st.text_area("กรอกที่อยู่ (บ้านเลขที่, หมู่/ซอย, ถนน, ตำบล/แขวง, อำเภอ/เขต, จังหวัด):", height=150)

# ความสัมพันธ์ในบ้าน
relationship_choices = ["บิดา", "มารดา", "บุตร", "พี่/น้อง", "บิดามารดา", "คนเดียว", "คู่สมรส"]
relationships = st.multiselect("เลือกความสัมพันธ์ในบ้าน:", relationship_choices)

# เหตุผลการยื่นคำร้อง
reason = st.text_area("เหตุผลการยื่นคำร้อง:")

# ข้อมูลสถานภาพสมรส
marital_status = st.selectbox("สถานภาพ:", ["โสด", "สมรส", "หย่า"])
children_count = ""
if marital_status in ["สมรส", "หม้าย", "หย่า"]:
    children_count = st.text_input("จำนวนบุตร:")

# สิทธิในการเบิกค่าบ้าน
house_rights = st.selectbox("สิทธิในการเบิกค่าบ้าน:", ["มีสิทธิ", "ไม่มีสิทธิ"])

# บันทึกข้อมูล
st.markdown("---")  # เพิ่มเส้นแบ่ง
if st.button("บันทึกข้อมูล", use_container_width=True):
    upload_to_github(name, position, room_type, address, ", ".join(relationships), reason, marital_status, children_count, id_card, house_rights, phone_number)

# ปรับแต่ง CSS ให้เหมาะสมกับมือถือ
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
    .stTextArea>textarea {
        font-size: 16px;
        padding: 12px;
    }
    .stSelectbox select {
        font-size: 16px;
        padding: 12px;
    }
    .stTextInput input {
        font-size: 16px;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# ข้อความแนะนำ
st.markdown("""
    <p style="color: #4CAF50; font-size: 16px;">โปรดกรอกข้อมูลให้ครบถ้วนและตรวจสอบก่อนบันทึก!</p>
""", unsafe_allow_html=True)
