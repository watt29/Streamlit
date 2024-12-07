import streamlit as st  # type: ignore
import sqlite3
import os

# ฟังก์ชันเชื่อมต่อกับฐานข้อมูล SQLite
def create_connection():
    conn = sqlite3.connect('form_data.db')
    return conn

# ฟังก์ชันสร้างตารางหากยังไม่มี
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    nickname TEXT,
                    id_card TEXT,
                    address TEXT,
                    phone_number TEXT,
                    foundation TEXT,
                    image_path TEXT
                )''')
    conn.commit()
    conn.close()

# ฟังก์ชันบันทึกข้อมูลลงในฐานข้อมูล
def insert_data(full_name, nickname, id_card, address, phone_number, foundation, image_path):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO users (full_name, nickname, id_card, address, phone_number, foundation, image_path)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (full_name, nickname, id_card, address, phone_number, foundation, image_path))
    conn.commit()
    conn.close()

# ฟังก์ชันดึงข้อมูลจากฐานข้อมูล
def get_all_users():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    rows = c.fetchall()
    conn.close()
    return rows

# สร้างตารางในฐานข้อมูล
create_table()

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
        
        # บันทึกข้อมูลลงในฐานข้อมูล
        insert_data(full_name, nickname, id_card, address, phone_number, foundation, image_path)
        st.success(f"ข้อมูลของคุณได้รับการบันทึกแล้ว\nมูลนิธิที่เลือก: {foundation}")
        if image_path:
            st.image(image_path, caption="ภาพที่อัปโหลด", use_column_width=True)
    else:
        st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

# เพิ่มส่วนที่แสดงข้อมูลที่บันทึกในฐานข้อมูล
st.subheader("ข้อมูลที่บันทึกไว้ในฐานข้อมูล")

# ดึงข้อมูลทั้งหมดจากฐานข้อมูลและแสดงในตาราง
users_data = get_all_users()

# ตรวจสอบว่ามีข้อมูลในฐานข้อมูลหรือไม่
if users_data:
    # แสดงข้อมูลในรูปแบบตาราง
    user_table = []
    for user in users_data:
        user_table.append({
            "ID": user[0],
            "ชื่อเต็ม": user[1],
            "ชื่อเล่น": user[2],
            "หมายเลขบัตรประชาชน": user[3],
            "ที่อยู่": user[4],
            "หมายเลขโทรศัพท์": user[5],
            "มูลนิธิ": user[6],
            "ที่อยู่ภาพ": user[7]
        })
    st.table(user_table)
else:
    st.warning("ยังไม่มีข้อมูลในฐานข้อมูล")
