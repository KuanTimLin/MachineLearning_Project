# 使用機器學習探討總經因子對S&P500的預測能力

此Project旨在建立完整Data ETL pipeline供前端模型探討總經因子對美股大盤(S&P500走向)的預測能力。

## 後端Data ETL pipeline
資料總共分成兩大部分:S&P500股價資料、總經因子資料。

![心智圖](image/心智圖.jpeg)
(Data ETL pipeline示意圖)


### S&P500股價資料

《Extract》

建立MySQL資料庫

<img src="image/建立mysql.png" alt="建立mysql" width="400"/>


從Yahoo Finance API串接S&P500股價資料

<img src="image/sp500_Load.png" alt="sp500_Load" width="400"/>

《Transform》

在python裡選定所需欄位、轉換日期欄位格式

<img src="image/sp500_transform.png" alt="sp500_transform" width="400"/>

《Load》

將資料用python加載到先前建立的MySQL資料庫

<img src="image/python腳本.png" alt="python腳本" width="400"/>

撰寫bash腳本執行python腳本，每日自動獲取最新S&P500股價

<img src="image/bash腳本.png" alt="bash腳本" width="400"/>

撰寫bat腳本使用每日定期執行bash腳本

<img src="image/windows_bat.png" alt="windows_bat" width="400"/>

### 總經因子資料

《Extract》

從FRED API獲取總經因子資料。

<img src="image/總經因子資料.png" alt="總經因子資料" width="400"/>

《Transform》

在python裡將資料欄位和日期欄位做轉換、清洗、合併。

<img src="image/總經因子清洗.png" alt="總經因子清洗" width="400"/>

《Load》

直接匯集成一張dataframe灌進模型裡。

<img src="image/合併資料.png" alt="合併資料" width="400"/>

## 前端機器學習模型

![模型簡易心智圖](image/模型簡易心智圖.JPEG)
(模型程式碼結構簡易示意圖)


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

<img src="image/S&P_500資料.png" alt="S&P_500資料" width="400"/>

使用statsmodels套件進行機器學習統計分析

<img src="image/多元回歸.png" alt="多元回歸" width="400"/>

結果

<img src="image/多元回歸結果.png" alt="多元回歸結果" width="600"/>

圖

<img src="image/圖.png" alt="圖" width="600"/>


解釋：























