"""
Nassau Candy Distributor — Product Line Profitability & Margin Performance Dashboard
Built with Streamlit + Plotly | Senior Data Scientist Grade
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy — Profitability Intelligence",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# GLOBAL THEME & CSS
# ──────────────────────────────────────────────
PALETTE = {
    "bg_dark":    "#0B1210",
    "bg_card":    "#141F1A",
    "bg_sidebar": "#0F1A15",
    "accent1":    "#FACC15",   # Golden Yellow
    "accent2":    "#22C55E",   # Emerald Green
    "accent3":    "#A3E635",   # Lime Green
    "accent4":    "#4ADE80",   # Fresh Green
    "accent5":    "#EF4444",   # Alert Red
    "text_main":  "#ECFDF3",
    "text_muted": "#93A69C",
    "border":     "#25352C",
}

DIVISION_COLORS = {
    "Chocolate": "#FACC15",   # yellow
    "Sugar":     "#4ADE80",   # green
    "Other":     "#EF4444",   # red
}

REGION_COLORS = {
    "Atlantic": "#4ADE80",   # green
    "Interior": "#FACC15",   # yellow
    "Pacific":  "#A3E635",   # lime
    "Gulf":     "#EF4444",   # red
}

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {{
      font-family: 'Plus Jakarta Sans', 'Inter', 'Segoe UI', sans-serif;
      background-color: {PALETTE['bg_dark']};
      color: {PALETTE['text_main']};
  }}
  .stApp {{
      background:
        radial-gradient(circle at 8% 0%, rgba(250,204,21,0.08) 0%, transparent 32%),
        radial-gradient(circle at 95% 15%, rgba(74,222,128,0.10) 0%, transparent 38%),
        radial-gradient(circle at 50% 100%, rgba(34,197,94,0.06) 0%, transparent 45%),
        {PALETTE['bg_dark']};
      background-attachment: fixed;
  }}
  h1, h2, h3, h4 {{ font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -0.01em; }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, {PALETTE['bg_sidebar']} 0%, #0A0E14 100%);
      border-right: 1px solid {PALETTE['border']};
  }}
  [data-testid="stSidebar"] .stMarkdown h1,
  [data-testid="stSidebar"] .stMarkdown h2,
  [data-testid="stSidebar"] .stMarkdown h3 {{
      color: {PALETTE['accent4']};
      font-weight: 700;
      letter-spacing: 0.02em;
  }}

  /* ── Metric Cards ── */
  .kpi-card {{
      position: relative;
      background: linear-gradient(135deg, rgba(20,31,26,0.92) 0%, rgba(15,26,21,0.92) 100%);
      backdrop-filter: blur(10px);
      border: 1px solid {PALETTE['border']};
      border-radius: 18px;
      padding: 24px 20px;
      text-align: center;
      box-shadow: 0 4px 24px rgba(0,0,0,0.35);
      transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
      height: 120px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      overflow: hidden;
  }}
  .kpi-card::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, {PALETTE['accent1']}, {PALETTE['accent4']});
      opacity: 0.85;
  }}
  .kpi-card:hover {{
      transform: translateY(-4px) scale(1.01);
      border-color: {PALETTE['accent4']}55;
      box-shadow: 0 10px 32px rgba(74,222,128,0.15);
  }}
  .kpi-label {{
      font-size: 0.76rem;
      font-weight: 600;
      letter-spacing: 0.09em;
      text-transform: uppercase;
      color: {PALETTE['text_muted']};
      margin-bottom: 8px;
  }}
  .kpi-value {{
      font-size: 1.65rem;
      font-weight: 800;
      line-height: 1;
      background: linear-gradient(90deg, {PALETTE['accent1']}, {PALETTE['accent4']});
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
  }}
  .kpi-delta {{
      font-size: 0.82rem;
      color: {PALETTE['accent4']};
      margin-top: 6px;
  }}

  /* ── Section Headers ── */
  .section-header {{
      font-size: 1.35rem;
      font-weight: 700;
      color: {PALETTE['text_main']};
      background: linear-gradient(90deg, rgba(250,204,21,0.10), transparent 70%);
      border-left: 4px solid {PALETTE['accent1']};
      border-radius: 0 10px 10px 0;
      padding: 8px 12px;
      margin: 28px 0 16px 0;
  }}

  /* ── Chart Cards ── */
  .chart-card {{
      background: {PALETTE['bg_card']};
      border: 1px solid {PALETTE['border']};
      border-radius: 16px;
      padding: 10px;
      box-shadow: 0 2px 16px rgba(0,0,0,0.3);
      transition: border-color 0.25s ease;
  }}
  .chart-card:hover {{ border-color: {PALETTE['accent4']}44; }}

  /* ── Divider ── */
  hr {{ border-color: {PALETTE['border']}; }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{
      background: {PALETTE['bg_card']};
      border: 1px solid {PALETTE['border']};
      border-radius: 14px;
      padding: 5px;
      gap: 8px;
      display: flex;
      justify-content: space-between;
  }}
  .stTabs [data-baseweb="tab"] {{
      border-radius: 10px;
      color: {PALETTE['text_muted']};
      font-weight: 600;
      font-size: 0.88rem;
      flex: 1;
      text-align: center;
      justify-content: center;
      transition: all 0.2s ease;
  }}
  .stTabs [data-baseweb="tab"]:hover {{
      color: {PALETTE['accent4']};
      background: rgba(74,222,128,0.08);
  }}
  .stTabs [aria-selected="true"] {{
      background: linear-gradient(90deg, {PALETTE['accent1']}, {PALETTE['accent4']}) !important;
      color: #0B1210 !important;
      font-weight: 800 !important;
      box-shadow: 0 4px 16px rgba(74,222,128,0.25);
  }}

  /* ── Sliders & Inputs ── */
  .stSlider > div > div > div > div {{ background: {PALETTE['accent1']}; }}
  .stMultiSelect [data-baseweb="tag"] {{
      background: {PALETTE['accent2']} !important;
  }}

  [data-baseweb="select"] [data-baseweb="popover"] li {{
      white-space: normal !important;
      word-break: break-word !important;
      line-height: 1.4 !important;
      padding: 8px 12px !important;
      min-width: 300px !important;
      max-width: 340px !important;
  }}
  [data-baseweb="select"] [data-baseweb="popover"] ul {{
      min-width: 300px !important;
      max-width: 340px !important;
      width: 340px !important;
  }}
  [data-baseweb="select"] > div:first-child {{
      white-space: normal !important;
      word-wrap: break-word !important;
      height: auto !important;
      min-height: 38px !important;
      width: 100% !important;
  }}
  [data-baseweb="select"] input {{
      caret-color: transparent !important;
  }}



  /* ── Scrollbar ── */

  /* ── Scrollbar ── */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: {PALETTE['bg_dark']}; }}
  ::-webkit-scrollbar-thumb {{ background: {PALETTE['border']}; border-radius: 3px; }}

  /* ── Table ── */
  .dataframe {{ font-size: 0.82rem; }}
  .stDataFrame {{ border-radius: 12px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA LOADING & ENGINEERING
# ──────────────────────────────────────────────
@st.cache_data
def load_and_engineer(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Parse dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"],  dayfirst=True)

    # Drop invalid rows
    df = df[(df["Sales"] > 0) & (df["Cost"] > 0) & (df["Units"] > 0)].copy()

    # KPI Engineering
    df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"] * 100).round(2)
    df["Profit per Unit"] = (df["Gross Profit"] / df["Units"]).round(2)
    df["Revenue per Unit"] = (df["Sales"] / df["Units"]).round(2)
    df["Cost per Unit"] = (df["Cost"] / df["Units"]).round(2)
    df["Lead Time (days)"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # Calendar fields
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)
    df["Week"] = df["Order Date"].dt.isocalendar().week.astype(int)

    # Factory mapping
    factory_map = {
        "Wonka Bar - Nutty Crunch Surprise":  "Lot's O' Nuts",
        "Wonka Bar - Fudge Mallows":          "Lot's O' Nuts",
        "Wonka Bar -Scrumdiddlyumptious":     "Lot's O' Nuts",
        "Wonka Bar - Milk Chocolate":         "Wicked Choccy's",
        "Wonka Bar - Triple Dazzle Caramel":  "Wicked Choccy's",
        "Laffy Taffy":                        "Sugar Shack",
        "SweeTARTS":                          "Sugar Shack",
        "Nerds":                              "Sugar Shack",
        "Fun Dip":                            "Sugar Shack",
        "Fizzy Lifting Drinks":               "Sugar Shack",
        "Everlasting Gobstopper":             "Secret Factory",
        "Lickable Wallpaper":                 "Secret Factory",
        "Wonka Gum":                          "Secret Factory",
        "Hair Toffee":                        "The Other Factory",
        "Kazookles":                          "The Other Factory",
    }
    df["Factory"] = df["Product Name"].map(factory_map)
    return df


DATA_PATH = "Nassau_Candy_Distributor.csv"
df_raw = load_and_engineer(DATA_PATH)


# ──────────────────────────────────────────────
# CHART LAYOUT DEFAULTS
# ──────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Segoe UI, sans-serif",
              color=PALETTE["text_main"], size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)",
                bordercolor=PALETTE["border"], borderwidth=1),
    xaxis=dict(gridcolor=PALETTE["border"],
               linecolor=PALETTE["border"], zerolinecolor=PALETTE["border"]),
    yaxis=dict(gridcolor=PALETTE["border"],
               linecolor=PALETTE["border"], zerolinecolor=PALETTE["border"]),
)


def apply_theme(fig, title=""):
    fig.update_layout(**CHART_LAYOUT, title=dict(text=title,
                      font=dict(size=15, color=PALETTE["text_main"])))
    return fig


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.image("image2.png", use_container_width=True)
    st.markdown("""
        <div style="text-align:center; margin-top:8px;">
            <div style="
                font-size:1rem; font-weight:800; letter-spacing:0.05em;
                background: linear-gradient(90deg, #FACC15, #22C55E);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            ">🍬 Nassau Candy</div>
            <div style="
                font-size:0.72rem; font-weight:600; letter-spacing:0.06em;
                color: #84CC16; margin-top:2px;
            ">Top Wholesale Candy Distributor</div>
            <div style="
                font-size:0.7rem; font-weight:500; margin-top:6px;
                background: linear-gradient(90deg, #4ADE80, #84CC16);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            ">✦ Your Swag. Your Way. ✦</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📅 Date Range")
    min_d, max_d = df_raw["Order Date"].min(), df_raw["Order Date"].max()
    date_range = st.date_input(
        "Select period",
        value=(min_d.date(), max_d.date()),
        min_value=min_d.date(), max_value=max_d.date(),
    )

    st.markdown("### 🏭 Division")
    divs = st.multiselect(
        "Filter divisions",
        options=sorted(df_raw["Division"].unique()),
        default=sorted(df_raw["Division"].unique()),
    )

    st.markdown("### 🌍 Region")
    regions = st.multiselect(
        "Filter regions",
        options=sorted(df_raw["Region"].unique()),
        default=sorted(df_raw["Region"].unique()),
    )

    st.markdown("### 📦 Ship Mode")
    ship_modes = st.multiselect(
        "Filter ship modes",
        options=sorted(df_raw["Ship Mode"].unique()),
        default=sorted(df_raw["Ship Mode"].unique()),
    )

    st.markdown("### 🎚 Margin Threshold")
    margin_threshold = st.slider(
        "Min Gross Margin (%)",
        min_value=0, max_value=80, value=0, step=5,
    )

    st.markdown("### 🔍 Product Search")
    product_search = st.selectbox(
        "Search product name",
        options=[""] + sorted(df_raw["Product Name"].unique().tolist()),
        index=0,
        format_func=lambda x: "All Products" if x == "" else x,
    )

    st.markdown("---")
    st.markdown(
        f"<small style='color:{PALETTE['text_muted']}'>Last refreshed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}</small>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FILTER DATA
# ──────────────────────────────────────────────
d1 = pd.Timestamp(date_range[0]) if len(
    date_range) > 0 else df_raw["Order Date"].min()
d2 = pd.Timestamp(date_range[1]) if len(
    date_range) > 1 else df_raw["Order Date"].max()

df = df_raw[
    (df_raw["Order Date"] >= d1) &
    (df_raw["Order Date"] <= d2) &
    (df_raw["Division"].isin(divs)) &
    (df_raw["Region"].isin(regions)) &
    (df_raw["Ship Mode"].isin(ship_modes)) &
    (df_raw["Gross Margin (%)"] >= margin_threshold)
].copy()

if product_search:
    df = df[df["Product Name"] == product_search]


# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="
  background: linear-gradient(135deg, {PALETTE['bg_card']} 0%, #16261C 50%, #10231A 100%);
  border: 1px solid {PALETTE['border']};
  border-radius: 22px;
  padding: 20px 28px;
  margin-bottom: 28px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(74,222,128,0.06) inset;
  position: relative;
  overflow: hidden;
">
  <div style="position:absolute; top:-40%; right:-8%; width:280px; height:280px; border-radius:50%;
              background: radial-gradient(circle, rgba(250,204,21,0.14) 0%, transparent 70%); pointer-events:none;"></div>
  <div style="display:flex; align-items:center; gap:14px; position:relative;">
    <img src="data:image/jpeg;base64,{__import__('base64').b64encode(open('images1.png','rb').read()).decode()}" style="width:120px; height:80px; border-radius:14px; object-fit:cover; box-shadow:0 4px 14px rgba(0,0,0,0.4);">
    <div>
      <h1 style="margin:0; font-size:2.1rem; font-weight:800;
                 background:linear-gradient(90deg,{PALETTE['accent1']},{PALETTE['accent3']},{PALETTE['accent4']});
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor
      </h1>
    </div>
  </div>
  <div style="margin-top:10px; color:{PALETTE['text_muted']}; font-size:0.82rem; display:flex; flex-wrap:wrap; gap:6px 0; justify-content:space-between;">
    <span>📊 <b style="color:{PALETTE['text_main']}">{len(df):,}</b> records</span>
    <span>📅 <b style="color:{PALETTE['text_main']}">{d1.strftime('%b %d, %Y')}</b> → <b style="color:{PALETTE['text_main']}">{d2.strftime('%b %d, %Y')}</b></span>
    <span>🏭 <b style="color:{PALETTE['text_main']}">{len(divs)}</b> divisions</span>
    <span>🌍 <b style="color:{PALETTE['text_main']}">{len(regions)}</b> regions</span>
    <span>📦 <b style="color:{PALETTE['text_main']}">{df['Ship Mode'].nunique()}</b> ship modes</span>
    <span>🛍️ <b style="color:{PALETTE['text_main']}">{df['Product Name'].nunique()}</b> products</span>
    <span>🏪 <b style="color:{PALETTE['text_main']}">{df['Factory'].nunique()}</b> factories</span>
    <span>🗺️ <b style="color:{PALETTE['text_main']}">{df['State/Province'].nunique()}</b> states</span>
    <span>👥 <b style="color:{PALETTE['text_main']}">{df['Customer ID'].nunique():,}</b> customers</span>
    <span>💰 Avg margin <b style="color:{PALETTE['accent4']}">{(df['Gross Profit'].sum()/df['Sales'].sum()*100):.1f}%</b></span>  </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# AGGREGATE HELPERS
# ──────────────────────────────────────────────
@st.cache_data
def product_summary(data: pd.DataFrame) -> pd.DataFrame:
    grp = data.groupby("Product Name").agg(
        Division=("Division", "first"),
        Factory=("Factory", "first"),
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Order_Count=("Order ID", "nunique"),
    ).reset_index()
    grp["Gross Margin (%)"] = (grp["Total_Profit"] /
                               grp["Total_Sales"] * 100).round(2)
    grp["Profit per Unit"] = (grp["Total_Profit"] /
                              grp["Total_Units"]).round(2)
    grp["Revenue Contribution (%)"] = (
        grp["Total_Sales"] / grp["Total_Sales"].sum() * 100).round(2)
    grp["Profit Contribution (%)"] = (
        grp["Total_Profit"] / grp["Total_Profit"].sum() * 100).round(2)
    return grp.sort_values("Total_Profit", ascending=False)


@st.cache_data
def division_summary(data: pd.DataFrame) -> pd.DataFrame:
    grp = data.groupby("Division").agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Products=("Product Name", "nunique"),
        Orders=("Order ID", "nunique"),
    ).reset_index()
    grp["Gross Margin (%)"] = (grp["Total_Profit"] /
                               grp["Total_Sales"] * 100).round(2)
    grp["Profit per Unit"] = (grp["Total_Profit"] /
                              grp["Total_Units"]).round(2)
    return grp


prod_df = product_summary(df)
div_df = division_summary(df)

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
total_cost = df["Cost"].sum()
total_units = df["Units"].sum()
avg_margin = (total_profit / total_sales * 100) if total_sales else 0
total_orders = df["Order ID"].nunique()


# ──────────────────────────────────────────────
# KPI CARDS
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Executive KPIs</div>',
            unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)

kpis = [
    (k1, "💰 Total Revenue",    f"${total_sales:,.0f}",    ""),
    (k2, "📊 Gross Profit",     f"${total_profit:,.0f}",   ""),
    (k3, "🎯 Gross Margin",     f"{avg_margin:.1f}%",      ""),
    (k4, "📦 Total Units",      f"{total_units:,}",        ""),
    (k5, "🧾 Total Orders",     f"{total_orders:,}",       ""),
    (k6, "🏭 Cost Base",        f"${total_cost:,.0f}",     ""),
]

for col, label, value, delta in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          {'<div class="kpi-delta">' + delta + '</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Product Profitability",
    "🏭 Division Performance",
    "💡 Cost vs Margin Diagnostics",
    "📐 Profit Concentration",
    "📅 Trend Analysis",
])


# ══════════════════════════════════════════════
# TAB 1 — PRODUCT PROFITABILITY
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">🏆 Product Profitability Overview</div>',
                unsafe_allow_html=True)

    # Row 1 — Slider + Gross Margin Leaderboard (full width)
    top_n = st.slider("Top N products", 5, 15, 10, key="top_n_bar")
    top_prods = prod_df.nlargest(top_n, "Gross Margin (%)")
    colors_bar = [DIVISION_COLORS.get(d, PALETTE["accent3"])
                  for d in top_prods["Division"]]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=top_prods["Gross Margin (%)"],
        y=top_prods["Product Name"],
        orientation="h",
        marker=dict(color=colors_bar, line=dict(
            color="rgba(255,255,255,0.1)", width=0.5)),
        text=[f"{v:.1f}%" for v in top_prods["Gross Margin (%)"]],
        textposition="outside",
        textfont=dict(color=PALETTE["text_main"], size=11),
        hovertemplate="<b>%{y}</b><br>Gross Margin: %{x:.2f}%<extra></extra>",
    ))
    apply_theme(fig_bar, "🎖 Product-level Gross Margin Leaderboard (%)")
    fig_bar.update_layout(height=420, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Row 2 — Bubble Chart (full width)
    fig_bubble = px.scatter(
        prod_df,
        x="Total_Sales", y="Total_Profit",
        size="Total_Units",
        color="Division",
        color_discrete_map=DIVISION_COLORS,
        hover_name="Product Name",
        hover_data={
            "Gross Margin (%)": True, "Profit per Unit": True, "Total_Units": True},
        size_max=50,
    )
    apply_theme(fig_bubble, "💎 Sales vs Profit Matrix (bubble = units)")
    fig_bubble.update_layout(height=420)
    fig_bubble.update_traces(marker=dict(
        opacity=0.8, line=dict(width=1, color="white")))
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Row 3 — Stacked Bar (full width)
    st.markdown('<div class="section-header">💵 Revenue · Cost · Profit Breakdown per Product</div>',
                unsafe_allow_html=True)

    fig_stack = go.Figure()
    fig_stack.add_trace(go.Bar(
        name="Cost", x=prod_df["Product Name"], y=prod_df["Total_Cost"], marker_color=PALETTE["accent5"]))
    fig_stack.add_trace(go.Bar(
        name="Gross Profit", x=prod_df["Product Name"], y=prod_df["Total_Profit"], marker_color=PALETTE["accent4"]))
    apply_theme(fig_stack, "Profit contribution: Cost vs Gross Profit")
    fig_stack.update_layout(barmode="stack", height=370, xaxis_tickangle=-35)
    st.plotly_chart(fig_stack, use_container_width=True)

    # Profit per Unit Ranking
    c3, c4 = st.columns(2)
    with c3:
        # Row — Profit per Unit full width
        fig_ppu = px.bar(
            prod_df.sort_values("Profit per Unit", ascending=True),
            x="Profit per Unit", y="Product Name",
            color="Division", color_discrete_map=DIVISION_COLORS,
            orientation="h",
        )
    apply_theme(fig_ppu, "⚡ Profit per Unit by Product")
    fig_ppu.update_layout(height=360)
    st.plotly_chart(fig_ppu, use_container_width=True)

    with c4:
        fig_rev_contrib = px.treemap(prod_df,
                                     path=["Division", "Product Name"],
                                     values="Total_Sales",
                                     color="Revenue Contribution (%)",
                                     color_continuous_scale=[
                                         "#1C2433", "#22C55E", "#FACC15"],
                                     hover_data={
                                         "Revenue Contribution (%)": ":.2f", "Total_Sales": ":,.0f"},
                                     )
        apply_theme(fig_rev_contrib,
                    "🍰 Revenue Contribution Share by Division & Product")
        fig_rev_contrib.update_traces(
            texttemplate="<b>%{label}</b><br>%{customdata[0]:.1f}%",
            textfont=dict(size=13),
        )
    fig_rev_contrib.update_layout(height=480, coloraxis_showscale=True)
    st.plotly_chart(fig_rev_contrib, use_container_width=True)

    st.markdown('<div class="section-header">🔎 Product Quadrant Analysis</div>',
                unsafe_allow_html=True)

    avg_sales = prod_df["Total_Sales"].mean()
    avg_margin = prod_df["Gross Margin (%)"].mean()

    def quadrant(row):
        if row["Total_Sales"] >= avg_sales and row["Gross Margin (%)"] >= avg_margin:
            return "⭐ Star (High Sales, High Margin)"
        elif row["Total_Sales"] >= avg_sales and row["Gross Margin (%)"] < avg_margin:
            return "⚠️ Cash Trap (High Sales, Low Margin)"
        elif row["Total_Sales"] < avg_sales and row["Gross Margin (%)"] >= avg_margin:
            return "💎 Hidden Gem (Low Sales, High Margin)"
        else:
            return "🔴 Laggard (Low Sales, Low Margin)"

    prod_df["Quadrant"] = prod_df.apply(quadrant, axis=1)

    quadrant_colors = {
        "⭐ Star (High Sales, High Margin)":      "#4ADE80",
        "⚠️ Cash Trap (High Sales, Low Margin)":  "#FACC15",
        "💎 Hidden Gem (Low Sales, High Margin)":  "#84CC16",
        "🔴 Laggard (Low Sales, Low Margin)":      "#EF4444",
    }

    fig_quad = px.scatter(
        prod_df,
        x="Total_Sales", y="Gross Margin (%)",
        color="Quadrant",
        color_discrete_map=quadrant_colors,
        size="Total_Profit", size_max=55,
        hover_name="Product Name",
        hover_data={"Total_Units": True,
                    "Profit per Unit": True, "Division": True},
    )
    fig_quad.add_vline(x=avg_sales, line_dash="dash", line_color=PALETTE["border"],
                       annotation_text="Avg Sales", annotation_font_color=PALETTE["text_muted"])
    fig_quad.add_hline(y=avg_margin, line_dash="dash", line_color=PALETTE["border"],
                       annotation_text="Avg Margin", annotation_font_color=PALETTE["text_muted"])
    apply_theme(
        fig_quad, "🔎 Product Quadrant: Sales vs Margin (size = total profit)")
    fig_quad.update_traces(marker=dict(
        opacity=0.85, line=dict(width=1, color="white")))
    fig_quad.update_layout(height=520)
    st.plotly_chart(fig_quad, use_container_width=True)

    st.markdown('<div class="section-header">🏅 Product Rankings & Classification</div>',
                unsafe_allow_html=True)

    rank_df = prod_df.copy()
    rank_df["Rank by Gross Profit"] = rank_df["Total_Profit"].rank(
        ascending=False).astype(int)
    rank_df["Rank by Gross Margin"] = rank_df["Gross Margin (%)"].rank(
        ascending=False).astype(int)

    # def classify(row):
    #     avg_s = rank_df["Total_Sales"].mean()
    #     avg_m = rank_df["Gross Margin (%)"].mean()
    #     avg_p = rank_df["Total_Profit"].mean()
    #     if row["Total_Profit"] >= avg_p and row["Gross Margin (%)"] >= avg_m:
    #         return "🌟 High-Profit / High-Margin"
    #     elif row["Total_Sales"] >= avg_s and row["Gross Margin (%)"] < avg_m:
    #         return "⚠️ High-Sales / Low-Margin"
    #     elif row["Total_Sales"] < avg_s and row["Total_Profit"] < avg_p:
    #         return "🔴 Low-Sales / Low-Profit"
    #     else:
    #         return "🔵 Moderate"

    def classify(row):
        high_sales = row["Total_Sales"] >= rank_df["Total_Sales"].quantile(0.5)
        high_margin = row["Gross Margin (%)"] >= 60
        high_profit = row["Total_Profit"] >= rank_df["Total_Profit"].quantile(
            0.5)

        if high_profit and high_margin:
            return "🌟 High-Profit / High-Margin"
        elif high_sales and not high_margin:
            return "⚠️ High-Sales / Low-Margin"
        elif not high_sales and not high_profit:
            return "🔴 Low-Sales / Low-Profit"
        else:
            return "🔵 Moderate"

    rank_df["Classification"] = rank_df.apply(classify, axis=1)

    class_colors = {
        "🌟 High-Profit / High-Margin": "#4ADE80",
        "⚠️ High-Sales / Low-Margin":   "#FACC15",
        "🔴 Low-Sales / Low-Profit":     "#EF4444",
        "🔵 Moderate":                   "#84CC16",
    }

    # Row 1 — Rank by Gross Profit
    fig_rank_profit = px.bar(
        rank_df.sort_values("Rank by Gross Profit"),
        x="Total_Profit", y="Product Name",
        color="Classification",
        color_discrete_map=class_colors,
        orientation="h",
        text="Total_Profit",
        hover_data={"Rank by Gross Profit": True, "Gross Margin (%)": True},
    )
    fig_rank_profit.update_traces(
        texttemplate="$%{text:,.0f}", textposition="outside")
    apply_theme(fig_rank_profit, "🥇 Products Ranked by Gross Profit")
    fig_rank_profit.update_layout(height=480, showlegend=True)
    st.plotly_chart(fig_rank_profit, use_container_width=True)

    # Row 2 — Rank by Gross Margin
    fig_rank_margin = px.bar(
        rank_df.sort_values("Rank by Gross Margin"),
        x="Gross Margin (%)", y="Product Name",
        color="Classification",
        color_discrete_map=class_colors,
        orientation="h",
        text="Gross Margin (%)",
        hover_data={"Rank by Gross Margin": True, "Total_Profit": True},
    )
    fig_rank_margin.update_traces(
        texttemplate="%{text:.1f}%", textposition="outside")
    apply_theme(fig_rank_margin, "🥈 Products Ranked by Gross Margin (%)")
    fig_rank_margin.update_layout(height=480, showlegend=False)
    st.plotly_chart(fig_rank_margin, use_container_width=True)

    # Row 3 — Classification Summary Cards
    st.markdown('<div class="section-header">🔍 Product Classification Summary</div>',
                unsafe_allow_html=True)

    for cls, color in class_colors.items():
        products_in_class = rank_df[rank_df["Classification"]
                                    == cls]["Product Name"].tolist()
        if products_in_class:
            st.markdown(f"""
            <div style="
                background: {PALETTE['bg_card']};
                border-left: 4px solid {color};
                border-radius: 10px;
                padding: 14px 18px;
                margin-bottom: 10px;
            ">
                <div style="font-weight:700; font-size:0.95rem; color:{color};">{cls}</div>
                <div style="color:{PALETTE['text_muted']}; font-size:0.85rem; margin-top:6px;">
                    {" &nbsp;|&nbsp; ".join(products_in_class)}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Data Table
    st.markdown('<div class="section-header">📋 Product Profitability Table</div>',
                unsafe_allow_html=True)
    display_cols = ["Product Name", "Division", "Factory", "Total_Sales", "Total_Cost",
                    "Total_Profit", "Total_Units", "Gross Margin (%)", "Profit per Unit",
                    "Revenue Contribution (%)", "Profit Contribution (%)"]
    st.dataframe(
        prod_df[display_cols].rename(columns={
            "Total_Sales": "Revenue ($)", "Total_Cost": "Cost ($)",
            "Total_Profit": "Profit ($)", "Total_Units": "Units",
        }).style
        .format({"Revenue ($)": "${:,.2f}", "Cost ($)": "${:,.2f}", "Profit ($)": "${:,.2f}",
                 "Gross Margin (%)": "{:.1f}%", "Profit per Unit": "${:.2f}",
                 "Revenue Contribution (%)": "{:.1f}%", "Profit Contribution (%)": "{:.1f}%"})
        .background_gradient(subset=["Gross Margin (%)"], cmap="RdYlGn")
        .background_gradient(subset=["Profit ($)"], cmap="Blues"),
        use_container_width=True, height=380,
    )


# ══════════════════════════════════════════════
# TAB 2 — DIVISION PERFORMANCE
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">🏭 Division Performance Dashboard</div>',
                unsafe_allow_html=True)

    d1c, d2c, d3c = st.columns(3)
    for col, (_, row), icon in zip([d1c, d2c, d3c], div_df.iterrows(), ["🍫", "🍭", "✨"]):
        with col:
            st.markdown(f"""
        <div class="kpi-card" style="height:auto; padding:20px;">
          <div class="kpi-label">{icon} {row['Division']}</div>
          <div class="kpi-value">{row['Gross Margin (%)']:.1f}%</div>
          <div style="color:{PALETTE['text_muted']}; font-size:0.8rem; margin-top:8px;">
            Rev: ${row['Total_Sales']:,.0f} | Profit: ${row['Total_Profit']:,.0f}
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    r1c, r2c = st.columns(2)

    with r1c:
        # Grouped bar: Revenue vs Profit by Division
        fig_div = go.Figure()
        fig_div.add_trace(go.Bar(name="Revenue", x=div_df["Division"], y=div_df["Total_Sales"],
                                 marker_color=PALETTE["accent3"], opacity=0.85))
        fig_div.add_trace(go.Bar(name="Cost",    x=div_df["Division"], y=div_df["Total_Cost"],
                                 marker_color=PALETTE["accent5"], opacity=0.85))
        fig_div.add_trace(go.Bar(name="Profit",  x=div_df["Division"], y=div_df["Total_Profit"],
                                 marker_color=PALETTE["accent4"], opacity=0.85))
        apply_theme(fig_div, "💼 Revenue vs Cost vs Profit by Division")
        fig_div.update_layout(barmode="group", height=380)
        st.plotly_chart(fig_div, use_container_width=True)

    with r2c:
        # Margin donut per division
        fig_donut = px.pie(
            div_df, values="Total_Profit", names="Division",
            hole=0.6, color="Division", color_discrete_map=DIVISION_COLORS,
        )
        apply_theme(fig_donut, "🎯 Profit Contribution by Division")
        fig_donut.update_traces(textinfo="percent+label",
                                pull=[0.03]*len(div_df))
        fig_donut.update_layout(height=380, showlegend=True)
        st.plotly_chart(fig_donut, use_container_width=True)

    # Margin by Division — violin plot
    r3c, r4c = st.columns(2)

    with r3c:
        fig_violin = px.violin(
            df, x="Division", y="Gross Margin (%)",
            color="Division", color_discrete_map=DIVISION_COLORS,
            box=True, points="outliers",
        )
        apply_theme(fig_violin, "📊 Gross Margin Distribution by Division")
        fig_violin.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_violin, use_container_width=True)

    with r4c:
        # Region x Division heatmap
        heat_data = df.groupby(["Region", "Division"])[
            "Gross Margin (%)"].mean().reset_index()
        heat_pivot = heat_data.pivot(
            index="Region", columns="Division", values="Gross Margin (%)")
        fig_heat = px.imshow(
            heat_pivot, text_auto=".1f", aspect="auto",
            color_continuous_scale=["#1C2433",
                                    PALETTE["accent2"], PALETTE["accent1"]],
        )
        apply_theme(fig_heat, "🗺 Avg Gross Margin: Region × Division (%)")
        fig_heat.update_layout(height=380)
        st.plotly_chart(fig_heat, use_container_width=True)

    # Region breakdown
    st.markdown('<div class="section-header">🌍 Region-Level Profitability</div>',
                unsafe_allow_html=True)
    reg_df = df.groupby("Region").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
    ).reset_index()
    reg_df["Gross Margin (%)"] = (
        reg_df["Total_Profit"] / reg_df["Total_Sales"] * 100).round(2)

    r5c, r6c = st.columns(2)
    with r5c:
        fig_reg_bar = px.bar(
            reg_df.sort_values("Total_Profit", ascending=False),
            x="Region", y=["Total_Sales", "Total_Profit"],
            color_discrete_sequence=[PALETTE["accent3"], PALETTE["accent4"]],
            barmode="group",
        )
        apply_theme(fig_reg_bar, "💰 Revenue vs Profit by Region")
        fig_reg_bar.update_layout(height=320)
        st.plotly_chart(fig_reg_bar, use_container_width=True)

    with r6c:
        fig_reg_mg = px.bar(
            reg_df.sort_values("Gross Margin (%)", ascending=False),
            x="Region", y="Gross Margin (%)",
            color="Region", color_discrete_map=REGION_COLORS,
            text="Gross Margin (%)", text_auto=".1f",
        )
        apply_theme(fig_reg_mg, "🎯 Gross Margin % by Region")
        fig_reg_mg.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig_reg_mg, use_container_width=True)

    st.markdown('<div class="section-header">🏭 Division Deep-Dive: Efficiency & Margin Issues</div>',
                unsafe_allow_html=True)

    # Aggregate metrics by Division
    div_analysis = df.groupby("Division").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Products=("Product Name", "nunique"),
        Avg_Margin=("Gross Margin (%)", "mean"),
    ).reset_index()

    div_analysis["Gross Margin (%)"] = (
        div_analysis["Total_Profit"] / div_analysis["Total_Sales"] * 100).round(2)
    div_analysis["Profit per Unit"] = (
        div_analysis["Total_Profit"] / div_analysis["Total_Units"]).round(2)
    div_analysis["Cost Ratio (%)"] = (
        div_analysis["Total_Cost"] / div_analysis["Total_Sales"] * 100).round(2)
    div_analysis["Revenue per Order"] = (
        div_analysis["Total_Sales"] / div_analysis["Total_Orders"]).round(2)
    div_analysis["Profit per Order"] = (
        div_analysis["Total_Profit"] / div_analysis["Total_Orders"]).round(2)
    div_analysis["Revenue vs Profit Gap"] = (
        div_analysis["Total_Sales"] - div_analysis["Total_Profit"]).round(2)

    # Classify efficiency
    avg_div_margin = div_analysis["Gross Margin (%)"].mean()
    avg_div_cost = div_analysis["Cost Ratio (%)"].mean()

    def div_classify(row):
        if row["Gross Margin (%)"] >= avg_div_margin and row["Cost Ratio (%)"] <= avg_div_cost:
            return "✅ Strong Financial Efficiency"
        elif row["Gross Margin (%)"] < avg_div_margin and row["Cost Ratio (%)"] > avg_div_cost:
            return "🔴 Structural Margin Issues"
        elif row["Gross Margin (%)"] >= avg_div_margin and row["Cost Ratio (%)"] > avg_div_cost:
            return "🟡 High Margin but High Cost"
        else:
            return "🟠 Low Margin but Low Cost"

    div_analysis["Efficiency Flag"] = div_analysis.apply(div_classify, axis=1)

    flag_colors = {
        "✅ Strong Financial Efficiency": "#4ADE80",
        "🔴 Structural Margin Issues":    "#EF4444",
        "🟡 High Margin but High Cost":   "#FDE047",
        "🟠 Low Margin but Low Cost":     "#FACC15",
    }

    # Classification Cards
    for _, row in div_analysis.iterrows():
        color = flag_colors.get(row["Efficiency Flag"], "#8B949E")
        st.markdown(f"""
        <div style="
            background: {PALETTE['bg_card']};
            border-left: 5px solid {color};
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        ">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:1.1rem; font-weight:800; color:{color};">
                    {row['Division']} Division
                </div>
                <div style="
                    background:{color}22;
                    border:1px solid {color};
                    border-radius:20px;
                    padding:4px 14px;
                    font-size:0.78rem;
                    font-weight:700;
                    color:{color};
                ">{row['Efficiency Flag']}</div>
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:20px; margin-top:12px;">
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">💰 Revenue</div>
                    <div style="color:{PALETTE['text_main']}; font-weight:700;">${row['Total_Sales']:,.0f}</div>
                </div>
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">📊 Gross Profit</div>
                    <div style="color:{PALETTE['text_main']}; font-weight:700;">${row['Total_Profit']:,.0f}</div>
                </div>
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">🎯 Gross Margin</div>
                    <div style="color:{color}; font-weight:700;">{row['Gross Margin (%)']:.1f}%</div>
                </div>
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">🏷 Cost Ratio</div>
                    <div style="color:{PALETTE['text_main']}; font-weight:700;">{row['Cost Ratio (%)']:.1f}%</div>
                </div>
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">⚡ Profit/Unit</div>
                    <div style="color:{PALETTE['text_main']}; font-weight:700;">${row['Profit per Unit']:.2f}</div>
                </div>
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">📦 Units</div>
                    <div style="color:{PALETTE['text_main']}; font-weight:700;">{row['Total_Units']:,}</div>
                </div>
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">🧾 Orders</div>
                    <div style="color:{PALETTE['text_main']}; font-weight:700;">{row['Total_Orders']:,}</div>
                </div>
                <div>
                    <div style="color:{PALETTE['text_muted']}; font-size:0.72rem;">📉 Rev vs Profit Gap</div>
                    <div style="color:{PALETTE['accent5']}; font-weight:700;">${row['Revenue vs Profit Gap']:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Average Margin by Division bar
    fig_avg_mg = px.bar(
        div_analysis.sort_values("Gross Margin (%)", ascending=False),
        x="Division", y="Gross Margin (%)",
        color="Efficiency Flag",
        color_discrete_map=flag_colors,
        text="Gross Margin (%)", text_auto=".1f",
        hover_data={"Cost Ratio (%)": True, "Profit per Unit": True},
    )
    fig_avg_mg.add_hline(y=avg_div_margin, line_dash="dash",
                         line_color=PALETTE["accent3"],
                         annotation_text=f"Avg: {avg_div_margin:.1f}%",
                         annotation_font_color=PALETTE["accent3"])
    apply_theme(
        fig_avg_mg, "📊 Average Gross Margin by Division (with efficiency flag)")
    fig_avg_mg.update_layout(height=380, showlegend=True)
    st.plotly_chart(fig_avg_mg, use_container_width=True)

    # Revenue vs Profit Imbalance
    fig_imbalance = go.Figure()
    fig_imbalance.add_trace(go.Bar(
        name="Revenue",
        x=div_analysis["Division"], y=div_analysis["Total_Sales"],
        marker_color=PALETTE["accent3"], opacity=0.85,
        text=div_analysis["Total_Sales"], texttemplate="$%{text:,.0f}", textposition="outside",
    ))
    fig_imbalance.add_trace(go.Bar(
        name="Gross Profit",
        x=div_analysis["Division"], y=div_analysis["Total_Profit"],
        marker_color=PALETTE["accent4"], opacity=0.85,
        text=div_analysis["Total_Profit"], texttemplate="$%{text:,.0f}", textposition="outside",
    ))
    fig_imbalance.add_trace(go.Bar(
        name="Cost",
        x=div_analysis["Division"], y=div_analysis["Total_Cost"],
        marker_color=PALETTE["accent5"], opacity=0.85,
        text=div_analysis["Total_Cost"], texttemplate="$%{text:,.0f}", textposition="outside",
    ))
    apply_theme(fig_imbalance, "⚖️ Revenue vs Profit Imbalance by Division")
    fig_imbalance.update_layout(barmode="group", height=400)
    st.plotly_chart(fig_imbalance, use_container_width=True)

    # Cost Ratio vs Margin scatter — efficiency quadrant
    fig_eff = px.scatter(
        div_analysis,
        x="Cost Ratio (%)", y="Gross Margin (%)",
        color="Efficiency Flag",
        color_discrete_map=flag_colors,
        size="Total_Sales", size_max=60,
        text="Division",
        hover_data={"Profit per Unit": True, "Revenue vs Profit Gap": True},
    )
    fig_eff.add_vline(x=avg_div_cost,   line_dash="dash", line_color=PALETTE["border"],
                      annotation_text="Avg Cost Ratio")
    fig_eff.add_hline(y=avg_div_margin, line_dash="dash", line_color=PALETTE["border"],
                      annotation_text="Avg Margin")
    fig_eff.update_traces(textposition="top center", textfont_size=12,
                          marker=dict(opacity=0.9, line=dict(width=1, color="white")))
    apply_theme(
        fig_eff, "🎯 Division Efficiency Quadrant: Cost Ratio vs Gross Margin")
    fig_eff.update_layout(
        height=480,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(range=[
            div_analysis["Cost Ratio (%)"].min() - 5,
            div_analysis["Cost Ratio (%)"].max() + 5,
        ]),
        yaxis=dict(range=[
            div_analysis["Gross Margin (%)"].min() - 5,
            div_analysis["Gross Margin (%)"].max() + 8,
        ]),
    )
    st.plotly_chart(fig_eff, use_container_width=True)

    st.markdown('<div class="section-header">📋 Division & Region Summary Table</div>',
                unsafe_allow_html=True)
    summary_div = df.groupby(["Division", "Region"]).agg(
        Revenue=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum"),
        Units=("Units", "sum"),
        Orders=("Order ID", "nunique"),
    ).reset_index()
    summary_div["Gross Margin (%)"] = (
        summary_div["Profit"] / summary_div["Revenue"] * 100).round(2)
    summary_div["Profit per Unit"] = (
        summary_div["Profit"] / summary_div["Units"]).round(2)
    st.dataframe(
        summary_div.style
        .format({
            "Revenue": "${:,.0f}", "Profit": "${:,.0f}", "Cost": "${:,.0f}",
            "Profit per Unit": "${:.2f}", "Gross Margin (%)": "{:.1f}%",
        })
        .background_gradient(subset=["Gross Margin (%)"], cmap="RdYlGn")
        .background_gradient(subset=["Profit"], cmap="Blues"),
        use_container_width=True, height=350,
    )


# ══════════════════════════════════════════════
# TAB 3 — COST & MARGIN DIAGNOSTICS
# ══════════════════════════════════════════════
with tab3:

    st.markdown('<div class="section-header">🔬 Cost Structure Diagnostics</div>',
                unsafe_allow_html=True)

    # Build diagnostics dataframe
    diag_df = prod_df.copy()
    diag_df["Cost Ratio (%)"] = (diag_df["Total_Cost"] /
                                 diag_df["Total_Sales"] * 100).round(2)
    diag_df["Revenue per Unit"] = (
        diag_df["Total_Sales"] / diag_df["Total_Units"]).round(2)
    diag_df["Cost per Unit"] = (
        diag_df["Total_Cost"] / diag_df["Total_Units"]).round(2)
    diag_df["Margin Gap"] = (
        diag_df["Gross Margin (%)"] - diag_df["Gross Margin (%)"].mean()).round(2)
    diag_df["Cost vs Avg"] = (
        diag_df["Total_Cost"] - diag_df["Total_Cost"].mean()).round(2)

    avg_margin_diag = diag_df["Gross Margin (%)"].mean()
    avg_cost_diag = diag_df["Cost Ratio (%)"].mean()

    # ── Classify Cost-Heavy & Margin-Poor ──
    def cost_structure_class(row):
        if row["Cost Ratio (%)"] > avg_cost_diag and row["Gross Margin (%)"] < avg_margin_diag:
            return "🔴 Cost-Heavy / Margin-Poor"
        elif row["Cost Ratio (%)"] > avg_cost_diag and row["Gross Margin (%)"] >= avg_margin_diag:
            return "🟠 Cost-Heavy / Margin-OK"
        elif row["Cost Ratio (%)"] <= avg_cost_diag and row["Gross Margin (%)"] < avg_margin_diag:
            return "🟡 Lean-Cost / Margin-Poor"
        else:
            return "🟢 Lean-Cost / High-Margin"

    diag_df["Cost Structure"] = diag_df.apply(cost_structure_class, axis=1)

    cost_struct_colors = {
        "🔴 Cost-Heavy / Margin-Poor":  "#EF4444",
        "🟠 Cost-Heavy / Margin-OK":    "#FACC15",
        "🟡 Lean-Cost / Margin-Poor":   "#FDE047",
        "🟢 Lean-Cost / High-Margin":   "#4ADE80",
    }

    # ── Pricing Inefficiency Flag ──
    def pricing_flag(row):
        if row["Revenue per Unit"] < row["Cost per Unit"] * 1.2:
            return "🔴 Severe Pricing Inefficiency"
        elif row["Revenue per Unit"] < row["Cost per Unit"] * 1.5:
            return "🟠 Moderate Pricing Inefficiency"
        elif row["Revenue per Unit"] < row["Cost per Unit"] * 2.0:
            return "🟡 Minor Pricing Inefficiency"
        else:
            return "🟢 Pricing Healthy"

    diag_df["Pricing Flag"] = diag_df.apply(pricing_flag, axis=1)

    # ── Action Flag ──
    def action_flag(row):
        if row["Gross Margin (%)"] < 15:
            return "🔴 Discontinuation Review"
        elif row["Cost Ratio (%)"] > 60 and row["Gross Margin (%)"] < 40:
            return "🟠 Cost Renegotiation"
        elif row["Gross Margin (%)"] < avg_margin_diag and row["Total_Sales"] > diag_df["Total_Sales"].mean():
            return "🟡 Repricing Needed"
        else:
            return "🟢 No Action Required"

    diag_df["Recommended Action"] = diag_df.apply(action_flag, axis=1)

    action_colors = {
        "🔴 Discontinuation Review": "#EF4444",
        "🟠 Cost Renegotiation":      "#FACC15",
        "🟡 Repricing Needed":        "#FDE047",
        "🟢 No Action Required":      "#4ADE80",
    }

    # ── KPI Summary Cards ──
    cost_heavy = diag_df[diag_df["Cost Structure"]
                         == "🔴 Cost-Heavy / Margin-Poor"]
    discontinue = diag_df[diag_df["Recommended Action"]
                          == "🔴 Discontinuation Review"]
    reprice = diag_df[diag_df["Recommended Action"] == "🟡 Repricing Needed"]
    renegotiate = diag_df[diag_df["Recommended Action"]
                          == "🟠 Cost Renegotiation"]

    dk1, dk2, dk3, dk4 = st.columns(4)
    for col, label, val, color in [
        (dk1, "🔴 Cost-Heavy/Margin-Poor",
         f"{len(cost_heavy)} products",  "#EF4444"),
        (dk2, "🔴 Discontinuation Review",
         f"{len(discontinue)} products", "#EF4444"),
        (dk3, "🟠 Cost Renegotiation",
         f"{len(renegotiate)} products", "#FACC15"),
        (dk4, "🟡 Repricing Needed",
         f"{len(reprice)} products",     "#FDE047"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {color};">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="font-size:1.4rem; background:none;
                   -webkit-text-fill-color:{color};">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1 — Cost-Heavy / Margin-Poor Scatter
    fig_cost_struct = px.scatter(
        diag_df,
        x="Cost Ratio (%)", y="Gross Margin (%)",
        color="Cost Structure",
        color_discrete_map=cost_struct_colors,
        size="Total_Sales", size_max=55,
        hover_name="Product Name",
        hover_data={"Total_Cost": True, "Total_Profit": True,
                    "Pricing Flag": True, "Division": True},
    )
    fig_cost_struct.add_vline(x=avg_cost_diag, line_dash="dash",
                              line_color=PALETTE["border"],
                              annotation_text="Avg Cost Ratio",
                              annotation_font_color=PALETTE["text_muted"])
    fig_cost_struct.add_hline(y=avg_margin_diag, line_dash="dash",
                              line_color=PALETTE["border"],
                              annotation_text="Avg Margin",
                              annotation_font_color=PALETTE["text_muted"])
    apply_theme(fig_cost_struct,
                "🔴 Cost-Heavy vs Margin-Poor Product Identification")
    fig_cost_struct.update_traces(marker=dict(
        opacity=0.85, line=dict(width=1, color="white")))
    fig_cost_struct.update_layout(height=480)
    st.plotly_chart(fig_cost_struct, use_container_width=True)

    # Row 2 — Pricing Inefficiency Bar
    pricing_order = ["🔴 Severe Pricing Inefficiency", "🟠 Moderate Pricing Inefficiency",
                     "🟡 Minor Pricing Inefficiency", "🟢 Pricing Healthy"]
    pricing_colors = {
        "🔴 Severe Pricing Inefficiency":   "#EF4444",
        "🟠 Moderate Pricing Inefficiency": "#FACC15",
        "🟡 Minor Pricing Inefficiency":    "#FDE047",
        "🟢 Pricing Healthy":               "#4ADE80",
    }
    fig_pricing = px.bar(
        diag_df.sort_values("Revenue per Unit", ascending=True),
        x="Revenue per Unit", y="Product Name",
        color="Pricing Flag",
        color_discrete_map=pricing_colors,
        orientation="h",
        hover_data={"Cost per Unit": True, "Gross Margin (%)": True,
                    "Pricing Flag": True, "Division": True},
        text="Revenue per Unit",
    )
    fig_pricing.update_traces(
        texttemplate="$%{text:.2f}", textposition="outside")
    apply_theme(
        fig_pricing, "💲 Pricing Inefficiency by Product (Revenue per Unit vs Cost)")
    fig_pricing.update_layout(height=500, showlegend=True)
    st.plotly_chart(fig_pricing, use_container_width=True)

    # Row 3 — Action Flag Bar
    fig_action = px.bar(
        diag_df.sort_values("Gross Margin (%)", ascending=True),
        x="Gross Margin (%)", y="Product Name",
        color="Recommended Action",
        color_discrete_map=action_colors,
        orientation="h",
        text="Gross Margin (%)",
        hover_data={"Cost Ratio (%)": True, "Total_Sales": True,
                    "Recommended Action": True, "Division": True},
    )
    fig_action.update_traces(
        texttemplate="%{text:.1f}%", textposition="outside")
    apply_theme(
        fig_action, "🚩 Product Action Flags: Reprice / Renegotiate / Discontinue")
    fig_action.update_layout(height=500, showlegend=True)
    st.plotly_chart(fig_action, use_container_width=True)

    st.markdown('<div class="section-header">💡 Cost vs Margin Diagnostics</div>',
                unsafe_allow_html=True)

    # Scatter: Cost vs Sales, colored by margin
    c1t3, c2t3 = st.columns([1.2, 1])

    with c1t3:
        fig_scatter = px.scatter(
            df, x="Cost", y="Sales",
            color="Gross Margin (%)",
            color_continuous_scale=["#EF4444", "#FACC15", "#4ADE80"],
            size="Units", size_max=18,
            hover_data=["Product Name", "Division",
                        "Gross Margin (%)", "Gross Profit"],
            opacity=0.75,
        )
    fig_scatter.add_shape(type="line", x0=df["Cost"].min(), y0=df["Cost"].min(),
                          x1=df["Cost"].max(), y1=df["Cost"].max(),
                          line=dict(color=PALETTE["accent5"], width=1.5, dash="dash"))
    apply_theme(fig_scatter, "🔍 Cost vs Sales Scatter (color = margin %)")
    fig_scatter.update_layout(height=420)
    st.plotly_chart(fig_scatter, use_container_width=True)

    with c2t3:
        # Margin risk flag
        risk_df = prod_df.copy()
    conditions = [
        (risk_df["Gross Margin (%)"] >= 45),
        (risk_df["Gross Margin (%)"] >= 30),
        (risk_df["Gross Margin (%)"] >= 15),
        (risk_df["Gross Margin (%)"] >= 0),
    ]
    choices = ["🟢 Healthy", "🟡 Acceptable", "🟠 At Risk", "🔴 Critical"]
    risk_df["Margin Flag"] = np.select(
        conditions, choices, default="🔴 Critical")
    flag_color = {"🟢 Healthy": "#4ADE80", "🟡 Acceptable": "#FDE047",
                  "🟠 At Risk": "#FACC15", "🔴 Critical": "#EF4444"}
    fig_risk = px.bar(
        risk_df.sort_values("Gross Margin (%)", ascending=True),
        x="Gross Margin (%)", y="Product Name",
        color="Margin Flag",
        color_discrete_map=flag_color,
        orientation="h",
        text="Gross Margin (%)", text_auto=".1f",
    )
    apply_theme(fig_risk, "🚨 Margin Risk Classification")
    fig_risk.update_layout(height=420)
    st.plotly_chart(fig_risk, use_container_width=True)

    # Cost per Unit vs Profit per Unit
    c3t3, c4t3 = st.columns(2)

    with c3t3:
        # Row 3 — Profit per Unit vs Volume (full width)
        fig_cpu = px.scatter(
            prod_df.sort_values("Profit per Unit", ascending=False),
            x="Product Name",
            y="Profit per Unit",
            size="Total_Units",
            color="Division",
            color_discrete_map=DIVISION_COLORS,
            hover_name="Product Name",
            hover_data={"Total_Units": True,
                        "Total_Profit": True, "Profit per Unit": True},
            size_max=60,
        )
    apply_theme(
        fig_cpu, "📏 Profit per Unit vs Volume (bubble size = units sold)")
    fig_cpu.update_layout(height=480, xaxis_tickangle=-35)
    fig_cpu.update_traces(marker=dict(
        opacity=0.85, line=dict(width=1, color="white")))
    st.plotly_chart(fig_cpu, use_container_width=True)

    with c4t3:
        # Cost efficiency: cost-to-revenue ratio
        prod_df["Cost Ratio (%)"] = (
            prod_df["Total_Cost"] / prod_df["Total_Sales"] * 100).round(2)
    fig_cr = px.bar(
        prod_df.sort_values("Cost Ratio (%)", ascending=False),
        x="Cost Ratio (%)", y="Product Name",
        color="Division", color_discrete_map=DIVISION_COLORS,
        orientation="h", text="Cost Ratio (%)", text_auto=".1f",
    )
    apply_theme(fig_cr, "🏷 Cost-to-Revenue Ratio by Product (lower = better)")
    fig_cr.update_layout(height=420)
    st.plotly_chart(fig_cr, use_container_width=True)

    # Ship Mode Profitability
    st.markdown('<div class="section-header">🚚 Ship Mode Profitability</div>',
                unsafe_allow_html=True)
    ship_df = df.groupby("Ship Mode").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Margin=("Gross Margin (%)", "mean"),
        Orders=("Order ID", "nunique"),
    ).reset_index().round(2)

    c5t3, c6t3 = st.columns(2)
    with c5t3:
        fig_ship = px.bar(
            ship_df, x="Ship Mode", y="Avg_Margin",
            color="Ship Mode", text="Avg_Margin", text_auto=".1f",
            color_discrete_sequence=[PALETTE["accent1"], PALETTE["accent2"],
                                     PALETTE["accent3"], PALETTE["accent4"]],
        )
        apply_theme(fig_ship, "📦 Avg Gross Margin by Ship Mode (%)")
        fig_ship.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig_ship, use_container_width=True)

    with c6t3:
        fig_ship_rev = px.pie(
            ship_df, values="Total_Sales", names="Ship Mode", hole=0.5,
            color_discrete_sequence=[PALETTE["accent1"], PALETTE["accent2"],
                                     PALETTE["accent3"], PALETTE["accent4"]],
        )
        apply_theme(fig_ship_rev, "🚚 Revenue Split by Ship Mode")
        fig_ship_rev.update_layout(height=320)
        st.plotly_chart(fig_ship_rev, use_container_width=True)

    st.markdown('<div class="section-header">🏷 Product Action Flags (Pricing Recommendations)</div>',
                unsafe_allow_html=True)

    action_df = prod_df.copy()
    action_df["Cost Ratio (%)"] = (
        action_df["Total_Cost"] / action_df["Total_Sales"] * 100).round(2)

    def action_flag(row):
        if row["Gross Margin (%)"] < 15:
            return "🔴 Discontinuation Review"
        elif row["Gross Margin (%)"] < 30 and row["Cost Ratio (%)"] > 70:
            return "🟠 Cost Renegotiation"
        elif row["Gross Margin (%)"] < 45 and row["Total_Sales"] > prod_df["Total_Sales"].mean():
            return "🟡 Repricing Needed"
        else:
            return "🟢 Healthy — No Action"

    action_df["Recommended Action"] = action_df.apply(action_flag, axis=1)

    st.dataframe(
        action_df[[
            "Product Name", "Division", "Factory",
            "Total_Sales", "Total_Cost", "Total_Profit",
            "Gross Margin (%)", "Cost Ratio (%)", "Recommended Action"
        ]].sort_values("Gross Margin (%)").style
        .format({
            "Total_Sales":     "${:,.0f}",
            "Total_Cost":      "${:,.0f}",
            "Total_Profit":    "${:,.0f}",
            "Gross Margin (%)": "{:.1f}%",
            "Cost Ratio (%)":  "{:.1f}%",
        })
        .background_gradient(subset=["Gross Margin (%)"], cmap="RdYlGn")
        .background_gradient(subset=["Cost Ratio (%)"],   cmap="Reds_r"),
        use_container_width=True, height=450,
    )


# ══════════════════════════════════════════════
# TAB 4 — PARETO & CONCENTRATION
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">📐 Profit Concentration (Pareto) Analysis</div>',
                unsafe_allow_html=True)

    # Build Pareto FIRST
    pareto = prod_df.sort_values("Total_Profit", ascending=False).copy()
    pareto["Cumulative Profit (%)"] = (
        pareto["Total_Profit"].cumsum() / pareto["Total_Profit"].sum() * 100).round(2)
    pareto["Product Rank"] = range(1, len(pareto) + 1)

    rev_pareto = prod_df.sort_values("Total_Sales", ascending=False).copy()
    rev_pareto["Cumulative Revenue (%)"] = (
        rev_pareto["Total_Sales"].cumsum() / rev_pareto["Total_Sales"].sum() * 100).round(2)

    # Concentration metrics TOP
    p80_profit = pareto[pareto["Cumulative Profit (%)"] <= 80].shape[0]
    p80_rev = rev_pareto[rev_pareto["Cumulative Revenue (%)"] <= 80].shape[0]
    top3_profit_pct = pareto.head(
        3)["Total_Profit"].sum() / pareto["Total_Profit"].sum() * 100

    cm1, cm2, cm3 = st.columns(3)
    for col, label, val in [
        (cm1, "Products driving 80% Profit",  f"{p80_profit} / {len(pareto)}"),
        (cm2, "Products driving 80% Revenue",
         f"{p80_rev} / {len(rev_pareto)}"),
        (cm3, "Top 3 Products' Profit Share", f"{top3_profit_pct:.1f}%"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="font-size:1.6rem;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1 — Profit Pareto (full width)
    fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    fig_pareto.add_trace(go.Bar(
        x=pareto["Product Name"], y=pareto["Total_Profit"],
        name="Gross Profit ($)",
        marker=dict(color=pareto["Total_Profit"],
                    colorscale=[[0, PALETTE["accent2"]], [1, PALETTE["accent1"]]]),
    ), secondary_y=False)
    fig_pareto.add_trace(go.Scatter(
        x=pareto["Product Name"], y=pareto["Cumulative Profit (%)"],
        name="Cumulative Profit %",
        line=dict(color=PALETTE["accent3"], width=2.5),
        mode="lines+markers", marker=dict(size=7),
    ), secondary_y=True)
    fig_pareto.add_hline(y=80, line_dash="dash", line_color=PALETTE["accent5"],
                         annotation_text="80% threshold", secondary_y=True)
    apply_theme(fig_pareto, "📐 Profit Pareto Chart")
    fig_pareto.update_layout(height=420, xaxis_tickangle=-35)
    fig_pareto.update_yaxes(title_text="Profit ($)",
                            secondary_y=False, gridcolor=PALETTE["border"])
    fig_pareto.update_yaxes(title_text="Cumulative Profit (%)", secondary_y=True, range=[
                            0, 105], gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pareto, use_container_width=True)

    # Row 2 — Revenue Pareto (full width)
    fig_rev_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    fig_rev_pareto.add_trace(go.Bar(
        x=rev_pareto["Product Name"], y=rev_pareto["Total_Sales"],
        name="Revenue ($)",
        marker=dict(color=rev_pareto["Total_Sales"],
                    colorscale=[[0, PALETTE["accent4"]], [1, PALETTE["accent3"]]]),
    ), secondary_y=False)
    fig_rev_pareto.add_trace(go.Scatter(
        x=rev_pareto["Product Name"], y=rev_pareto["Cumulative Revenue (%)"],
        name="Cumulative Revenue %",
        line=dict(color=PALETTE["accent1"], width=2.5),
        mode="lines+markers", marker=dict(size=7),
    ), secondary_y=True)
    fig_rev_pareto.add_hline(y=80, line_dash="dash", line_color=PALETTE["accent5"],
                             annotation_text="80% threshold", secondary_y=True)
    apply_theme(fig_rev_pareto, "📐 Revenue Pareto Chart")
    fig_rev_pareto.update_layout(height=420, xaxis_tickangle=-35)
    fig_rev_pareto.update_yaxes(
        title_text="Revenue ($)", secondary_y=False, gridcolor=PALETTE["border"])
    fig_rev_pareto.update_yaxes(title_text="Cumulative Revenue (%)", secondary_y=True, range=[
                                0, 105], gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_rev_pareto, use_container_width=True)

    # Row 3 — Treemap (full width)
    fig_tree = px.treemap(
        prod_df, path=["Division", "Product Name"],
        values="Total_Profit",
        color="Gross Margin (%)",
        color_continuous_scale=["#EF4444", "#FACC15", "#FDE047", "#4ADE80"],
        hover_data={"Total_Sales": True, "Profit per Unit": True},
    )
    apply_theme(
        fig_tree, "🌳 Profit Treemap: Division → Product (color = Gross Margin %)")
    fig_tree.update_layout(height=450)
    st.plotly_chart(fig_tree, use_container_width=True)

    # Row 4 — Advanced State Map (full width)
    st.markdown('<div class="section-header">🗺 State-Level Profit Concentration</div>',
                unsafe_allow_html=True)

    # ── City-level aggregation (for dot markers + labels) ──
    city_coords = {
        "New York City": (40.7128, -74.0060), "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298), "Houston": (29.7604, -95.3698),
        "Phoenix": (33.4484, -112.0740), "Philadelphia": (39.9526, -75.1652),
        "San Antonio": (29.4241, -98.4936), "San Diego": (32.7157, -117.1611),
        "Dallas": (32.7767, -96.7970), "San Jose": (37.3382, -121.8863),
        "Austin": (30.2672, -97.7431), "Jacksonville": (30.3322, -81.6557),
        "Fort Worth": (32.7555, -97.3308), "Columbus": (39.9612, -82.9988),
        "Charlotte": (35.2271, -80.8431), "Indianapolis": (39.7684, -86.1581),
        "San Francisco": (37.7749, -122.4194), "Seattle": (47.6062, -122.3321),
        "Denver": (39.7392, -104.9903), "Nashville": (36.1627, -86.7816),
        "Oklahoma City": (35.4676, -97.5164), "El Paso": (31.7619, -106.4850),
        "Washington": (38.9072, -77.0369), "Las Vegas": (36.1699, -115.1398),
        "Memphis": (35.1495, -90.0490), "Louisville": (38.2527, -85.7585),
        "Portland": (45.5051, -122.6750), "Baltimore": (39.2904, -76.6122),
        "Milwaukee": (43.0389, -87.9065), "Albuquerque": (35.0844, -106.6504),
        "Tucson": (32.2226, -110.9747), "Fresno": (36.7378, -119.7871),
        "Sacramento": (38.5816, -121.4944), "Mesa": (33.4152, -111.8315),
        "Kansas City": (39.0997, -94.5786), "Atlanta": (33.7490, -84.3880),
        "Omaha": (41.2565, -95.9345), "Colorado Springs": (38.8339, -104.8214),
        "Raleigh": (35.7796, -78.6382), "Long Beach": (33.7701, -118.1937),
        "Virginia Beach": (36.8529, -75.9780), "Minneapolis": (44.9778, -93.2650),
        "Tampa": (27.9506, -82.4572), "New Orleans": (29.9511, -90.0715),
        "Arlington": (32.7357, -97.1081), "Bakersfield": (35.3733, -119.0187),
        "Honolulu": (21.3069, -157.8583), "Anaheim": (33.8366, -117.9143),
        "Aurora": (39.7294, -104.8319), "Santa Ana": (33.7455, -117.8677),
        "Corpus Christi": (27.8006, -97.3964), "Riverside": (33.9806, -117.3755),
        "St. Louis": (38.6270, -90.1994), "Lexington": (38.0406, -84.5037),
        "Pittsburgh": (40.4406, -79.9959), "Stockton": (37.9577, -121.2908),
        "Cincinnati": (39.1031, -84.5120), "St. Paul": (44.9537, -93.0900),
        "Greensboro": (36.0726, -79.7920), "Toledo": (41.6528, -83.5379),
        "Newark": (40.7357, -74.1724), "Plano": (33.0198, -96.6989),
        "Henderson": (36.0395, -114.9817), "Lincoln": (40.8136, -96.7026),
        "Buffalo": (42.8864, -78.8784), "Fort Wayne": (41.0793, -85.1394),
        "Jersey City": (40.7178, -74.0431), "Chula Vista": (32.6401, -117.0842),
        "Orlando": (28.5383, -81.3792), "St. Petersburg": (27.7731, -82.6400),
        "Norfolk": (36.8508, -76.2859), "Chandler": (33.3062, -111.8413),
        "Laredo": (27.5306, -99.4803), "Madison": (43.0731, -89.4012),
        "Durham": (35.9940, -78.8986), "Lubbock": (33.5779, -101.8552),
        "Winston-Salem": (36.0999, -80.2442), "Garland": (32.9126, -96.6389),
        "Glendale": (33.5387, -112.1860), "Hialeah": (25.8576, -80.2781),
        "Reno": (39.5296, -119.8138), "Baton Rouge": (30.4515, -91.1871),
        "Irvine": (33.6846, -117.8265), "Chesapeake": (36.7682, -76.2875),
        "Irving": (32.8140, -96.9489), "Scottsdale": (33.4942, -111.9261),
        "North Las Vegas": (36.1989, -115.1175), "Fremont": (37.5485, -121.9886),
        "Gilbert": (33.3528, -111.7890), "San Bernardino": (34.1083, -117.2898),
        "Boise": (43.6150, -116.2023), "Birmingham": (33.5186, -86.8104),
        "Rochester": (43.1566, -77.6088), "Richmond": (37.5407, -77.4360),
        "Spokane": (47.6588, -117.4260), "Des Moines": (41.5868, -93.6250),
        "Montgomery": (32.3668, -86.3000), "Modesto": (37.6391, -120.9969),
        "Fayetteville": (36.0626, -94.1574), "Tacoma": (47.2529, -122.4443),
        "Akron": (41.0814, -81.5190), "Yonkers": (40.9312, -73.8988),
        "Oxnard": (34.1975, -119.1771), "Little Rock": (34.7465, -92.2896),
        "Columbus": (39.9612, -82.9988), "Huntington Beach": (33.6595, -117.9988),
        "Grand Rapids": (42.9634, -85.6681), "Glendale": (34.1425, -118.2551),
        "Salt Lake City": (40.7608, -111.8910), "Tallahassee": (30.4518, -84.2807),
        "Huntsville": (34.7304, -86.5861), "Worcester": (42.2626, -71.8023),
        "Knoxville": (35.9606, -83.9207), "Providence": (41.8240, -71.4128),
        "Tempe": (33.4255, -111.9400), "Brownsville": (25.9017, -97.4975),
        "Overland Park": (38.9822, -94.6708), "Santa Clarita": (34.3917, -118.5426),
        "Garden Grove": (33.7743, -117.9378), "Oceanside": (33.1959, -117.3795),
        "Chattanooga": (35.0456, -85.3097), "Fort Lauderdale": (26.1224, -80.1373),
        "Rancho Cucamonga": (34.1064, -117.5931), "Santa Rosa": (38.4404, -122.7141),
        "Elk Grove": (38.4088, -121.3716), "Ontario": (34.0633, -117.6509),
        "Eugene": (44.0521, -123.0868), "Peoria": (40.6936, -89.5890),
        "Corona": (33.8753, -117.5664), "Cape Coral": (26.5629, -81.9495),
        "Springfield": (37.2153, -93.2982), "Fort Collins": (40.5853, -105.0844),
        "Jackson": (32.2988, -90.1848), "Alexandria": (38.8048, -77.0469),
        "Hayward": (37.6688, -122.0808), "Lancester": (34.6868, -118.1542),
        "Salinas": (36.6777, -121.6555), "Palmdale": (34.5794, -118.1165),
        "Sunnyvale": (37.3688, -122.0363), "Pomona": (34.0552, -117.7500),
        "Escondido": (33.1192, -117.0864), "Kansas City": (39.0997, -94.5786),
        "Roseville": (38.7521, -121.2880), "Torrance": (33.8358, -118.3406),
        "Pasadena": (34.1478, -118.1445), "Paterson": (40.9176, -74.1719),
        "Bridgeport": (41.1670, -73.2048), "McAllen": (26.2034, -98.2300),
        "Mesquite": (32.7668, -96.5992), "Macon": (32.8407, -83.6324),
        "Syracuse": (43.0481, -76.1474), "Surprise": (33.6292, -112.3679),
        "Savannah": (32.0809, -81.0912), "Gainesville": (29.6516, -82.3248),
        "Hollywood": (26.0112, -80.1495), "Aurora": (41.7606, -88.3201),
        "Naperville": (41.7508, -88.1535), "Metairie": (29.9935, -90.1715),
        "Lakewood": (39.7047, -105.0814), "Clarksville": (36.5298, -87.3595),
        "Rockford": (42.2711, -89.0937), "Joliet": (41.5250, -88.0817),
        "Shreveport": (32.5252, -93.7502), "Moreno Valley": (33.9425, -117.2297),
        "Fontana": (34.0922, -117.4350), "Glendale": (33.5387, -112.1860),
        "Fargo": (46.8772, -96.7898), "Yonkers": (40.9312, -73.8988),
        "Amarillo": (35.2220, -101.8313), "Bossier City": (32.5160, -93.7321),
        "Frisco": (33.1507, -96.8236), "Port Arthur": (29.8849, -93.9399),
        "Spokane Valley": (47.6732, -117.2394), "McKinney": (33.1972, -96.6397),
        "Roswell": (34.0232, -84.3616), "Denton": (33.2148, -97.1331),
        "Dover": (39.1582, -75.5244), "Athens": (33.9609, -83.3831),
        "Mount Pleasant": (32.8323, -79.8284), "Pembroke Pines": (26.0072, -80.2962),
        "Springfield": (39.7817, -89.6501), "Sioux Falls": (43.5446, -96.7311),
        "Vancouver": (45.6387, -122.6615), "Tacoma": (47.2529, -122.4443),
        "Murfreesboro": (35.8456, -86.3903), "Dayton": (39.7589, -84.1916),
        "Cedar Rapids": (41.9779, -91.6656), "Tempe": (33.4255, -111.9400),
        "Columbia": (34.0007, -81.0348), "Chesapeake": (36.7682, -76.2875),
        "Tallahassee": (30.4518, -84.2807), "Arvada": (39.8028, -105.0875),
        "Lubbock": (33.5779, -101.8552), "Reno": (39.5296, -119.8138),
        "Laredo": (27.5306, -99.4803), "Springfield": (37.2153, -93.2982),
        "Pasadena": (29.6911, -95.2091), "Lexington-Fayette": (38.0406, -84.5037),
        "Ann Arbor": (42.2808, -83.7430), "Wilmington": (34.2257, -77.9447),
        "Stamford": (41.0534, -73.5387), "Warren": (42.5145, -83.0147),
        "Thousand Oaks": (34.1705, -118.8376), "Westminster": (39.8366, -105.0372),
        "Hampton": (37.0299, -76.3452), "Cary": (35.7915, -78.7811),
        "Columbia": (38.9517, -92.3341), "Sterling Heights": (42.5803, -83.0302),
        "New Haven": (41.3082, -72.9282), "Miramar": (25.9871, -80.2330),
        "Coral Springs": (26.2709, -80.2706), "Erie": (42.1292, -80.0851),
        "Round Rock": (30.5083, -97.6789), "Bellevue": (47.6101, -122.2015),
        "Allentown": (40.6023, -75.4714), "New York City": (40.7128, -74.0060),
        "Edmonds": (47.8107, -122.3774), "Fairfield": (38.2494, -122.0400),
        "Loveland": (40.3978, -105.0749), "Grand Rapids": (42.9634, -85.6681),
        "Albuquerque": (35.0844, -106.6504),
    }

    state_df = df.groupby("State/Province").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Avg_Margin=("Gross Margin (%)", "mean"),
    ).reset_index()
    state_df["Gross Margin (%)"] = (
        state_df["Total_Profit"] / state_df["Total_Sales"] * 100).round(2)
    state_df["Profit per Order"] = (
        state_df["Total_Profit"] / state_df["Total_Orders"]).round(2)
    state_df["Revenue per Unit"] = (
        state_df["Total_Sales"] / state_df["Total_Units"]).round(2)
    state_df["Profit Rank"] = state_df["Total_Profit"].rank(
        ascending=False).astype(int)

    # ── City-level aggregation ──
    city_df = df.groupby(["City", "State/Province"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Avg_Margin=("Gross Margin (%)", "mean"),
    ).reset_index()
    city_df["Gross Margin (%)"] = (
        city_df["Total_Profit"] / city_df["Total_Sales"] * 100).round(2)
    city_df["Profit per Order"] = (
        city_df["Total_Profit"] / city_df["Total_Orders"]).round(2)

    # Attach lat/lon
    city_df["lat"] = city_df["City"].map(
        lambda c: city_coords.get(c, (None, None))[0])
    city_df["lon"] = city_df["City"].map(
        lambda c: city_coords.get(c, (None, None))[1])
    city_df = city_df.dropna(subset=["lat", "lon"])

    # Map toggle
    map_metric = st.selectbox(
        "🎯 Color map by",
        options=["Total_Profit",
                 "Gross Margin (%)", "Total_Orders", "Total_Units", "Profit per Order"],
        format_func=lambda x: {
            "Total_Profit":     "💰 Gross Profit ($)",
            "Gross Margin (%)": "📊 Gross Margin (%)",
            "Total_Orders":     "🧾 Total Orders",
            "Total_Units":      "📦 Total Units",
            "Profit per Order": "⚡ Profit per Order ($)",
        }[x],
        key="map_metric"
    )

    colorscales = {
        "Total_Profit":     [[0, "#0B1210"], [0.3, "#123322"], [0.6, "#22C55E"], [0.85, "#FACC15"], [1.0, "#FDE047"]],
        "Gross Margin (%)": [[0, "#EF4444"], [0.4, "#FACC15"], [0.7, "#FDE047"], [1.0, "#4ADE80"]],
        "Total_Orders":     [[0, "#0B1210"], [0.4, "#84CC16"], [0.75, "#22C55E"], [1.0, "#FACC15"]],
        "Total_Units":      [[0, "#0B1210"], [0.4, "#4ADE80"], [0.75, "#84CC16"], [1.0, "#22C55E"]],
        "Profit per Order": [[0, "#1C2433"], [0.4, "#84CC16"], [0.75, "#FACC15"], [1.0, "#FDE047"]],
    }

    metric_label_map = {
        "Total_Profit":     "Gross Profit ($)",
        "Gross Margin (%)": "Gross Margin (%)",
        "Total_Orders":     "Total Orders",
        "Total_Units":      "Total Units",
        "Profit per Order": "Profit per Order ($)",
    }

    fig_map = go.Figure()

    # ── Layer 1: State Choropleth ──
    fig_map.add_trace(go.Choropleth(
        locations=state_df["State/Province"],
        z=state_df[map_metric],
        locationmode="USA-states",
        colorscale=colorscales[map_metric],
        colorbar=dict(
            title=dict(text=metric_label_map[map_metric],
                       font=dict(color=PALETTE["text_main"], size=11)),
            tickfont=dict(color=PALETTE["text_main"], size=10),
            bgcolor="rgba(22,27,34,0.9)",
            outlinecolor=PALETTE["border"],
            outlinewidth=1,
            thickness=16,
            len=0.7,
            x=1.01,
        ),
        hovertemplate=(
            "<b style='font-size:14px'>%{location}</b><br>"
            "━━━━━━━━━━━━━━━━━━<br>"
            "💰 Gross Profit:  <b>$%{customdata[0]:,.0f}</b><br>"
            "📊 Gross Margin:  <b>%{customdata[1]:.1f}%</b><br>"
            "🧾 Orders:        <b>%{customdata[2]:,}</b><br>"
            "📦 Units:         <b>%{customdata[3]:,}</b><br>"
            "⚡ Profit/Order:  <b>$%{customdata[4]:.2f}</b><br>"
            "🏆 Profit Rank:   <b>#%{customdata[5]}</b><br>"
            "<extra></extra>"
        ),
        customdata=state_df[[
            "Total_Profit", "Gross Margin (%)",
            "Total_Orders", "Total_Units",
            "Profit per Order", "Profit Rank"
        ]].values,
        marker_line_color="#30363D",
        marker_line_width=1.2,
    ))

    # ── Layer 2: City Scatter Markers ──
    city_metric_vals = city_df[map_metric]
    city_metric_min = city_metric_vals.min()
    city_metric_max = city_metric_vals.max()
    city_metric_range = city_metric_max - \
        city_metric_min if city_metric_max != city_metric_min else 1

    fig_map.add_trace(go.Scattergeo(
        lat=city_df["lat"],
        lon=city_df["lon"],
        mode="markers+text",
        text=city_df["City"],
        textposition="top center",
        textfont=dict(
            size=8,
            color="white",
            family="Inter, sans-serif",
        ),
        marker=dict(
            size=((city_df[map_metric] - city_metric_min) /
                  city_metric_range * 14 + 5),
            color=city_df[map_metric],
            colorscale=colorscales[map_metric],
            opacity=0.88,
            line=dict(width=0.8, color="white"),
            showscale=False,
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            f"{metric_label_map[map_metric]}: <b>%{{customdata[0]:,.1f}}</b><br>"
            "💰 Gross Profit: <b>$%{customdata[1]:,.0f}</b><br>"
            "📊 Gross Margin: <b>%{customdata[2]:.1f}%</b><br>"
            "🧾 Orders: <b>%{customdata[3]:,}</b><br>"
            "📦 Units: <b>%{customdata[4]:,}</b><br>"
            "<extra></extra>"
        ),
        customdata=city_df[[map_metric, "Total_Profit",
                            "Gross Margin (%)", "Total_Orders", "Total_Units"]].values,
        name="Cities",
        showlegend=False,
    ))

    fig_map.update_layout(
        geo=dict(
            scope="usa",
            bgcolor="rgba(0,0,0,0)",
            lakecolor="#0B1210",
            landcolor="#141F1A",
            subunitcolor="#30363D",
            countrycolor="#30363D",
            showlakes=True,
            showland=True,
            showframe=False,
            showcoastlines=False,
            projection_type="albers usa",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text_main"]),
        margin=dict(l=0, r=60, t=50, b=0),
        height=560,
        title=dict(
            text=f"🗺 State-Level & City <b>{metric_label_map[map_metric]}</b> (USA)",
            font=dict(size=15, color=PALETTE["text_main"]),
            x=0.01,
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown('<div class="section-header">🚨 Congestion-Prone States & Over-Dependency Risk</div>',
                unsafe_allow_html=True)

    # Aggregate by state
    congest_df = df.groupby("State/Province").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Divisions=("Division", "nunique"),
        Products=("Product Name", "nunique"),
    ).reset_index()

    congest_df["Gross Margin (%)"] = (
        congest_df["Total_Profit"] / congest_df["Total_Sales"] * 100).round(2)
    congest_df["Revenue Share (%)"] = (
        congest_df["Total_Sales"] / congest_df["Total_Sales"].sum() * 100).round(2)
    congest_df["Profit Share (%)"] = (
        congest_df["Total_Profit"] / congest_df["Total_Profit"].sum() * 100).round(2)
    congest_df["Order Concentration (%)"] = (
        congest_df["Total_Orders"] / congest_df["Total_Orders"].sum() * 100).round(2)

    # Flag congestion & dependency
    top_revenue_threshold = congest_df["Revenue Share (%)"].quantile(0.80)
    top_order_threshold = congest_df["Order Concentration (%)"].quantile(0.80)
    top_profit_threshold = congest_df["Profit Share (%)"].quantile(0.80)

    def risk_flag(row):
        flags = []
        if row["Revenue Share (%)"] >= top_revenue_threshold:
            flags.append("💰 Revenue Over-Dependency")
        if row["Order Concentration (%)"] >= top_order_threshold:
            flags.append("📦 Order Congestion")
        if row["Profit Share (%)"] >= top_profit_threshold:
            flags.append("📊 Profit Concentration Risk")
        if row["Divisions"] == 1:
            flags.append("⚠️ Single Division Dependency")
        return " | ".join(flags) if flags else "✅ Healthy"

    congest_df["Risk Flag"] = congest_df.apply(risk_flag, axis=1)
    congest_df["Risk Score"] = (
        (congest_df["Revenue Share (%)"] >= top_revenue_threshold).astype(int) +
        (congest_df["Order Concentration (%)"] >= top_order_threshold).astype(int) +
        (congest_df["Profit Share (%)"] >= top_profit_threshold).astype(int) +
        (congest_df["Divisions"] == 1).astype(int)
    )

    risk_color_map = {0: "#4ADE80", 1: "#FDE047",
                      2: "#FACC15", 3: "#EF4444", 4: "#B91C1C"}

    # KPI Summary
    high_risk = congest_df[congest_df["Risk Score"] >= 2]
    healthy = congest_df[congest_df["Risk Score"] == 0]
    top3_rev = congest_df.nlargest(3, "Revenue Share (%)")[
        "Revenue Share (%)"].sum()

    ck1, ck2, ck3, ck4 = st.columns(4)
    for col, label, val in [
        (ck1, "🚨 High Risk States",         f"{len(high_risk)}"),
        (ck2, "✅ Healthy States",            f"{len(healthy)}"),
        (ck3, "📊 Top 3 States Revenue Share", f"{top3_rev:.1f}%"),
        (ck4, "⚠️ Single Division States",
         f"{(congest_df['Divisions']==1).sum()}"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="font-size:1.6rem;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1 — Risk Score Bar Chart
    fig_risk_state = px.bar(
        congest_df.sort_values("Risk Score", ascending=False).head(20),
        x="State/Province", y="Risk Score",
        color="Risk Score",
        color_continuous_scale=["#4ADE80", "#FDE047",
                                "#FACC15", "#EF4444", "#B91C1C"],
        hover_data={"Revenue Share (%)": True, "Profit Share (%)": True,
                    "Order Concentration (%)": True, "Risk Flag": True},
        text="Risk Score",
    )
    apply_theme(fig_risk_state,
                "🚨 Top 20 States by Congestion & Dependency Risk Score")
    fig_risk_state.update_traces(textposition="outside")
    fig_risk_state.update_layout(
        height=420, xaxis_tickangle=-35, coloraxis_showscale=False,
        yaxis=dict(range=[0, congest_df["Risk Score"].max() + 1]),
        uniformtext_minsize=10, uniformtext_mode="show",
    )
    st.plotly_chart(fig_risk_state, use_container_width=True)

    # Row 2 — Revenue Share vs Order Concentration Scatter
    fig_congest = px.scatter(
        congest_df,
        x="Order Concentration (%)", y="Revenue Share (%)",
        size="Total_Profit", size_max=50,
        color="Risk Score",
        color_continuous_scale=["#4ADE80", "#FDE047",
                                "#FACC15", "#EF4444", "#B91C1C"],
        hover_name="State/Province",
        hover_data={"Profit Share (%)": True, "Gross Margin (%)": True,
                    "Risk Flag": True, "Divisions": True},
        text="State/Province",
    )
    fig_congest.add_vline(x=congest_df["Order Concentration (%)"].mean(),
                          line_dash="dash", line_color=PALETTE["border"],
                          annotation_text="Avg Order Conc.")
    fig_congest.add_hline(y=congest_df["Revenue Share (%)"].mean(),
                          line_dash="dash", line_color=PALETTE["border"],
                          annotation_text="Avg Revenue Share")
    apply_theme(
        fig_congest, "📦 Order Congestion vs Revenue Share (size = profit, color = risk)")
    fig_congest.update_traces(
        mode="markers",
        marker=dict(opacity=0.85, line=dict(width=1, color="white")),
    )
    fig_congest.update_layout(height=500)
    st.plotly_chart(fig_congest, use_container_width=True)

    # Row 3 — Profit Share vs Revenue Share (over-dependency)
    fig_dep = px.bar(
        congest_df.sort_values("Profit Share (%)", ascending=False).head(15),
        x="State/Province",
        y=["Revenue Share (%)", "Profit Share (%)", "Order Concentration (%)"],
        barmode="group",
        color_discrete_sequence=[PALETTE["accent3"],
                                 PALETTE["accent4"], PALETTE["accent1"]],
    )
    fig_dep.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="outside",
        textfont=dict(size=11, color=PALETTE["text_main"]),
    )
    apply_theme(
        fig_dep, "📊 Revenue · Profit · Order Share by State (Top 15) — Over-Dependency View")
    fig_dep.update_layout(
        height=500,
        xaxis_tickangle=-35,
        yaxis=dict(range=[0, congest_df["Revenue Share (%)"].max() + 5]),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    st.plotly_chart(fig_dep, use_container_width=True)

    # Row 4 — Risk Detail Table
    st.markdown('<div class="section-header">📋 State Risk Classification Table</div>',
                unsafe_allow_html=True)
    risk_table = congest_df.sort_values("Risk Score", ascending=False)[[
        "State/Province", "Total_Sales", "Total_Profit", "Total_Orders",
        "Revenue Share (%)", "Profit Share (%)", "Order Concentration (%)",
        "Gross Margin (%)", "Divisions", "Risk Score", "Risk Flag"
    ]]
    st.dataframe(
        risk_table.style
        .format({
            "Total_Sales":              "${:,.0f}",
            "Total_Profit":             "${:,.0f}",
            "Revenue Share (%)":        "{:.2f}%",
            "Profit Share (%)":         "{:.2f}%",
            "Order Concentration (%)":  "{:.2f}%",
            "Gross Margin (%)":         "{:.1f}%",
        })
        .background_gradient(subset=["Risk Score"],          cmap="RdYlGn_r")
        .background_gradient(subset=["Revenue Share (%)"],   cmap="Reds")
        .background_gradient(subset=["Profit Share (%)"],    cmap="Oranges")
        .background_gradient(subset=["Gross Margin (%)"],    cmap="Greens"),
        use_container_width=True, height=420,
    )

    # Top & Bottom 5 states table side by side
    st.markdown('<div class="section-header">📋 Top & Bottom Performing States</div>',
                unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1:
        top5 = state_df.nlargest(5, "Total_Profit")[
            ["State/Province", "Total_Profit",
                "Gross Margin (%)", "Total_Orders", "Profit per Order"]
        ].reset_index(drop=True)
        top5.index += 1
        st.markdown("#### 🏆 Top 5 States by Profit")
        st.dataframe(
            top5.style
            .format({"Total_Profit": "${:,.0f}", "Gross Margin (%)": "{:.1f}%", "Profit per Order": "${:.2f}"})
            .background_gradient(subset=["Total_Profit"], cmap="Greens"),
            use_container_width=True,
        )
    with t2:
        bot5 = state_df.nsmallest(5, "Total_Profit")[
            ["State/Province", "Total_Profit",
                "Gross Margin (%)", "Total_Orders", "Profit per Order"]
        ].reset_index(drop=True)
        bot5.index += 1
        st.markdown("#### ⚠️ Bottom 5 States by Profit")
        st.dataframe(
            bot5.style
            .format({"Total_Profit": "${:,.0f}", "Gross Margin (%)": "{:.1f}%", "Profit per Order": "${:.2f}"})
            .background_gradient(subset=["Total_Profit"], cmap="Reds"),
            use_container_width=True,
        )


# ══════════════════════════════════════════════
# TAB 5 — TREND ANALYSIS
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">📅 Temporal Trend Analysis</div>',
                unsafe_allow_html=True)

    monthly = df.groupby("Month").agg(
        Revenue=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum"),
        Units=("Units", "sum"),
        Orders=("Order ID", "nunique"),
    ).reset_index()
    monthly["Gross Margin (%)"] = (monthly["Profit"] /
                                   monthly["Revenue"] * 100).round(2)

    # Revenue & Profit trend
    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Revenue"], name="Revenue",
        fill="tozeroy", fillcolor=f"rgba(132,204,22,0.15)",
        line=dict(color=PALETTE["accent3"], width=2.5),
        mode="lines+markers",
    ), secondary_y=False)
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Profit"], name="Gross Profit",
        fill="tozeroy", fillcolor=f"rgba(74,222,128,0.15)",
        line=dict(color=PALETTE["accent4"], width=2.5),
        mode="lines+markers",
    ), secondary_y=False)
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Gross Margin (%)"], name="Gross Margin %",
        line=dict(color=PALETTE["accent1"], width=2, dash="dot"),
        mode="lines+markers", marker=dict(size=6),
    ), secondary_y=True)
    apply_theme(fig_trend, "📈 Monthly Revenue, Profit & Margin Trend")
    fig_trend.update_layout(height=400)
    fig_trend.update_yaxes(title_text="$ Amount",
                           secondary_y=False, gridcolor=PALETTE["border"])
    fig_trend.update_yaxes(title_text="Gross Margin (%)",
                           secondary_y=True, gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_trend, use_container_width=True)

    c1t5, c2t5 = st.columns(2)

    with c1t5:
        # Division monthly trend
        div_monthly = df.groupby(["Month", "Division"])[
            "Gross Profit"].sum().reset_index()
        fig_div_trend = px.line(
            div_monthly, x="Month", y="Gross Profit", color="Division",
            color_discrete_map=DIVISION_COLORS, markers=True,
        )
        apply_theme(fig_div_trend, "🏭 Monthly Profit Trend by Division")
        fig_div_trend.update_layout(height=360)
        st.plotly_chart(fig_div_trend, use_container_width=True)

    with c2t5:
        # Margin heatmap: Month x Division
        margin_heat = df.groupby(["Month", "Division"])[
            "Gross Margin (%)"].mean().reset_index()
        margin_pivot = margin_heat.pivot(
            index="Division", columns="Month", values="Gross Margin (%)")
        margin_pivot.columns = [c.strftime("%b %Y")
                                for c in margin_pivot.columns]
        fig_mheat = px.imshow(
            margin_pivot, text_auto=".0f", aspect="auto",
            color_continuous_scale=["#EF4444", "#FACC15", "#4ADE80"],
        )
        apply_theme(fig_mheat, "📊 Monthly Margin Heatmap: Division × Month")
        fig_mheat.update_layout(height=360)
        st.plotly_chart(fig_mheat, use_container_width=True)

    # Quarterly KPI comparison
    st.markdown('<div class="section-header">📆 Quarterly Performance</div>',
                unsafe_allow_html=True)
    quarterly = df.groupby("Quarter").agg(
        Revenue=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
    ).reset_index()
    quarterly["Gross Margin (%)"] = (
        quarterly["Profit"] / quarterly["Revenue"] * 100).round(2)

    c3t5, c4t5 = st.columns(2)
    with c3t5:
        fig_q = px.bar(
            quarterly, x="Quarter", y=["Revenue", "Profit"],
            barmode="group",
            color_discrete_sequence=[PALETTE["accent3"], PALETTE["accent4"]],
            text_auto=".2s",
        )
        apply_theme(fig_q, "📦 Quarterly Revenue vs Profit")
        fig_q.update_layout(height=320)
        st.plotly_chart(fig_q, use_container_width=True)

    with c4t5:
        fig_qm = px.line(
            quarterly, x="Quarter", y="Gross Margin (%)",
            markers=True, text="Gross Margin (%)",
            color_discrete_sequence=[PALETTE["accent1"]],
        )
        fig_qm.update_traces(texttemplate="%{text:.1f}%", textposition="top center",
                             marker=dict(size=10, color=PALETTE["accent2"]),
                             fill="tozeroy", fillcolor=f"rgba(250,204,21,0.12)")
        apply_theme(fig_qm, "🎯 Gross Margin % by Quarter")
        fig_qm.update_layout(height=320)
        st.plotly_chart(fig_qm, use_container_width=True)

    # Top product monthly trends
    st.markdown('<div class="section-header">🌟 Top Products Monthly Revenue Trend</div>',
                unsafe_allow_html=True)
    top5_products = prod_df.nlargest(5, "Total_Sales")["Product Name"].tolist()
    prod_monthly = df[df["Product Name"].isin(top5_products)].groupby(
        ["Month", "Product Name"])["Sales"].sum().reset_index()
    fig_ptend = px.line(
        prod_monthly, x="Month", y="Sales", color="Product Name",
        markers=True,
        color_discrete_sequence=[PALETTE["accent1"], PALETTE["accent2"],
                                 PALETTE["accent3"], PALETTE["accent4"], PALETTE["accent5"]],
    )
    apply_theme(fig_ptend, "🌟 Top 5 Products — Monthly Revenue Trend")
    fig_ptend.update_layout(height=380)
    st.plotly_chart(fig_ptend, use_container_width=True)

    st.markdown('<div class="section-header">📋 Monthly Performance Summary Table</div>',
                unsafe_allow_html=True)
    summary_trend = df.groupby(["Month", "Division"]).agg(
        Revenue=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum"),
        Units=("Units", "sum"),
        Orders=("Order ID", "nunique"),
    ).reset_index()
    summary_trend["Gross Margin (%)"] = (
        summary_trend["Profit"] / summary_trend["Revenue"] * 100).round(2)
    summary_trend["Profit per Unit"] = (
        summary_trend["Profit"] / summary_trend["Units"]).round(2)
    summary_trend["Month"] = summary_trend["Month"].dt.strftime("%b %Y")
    st.dataframe(
        summary_trend.sort_values(["Month", "Division"]).style
        .format({
            "Revenue": "${:,.0f}", "Profit": "${:,.0f}", "Cost": "${:,.0f}",
            "Gross Margin (%)": "{:.1f}%", "Profit per Unit": "${:.2f}",
        })
        .background_gradient(subset=["Gross Margin (%)"], cmap="RdYlGn")
        .background_gradient(subset=["Profit"], cmap="Blues"),
        use_container_width=True, height=400,
    )


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; color:{PALETTE['text_muted']}; font-size:0.8rem; padding:12px 0;">
  🍬 Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor <br>
</div>
""", unsafe_allow_html=True)