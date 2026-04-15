import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page set
st.set_page_config(page_title="Moutai vs Wuliangye Financial ratio comparison", layout="wide")
st.title("🍶 Moutai vs Wuliangye Financial ratio comparison")
st.markdown("### Based on core indicators such as ROE, ROA, and profit margin")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("financial_ratios.csv")
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

# Define the name of the indicator
metrics = {
    "roe": "ROE (Return on Equity %)",
    "roa": "ROA (Return on Assets %)",
    "profitmargin": "profitmargin %",
    "turnover": "turnover %",
    "leverage": "leverage (No%)"
}

# Sidebar: Select Indicators
selected_metric = st.sidebar.selectbox(
    "Select the financial indicators to compare",
    options=list(metrics.keys()),
    format_func=lambda x: metrics[x]
)

# Sidebar: Select Year Range
years = sorted(df["year"].unique())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years))
)

# Filter data based on selection
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Main interface: Display key KPIs (latest year)
latest_year = filtered_df["year"].max()
latest_data = filtered_df[filtered_df["year"] == latest_year]

col1, col2 = st.columns(2)
with col1:
    moutai_roe = latest_data[latest_data["Company"]=="Moutai"]["roe"].values[0] * 100
    st.metric("🥇 Moutai ROE", f"{moutai_roe:.1f}%")
with col2:
    wly_roe = latest_data[latest_data["Company"]=="Wuliangye"]["roe"].values[0] * 100
    st.metric("🥈 Wuliangye ROE", f"{wly_roe:.1f}%")

# Draw a line chart
st.subheader(f"📈 {metrics[selected_metric]} trend comparison")

plot_df = filtered_df.copy()
if selected_metric != "leverage":
    plot_df[selected_metric] = plot_df[selected_metric] * 100

fig_line = px.line(
    plot_df,
    x="year",
    y=selected_metric,
    color="Company",
    markers=True,
    title=f"{metrics[selected_metric]} change over time",
    labels={selected_metric: metrics[selected_metric], "year": "year"}
)
st.plotly_chart(fig_line, use_container_width=True)

# Draw a bar chart
st.subheader(f"📊 Each year {metrics[selected_metric]} comparision")
fig_bar = px.bar(
    plot_df,
    x="year",
    y=selected_metric,
    color="Company",
    barmode="group",
    title=f"{metrics[selected_metric]} annual comparison",
    labels={selected_metric: metrics[selected_metric], "year": "year"}
)
st.plotly_chart(fig_bar, use_container_width=True)

# Display the original data table
with st.expander("📋 view raw data"):
    st.dataframe(filtered_df)

# Analysis conclusion
st.subheader("💡 Core Findings")
st.markdown("""
- **Maotai's ROE continues to rise**（31.9% → 36.9%）， far higher than Wuliangye's （~24%）
- **Maotai's net profit margin remains stable at over 52%**，while Wuliangye's is around 37%, indicating a significant brand premium
- **Turnover**：Maotai has increased from 48.8% to 57.2%, resulting in improved operational efficiency
- **Leverage**：Both companies have very low levels (1.2-1.4 times), with low financial risk
""")

st.caption("Data Source：CSMAR (via WRDS) | Analysis period：2022-2024")
