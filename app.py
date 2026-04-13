import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(page_title="茅台 vs 五粮液 财务比率对比", layout="wide")
st.title("🍶 贵州茅台 vs 五粮液 财务比率对比")
st.markdown("### 基于 ROE、ROA、利润率等核心指标")

# 加载数据（确保 CSV 文件在相同目录）
@st.cache_data
def load_data():
    df = pd.read_csv("financial_ratios.csv")
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

# 定义指标的中英文名称
metrics = {
    "roe": "ROE (净资产收益率 %)",
    "roa": "ROA (总资产收益率 %)",
    "profitmargin": "净利润率 %",
    "turnover": "总资产周转率 %",
    "leverage": "杠杆倍数 (无%)"
}

# 侧边栏：选择指标
selected_metric = st.sidebar.selectbox(
    "选择要对比的财务指标",
    options=list(metrics.keys()),
    format_func=lambda x: metrics[x]
)

# 侧边栏：选择年份范围
years = sorted(df["year"].unique())
year_range = st.sidebar.slider(
    "选择年份范围",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years))
)

# 根据选择过滤数据
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# 主界面：显示关键 KPI（最新一年）
latest_year = filtered_df["year"].max()
latest_data = filtered_df[filtered_df["year"] == latest_year]

col1, col2 = st.columns(2)
with col1:
    moutai_roe = latest_data[latest_data["Company"]=="Moutai"]["roe"].values[0] * 100
    st.metric("🥇 茅台 ROE", f"{moutai_roe:.1f}%")
with col2:
    wly_roe = latest_data[latest_data["Company"]=="Wuliangye"]["roe"].values[0] * 100
    st.metric("🥈 五粮液 ROE", f"{wly_roe:.1f}%")

# 绘制折线图
st.subheader(f"📈 {metrics[selected_metric]} 趋势对比")

plot_df = filtered_df.copy()
if selected_metric != "leverage":
    plot_df[selected_metric] = plot_df[selected_metric] * 100

fig_line = px.line(
    plot_df,
    x="year",
    y=selected_metric,
    color="Company",
    markers=True,
    title=f"{metrics[selected_metric]} 随时间变化",
    labels={selected_metric: metrics[selected_metric], "year": "年份"}
)
st.plotly_chart(fig_line, use_container_width=True)

# 柱状对比图
st.subheader(f"📊 各年份 {metrics[selected_metric]} 对比")
fig_bar = px.bar(
    plot_df,
    x="year",
    y=selected_metric,
    color="Company",
    barmode="group",
    title=f"{metrics[selected_metric]} 年度对比",
    labels={selected_metric: metrics[selected_metric], "year": "年份"}
)
st.plotly_chart(fig_bar, use_container_width=True)

# 显示原始数据表格
with st.expander("📋 查看原始数据"):
    st.dataframe(filtered_df)

# 分析结论
st.subheader("💡 核心发现")
st.markdown("""
- **茅台 ROE 持续上升**（31.9% → 36.9%），远高于五粮液（~24%）
- **茅台净利润率稳定在 52% 以上**，五粮液约 37%，品牌溢价显著
- **总资产周转率**：茅台从 48.8% 提升至 57.2%，营运效率改善
- **杠杆水平**：两家均很低（1.2-1.4倍），财务风险小
""")

st.caption("数据来源：CSMAR (via WRDS) | 分析期间：2022-2024")