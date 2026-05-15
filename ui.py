import streamlit as st
import pandas as pd
from main import calculate_lots

st.set_page_config(page_title="Forex Position Sizing & Lot Calculator", page_icon="📈", layout="centered")

st.title("📈 Forex Position Sizing & Lot Calculator")
st.markdown("เครื่องมือคำนวณการออก Lot แบบสมจริง (เช่น ทุน $10 ทนลาก 1000 จุด จะออกได้ 0.01 Lot เท่ากับความเสี่ยงสูญเสีย $10)")

# 1. ส่วนรับข้อมูลจากผู้ใช้ (Input Section)
st.header("1. ข้อมูลการเทรด (Input Section)")

col1, col2 = st.columns(2)
with col1:
    balance = st.number_input("💵 เงินทุน (Balance) - USD ($)", min_value=0.01, value=10.0, step=1.0, format="%.2f")
    risk_percent = st.number_input("⚠️ ความเสี่ยง (Risk %) - 100% คือยอมเสียทั้งหมด", min_value=0.01, max_value=100.0, value=100.0, step=1.0, format="%.2f")
    stop_loss = st.number_input("📉 ระยะทนลาก / จุดตัดขาดทุน (Points)", min_value=1.0, value=1000.0, step=100.0, format="%.1f", help="เช่น 1000 จุด (หรือ 100 Pips)")

with col2:
    point_value = st.number_input("💲 มูลค่าต่อ 1 จุด (Point Value)", min_value=0.01, value=1.0, step=0.1, format="%.2f", help="ค่าปริยาย 1.0 คือ 1 Standard Lot (เช่น XAUUSD) ขยับ 1 จุด = $1")
    split_count = st.number_input("🔪 จำนวนไม้ที่ต้องการแบ่งซอย", min_value=1, value=1, step=1)

st.divider()

# 2. ผลลัพธ์การคำนวณ (Output Section)
st.header("2. ผลลัพธ์การคำนวณ (Output Section)")

if balance <= 0 or risk_percent <= 0 or stop_loss <= 0 or point_value <= 0 or split_count <= 0:
    st.error("⚠️ กรุณาป้อนข้อมูลให้ถูกต้อง (ค่าต้องมากกว่า 0)")
else:
    # เรียกใช้ฟังก์ชันจากไฟล์ main.py
    result = calculate_lots(balance, risk_percent, stop_loss, point_value, split_count)
    
    risk_amount = result["risk_amount"]
    max_lot_size = result["max_lot_size"]
    split_lot_size = result["split_lot_size"]

    st.success(f"**💰 จำนวนเงินที่ยอมเสียสูงสุด (Risk Amount):** ${risk_amount:,.2f}")
    
    if max_lot_size < 0.01:
        st.error(f"**📦 ขนาด Lot รวมที่ออกได้:** {max_lot_size:,.4f} Lots \n\n 👉 *(น้อยกว่า 0.01 Lot ตามมาตรฐาน MT4/MT5 โปรดพิจารณาเพิ่มทุน หรือลดระยะทนลากลง)*")
    else:
        st.info(f"**📦 ขนาด Lot รวมสูงสุดที่อนุญาตให้ออกได้:** {max_lot_size:,.4f} Lots")
    
    st.subheader("📊 ตารางสรุปการซอยไม้")
    
    # แจ้งเตือนเรื่อง Lot ขนาดเล็กกว่า 0.01
    if split_lot_size < 0.01 and max_lot_size >= 0.01: 
        st.warning(f"⚠️ ไม้ที่ถูกซอยออกมา แต่ละไม้มีขนาด ({split_lot_size:.4f}) ซึ่งน้อยกว่า 0.01 Lot แนะนำให้ลดจำนวนไม้ซอยลง")

    # เก็บรูปแบบ Lot 2 ตำแหน่ง สำหรับแสดงในตาราง
    split_data = []
    total_split_lot = 0.0
    rounded_split_lot = round(split_lot_size, 2)
    display_lot = max(0.00, rounded_split_lot)

    for i in range(1, int(split_count) + 1):
        split_data.append({
            "ไม้ที่ (Position)": f"ไม้ที่ {i}", 
            "ขนาด Lot (Lot Size)": f"{display_lot:.2f}"
        })
        total_split_lot += display_lot

    df = pd.DataFrame(split_data)
    df.index = df.index + 1  
    st.table(df)

    # เช็คผลรวมเผื่อการปัดทศนิยม
    diff = round(total_split_lot - max_lot_size, 2)
    if diff > 0 and total_split_lot > 0:
        st.warning(f"📝 หมายเหตุ: ผลรวมของการซอยไม้หลังจากปัดเศษ ({total_split_lot:.2f} Lots) มากกว่า Lot รวมสูงสุด ({max_lot_size:.4f} Lots) เล็กน้อย โปรดระมัดระวังในการตั้งออเดอร์")
    elif max_lot_size >= 0.01:
        st.caption(f"📝 หมายเหตุ: ผลรวมของการซอยไม้ที่แสดงในตารางคือ {total_split_lot:.2f} Lots")
