import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os

# ตั้งชื่อไฟล์ CSV ใหม่
csv_file = 'budget_data.csv'  # เปลี่ยนชื่อไฟล์ที่นี่

# ตรวจสอบว่ามีข้อมูลเก่าหรือไม่
if 'df' not in st.session_state:
    # ถ้าไม่มีข้อมูลใน session_state ให้สร้างข้อมูลใหม่
    if not os.path.exists(csv_file):
        data = {
            'รายการ': [
                'โครงการ การมีส่วนร่วมของประชาชนในการป้องกันอาชญากรรม (เครือข่ายตำบล)', 
                'โครงการชุมชนสัมพันธ์ การมีส่วนร่วมของประชาชนในการป้องกันอาชญากรรม',
                'โครงการการสร้างภูมิคุ้มกันในกลุ่มเป้าหมายระดับโรงเรียน',
                'โครงการการสกัดกั้น ปราบปราม การผลิตการค้ายาเสพติด',
                'โครงการรณรงค์ป้องกันและแก้ไขปัญหาอุบัติเหตุทางถนนช่วงเทศกาลสำคัญ',
            ],
            'งบประมาณที่ได้รับ (บาท)': [15000, 26000, 2140, 55180, 42000],
            'ผลการเบิกจ่าย (บาท)': [14000, 25000, 2100, 50000, 40000]  # ผลการเบิกจ่าย
        }

        # สร้าง DataFrame
        df = pd.DataFrame(data)
        # บันทึก DataFrame ลงไฟล์ CSV ใหม่
        df.to_csv(csv_file, index=False)
    else:
        # โหลดข้อมูลจาก CSV หากมีไฟล์
        df = pd.read_csv(csv_file)

    # เพิ่มคอลัมน์คำนวณเปอร์เซ็นต์การเบิกจ่าย
    df['เปอร์เซ็นต์การเบิกจ่าย (%)'] = (df['ผลการเบิกจ่าย (บาท)'] / df['งบประมาณที่ได้รับ (บาท)'] * 100).round(2)

    # เก็บข้อมูลใน session_state
    st.session_state.df = df

else:
    df = st.session_state.df

# เพิ่มตัวเลือกให้เลือกดูกราฟหรือกรอกข้อมูลใหม่
option = st.selectbox(
    'เลือกตัวเลือก:',
    ['ดูกราฟ', 'กรอกข้อมูลใหม่', 'แก้ไขข้อมูลเดิม']
)

# ถ้าเลือกดูกราฟ
if option == 'ดูกราฟ':
    # สร้างกราฟการเปรียบเทียบงบประมาณที่ได้รับและผลการเบิกจ่าย
    index = np.arange(len(df))  # สร้าง index สำหรับการแสดงผลกราฟ

    fig, ax = plt.subplots(figsize=(10, 6))

    # กราฟแท่ง
    bar_width = 0.35

    # กราฟงบประมาณที่ได้รับ
    bars1 = ax.bar(index, df['งบประมาณที่ได้รับ (บาท)'], bar_width, label='งบประมาณที่ได้รับ (บาท)', color='skyblue')

    # กราฟผลการเบิกจ่าย
    bars2 = ax.bar(index + bar_width, df['ผลการเบิกจ่าย (บาท)'], bar_width, label='ผลการเบิกจ่าย (บาท)', color='orange')

    # เพิ่มตัวเลขบนแท่ง
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 100, f'{height}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkblue')

    for i, bar in enumerate(bars2):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 100, f'{height}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkred')

    # ปรับแต่งกราฟ
    ax.set_xlabel('รายการ')
    ax.set_ylabel('จำนวนเงิน (บาท)')
    ax.set_title('การเปรียบเทียบงบประมาณที่ได้รับและผลการเบิกจ่าย')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(df['รายการ'], rotation=45, ha="right")
    ax.legend()

    # แสดงกราฟใน Streamlit
    st.write("### การเปรียบเทียบงบประมาณที่ได้รับและผลการเบิกจ่าย")
    st.pyplot(fig)

# ถ้าเลือกกรอกข้อมูลใหม่
if option == 'กรอกข้อมูลใหม่':
    # ฟอร์มกรอกข้อมูล
    st.write("### กรอกข้อมูลโครงการใหม่")
    new_project = st.text_input('ชื่อโครงการใหม่')
    new_budget = st.number_input('งบประมาณที่ได้รับ (บาท)', min_value=0)
    new_spent = st.number_input('ผลการเบิกจ่าย (บาท)', min_value=0)
    
    if st.button('เพิ่มข้อมูล'):
        if new_project and new_budget > 0 and new_spent >= 0:
            new_data = {
                'รายการ': [new_project],
                'งบประมาณที่ได้รับ (บาท)': [new_budget],
                'ผลการเบิกจ่าย (บาท)': [new_spent]
            }
            new_df = pd.DataFrame(new_data)
            # เพิ่มข้อมูลใหม่ใน DataFrame
            df = pd.concat([df, new_df], ignore_index=True)
            # คำนวณเปอร์เซ็นต์การเบิกจ่าย
            df['เปอร์เซ็นต์การเบิกจ่าย (%)'] = (df['ผลการเบิกจ่าย (บาท)'] / df['งบประมาณที่ได้รับ (บาท)'] * 100).round(2)
            # อัปเดต DataFrame ใน session_state
            st.session_state.df = df
            # บันทึกข้อมูลใน CSV
            df.to_csv(csv_file, index=False)
            st.success("ข้อมูลถูกเพิ่มเรียบร้อยแล้ว")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")

# ถ้าเลือกแก้ไขข้อมูลเดิม
if option == 'แก้ไขข้อมูลเดิม':
    # เลือกรายการที่ต้องการแก้ไข
    project_to_edit = st.selectbox('เลือกชื่อโครงการที่ต้องการแก้ไข', df['รายการ'])

    # ค้นหาข้อมูลของโครงการที่เลือก
    project_index = df[df['รายการ'] == project_to_edit].index[0]
    old_budget = df.at[project_index, 'งบประมาณที่ได้รับ (บาท)']
    old_spent = df.at[project_index, 'ผลการเบิกจ่าย (บาท)']

    # กรอกข้อมูลใหม่
    st.write(f"แก้ไขข้อมูลสำหรับโครงการ: {project_to_edit}")
    new_budget = st.number_input('งบประมาณที่ได้รับ (บาท)', min_value=0, value=old_budget)
    new_spent = st.number_input('ผลการเบิกจ่าย (บาท)', min_value=0, value=old_spent)

    if st.button('อัปเดตข้อมูล'):
        # อัปเดตข้อมูลใน DataFrame
        df.at[project_index, 'งบประมาณที่ได้รับ (บาท)'] = new_budget
        df.at[project_index, 'ผลการเบิกจ่าย (บาท)'] = new_spent
        # คำนวณเปอร์เซ็นต์การเบิกจ่ายใหม่
        df['เปอร์เซ็นต์การเบิกจ่าย (%)'] = (df['ผลการเบิกจ่าย (บาท)'] / df['งบประมาณที่ได้รับ (บาท)'] * 100).round(2)
        # อัปเดตข้อมูลใน session_state
        st.session_state.df = df
        # บันทึกข้อมูลใน CSV
        df.to_csv(csv_file, index=False)
        st.success("ข้อมูลได้รับการอัปเดตเรียบร้อยแล้ว")
