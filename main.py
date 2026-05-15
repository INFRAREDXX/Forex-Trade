def calculate_lots(balance: float, risk_percent: float, stop_loss_points: float, point_value: float, split_count: int):
    """
    แกนหลักสำหรับคำนวณ Lot Size และ Risk
    """
    # 1. คำนวณจำนวนเงินที่เสี่ยง (Risk Amount)
    risk_amount = balance * (risk_percent / 100.0)
    
    # 2. คำนวณขนาด Lot Size รวมสูงสุด
    # Lot Size = Risk Amount / (Stop Loss จุด * Point Value)
    if stop_loss_points <= 0 or point_value <= 0:
        max_lot_size = 0.0
    else:
        max_lot_size = risk_amount / (stop_loss_points * point_value)
        
    # 3. คำนวณขนาด Lot ของแต่ละไม้ที่ซอย
    split_lot_size = max_lot_size / split_count if split_count > 0 else 0.0
    
    return {
        "risk_amount": risk_amount,
        "max_lot_size": max_lot_size,
        "split_lot_size": split_lot_size
    }
