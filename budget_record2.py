import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# ตั้งค่าฟอนต์ Tahoma สำหรับ matplotlib
font_path = r'C:\Windows\Fonts\tahoma.ttf'

# ตรวจสอบว่าฟอนต์ Tahoma มีอยู่ในเครื่องหรือไม่
if os.path.exists(font_path):
    font_prop = font_manager.FontProperties(fname=font_path)
else:
    st.warning("ฟอนต์ Tahoma ไม่พบในเครื่อง จะใช้ฟอนต์เริ่มต้นแทน")
    font_prop = font_manager.FontProperties()  # ใช้ฟอนต์เริ่มต้น

# ชื่อไฟล์ CSV สำหรับบันทึกข้อมูล
csv_file = 'budget_data.csv'

# ฟังก์ชันโหลดข้อมูลจาก CSV ถ้ามีไฟล์อยู่
def load_data():
    try:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
        else:
            # ถ้าไม่มีไฟล์ CSV สร้าง DataFrame จากข้อมูลตัวอย่าง
            data = {
                'รายการงบประมาณ': [
                    'ค่า OT', 'รวมค่าตอบแทนคุ้มครองพยาน', 'ค่าตอบแทนพยาน', 'ค่าคุ้มครองพยาน', 'ค่าตอบแทนนักจิตวิทยา',
                    'ค่าตอบแทนชันสูตรพลิกศพ', 'คชจ.ในการส่งหมายเรียกพยาน', 'ค่าตอบแทนสอบสวนคดีอาญาฯ',
                    'ค่าเบี้ยเลี้ยงที่พักพาหนะ', 'ค่าซ่อมแซมยานพาหนะ', 'ค่าจ้างเหมาทำความสะอาด', 'วัสดุสำนักงาน',
                    'วัสดุน้ำมัน', 'วัสดุจราจร', 'วัสดุอาหารผู้ต้องหา', 'ค่าสาธารณูปโภค',
                    'งานสอบสวน', 'งานปราบปราม'
                ],
                'งบประมาณที่ได้รับ (บาท)': [
                    489600, 22000, 21800, 200, 4500, 27500, 1200, 0, 51600, 11900, 26400, 4600, 751700, 3300, 9300, 34000,
                    19400, 28400
                ],
                'จำนวนเงินที่ใช้ไปแล้ว (บาท)': [0.0] * 18
            }
            df = pd.DataFrame(data)
            df.to_csv(csv_file, index=False)  # บันทึกข้อมูลเริ่มต้นลงใน CSV
        return df
    except Exception as e:
        st.error("ไม่สามารถโหลดข้อมูลจากไฟล์ CSV ได้ กรุณาตรวจสอบไฟล์")
        return pd.DataFrame()  # ส่ง DataFrame ว่างในกรณีที่โหลดไฟล์ไม่ได้

# ฟังก์ชันบันทึกข้อมูลลงใน CSV
def save_data(df):
    try:
        df.to_csv(csv_file, index=False)
        st.success("ข้อมูลบันทึกลงในไฟล์ CSV เรียบร้อยแล้ว")
    except Exception as e:
        st.error("เกิดข้อผิดพลาดขณะบันทึกข้อมูล")

# ฟังก์ชันคำนวณเปอร์เซ็นต์การใช้จ่าย
def calculate_percentage_spent(df):
    df['เปอร์เซ็นต์การใช้จ่าย (%)'] = (df['จำนวนเงินที่ใช้ไปแล้ว (บาท)'] / df['งบประมาณที่ได้รับ (บาท)']) * 100
    df['เปอร์เซ็นต์การใช้จ่าย (%)'] = df['เปอร์เซ็นต์การใช้จ่าย (%)'].round(2)
    return df

# ฟังก์ชันสร้างกราฟแท่งแนวนอน
def plot_budget_chart(df):
    fig, ax = plt.subplots(figsize=(20, 10))
    x = np.arange(len(df))

    # แสดงแท่งกราฟที่ใช้จ่าย
    ax.barh(x - 0.2, df['จำนวนเงินที่ใช้ไปแล้ว (บาท)'], color='#32CD32', label='จำนวนเงินที่ใช้ไปแล้ว', edgecolor='black', height=0.45)

    # แสดงแท่งกราฟงบประมาณที่ได้รับ
    ax.barh(x + 0.2, df['งบประมาณที่ได้รับ (บาท)'], color='#FF6347', label='งบประมาณที่ได้รับ', edgecolor='black', height=0.45)

    # เพิ่มค่าให้กับแต่ละแท่ง
    for i, (spent, budget) in enumerate(zip(df['จำนวนเงินที่ใช้ไปแล้ว (บาท)'], df['งบประมาณที่ได้รับ (บาท)'])):
        ax.text(spent + 10000, i - 0.2, f'{spent:,.2f}', va='center', fontproperties=font_prop, fontsize=12, fontweight='bold', color="black")
        ax.text(budget + 10000, i + 0.2, f'{budget:,.2f}', va='center', fontproperties=font_prop, fontsize=12, fontweight='bold', color="black")

    ax.set_xlabel('จำนวนเงิน (บาท)', fontproperties=font_prop, fontsize=12, color="black")
    ax.set_ylabel('รายการงบประมาณ', fontproperties=font_prop, fontsize=12, color="black")
    ax.set_title('การใช้จ่ายและงบประมาณที่ได้รับ', fontproperties=font_prop, fontsize=14, color="black")
    
    # แสดงชื่อหมวดหมู่ที่แกน Y
    ax.set_yticks(x)
    ax.set_yticklabels(df['รายการงบประมาณ'], fontproperties=font_prop, fontsize=14, color="black")

    ax.legend(prop=font_prop, fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

# ฟังก์ชันจัดแต่งตารางให้สวยงาม
def style_dataframe(df):
    # กำหนดการจัดรูปแบบคอลัมน์
    df_styled = df.style.format({
        'งบประมาณที่ได้รับ (บาท)': '{:,.2f}',
        'จำนวนเงินที่ใช้ไปแล้ว (บาท)': '{:,.2f}',
        'เปอร์เซ็นต์การใช้จ่าย (%)': '{:,.2f}%'
    })

    # สีพื้นหลังของแถวที่สลับกันเพื่อให้อ่านง่าย
    df_styled = df_styled.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('background-color', '#0072B2'), ('color', 'white'), ('font-weight', 'bold')]
        },
        {
            'selector': 'tbody tr:nth-child(odd)',
            'props': [('background-color', '#f2f2f2')]  # สีพื้นหลังของแถวคี่
        },
        {
            'selector': 'tbody tr:nth-child(even)',
            'props': [('background-color', '#ffffff')]  # สีพื้นหลังของแถวคู่
        },
        {
            'selector': 'tbody tr:hover',
            'props': [('background-color', '#d3e0ea')]  # เมื่อเอาเมาส์ไปวางที่แถว
        },
        {
            'selector': 'td',
            'props': [('text-align', 'center')]  # จัดตำแหน่งตัวเลขให้อยู่กลาง
        }]
    )

    return df_styled

# Custom CSS to change the background color to white and adjust text colors
st.markdown("""
    <style>
        body {
            background-color: white;
            color: black;
        }
        .block-container {
            background-color: white;
        }
        .css-1v3fvcr {
            background-color: white;
        }
        h1, h2, h3, h4, h5, h6 {
            color: black;
        }
        .css-18e3th9 {
            color: black;
        }
        .stButton>button {
            color: black;
            background-color: #0072B2;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# เมนูต่าง ๆ
page = st.sidebar.radio("เลือกหน้า", ("บันทึกข้อมูล", "ดูกราฟ"))

# โหลดข้อมูล
df = load_data()

# หน้าบันทึกข้อมูล
if page == "บันทึกข้อมูล":
    st.title("บันทึกข้อมูลการใช้จ่ายงบประมาณ")
    # คำนวณเปอร์เซ็นต์การใช้จ่าย
    df = calculate_percentage_spent(df)
    st.dataframe(style_dataframe(df))
    st.markdown("**บันทึกข้อมูลการใช้จ่ายงบประมาณ**")
    for idx, row in df.iterrows():
        df.at[idx, 'จำนวนเงินที่ใช้ไปแล้ว (บาท)'] = st.number_input(
            f"จำนวนเงินที่ใช้ไปแล้ว ({row['รายการงบประมาณ']})",
            value=row['จำนวนเงินที่ใช้ไปแล้ว (บาท)'],
            min_value=0.0
        )

    # บันทึกข้อมูลเมื่อกดปุ่ม
    if st.button("บันทึกข้อมูล"):
        save_data(df)

# แสดงกราฟเมื่อเลือกหน้า "ดูกราฟ"
elif page == "ดูกราฟ":
    st.title("กราฟการใช้จ่ายงบประมาณ")
    plot_budget_chart(df)
