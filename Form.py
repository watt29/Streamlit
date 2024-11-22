import streamlit as st
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

# บันทึกข้อมูลลงไฟล์ CSV
st.markdown("---")  # เพิ่มเส้นแบ่ง
if st.button("บันทึกข้อมูล", use_container_width=True):
    save_data_to_csv(name, position, room_type, address, ", ".join(relationships), reason, marital_status, children_count, id_card, house_rights, phone_number)

# แสดงข้อมูลที่บันทึกแล้วในรูปแบบตาราง
st.markdown("### ข้อมูลที่บันทึกไว้:")
try:
    with open("form_data.csv", mode="r", encoding="utf-8") as file:
        csv_data = csv.reader(file)
        # อ่านข้อมูลจากไฟล์ CSV
        rows = list(csv_data)
        if len(rows) > 1:
            # แสดงข้อมูลในรูปแบบตาราง
            st.dataframe(rows[1:], columns=rows[0])  # แสดงข้อมูลที่ไม่รวม header
            # สร้างปุ่มลบแถว
            delete_rows = st.multiselect("เลือกแถวที่ต้องการลบ", options=range(1, len(rows)), format_func=lambda x: str(rows[x][0]))
            if st.button("ลบข้อมูลที่เลือก"):
                delete_data_from_csv(delete_rows)
except FileNotFoundError:
    st.warning("ยังไม่มีข้อมูลที่บันทึกไว้")

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
