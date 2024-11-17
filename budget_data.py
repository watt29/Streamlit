import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# Set font path for Tahoma
font_path = r'C:\Windows\Fonts\tahoma.ttf'

# Check if Tahoma font is available
if os.path.exists(font_path):
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()  # Set Tahoma font for matplotlib
else:
    st.warning("Tahoma font not found, defaulting to Arial.")
    plt.rcParams['font.family'] = 'Arial'  # Use default font if Tahoma is not found

# Define CSV file name
csv_file = 'budget_data.csv'

# Check if there is existing data in session_state
if 'df' not in st.session_state:
    # If no data in session_state, create new data
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
            'ผลการเบิกจ่าย (บาท)': [14000, 25000, 2100, 50000, 40000]  # Actual spending
        }

        # Create DataFrame
        df = pd.DataFrame(data)
        # Save DataFrame to CSV
        df.to_csv(csv_file, index=False)
    else:
        # Load data from CSV if it exists
        df = pd.read_csv(csv_file)

    # Add percentage column for spending
    df['เปอร์เซ็นต์การเบิกจ่าย (%)'] = (df['ผลการเบิกจ่าย (บาท)'] / df['งบประมาณที่ได้รับ (บาท)'] * 100).round(2)

    # Store DataFrame in session_state
    st.session_state.df = df
else:
    df = st.session_state.df

# Option to view graph, enter new data, or edit existing data
option = st.selectbox(
    'เลือกตัวเลือก:',
    ['ดูกราฟ', 'กรอกข้อมูลใหม่', 'แก้ไขข้อมูลเดิม']
)

# If 'ดูกราฟ' is selected
if option == 'ดูกราฟ':
    # Generate comparison bar chart for received budget vs actual spending
    index = np.arange(len(df))  # Create index for chart

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.35  # Bar width

    # Budget received bars
    bars1 = ax.bar(index, df['งบประมาณที่ได้รับ (บาท)'], bar_width, label='งบประมาณที่ได้รับ (บาท)', color='skyblue')

    # Actual spending bars
    bars2 = ax.bar(index + bar_width, df['ผลการเบิกจ่าย (บาท)'], bar_width, label='ผลการเบิกจ่าย (บาท)', color='orange')

    # Annotate bars with values
    for i, bar in enumerate(bars1):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100, f'{bar.get_height()}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkblue')

    for i, bar in enumerate(bars2):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100, f'{bar.get_height()}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkred')

    # Chart settings
    ax.set_xlabel('รายการ')
    ax.set_ylabel('จำนวนเงิน (บาท)')
    ax.set_title('การเปรียบเทียบงบประมาณที่ได้รับและผลการเบิกจ่าย')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(df['รายการ'], rotation=45, ha="right")
    ax.legend()

    # Display chart in Streamlit
    st.write("### การเปรียบเทียบงบประมาณที่ได้รับและผลการเบิกจ่าย")
    st.pyplot(fig)

# If 'กรอกข้อมูลใหม่' is selected
if option == 'กรอกข้อมูลใหม่':
    # Input form for new project data
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
            # Add new data to DataFrame
            df = pd.concat([df, new_df], ignore_index=True)
            # Recalculate percentage of spending
            df['เปอร์เซ็นต์การเบิกจ่าย (%)'] = (df['ผลการเบิกจ่าย (บาท)'] / df['งบประมาณที่ได้รับ (บาท)'] * 100).round(2)
            # Update session state
            st.session_state.df = df
            # Save updated data to CSV
            df.to_csv(csv_file, index=False)
            st.success("ข้อมูลถูกเพิ่มเรียบร้อยแล้ว")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")

# If 'แก้ไขข้อมูลเดิม' is selected
if option == 'แก้ไขข้อมูลเดิม':
    # Select the project to edit
    project_to_edit = st.selectbox('เลือกชื่อโครงการที่ต้องการแก้ไข', df['รายการ'])

    # Find the selected project data
    project_index = df[df['รายการ'] == project_to_edit].index[0]
    old_budget = df.at[project_index, 'งบประมาณที่ได้รับ (บาท)']
    old_spent = df.at[project_index, 'ผลการเบิกจ่าย (บาท)']

    # Input new values for the selected project
    st.write(f"แก้ไขข้อมูลสำหรับโครงการ: {project_to_edit}")
    new_budget = st.number_input('งบประมาณที่ได้รับ (บาท)', min_value=0, value=old_budget)
    new_spent = st.number_input('ผลการเบิกจ่าย (บาท)', min_value=0, value=old_spent)

    if st.button('อัปเดตข้อมูล'):
        # Update data in DataFrame
        df.at[project_index, 'งบประมาณที่ได้รับ (บาท)'] = new_budget
        df.at[project_index, 'ผลการเบิกจ่าย (บาท)'] = new_spent
        # Recalculate percentage of spending
        df['เปอร์เซ็นต์การเบิกจ่าย (%)'] = (df['ผลการเบิกจ่าย (บาท)'] / df['งบประมาณที่ได้รับ (บาท)'] * 100).round(2)
        # Update session state
        st.session_state.df = df
        # Save updated data to CSV
        df.to_csv(csv_file, index=False)
        st.success("ข้อมูลได้รับการอัปเดตเรียบร้อยแล้ว")
