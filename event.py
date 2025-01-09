import streamlit as st
import folium
from streamlit_folium import st_folium

# ข้อมูลเหตุการณ์ในอำเภอมหาราช
data = {
    'Location Name': ['ตลาดมหาราช', 'วัดมหาราช', 'สถานีตำรวจมหาราช'],
    'Latitude': [14.54749, 14.6123, 14.6178],
    'Longitude': [100.50327, 100.5184, 100.5251],
    'Crime Frequency': [4, 6, 2],
    'Incident Details': [
        'เหตุลักทรัพย์ที่ตลาด 2 ครั้งในสัปดาห์ที่ผ่านมา',
        'เหตุทะเลาะวิวาทในพื้นที่วัด 4 ครั้ง',
        'เหตุชิงทรัพย์ใกล้สถานีตำรวจ 1 ครั้ง'
    ]
}

# สร้างแผนที่ Folium
m = folium.Map(location=[14.6100, 100.5200], zoom_start=13)

# เพิ่ม Marker สำหรับแต่ละเหตุการณ์
for i in range(len(data['Location Name'])):
    folium.Marker(
        location=[data['Latitude'][i], data['Longitude'][i]],
        popup=(
            f"<b>{data['Location Name'][i]}</b><br>"
            f"จำนวนเหตุการณ์: {data['Crime Frequency'][i]} ครั้ง<br>"
            f"รายละเอียด: {data['Incident Details'][i]}"
        ),
        icon=folium.Icon(color='blue')
    ).add_to(m)

# แสดงแผนที่ใน Streamlit
st.title("แผนที่เหตุการณ์อาชญากรรมในอำเภอมหาราช")
st_folium(m, width=700)
