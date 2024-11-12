# 使用機器學習探討總經因子對S&P500的預測能力

此Project旨在建立完整Data ETL pipeline供前端模型探討總經因子對美股大盤(S&P500走向)的預測能力。

## 後端Data ETL pipeline
資料總共分成兩大部分:S&P500股價資料、總經因子資料。

![心智圖](image/心智圖.jpeg)
(Data ETL pipeline示意圖)


### S&P500股價資料

《Extract》

建立MySQL資料庫

![建立mysql](image/建立mysql.png)

從Yahoo Finance API串接S&P500股價資料

![sp500_Load](image/sp500_Load.png)

《Transform》

在python裡選定所需欄位、轉換日期欄位格式

![sp500_transform](image/sp500_transform.png)

《Load》

將資料用python加載到先前建立的MySQL資料庫

![python腳本](image/python腳本.png)

撰寫bash腳本執行python腳本，每日自動獲取最新S&P500股價

![bash腳本](image/bash腳本.png)

撰寫bat腳本使用每日定期執行bash腳本

![windows_bat](image/windows_bat.png)

### 總經因子資料

《Extract》

從FRED API獲取總經因子資料。

![總經因子資料](image/總經因子資料.png)

《Transform》

在python裡將資料欄位和日期欄位做轉換、清洗、合併。

![總經因子清洗](image/總經因子清洗.png)

《Load》

直接匯集成一張dataframe灌進模型裡。

![合併資料](image/合併資料.png)

## 前端機器學習模型

這裡機器學習算法使用"多元迴歸"。

Y = β0 + β1X1 + β2X2 + β3X3 + β4X4 + β5X5

目標變數:
S&P收盤價

自變數:

1.CORPORATE EARNINGS:

2.REAL GROSS NATIONAL PRODUCT

3.inflation rate:

4.Money Supply:

5.利率：


### 程式碼

S&P500股價資料從遠端Windows主機的MySQL截取

![S&P_500資料](image/S&P_500資料.png)

使用statsmodels套件進行機器學習統計分析

![多元回歸](image/多元回歸.png)

結果

![多元回歸結果](image/多元回歸結果.png)

圖

![圖](image/圖.png)


解釋：























