import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import urllib
import os

# URL ของฟอนต์ที่อัพโหลดไปยัง GitHub (raw link)
font_url = "https://raw.githubusercontent.com/watt29/Streamlit/main/Kanit-Regular.ttf"

# กำหนดเส้นทางที่จะบันทึกไฟล์ฟอนต์
font_path = "Kanit-Regular.ttf"

# โหลดฟอนต์จาก URL
try:
    urllib.request.urlretrieve(font_url, font_path)  # ดาวน์โหลดฟอนต์จาก URL
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()  # ตั้งค่าให้ matplotlib ใช้ฟอนต์นี้
    print("Font used:", plt.rcParams['font.family'])
except Exception as e:
    st.warning(f"ไม่สามารถดาวน์โหลดฟอนต์ได้: {e}")
    plt.rcParams['font.family'] = 'Arial'  # ใช้ฟอนต์เริ่มต้นถ้าโหลดฟอนต์ไม่ได้

# ชื่อไฟล์ CSV สำหรับบันทึกข้อมูล
csv_file = 'budget_data.csv'

# ฟังก์ชันโหลดข้อมูลจาก CSV ถ้ามีไฟล์อยู่
def load_data():
    try:
        if os.path.exists(csv_file):  # ใช้ os.path.exists เพื่อตรวจสอบว่าไฟล์มีอยู่หรือไม่
            df = pd.read_csv(csv_file)
        else:
            # ถ้าไม่มีไฟล์ CSV สร้าง DataFrame จากข้อมูลตัวอย่าง
            data = {
                'รายการ': [
                    'โครงการ การมีส่วนร่วมของประชาชนในการป้องกันอาชญากรรม (เครือข่ายตำบล)', 
                    'โครงการชุมชนสัมพันธ์ การมีส่วนร่วมของประชาชนในการป้องกันอาชญากรรม',
                    'โครงการการสร้างภูมิคุ้มกันในกลุ่มเป้าหมายระดับโรงเรียน',
                    'โครงการการสกัดกั้น ปราบปราม การผลิตการค้ายาเสพติด',
                    'โครงการรณรงค์ป้องกันและแก้ไขปัญหาอุบัติเหตุทางถนนช่วงเทศกาลสำคัญ',
                    'รวม'
                ],
                'งบประมาณที่ได้รับ (บาท)': [15000, 26000, 2140, 55180, 42000, 140320],
                'ผลการเบิกจ่าย (บาท)': [0.0, 0.0, 0.0, 0.0, 0.0, 140320]  # กำหนดค่าเริ่มต้นเป็น 0
            }
            df = pd.DataFrame(data)
            df.to_csv(csv_file, index=False)  # บันทึกข้อมูลเริ่มต้นลงใน CSV
        return df
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
        return pd.DataFrame()

# โหลดข้อมูล
df = load_data()

# แปลงคอลัมน์ให้เป็นตัวเลข และแทนที่ NaN ด้วย 0
df['งบประมาณที่ได้รับ (บาท)'] = pd.to_numeric(df['งบประมาณที่ได้รับ (บาท)'], errors='coerce').fillna(0)
df['ผลการเบิกจ่าย (บาท)'] = pd.to_numeric(df['ผลการเบิกจ่าย (บาท)'], errors='coerce').fillna(0)

# แสดงข้อมูลใน Streamlit
st.title("ข้อมูลงบประมาณโครงการ")
st.write("ข้อมูลงบประมาณและการเบิกจ่ายในโครงการต่างๆ")
st.dataframe(df)

# ฟอร์มกรอกข้อมูลใหม่
st.header("กรอกข้อมูลโครงการใหม่")
project_name = st.text_input("ชื่อโครงการ")
budget_received = st.number_input("งบประมาณที่ได้รับ (บาท)", min_value=0)
amount_spent = st.number_input("ผลการเบิกจ่าย (บาท)", min_value=0)

# ถ้าผู้ใช้กรอกข้อมูลแล้วกดปุ่มบันทึก
if st.button("บันทึกข้อมูล"):
    if project_name and budget_received >= 0 and amount_spent >= 0:
        # เพิ่มข้อมูลลงใน DataFrame
        new_data = pd.DataFrame({
            'รายการ': [project_name],
            'งบประมาณที่ได้รับ (บาท)': [budget_received],
            'ผลการเบิกจ่าย (บาท)': [amount_spent]
        })

        # เพิ่มข้อมูลใหม่ลงใน DataFrame เดิม
        df = pd.concat([df, new_data], ignore_index=True)

        # แปลงข้อมูลให้เป็นตัวเลขและแทนที่ NaN ด้วย 0
        df['งบประมาณที่ได้รับ (บาท)'] = pd.to_numeric(df['งบประมาณที่ได้รับ (บาท)'], errors='coerce').fillna(0)
        df['ผลการเบิกจ่าย (บาท)'] = pd.to_numeric(df['ผลการเบิกจ่าย (บาท)'], errors='coerce').fillna(0)

        # บันทึกข้อมูลลงในไฟล์ CSV
        df.to_csv(csv_file, index=False)

        st.success("บันทึกข้อมูลสำเร็จ!")
        st.dataframe(df)  # แสดงข้อมูลใหม่
    else:
        st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

# ฟอร์มแก้ไขข้อมูล
st.header("แก้ไขข้อมูลโครงการ")
project_to_edit = st.selectbox("เลือกโครงการที่ต้องการแก้ไข", df['รายการ'].tolist())

# ค้นหาข้อมูลโครงการที่เลือก
if project_to_edit:
    project_index = df[df['รายการ'] == project_to_edit].index[0]
    current_budget = df.loc[project_index, 'งบประมาณที่ได้รับ (บาท)']
    current_spent = df.loc[project_index, 'ผลการเบิกจ่าย (บาท)']

    # ตรวจสอบว่า current_spent เป็นตัวเลขหรือไม่
    if not isinstance(current_spent, (int, float)): 
        current_spent = 0.0  # กำหนดค่าเริ่มต้นเป็น 0 ถ้าเป็น None หรือ NaN

    # แสดงข้อมูลปัจจุบันในฟอร์ม
    new_budget = st.number_input("งบประมาณที่ได้รับ (บาท)", min_value=0, value=current_budget)
    new_spent = st.number_input("ผลการเบิกจ่าย (บาท)", min_value=0, value=current_spent)

    if st.button("บันทึกการแก้ไข"):
        # แก้ไขข้อมูลใน DataFrame
        df.loc[project_index, 'งบประมาณที่ได้รับ (บาท)'] = new_budget
        df.loc[project_index, 'ผลการเบิกจ่าย (บาท)'] = new_spent

        # บันทึกข้อมูลที่แก้ไขลงใน CSV
        df.to_csv(csv_file, index=False)

        st.success("แก้ไขข้อมูลสำเร็จ!")
        st.dataframe(df)  # แสดงข้อมูลที่แก้ไข

# แสดงกราฟแสดงผลการเบิกจ่าย
fig, ax = plt.subplots(figsize=(10, 6))

# สร้างกราฟแท่งจากข้อมูลในตาราง
ax.bar(df['รายการ'], df['งบประมาณที่ได้รับ (บาท)'], label='งบประมาณที่ได้รับ', alpha=0.7)
ax.bar(df['รายการ'], df['ผลการเบิกจ่าย (บาท)'], label='ผลการเบิกจ่าย', alpha=0.7)

# เพิ่มรายละเอียดในกราฟ
ax.set_xlabel('รายการโครงการ', fontproperties=font_prop, fontsize=12)
ax.set_ylabel('จำนวนเงิน (บาท)', fontproperties=font_prop, fontsize=12)
ax.set_title('การเปรียบเทียบงบประมาณที่ได้รับและผลการเบิกจ่าย', fontproperties=font_prop, fontsize=14)
ax.legend()

# แสดงกราฟใน Streamlit
st.pyplot(fig)
