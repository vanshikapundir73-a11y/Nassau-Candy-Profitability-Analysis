
import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍬",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Nassau Candy Distributor.csv")

df = load_data()

# Dashboard title
st.title("🍬 Nassau Candy Profitability Dashboard")
st.write("Product Line Profitability and Margin Performance Analysis")

st.divider()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

divisions = st.sidebar.multiselect(
    "Select Division",
    options=sorted(df["Division"].dropna().unique()),
    default=sorted(df["Division"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

filtered_df = df[
    df["Division"].isin(divisions) &
    df["Region"].isin(regions)
]

# KPIs
total_sales = filtered_df["Sales"].sum()
total_cost = filtered_df["Cost"].sum()
total_profit = filtered_df["Gross Profit"].sum()
gross_margin = (
    total_profit / total_sales * 100
    if total_sales else 0
)
transactions = len(filtered_df)
products = filtered_df["Product Name"].nunique()

st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Cost", f"${total_cost:,.2f}")
col3.metric("Gross Profit", f"${total_profit:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Gross Margin", f"{gross_margin:.2f}%")
col5.metric("Transactions", f"{transactions:,}")
col6.metric("Unique Products", products)

st.divider()

# Product profitability
st.subheader("Product-wise Profitability")

product_profit = (
    filtered_df.groupby("Product Name", as_index=False)
    ["Gross Profit"].sum()
    .sort_values("Gross Profit", ascending=False)
)

fig1 = px.bar(
    product_profit,
    x="Product Name",
    y="Gross Profit",
    title="Gross Profit by Product",
    color="Gross Profit"
)
st.plotly_chart(fig1, use_container_width=True)

# Sales by division
st.subheader("Sales by Division")

division_sales = (
    filtered_df.groupby("Division", as_index=False)["Sales"].sum()
)

fig2 = px.pie(
    division_sales,
    names="Division",
    values="Sales",
    title="Sales Contribution by Division"
)
st.plotly_chart(fig2, use_container_width=True)

# Regional performance
st.subheader("Regional Sales Performance")

region_sales = (
    filtered_df.groupby("Region", as_index=False)["Sales"].sum()
)

fig3 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region",
    color="Sales"
)
st.plotly_chart(fig3, use_container_width=True)


# Margin analysis
st.subheader("Product Margin Analysis")

margin_data = (
    filtered_df.groupby("Product Name", as_index=False)
    .agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    })
)

margin_data["Gross Margin %"] = (
    margin_data["Gross Profit"] / margin_data["Sales"] * 100
)

margin_data = margin_data.sort_values(
    "Gross Margin %", ascending=False
)

fig4 = px.bar(
    margin_data,
    x="Product Name",
    y="Gross Margin %",
    title="Gross Margin by Product",
    color="Gross Margin %"
)

st.plotly_chart(fig4, use_container_width=True)

# Data table
st.subheader("Filtered Transaction Data")
st.dataframe(filtered_df, use_container_width=True)

st.success("Dashboard loaded successfully!")
