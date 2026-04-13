import wrds
import pandas as pd
def build_financial_ratio_report(username, company_dict, start_year):
    conn = wrds.Connection(wrds_username=username)
    stock_list = tuple(company_dict.keys())
    sql = f"""
    SELECT
        stkcd,
        accper,
        b002000000 / a003000000 AS roe,
        b002000000 / a001000000 AS roa,
        b002000000 / b001101000 AS profitmargin,
        b001101000 / a001000000 AS turnover,
        a001000000 / a003000000 AS leverage
    FROM csmar.wrds_csmar_financial_master
    WHERE stkcd IN {stock_list}
      AND typrep = 'A'
    """
    data = conn.raw_sql(sql, date_cols=["accper"])
    conn.close()
    df = data[data["accper"].dt.month == 12].copy()
    df["year"] = df["accper"].dt.year
    df = df[df["year"] >= start_year].copy()
    df = df.drop(columns=["accper"])
    df["Company"] = df["stkcd"].map(company_dict)

    roa_pivot = (
        df.pivot(index="Company", columns="year", values="roa")
        .mul(100)
        .round(1)
        .astype(str)
        + "%"
    )
    roa_pivot = roa_pivot.rename_axis(columns=None)
    roa_pivot = roa_pivot.rename_axis("ROA", axis="index")

   
    roe_pivot = (
        df.pivot(index="Company", columns="year", values="roe")
        .mul(100)
        .round(1)
        .astype(str)
        + "%"
    )
    roe_pivot = roe_pivot.rename_axis(columns=None)
    roe_pivot = roe_pivot.rename_axis("ROE", axis="index")

    
    pm_pivot = (
        df.pivot(index="Company", columns="year", values="profitmargin")
        .mul(100)
        .round(1)
        .astype(str)
        + "%"
    )
    pm_pivot = pm_pivot.rename_axis(columns=None)
    pm_pivot = pm_pivot.rename_axis("Profit Margin", axis="index")

    
    to_pivot = (
        df.pivot(index="Company", columns="year", values="turnover")
        .mul(100)
        .round(1)
        .astype(str)
        + "%"
    )
    to_pivot = to_pivot.rename_axis(columns=None)
    to_pivot = to_pivot.rename_axis("Turnover", axis="index")

   
    lev_pivot = (
        df.pivot(index="Company", columns="year", values="leverage")
        .round(2)
    )
    lev_pivot = lev_pivot.rename_axis(columns=None)
    lev_pivot = lev_pivot.rename_axis("Leverage", axis="index")

   
    return {
        "raw_data":     df,           
        "roa_pivot":    roa_pivot,   
        "roe_pivot":    roe_pivot,    
        "pm_pivot":     pm_pivot,      
        "to_pivot":     to_pivot,      
        "lev_pivot":    lev_pivot,     
        "roa_markdown": roa_pivot.to_markdown(),
        "roe_markdown": roe_pivot.to_markdown(), 
        "pm_markdown":  pm_pivot.to_markdown(),
        "to_markdown":  to_pivot.to_markdown(),
        "lev_markdown": lev_pivot.to_markdown(),
    }
    username = 'yuxunmei'
company_dict = {
    '600519': 'Moutai',   
    '000858': 'Wuliangye',   
}
start_year = 2022
result = build_financial_ratio_report(
    username=username,
    company_dict=company_dict,
    start_year=start_year
)
result["raw_data"]
result["raw_data"].to_csv("financial_ratios.csv", index=False)
print("The data has been saved as: financial_ratios.csv")
print(result["roe_markdown"])
print(result["roa_markdown"])
print(result["pm_markdown"])
print(result["to_markdown"])
print(result["lev_markdown"])
db.close()