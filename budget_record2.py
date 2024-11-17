import urllib.request
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import os

# URL ฟอนต์
font_url = "https://raw.githubusercontent.com/watt29/Streamlit/main/Kanit-Regular.ttf"
font_path = "Kanit-Regular.ttf"

# โหลดฟอนต์จาก URL
try:
    urllib.request.urlretrieve(font_url, font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except Exception:
    plt.rcParams['font.family'] = 'Arial'  # ใช้ฟอนต์ Arial เป็นค่าเริ่มต้นหากโหลดฟอนต์ไม่สำเร็จ

# ชื่อไฟล์ CSV
csv_file = 'budget_data1.csv'

# ฟังก์ชันโหลดข้อมูลจาก CSV
def load_data():
    try:
        if os.path.exists(csv_file):
            return pd.read_csv(csv_file)
        else:
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
            df.to_csv(csv_file, index=False)
            return df
    except Exception:
        st.error("ไม่สามารถโหลดข้อมูลจากไฟล์ CSV ได้")
        return pd.DataFrame()

# ฟังก์ชันบันทึกข้อมูลลง CSV
def save_data(df):
    try:
        df.to_csv(csv_file, index=False)
        st.success("ข้อมูลบันทึกเรียบร้อย")
    except Exception:
        st.error("เกิดข้อผิดพลาดขณะบันทึกข้อมูล")

# ฟังก์ชันคำนวณเปอร์เซ็นต์การใช้จ่าย
def calculate_percentage_spent(df):
    df['เปอร์เซ็นต์การใช้จ่าย (%)'] = (df['จำนวนเงินที่ใช้ไปแล้ว (บาท)'] / df['งบประมาณที่ได้รับ (บาท)']) * 100
    df['เปอร์เซ็นต์การใช้จ่าย (%)'] = df['เปอร์เซ็นต์การใช้จ่าย (%)'].fillna(0).round(2)
    return df

# ฟังก์ชันสร้างกราฟ
def plot_budget_chart(df):
    fig, ax = plt.subplots(figsize=(12, 8))
    x = np.arange(len(df))

    ax.barh(x - 0.2, df['จำนวนเงินที่ใช้ไปแล้ว (บาท)'], color='#32CD32', label='จำนวนเงินที่ใช้ไปแล้ว', edgecolor='black', height=0.4)
    ax.barh(x + 0.2, df['งบประมาณที่ได้รับ (บาท)'], color='#FF6347', label='งบประมาณที่ได้รับ', edgecolor='black', height=0.4)

    for i, (spent, budget) in enumerate(zip(df['จำนวนเงินที่ใช้ไปแล้ว (บาท)'], df['งบประมาณที่ได้รับ (บาท)'])):
        ax.text(spent + 5000, i - 0.2, f'{spent:,.2f}', va='center', fontsize=10, fontproperties=font_prop)
        ax.text(budget + 5000, i + 0.2, f'{budget:,.2f}', va='center', fontsize=10, fontproperties=font_prop)

    ax.set_xlabel('จำนวนเงิน (บาท)', fontproperties=font_prop)
    ax.set_ylabel('รายการงบประมาณ', fontproperties=font_prop)
    ax.set_yticks(x)
    ax.set_yticklabels(df['รายการงบประมาณ'], fontsize=10, fontproperties=font_prop)
    ax.set_title('การใช้จ่ายงบประมาณ', fontproperties=font_prop)
    ax.legend(prop=font_prop)
    st.pyplot(fig)

# โหลดข้อมูล
df = load_data()

# เมนูหลัก
page = st.sidebar.radio("เลือกหน้า", ["บันทึกข้อมูล", "ดูกราฟ"])

# หน้า "บันทึกข้อมูล"
if page == "บันทึกข้อมูล":
    st.title("บันทึกข้อมูล")
    for i in range(len(df)):
        df.at[i, 'จำนวนเงินที่ใช้ไปแล้ว (บาท)'] = st.number_input(
            f"{df.loc[i, 'รายการงบประมาณ']}",
            value=float(df.loc[i, 'จำนวนเงินที่ใช้ไปแล้ว (บาท)']),
            min_value=0.0
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("บันทึกข้อมูล"):
            save_data(df)
    with col2:
        if st.button("ล้างข้อมูล"):
            df['จำนวนเงินที่ใช้ไปแล้ว (บาท)'] = 0.0
            save_data(df)
            st.success("ล้างข้อมูลเรียบร้อย!")

    st.subheader("ข้อมูลปัจจุบัน")
    st.dataframe(calculate_percentage_spent(df))

# หน้า "ดูกราฟ"
elif page == "ดูกราฟ":
    st.title("ดูกราฟ")
    df = calculate_percentage_spent(df)
    plot_budget_chart(df)

    st.subheader("ข้อมูลสรุปงบประมาณ")
    st.dataframe(df)

    st.download_button(
        label="ดาวน์โหลดข้อมูลเป็น Excel",
        data=df.to_csv(index=False, encoding='utf-8-sig'),
        file_name="budget_summary.csv",
        mime="text/csv"
    )
