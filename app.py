
import streamlit as st
import pandas as pd
import plotly.express as px

# Must be the first Streamlit command
st.set_page_config(page_title="Moutai vs Wuliangye Financial Ratio Comparison", layout="wide")

# Load data with caching
@st.cache_data
def load_data():
    from pathlib import Path
    current_dir = Path(__file__).parent
    csv_path = current_dir / "financial_ratios.csv"
    df = pd.read_csv(csv_path)
    df["year"] = df["year"].astype(int)
    return df
df = load_data()

st.title("🍶 Moutai vs Wuliangye Financial Ratio Comparison")
st.markdown("### Based on core indicators such as ROE, ROA, and profit margin")

# Define metric names and display units
metrics = {
    "roe": "ROE (Return on Equity, %)",
    "roa": "ROA (Return on Assets, %)",
    "profitmargin": "Profit Margin (%)",
    "turnover": "Asset Turnover (%)",
    "leverage": "Leverage (Total Assets / Equity)"
}

# Sidebar: select metric
selected_metric = st.sidebar.selectbox(
    "Select financial indicator to compare",
    options=list(metrics.keys()),
    format_func=lambda x: metrics[x]
)

# Sidebar: year range slider
years = sorted(df["year"].unique())
year_range = st.sidebar.slider(
    "Select year range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years))
)

# Filter data by year range
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Check if filtered data is not empty
if filtered_df.empty:
    st.warning("No data available for the selected year range. Please adjust the range.")
    st.stop()

# Display key ROE metrics for the latest year in the filtered range
latest_year = filtered_df["year"].max()
latest_data = filtered_df[filtered_df["year"] == latest_year]

col1, col2 = st.columns(2)
with col1:
    moutai_roe = latest_data[latest_data["Company"] == "Moutai"]["roe"].values[0] * 100
    st.metric("🥇 Moutai ROE", f"{moutai_roe:.1f}%")
with col2:
    wly_roe = latest_data[latest_data["Company"] == "Wuliangye"]["roe"].values[0] * 100
    st.metric("🥈 Wuliangye ROE", f"{wly_roe:.1f}%")

# Prepare data for plotting (convert decimals to percentages for non-leverage metrics)
plot_df = filtered_df.copy()
if selected_metric != "leverage":
    plot_df[selected_metric] = plot_df[selected_metric] * 100

# Line chart
st.subheader(f"📈 {metrics[selected_metric]} Trend Comparison")
fig_line = px.line(
    plot_df,
    x="year",
    y=selected_metric,
    color="Company",
    markers=True,
    title=f"{metrics[selected_metric]} over time",
    labels={selected_metric: metrics[selected_metric], "year": "Year"}
)
st.plotly_chart(fig_line, use_container_width=True)

# Bar chart
st.subheader(f"📊 Year-by-Year Comparison of {metrics[selected_metric]}")
fig_bar = px.bar(
    plot_df,
    x="year",
    y=selected_metric,
    color="Company",
    barmode="group",
    title=f"{metrics[selected_metric]} by year",
    labels={selected_metric: metrics[selected_metric], "year": "Year"}
)
st.plotly_chart(fig_bar, use_container_width=True)

# Raw data table
with st.expander("📋 View raw data"):
    st.dataframe(filtered_df)

# Core findings
st.subheader("💡 Core Findings")
st.markdown("""
- **Moutai's ROE continues to rise** (31.9% → 36.9%), far higher than Wuliangye's (~24%).
- **Moutai's net profit margin remains stable at over 52%**, while Wuliangye's is around 37%, indicating a significant brand premium.
- **Asset turnover**: Moutai increased from 48.8% to 57.2%, showing improved operational efficiency.
- **Leverage**: Both companies have very low leverage (1.2-1.4x), indicating low financial risk.
""")

st.caption("Data Source: CSMAR (via WRDS) | Analysis period: 2022-2024")