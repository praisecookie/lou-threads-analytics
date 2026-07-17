import streamlit as st
import duckdb
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Lou Threads BI", layout="wide")
st.title("👗 Lou Threads: Strategy Intelligence")
st.markdown(
    "Analyzing True ROI, Customer Satisfaction, and Trend Hype to decide our Fall Strategy.")

# --- Sidebar & Authentication ---
st.sidebar.header("Database Connection")
md_token = st.sidebar.text_input("MotherDuck Access Token", type="password")

if not md_token:
    st.warning(
        "👈 Please enter your MotherDuck token in the sidebar to load the dashboard.")
    st.stop()

# --- Data Fetching (Cached for performance) ---


@st.cache_data(ttl=600)
def fetch_data(token):
    # Securely connect to the cloud database
    conn = duckdb.connect(f"md:lou_threads_db?motherduck_token={token}")
    df = conn.execute("SELECT * FROM fct_collection_performance").fetchdf()
    conn.close()
    return df


try:
    df = fetch_data(md_token)
except Exception as e:
    st.error(f"Connection failed. Please check your token. Error: {e}")
    st.stop()

# --- Interactive Filters ---
st.sidebar.markdown("---")
category_filter = st.sidebar.multiselect(
    "Filter by Strategy:",
    options=df['collection_category'].unique(),
    default=df['collection_category'].unique()
)

filtered_df = df[df['collection_category'].isin(category_filter)]

# --- Top Level KPIs ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Gross Revenue",
              f"${filtered_df['total_gross_revenue'].sum():,.2f}")
with col2:
    st.metric("Total Marketing Spend",
              f"${filtered_df['marketing_spend'].sum():,.2f}")
with col3:
    st.metric("Net Profit", f"${filtered_df['net_profit'].sum():,.2f}")
with col4:
    avg_rating = filtered_df['avg_customer_rating'].mean()
    st.metric("Avg Customer Rating", f"{avg_rating:.2f} ⭐")

st.markdown("---")

# --- Visualizations ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Financial ROI by Collection")
    fig_roi = px.bar(
        filtered_df,
        x="collection_name",
        y="marketing_roi_pct",
        color="collection_category",
        text="marketing_roi_pct",
        labels={
            "marketing_roi_pct": "ROI (%)", "collection_name": "Collection"}
    )
    fig_roi.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig_roi, use_container_width=True)

with chart_col2:
    st.subheader("Social Hype vs. Return Rate")
    # Bubble chart showing Risk vs Reward
    fig_risk = px.scatter(
        filtered_df,
        x="google_trends_score",
        y="return_rate_pct",
        color="collection_category",
        size="total_gross_revenue",  # Size of bubble = revenue
        hover_name="collection_name",
        labels={
            "google_trends_score": "Google Trends Score (Hype)",
            "return_rate_pct": "Return Rate (%)"
        }
    )
    st.plotly_chart(fig_risk, use_container_width=True)

# --- Raw Data Table ---
st.markdown("---")
st.subheader("Raw Analytics Data (Marts Layer)")
st.dataframe(filtered_df, use_container_width=True)
