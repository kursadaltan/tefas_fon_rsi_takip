import pandas as pd
import numpy as np
import ta 
from ta.utils import dropna
import requests
import json
from io import StringIO
import datetime

# Bugünün tarihini al
bugun = datetime.date.today()
# Başlangıç tarihini bugünden 30 gün önce olarak ayarla
baslangic_tarihi = bugun - datetime.timedelta(days=80)
# Bitiş tarihini bugün olarak ayarla
bitis_tarihi = bugun
# Başlangıç ve bitiş tarihlerini istenen formatta (gün.ay.yıl) stringe dönüştür
baslangic_str = baslangic_tarihi.strftime("%d.%m.%Y")
bitis_str = bitis_tarihi.strftime("%d.%m.%Y")


# Curl komutundaki header bilgilerini bir sözlük olarak tanımla
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'tr',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.tefas.gov.tr',
    'Referer': 'https://www.tefas.gov.tr/TarihselVeriler.aspx',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

# Curl komutundaki data-raw bilgisini bir sözlük olarak tanımla
data = {
  'fontip': 'YAT',
  'sfontur': '104',
  'fonkod': '',
  'fongrup': '',
  'bastarih': baslangic_str,
  'bittarih': bitis_str,
  'fonturkod': '',
  'fonunvantip': ''
}

# Curl komutundaki URL'yi tanımla
url = 'https://www.tefas.gov.tr/api/DB/BindHistoryInfo'

# HTTP GET isteği gönder
response = requests.post(url, headers=headers, data=data)

data = response.json()['data']
text = json.dumps(data)
text_io = StringIO(text)
# JSON verilerini DataFrame'e dönüştür
df = pd.read_json(text_io)
# Tarih sırasına göre sırala
df = df.sort_values(by="TARIH")

# Fon koduna göre grupla
grouped_df = df.groupby("FONKODU")

filtered_group = {}

#Eğer fonun adında Özel Fon varsa, bu fonları sil
df = df[~df["FONUNVAN"].str.contains("ÖZEL FON")]

# Her bir fon için RSI hesaplamak için fonksiyonu çağırabilirsiniz
for fon_kodu, group in grouped_df:
    prices = group["FIYAT"]
    
    if len(prices) < 14:
        continue
    
    rsi = ta.momentum.RSIIndicator(prices).rsi()
    last_two_rsi = rsi[-1:]
    
    if any(value <= 40 for value in last_two_rsi) and any(value > 0 for value in last_two_rsi):
        filtered_group[fon_kodu] = last_two_rsi.iloc[-1]

# Sonuçları yazdır
for fon_kodu, son_rsi_degeri in filtered_group.items():
    print(f"Fon Kodu: {fon_kodu}, Son RSI Değeri: {son_rsi_degeri}")