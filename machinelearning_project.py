import yfinance as yf
import pandas as pd
import datetime as dt
import requests
import numpy as np
import mysql.connector


###############
#   S&P 500   #
###############


# 設定連接資訊
db = mysql.connector.connect(
    host="192.168.50.211",  # 電腦 A 的 IP 位址
    user="user_2",          # 您在電腦 A 上授權的使用者名稱
    password="12345678",  # 該使用者的密碼
    database="machinelearning"  # 目標資料庫名稱
)

# 建立游標
cursor = db.cursor()

# 測試查詢
query = "SELECT * FROM sp500_daily"
cursor.execute(query)

# 取得查詢結果
results = cursor.fetchall()

# 獲取欄位名稱
column_names = [i[0] for i in cursor.description]

# 關閉游標和連接
cursor.close()
db.close()

# 將查詢結果轉換成 DataFrame
df = pd.DataFrame(results, columns=column_names)

#將日期轉成datetime格式
df['date'] = pd.to_datetime(df['date'])

#將日期化為索引
df.set_index('date', inplace=True)

df.index = df.index.tz_localize('America/New_York')


Test = df.loc['2000-01-01 00:00:00-05:00':'2024-01-01 00:00:00-05:00']
SP500 = Test[['close_price']]
SP500 = SP500.reset_index()
SP500 = SP500.rename(columns={'date': 'Date'})


#SP500

##############################
#  FRED API - INTEREST RATES #
##############################


# 設定API KEY
api_key = '655c7c4de3e1906ab64007617f6290fb'

# 設定美債10年債卷利率的FRED API資料
series_id = 'DGS10'
url = f'https://api.stlouisfed.org/fred/series/observations'
params = {
    'series_id': series_id,
    'api_key': api_key,
    'file_type': 'json',
    'observation_start': '2000-01-01',  # Start date (YYYY-MM-DD)
    'observation_end': '2024-01-01',    # End date (optional)
}

# Send the request to the FRED API
response = requests.get(url, params=params)
# 檢查請求是否成功
if response.status_code == 200:
    data = response.json()
    observations = data['observations']

    # 建立空的 DataFrame
    interest_rate = pd.DataFrame(columns=["Date", "Value"])

    # 逐筆新增資料
    for idx, obs in enumerate(observations):
        date = obs["date"]
        value = obs["value"]  # 原始值

        # 檢查 value 是否為有效數字
        if value not in ['.', '']:
            try:
                value = float(value)  # 將 value 轉為浮點數
                print(f"Date: {date}, Value: {value}")
                interest_rate.loc[idx] = [date, value]
            except ValueError as e:
                print(f"Error converting value: {value} on date: {date}. Error: {e}")
        else:
            print(f"Invalid value on date {date}: {value}")

    # 顯示 DataFrame 的前幾筆資料
    print(interest_rate.head())
else:
    print(f"Error: {response.status_code}, {response.text}")


#interest_rate

##############################################################
#  FRED API - DOMESTIC CORPORATE PROFITS (CORPORATE EARNINGS)#
##############################################################



# 設定系列 ID 和日期範圍
series_id = 'CPROFIT'
start_date = '2020-01-01'  # 起始日期 (YYYY-MM-DD)
end_date = '2024-01-01'    # 結束日期 (YYYY-MM-DD)

# 定義 API 請求的 URL 和參數
url = f"https://api.stlouisfed.org/fred/series/observations"
params = {
    'series_id': series_id,
    'api_key': api_key,
    'file_type': 'json',
    'observation_start': start_date,
    'observation_end': end_date,
}


# 檢查請求是否成功
if response.status_code == 200:
    data = response.json()
    observations = data['observations']

    # 建立空的 DataFrame
    corporate_profits = pd.DataFrame(columns=["Date", "Value"])

    # 逐筆新增資料到 DataFrame
    for obs in observations:
        date = obs["date"]
        value = obs["value"]

        # 檢查 value 是否有效
        if value not in ['.', '']:
            try:
                value = float(value)
                # 使用 pd.concat 來新增資料
                new_row = pd.DataFrame({"Date": [date], "Value": [value]})
                corporate_profits = pd.concat([corporate_profits, new_row], ignore_index=True)
            except ValueError as e:
                print(f"Error converting value: {value} on date: {date}. Error: {e}")

    # 將 'Date' 轉換為日期格式並設為索引
    corporate_profits['Date'] = pd.to_datetime(corporate_profits['Date'])
    corporate_profits.set_index('Date', inplace=True)

    # 使用 resample() 填充為每日資料
    corporate_profits_daily = corporate_profits.resample('D').ffill()

    # 將 'Date' 從索引移回欄位
    corporate_profits_daily = corporate_profits_daily.reset_index()

    # 顯示結果的前幾筆資料
    print("\nDomestic Corporate Profits Data (Daily):")
    print(corporate_profits_daily.head(10))

else:
    print(f"Error: {response.status_code}, {response.text}")

#corporate_profits_daily

##########################################
#  FRED API - REAL GROSS NATIONAL PRODUCT#
##########################################

# Replace with your FRED API key
series_id = "GNPCA"

# Define the endpoint and parameters for the API request
url = f"https://api.stlouisfed.org/fred/series/observations"
params = {
    'series_id': series_id,
    'api_key': api_key,
    'file_type': 'json',
    'observation_start': '2000-01-01',  # Start date (optional)
    'observation_end': '2024-01-01',    # End date (optional)
}

# Send the request to FRED API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    observations = data['observations']

    # 建立空的 DataFrame
    GNP = pd.DataFrame(columns=["Date", "Value"])

    # 逐筆新增資料到 DataFrame
    for idx, obs in enumerate(observations):
        date = obs["date"]
        value = float(obs["value"])  # 將 value 轉為浮點數
        print(f"Date: {date}, Value: {value}")
        GNP.loc[idx] = [date, value]

    # 將 'Date' 欄位轉換為日期格式並設為索引
    GNP['Date'] = pd.to_datetime(GNP['Date'])
    GNP.set_index('Date', inplace=True)

    # 使用 resample() 方法將年度資料填充為每日資料
    GNP_daily = GNP.resample('D').ffill()

    # 創建從 2000 年到 2024 年的完整日期範圍
    full_date_range = pd.date_range(start='2000-01-01', end='2024-12-31', freq='D')

    # 將完整日期範圍轉換為 DataFrame
    full_dates_df = pd.DataFrame(full_date_range, columns=['Date'])
    full_dates_df.set_index('Date', inplace=True)

    # 合併完整日期範圍與原始 GNP_daily 資料
    GNP_filled = full_dates_df.merge(GNP_daily, left_index=True, right_index=True, how='left')

    # 使用前向填充填補缺失值
    GNP_filled['Value'] = GNP_filled['Value'].ffill()

    # 將 'Date' 從索引移回欄位
    GNP_filled = GNP_filled.reset_index()
    # 顯示合併後的結果
    print("\nFilled GNP Daily Data:")
    print(GNP_filled.head(10))  # 顯示前 10 筆資料
else:
    print(f"Error: {response.status_code}, {response.text}")

#GNP_daily


####################
#  inflation rate  #
####################


# API Parameters
series_id = "CPIAUCSL"  # CPI for All Urban Consumers

# API URL and request parameters
url = "https://api.stlouisfed.org/fred/series/observations"
params = {
    'series_id': series_id,
    'api_key': api_key,
    'file_type': 'json',
    'observation_start': '2000-01-01',
    'observation_end': '2024-01-01',
}

# Make the API request
response = requests.get(url, params=params)

# Handle the response
if response.status_code == 200:
    data = response.json()
    observations = data['observations']

    # Create a DataFrame from the observations
    inflation_rate = pd.DataFrame(observations)

    # Convert 'date' to datetime format and 'value' to numeric
    inflation_rate['Date'] = pd.to_datetime(inflation_rate['date'])
    inflation_rate['Value'] = pd.to_numeric(inflation_rate['value'], errors='coerce')

    # Set 'Date' as the index
    inflation_rate.set_index('Date', inplace=True)

    # Calculate Year-over-Year % Change (12-month pct change)
    inflation_rate['inflation_rate'] = inflation_rate['Value'].pct_change(12) * 100

    # Resample to daily frequency and use linear interpolation to fill gaps
    inflation_rate_daily = inflation_rate.resample('D').interpolate(method='linear')

    # Reset index to make 'Date' a column (optional)
    inflation_rate_daily = inflation_rate_daily.reset_index()

    # Display the first few rows of the daily resampled data
    print("\nDaily Inflation Rate Data:")
    print(inflation_rate_daily[['Date', 'inflation_rate']].head(15))

else:
    print(f"Error: {response.status_code}, {response.text}")


#inflation_rate_daily

#############################
#  FRED API - Money Supply  #
#############################


# API Parameters
series_id = "M2SL"
start_date = "2000-01-01"
end_date = "2024-01-01"

# API URL and request parameters
url = "https://api.stlouisfed.org/fred/series/observations"
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "observation_start": start_date,
    "observation_end": end_date,
}

# Send the request to the API
response = requests.get(url, params=params)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()
    observations = data.get("observations", [])

    # Extract and clean the data into a list of dictionaries
    clean_data = [
        {"Date": obs["date"], "Value": float(obs["value"])}
        for obs in observations if obs["value"] != "."
    ]

    # Convert to DataFrame and set Date as index
    Money_Supply = pd.DataFrame(clean_data)
    Money_Supply["Date"] = pd.to_datetime(Money_Supply["Date"])
    Money_Supply.set_index("Date", inplace=True)

    # Resample to daily frequency and apply linear interpolation
    Money_Supply_Daily = Money_Supply.resample("D").interpolate(method="linear")

    # Reset the index to make the Date an independent column
    Money_Supply_Daily = Money_Supply_Daily.reset_index()

    # Print the first few rows of the daily resampled data
    print("\nDaily Money Supply Data:")
    print(Money_Supply_Daily.head(10))

else:
    print(f"Error: {response.status_code}, {response.text}")


##
#Money_Supply_Daily

##############
#   資料合併  #
##############

# 假設你的資料集是這樣的
# interest_rate, Money_Supply 和 inflation_rate 已經存在且是 DataFrame

# 確保日期列是 datetime 格式
corporate_profits_daily ['Date'] = pd.to_datetime(corporate_profits_daily['Date'])
interest_rate['Date'] = pd.to_datetime(interest_rate['Date'])
GNP_filled['Date'] = pd.to_datetime(GNP_filled['Date'])
#Money_Supply['Date'] = pd.to_datetime(Money_Supply['Date'])
#inflation_rate['Date'] = pd.to_datetime(inflation_rate['Date'])

# 合併資料集
merged_data_1 = corporate_profits_daily.merge(interest_rate, on='Date', how='inner', suffixes=('_corporate_profits', '_interest_rate'))
merged_data_2 = merged_data_1.merge(GNP_filled, on='Date', how='inner', suffixes=('', '_GNP'))
merged_data_3 = merged_data_2.merge(Money_Supply_Daily, on='Date', how='inner', suffixes=('', '_Money_Supply'))
merged_data_4 = merged_data_3.merge(inflation_rate_daily, on='Date', how='inner', suffixes=('', '_inflation_rate'))

#處理用來跑回歸的dataframe
merged_data_4 = merged_data_4.drop('realtime_start', axis=1)
merged_data_4 = merged_data_4.drop('realtime_end', axis=1)
merged_data_4 = merged_data_4.drop('date', axis=1)
merged_data_4 = merged_data_4.drop('value', axis=1)
merged_data_4 = merged_data_4.drop('Value_inflation_rate', axis=1)
merged_data_4 = merged_data_4.rename(columns={'Value': 'GNP'})

merged_data_4 = merged_data_4.dropna()


#合併大盤股價
SP500['Date'] = SP500['Date'].dt.tz_localize(None)
merged_data_5 = merged_data_4.merge(SP500, on='Date', how='inner', suffixes=('', 'SP500'))

#重新命名大盤名稱
merged_data_5.columns.values[6] = "SP500"

###############
#   多元回歸   #
###############

import statsmodels.api as sm

# 設定因變數（Y）和自變數（X）
Y = merged_data_5.iloc[:, -1]
X = merged_data_5.drop(merged_data_5.columns[[0]], axis=1)  # 刪除因變數和日期欄位
X = X.drop(X.columns[-1], axis=1)

# 添加常數項
X = sm.add_constant(X)

# 擬合多元回歸模型
model = sm.OLS(Y, X).fit()

# 查看回歸結果
print(model.summary())


#############
#    繪圖    #
#############

import matplotlib.pyplot as plt
import seaborn as sns

# 假設已擬合模型
# 獲取預測值和殘差
predicted_values = model.fittedvalues  # 預測值
residuals = model.resid                # 殘差

# 1. 繪製殘差圖
plt.figure(figsize=(10, 6))
plt.scatter(predicted_values, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel("預測值")
plt.ylabel("殘差")
plt.title("殘差圖")
plt.show()

# 2. 繪製 QQ 圖
plt.figure(figsize=(10, 6))
sm.qqplot(residuals, line='45', fit=True)
plt.title("殘差 QQ 圖")
plt.show()

# 3. 預測值 vs. 真實值
plt.figure(figsize=(10, 6))
plt.scatter(Y, predicted_values)
plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--')  # 對角線
plt.xlabel("真實值")
plt.ylabel("預測值")
plt.title("預測值 vs. 真實值")
plt.show()














