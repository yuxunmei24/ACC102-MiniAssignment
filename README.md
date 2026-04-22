# ACC102-MiniAssignment:Moutai vs Wuliangye Financial Ratio Comparison
## 1. Problem & User 
This interactive tool compares the profitability, efficiency, and leverage of Kweichow Moutai (600519) and Wuliangye (000858) to help business students and investors quickly understand which liquor giant delivers stronger financial performance.

## 2. Data 
(1) Source: CSMAR database accessed via WRDS.
(2) Access date:2026,April 15
(3) Key fields: Company name, year, ROE, ROA, profit margin, asset turnover, leverage.

## 3. Methods 
(1) Connected to WRDS and extracted annual financial data for both firms (2022–2024).
(2) Calculated five key ratios using SQL and pandas.
(3) Exported cleaned data to CSV.
(4) Built an interactive Streamlit app with Plotly visualisations (line & bar charts).
(5) Added sidebar filters for metric selection and year range.

## 4. Key Findings 
- Moutai’s ROE improved from 31.9% (2022) to 36.9% (2024), far above Wuliangye’s 24%.
- Moutai’s net profit margin remained stable at 52%, while Wuliangye stayed at 37%.
- Asset turnover of Moutai rose from 48.8% to 57.2%, indicating better operational efficiency.
- Both companies have very low leverage (1.2–1.4), implying low financial risk.

## 5. How to run 
(1) Clone the respository:https://github.com/yuxunmei24/ACC102-MiniAssignment
(2) Download these files: app.py,requirements.txt,financial_ratios.csv on Desktop,then create a new file folder named acc102 on your desktop,and put these files into the folder.
(3) Open the terminal and input these codes below:
pip install streamlit
cd Desktop/acc102
streamlit run app.py
(4) Press enter,finally it will turn to the Streamlit page where we can show the app product.
## 6. Product link / Demo
Live app: http://localhost:8501
Demo video: 【ACC102 Track 4 Mini Assignment-哔哩哔哩】 https://b23.tv/udRjKec
## 7. Limitations & next steps
(1) Limitations: Only three years of data (2022–2024); qualitative factors (brand strategy, management) not included.
(2) Next steps: Extend time horizon to 5 years; add DuPont analysis and cash flow metrics.
