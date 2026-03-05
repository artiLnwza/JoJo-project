import pandas as pd
import random
import sys
import matplotlib.pyplot as plt
 

file = 'XAU_USD Historical Data.csv' 

try:
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date']) #แปลงวันที่
    df = df.sort_values('Date').reset_index(drop=True) #เรียงวันที่ใหม่
    fix = ['Price', 'Open', 'High', 'Low'] #เช้คหมด4ตัว
    for err in fix:
        df[err] = df[err].astype(str).str.replace(',', '').astype(float) #ลบ ,  ที่ตัวเลข แบบ5,400 เป้น 5400

except FileNotFoundError:
    sys.exit()

moneyS = float(input("เงินเริ่ม : "))
trades = int(input("จำนวนออกไม้ : "))          
distance = 150.0    # RR 1:1       

moneyR = moneyS
win = 0
loss = 0
dataRows = len(df)
bob = [moneyS] #เก้บเงิน
note = [] 

for trade in range(trades):
    if moneyR <= 0:
        print("แตกกกหนึ่ง!!!")
        print(" ")
        break

    index = random.randint(0, dataRows - 100)# แอบมีปัญหา
    price = df['Price'].iloc[index] # เก็บik8kเข้าเทรด
    dayday = df['Date'].iloc[index].strftime('%d-%m-%Y') # เก็บวันที่เข้าเทรด
    direction = random.choice(['Buy', 'Sell'])  # เลือกสุ่ม Buy/Sell การจากใช้ choice
    spread = random.uniform(1.0, 3.0) # สุ่มค่าspread ตัวนี้ผมหาข้อมูลมาว่าตลอด5 ปีใช้ค่า 1-3 ดีที่สุด (ไม่นับการข่าว)
    
    #คิดการเข้า
    if direction == 'Buy':
        realOrder = price + spread # คิดค่า spread
        tp = realOrder + distance #หา tp
        sl = realOrder - distance #หา sl
    else:#ถ้าไม่ใช่ buy ก็หาของ sell
        realOrder = price - spread  
        tp = realOrder - distance
        sl = realOrder + distance
            
    #คิดแพ้ชนะ
    result = "Loss" 
    for i in range(index + 1, dataRows):
        high = df['High'].iloc[i]
        low = df['Low'].iloc[i]
        
        if direction == 'Buy':
            if low <= sl:   
                result = "Loss"
                break
            elif high >= tp: 
                result = "Win"
                break

        elif direction == 'Sell':
            if high >= sl:   
                result = "Loss"
                break
            elif low <= tp:  
                result = "Win"
                break
                    
    if result == "Win":
    
        moneyR += distance # RR 1:1
        win += 1
        profit = distance
        
    else:
        moneyR -= distance
        loss += 1
        profit = -distance
        
    bob.append(moneyR)
    
    #บันทึกข้อมูล
    note.append({
        'Trade_No': trade + 1,
        'Date': dayday,
        'Direction': direction,
        'Market_Price': round(price, 2),
        'Spread': round(spread, 2),
        'Entry': round(realOrder, 2),
        'TP': round(tp, 2),
        'SL': round(sl, 2),
        'Result': result,
        'P/L': profit,
        'Balance': round(moneyR, 2)
    })


#จัดหน้าสวยๆ
noteDF = pd.DataFrame(note)
print(noteDF.head(trades).to_string(index=False)) 
noteDF.to_csv('trade_history.csv', index=False)

print("\nสรุปผล")
print(f"ทุนเริ่มต้น: {moneyS:.2f}")
print(f"เงินทุนเหลือ: {moneyR:.2f} ")
print(f"Win : {win} ไม้")
print(f"Loss : {loss} ไม้")

totalTrades = win + loss
winrate = 0.0
if totalTrades > 0:#กันอาจารย์ เทรด 0 รอบ
    winrate = (win / totalTrades) * 100
    print(f"Win Rate (อัตราชนะ): {winrate:.2f}%")

plt.plot(bob)
plt.grid(True, linestyle=':')
plt.show()