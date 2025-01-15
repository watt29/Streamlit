import streamlit as st
import requests
import pandas as pd

# ตั้งค่าตัวแปรจากข้อมูลที่ให้มา
NOTION_TOKEN = "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"
DATABASE_ID = "1784dda124a080e5acfaf1eec21a66c6"

# URL สำหรับเรียก Notion API
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

# ตั้งค่า headers สำหรับการขอข้อมูลจาก Notion API
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"  # กำหนดเวอร์ชัน API ที่ใช้
}

# ทำการขอข้อมูลจาก Notion API
response = requests.post(url, headers=headers)

# ตรวจสอบว่าได้ผลลัพธ์สำเร็จหรือไม่
if response.status_code == 200:
    data = response.json()
    
    # สร้าง DataFrame จากข้อมูลที่ได้
    rows = []
    for result in data.get("results", []):
        row = {}
        for property_name, property_data in result["properties"].items():
            # ตรวจสอบว่าเป็น "title" หรือไม่
            row[property_name] = property_data.get("title", [{"text": {"content": ""}}])[0]["text"]["content"]
        rows.append(row)

    # สร้าง DataFrame จากข้อมูลที่ได้
    df = pd.DataFrame(rows)

    # ช่องค้นหาที่จะใช้กรองข้อมูล
    search_term = st.text_input("ค้นหาข้อมูล (ชื่อ, ตำแหน่ง, เบอร์โทรศัพท์, หรือที่ทำงาน)")

    if search_term:
        # กรองข้อมูลตามคำค้น
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        # ถ้าไม่มีคำค้น ให้แสดงข้อมูลทั้งหมด
        filtered_df = df

    # แปลงเบอร์โทรให้เป็นลิงก์
    if 'เบอร์โทรศัพท์' in filtered_df.columns:
        filtered_df['เบอร์โทรศัพท์'] = filtered_df['เบอร์โทรศัพท์'].apply(lambda x: f'<a href="tel:{x}">{x}</a>' if pd.notnull(x) else '')

    # ใช้ st.markdown เพื่อแสดง DataFrame ที่ปรับแต่ง
    st.markdown("""
        <style>
        .stDataFrame td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }
        .stDataFrame th {
            background-color: #f0f0f0;
            text-align: center;
            font-weight: bold;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(filtered_df.to_html(escape=False), unsafe_allow_html=True)

else:
    st.error(f"Error: {response.status_code} - {response.text}")
