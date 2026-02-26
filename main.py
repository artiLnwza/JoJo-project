import pandas as pd
import random
import sys
import matplotlib.pyplot as plt 

file_name = 'XAU_USD Historical Data.csv' 

try:
    df = pd.read_csv(file_name)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    cols_to_fix = ['Price', 'Open', 'High', 'Low']
    for col in cols_to_fix:
        df[col] = df[col].astype(str).str.replace(',', '').astype(float)
    
except FileNotFoundError:
    
    sys.exit()


initial_capital = float(input("เงินเริ่ม : "))
num_trades = int(input("จำนวนออกไม้ : "))          
distance = 20.0            



current_capital = initial_capital
win_count = 0
loss_count = 0
total_rows = len(df)
equity_curve = [initial_capital] 


trade_log = []


for trade in range(num_trades):
    if current_capital <= 0:
        print(f" พอร์ตแตก {trade + 1}")
        break

    entry_index = random.randint(0, total_rows - 100)
    entry_price = df['Price'].iloc[entry_index]
    entry_date = df['Date'].iloc[entry_index].strftime('%Y-%m-%d') # เก็บวันที่เข้าเทรด
    direction = random.choice(['Buy', 'Sell'])
    spread = random.uniform(1.0, 3.0)
    
    if direction == 'Buy':
        actual_entry = entry_price + spread 
        tp_price = actual_entry + distance
        sl_price = actual_entry - distance
    else:
        actual_entry = entry_price - spread  
        tp_price = actual_entry - distance
        sl_price = actual_entry + distance
        
    trade_result = "Loss" 
    for i in range(entry_index + 1, total_rows):
        high_price = df['High'].iloc[i]
        low_price = df['Low'].iloc[i]
        
        if direction == 'Buy':
            if low_price <= sl_price:   
                trade_result = "Loss"
                break
            elif high_price >= tp_price: 
                trade_result = "Win"
                break
        elif direction == 'Sell':
            if high_price >= sl_price:   
                trade_result = "Loss"
                break
            elif low_price <= tp_price:  
                trade_result = "Win"
                break
                
    if trade_result == "Win":
        current_capital += distance
        win_count += 1
        profit_loss = distance
    else:
        current_capital -= distance
        loss_count += 1
        profit_loss = -distance
        
    equity_curve.append(current_capital)
    
    # บันทึกข้อมูล
    trade_log.append({
        'Trade_No': trade + 1,
        'Date': entry_date,
        'Direction': direction,
        'Market_Price': round(entry_price, 2),
        'Spread': round(spread, 2),
        'Actual_Entry': round(actual_entry, 2),
        'TP': round(tp_price, 2),
        'SL': round(sl_price, 2),
        'Result': trade_result,
        'P/L': profit_loss,
        'Balance': round(current_capital, 2)
    })


log_df = pd.DataFrame(trade_log)
print(log_df.head(num_trades).to_string(index=False)) 
log_df.to_csv('trade_history.csv', index=False)

print("สรุปผล")
print(f"ทุนเริ่มต้น: {initial_capital:.2f} ")
print(f"เงินทุนคงเหลือ: {current_capital:.2f} ")
print(f"Win : {win_count} ไม้")
print(f"Loss : {loss_count} ไม้")

total_executed_trades = win_count + loss_count
if total_executed_trades > 0:
    win_rate = (win_count / total_executed_trades) * 100
    print(f"Win Rate (อัตราชนะ): {win_rate:.2f}%")


plt.figure(figsize=(10, 6))
plt.plot(equity_curve, color='red' if current_capital < initial_capital else 'green', linewidth=2)
plt.title(f'Win Rate: {win_rate:.2f}%', fontsize=14)
plt.grid(True, linestyle=':', alpha=0.7)
plt.show()