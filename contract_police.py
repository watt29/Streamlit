import streamlit as st
import requests
import pandas as pd

# ตั้งค่าตัวแปรจากข้อมูลที่ให้มา
NOTION_TOKEN = "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"
DATABASE_ID = "1784dda124a080e5acfaf1eec21a66c6"

# URL สำหรับเรียก Notion API
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

# Headers ที่ต้องการ
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2021-05-13",  # ใช้เวอร์ชันล่าสุดที่รองรับ
    "Content-Type": "application/json",
}

# ฟังก์ชันเพื่อดึงข้อมูลจาก Notion API พร้อมการทำ Pagination
def fetch_notion_data():
    all_data = []  # ใช้เก็บข้อมูลทั้งหมด
    next_cursor = None  # เริ่มต้นไม่มี cursor
    
    while True:
        # ถ้ามี cursor ในคำขอก่อนหน้านี้ ให้ใช้มัน
        payload = {}
        if next_cursor:
            payload['start_cursor'] = next_cursor  # ใช้ cursor ถ้ามี

        # ส่งคำขอไปที่ Notion API
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['results'])  # รวมข้อมูลจากชุดนี้
            
            # ตรวจสอบว่ามี next_cursor หรือไม่
            next_cursor = data.get('next_cursor')  # เอาค่า cursor ถ้ามี
            if not next_cursor:
                break  # ถ้าไม่มี next_cursor แสดงว่าได้ข้อมูลทั้งหมดแล้ว
        else:
            st.error(f"ไม่สามารถดึงข้อมูลได้, สถานะ: {response.status_code}")
            break
    
    return all_data

# ฟังก์ชันแปลงข้อมูลที่ได้จาก Notion ให้เป็น DataFrame ของ Pandas
def convert_to_dataframe(data):
    rows = []
    for result in data:
        try:
            name = result['properties']['ชื่อ']['title'][0]['text']['content']
            position = result['properties']['ตำแหน่ง']['rich_text'][0]['text']['content']
            phone = result['properties'].get('เบอร์โทรศัพท์', {}).get('phone_number', 'ไม่มีข้อมูลเบอร์โทรศัพท์')
            workplace = result['properties'].get('ที่ทำงาน', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'ไม่มีข้อมูลที่ทำงาน')

            # สร้างลิงก์โทรศัพท์ในกรณีที่มีเบอร์โทรศัพท์
            if phone != 'ไม่มีข้อมูลเบอร์โทรศัพท์':
                phone = f"[{phone}](tel:{phone})"
            
            rows.append([name, position, phone, workplace])
        except KeyError as e:
            st.warning(f"ข้อมูลบางอย่างขาดหายไป: {e}")
    
    # สร้าง DataFrame จากรายการที่ได้
    df = pd.DataFrame(rows, columns=["ชื่อ", "ตำแหน่ง", "เบอร์โทรศัพท์", "ที่ทำงาน"])
    return df

# ฟังก์ชันเพื่อเน้นแถวที่ตรงกับคำค้นหา
def highlight_search_results(row, search_term):
    return ['background-color: yellow' if search_term.lower() in str(val).lower() else '' for val in row]

# สร้าง UI ด้วย Streamlit
st.title("เบอร์โทรศัพท์ข้าราชตำรวจและข้าราชการอื่นๆ")
st.write("แสดงข้อมูลจากฐานข้อมูล Notion พร้อมฟังก์ชันการค้นหา")

# ดึงข้อมูลจาก Notion API
data = fetch_notion_data()

# ถ้ามีข้อมูล
if data:
    df = convert_to_dataframe(data)

    # เพิ่มช่องค้นหาในตาราง
    search_term = st.text_input("ค้นหาข้อมูล (ชื่อ, ตำแหน่ง, เบอร์โทรศัพท์, หรือที่ทำงาน)")

    if search_term:
        # ฟิลเตอร์แถวที่มีคำค้นหาในคอลัมน์ต่างๆ
        df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.write(f"พบผลลัพธ์ {len(df_filtered)} รายการจากการค้นหาคำว่า '{search_term}'")

        # ใช้ฟังก์ชัน highlight เพื่อเน้นแถวที่ตรงกับคำค้นหา
        st.dataframe(df_filtered.style.apply(lambda row: highlight_search_results(row, search_term), axis=1))

    else:
        # ถ้าไม่มีการค้นหา ให้แสดงตารางทั้งหมด
        st.write("ผลลัพธ์ทั้งหมด:")
        st.dataframe(df)

else:
    st.write("ไม่พบข้อมูลจากฐานข้อมูล Notion")
