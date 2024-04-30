import pandas as pd
import numpy as np
import ta 
from ta.utils import dropna

# Excel dosyasını oku
df = pd.read_csv("veri.csv")
df = dropna(df)
# Tarih sırasına göre sırala
df = df.sort_values(by="Tarih")
# Fon koduna göre grupla
grouped_df = df.groupby("Fon Kodu")
filtered_group = {}


# Her bir fon için RSI hesaplamak için fonksiyonu çağırabilirsiniz
for fon_kodu, group in grouped_df:
    # Her bir fon için işlemleri gerçekleştir
    # Örneğin, burada RSI hesaplaması yapabilirsiniz
    group["Fiyat"] = group["Fiyat"].str.replace(",", ".").astype(float)
    prices = group["Fiyat"]
    if len(prices) < 14:
        continue
    
    # Fiyatları float tipine dönüştür
    # rsi = calculate_RSI(prices)
    rsi = ta.momentum.RSIIndicator(prices).rsi().to_list()
    # Son 3 RSI değerini al
    last_three_rsi = rsi[-3:]
    # Son 3 RSI değerinin herhangi biri 40'ın altındaysa
    if any(value <= 40 for value in last_three_rsi):
        # Filtrelenmiş grupları ve son RSI değerlerini sakla
        filtered_group[fon_kodu] = last_three_rsi[-1]  # Son RSI değerini al

# Sonuçları yazdır
for fon_kodu, son_rsi_degeri in filtered_group.items():
    print(f"Fon Kodu: {fon_kodu}, Son RSI Değeri: {son_rsi_degeri}")



