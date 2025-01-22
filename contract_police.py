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
            rows.append([name, phone, position, workplace])
        except KeyError as e:
            st.warning(f"ข้อมูลบางอย่างขาดหายไป: {e}")
    
    # สร้าง DataFrame จากรายการที่ได้
    df = pd.DataFrame(rows, columns=["ชื่อ", "เบอร์โทรศัพท์", "ตำแหน่ง", "ที่ทำงาน"])
    return df

# ฟังก์ชันเพื่อเน้นแถวที่ตรงกับคำค้นหา
def highlight_search_results(row, search_term):
    return ['background-color: #ffeb3b' if search_term.lower() in str(val).lower() else '' for val in row]

# ปรับแต่งธีม Streamlit สำหรับมือถือและข้อมูล
st.markdown(
    """
    <style>
        /* Body Styling */
        body {
            font-size: 14px;  
            line-height: 1.6;
            background-color: #eaf7ff;  /* สีพื้นหลังที่ดูเย็นตา */
            color: #333;
            font-family: 'Arial', sans-serif;
        }

        /* Header */
        h1 {
            font-size: 32px;
            color: #4CAF50;
            font-weight: 600;
            text-align: center;
            padding: 20px 0;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        h2 {
            font-size: 22px;
            color: #444;
            margin-bottom: 30px;
            text-align: center;
        }

        /* Button */
        .stButton>button {
            font-size: 16px;
            padding: 12px 30px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s, box-shadow 0.3s;
        }

        .stButton>button:hover {
            background-color: #45a049;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }

        /* Input Fields */
        .stTextInput>div>input {
            font-size: 16px;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #ccc;
            background-color: #fff;
            margin-bottom: 20px;
            transition: border 0.3s;
        }

        .stTextInput>div>input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
        }

        /* DataTable Styling */
        .stDataFrame {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow-x: auto;
            font-size: 14px;
            margin-top: 20px;
        }

        .stDataFrame th {
            background-color: #4CAF50;
            color: white;
            font-weight: 600;
            padding: 15px;
        }

        .stDataFrame td {
            font-size: 14px;
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        .stDataFrame tr:hover {
            background-color: #f1f1f1;
        }

        .stTextInput {
            width: 100%;
        }

        /* Customizing the "เบอร์โทรศัพท์" Column */
        .stDataFrame td:nth-child(2) {
            font-size: 13px;
            color: #4CAF50;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# สร้าง UI ด้วย Streamlit
st.markdown("---")

# ดึงข้อมูลจาก Notion API
data = fetch_notion_data()

# ถ้ามีข้อมูล
if data:
    df = convert_to_dataframe(data)

    # เพิ่มช่องค้นหาข้อมูล
    search_term = st.text_input("🔍 ค้นหาข้อมูล (ชื่อ, เบอร์โทรศัพท์, ตำแหน่ง, หรือที่ทำงาน)", "")

    # แสดงข้อมูลทั้งหมด โดยทำการเน้นแถวที่ตรงกับคำค้นหา
    st.write("ผลลัพธ์ทั้งหมด:")
    if search_term:
        # ค้นหาคำในทุกคอลัมน์
        df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.write(f"พบผลลัพธ์ {len(df_filtered)} รายการจากการค้นหาคำว่า '{search_term}'")

        # ใช้ฟังก์ชัน highlight เพื่อเน้นแถวที่ตรงกับคำค้นหา
        st.dataframe(df_filtered.style.apply(lambda row: highlight_search_results(row, search_term), axis=1))
    else:
        # แสดงข้อมูลทั้งหมดเมื่อไม่มีการค้นหา
        st.dataframe(df)

else:
    st.write("ไม่พบข้อมูลจากฐานข้อมูล Notion")
