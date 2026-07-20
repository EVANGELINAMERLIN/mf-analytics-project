
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
import os

st.set_page_config(
    page_title="Bluestock MF Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  .stMetric {
    background:#1a1a2e;
    border:1px solid #4ECDC4;
    border-radius:10px;
    padding:10px;
  }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    db = os.path.join(
        os.path.dirname(__file__),
        "bluestock_mf.db")
    conn    = sqlite3.connect(db)
    df_nav  = pd.read_sql(
        "SELECT * FROM fact_nav", conn)
    df_fund = pd.read_sql(
        "SELECT * FROM dim_fund", conn)
    df_txn  = pd.read_sql(
        "SELECT * FROM fact_transactions", conn)
    df_aum  = pd.read_sql(
        "SELECT * FROM fact_aum", conn)
    conn.close()
    df_nav["date"] = pd.to_datetime(df_nav["date"])
    df_txn["transaction_date"] = pd.to_datetime(
        df_txn["transaction_date"])
    return df_nav, df_fund, df_txn, df_aum

df_nav, df_fund, df_txn, df_aum = load_data()

nav_pivot = df_nav.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
).sort_index()
daily_returns = nav_pivot.pct_change().dropna()

# ── Sidebar ────────────────────────────────────────────
st.sidebar.title("Bluestock MF Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Overview",
     "NAV & Performance",
     "Investor Analytics",
     "Fund Recommender"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filters**")

houses = ["All"] + sorted(
    df_fund["fund_house"].unique().tolist())
sel_house = st.sidebar.selectbox(
    "Fund House", houses)

cats = ["All"] + sorted(
    df_fund["category"].unique().tolist())
sel_cat = st.sidebar.selectbox(
    "Category", cats)

risks = ["All"] + sorted(
    df_fund["risk_category"].unique().tolist())
sel_risk = st.sidebar.selectbox(
    "Risk Category", risks)

df_filt = df_fund.copy()
if sel_house != "All":
    df_filt = df_filt[
        df_filt["fund_house"]==sel_house]
if sel_cat != "All":
    df_filt = df_filt[
        df_filt["category"]==sel_cat]
if sel_risk != "All":
    df_filt = df_filt[
        df_filt["risk_category"]==sel_risk]

# ══════════════════════════════════════════════════════
if page == "Overview":
    st.title("📊 Bluestock MF Analytics Dashboard")
    st.markdown("---")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total AUM",
        f"Rs.{df_aum['aum_crores'].sum()/1e5:.1f}L Cr")
    c2.metric("Transactions", f"{len(df_txn):,}")
    c3.metric("SIP Amount",
        f"Rs.{df_txn[df_txn['transaction_type'].str.upper()=='SIP']['amount_inr'].sum()/1e7:.1f} Cr")
    c4.metric("Investors",
        f"{df_txn['investor_id'].nunique():,}")
    c5.metric("Schemes", f"{len(df_fund)}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("AUM by Fund House")
        aum_h = df_aum.groupby("fund_house")[
            "aum_crores"].sum().sort_values(
            ascending=False).reset_index()
        fig = px.bar(
            aum_h, x="aum_crores",
            y="fund_house",
            orientation="h",
            color="aum_crores",
            color_continuous_scale="Viridis")
        fig.update_layout(
            template="plotly_dark", height=400)
        st.plotly_chart(
            fig, use_container_width=True)

    with col2:
        st.subheader("Category Split")
        cat_d = df_fund["category"].value_counts()
        fig = px.pie(
            values=cat_d.values,
            names=cat_d.index,
            hole=0.45)
        fig.update_layout(
            template="plotly_dark", height=400)
        st.plotly_chart(
            fig, use_container_width=True)

    st.subheader("Monthly Transactions")
    df_txn["month"] = df_txn[
        "transaction_date"
    ].dt.to_period("M").astype(str)
    monthly = df_txn.groupby(
        ["month","transaction_type"]
    )["amount_inr"].sum().reset_index()
    fig = px.line(
        monthly, x="month",
        y="amount_inr",
        color="transaction_type")
    fig.update_layout(
        template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════
elif page == "NAV & Performance":
    st.title("📈 NAV & Performance")
    st.markdown("---")

    sel_codes = st.multiselect(
        "Select Funds",
        options=df_fund["amfi_code"].tolist(),
        default=df_fund["amfi_code"].tolist()[:5],
        format_func=lambda x:
            df_fund[df_fund["amfi_code"]==x
            ]["scheme_name"].values[0][:40]
            if len(df_fund[
                df_fund["amfi_code"]==x]) > 0
            else str(x)
    )

    period = st.select_slider(
        "Time Period",
        options=["1 Year","2 Years",
                 "3 Years","All"],
        value="3 Years"
    )
    yrs = {"1 Year":1,"2 Years":2,
           "3 Years":3,"All":10}[period]

    if sel_codes:
        fig   = go.Figure()
        cols  = px.colors.qualitative.Plotly
        for i, code in enumerate(sel_codes[:10]):
            if code not in nav_pivot.columns:
                continue
            s = nav_pivot[code].dropna()
            c = s.index.max() -                 pd.DateOffset(years=yrs)
            s = s[s.index >= c]
            if len(s) == 0:
                continue
            norm = s / s.iloc[0] * 100
            name = df_fund[
                df_fund["amfi_code"]==code
            ]["scheme_name"].values[0][:30]
            fig.add_trace(go.Scatter(
                x=norm.index, y=norm.values,
                mode="lines", name=name,
                line=dict(
                    color=cols[i%len(cols)],
                    width=2)
            ))
        fig.update_layout(
            title="NAV (Normalized to 100)",
            template="plotly_dark",
            height=500,
            hovermode="x unified")
        st.plotly_chart(
            fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        risk_d = df_filt["risk_category"
                         ].value_counts()
        fig = px.pie(
            values=risk_d.values,
            names=risk_d.index,
            hole=0.4,
            title="Risk Distribution")
        fig.update_layout(
            template="plotly_dark", height=350)
        st.plotly_chart(
            fig, use_container_width=True)
    with col2:
        fig = px.histogram(
            df_filt,
            x="expense_ratio_pct",
            nbins=20,
            title="Expense Ratio Distribution")
        fig.update_layout(
            template="plotly_dark", height=350)
        st.plotly_chart(
            fig, use_container_width=True)

    st.subheader("Fund Details")
    st.dataframe(
        df_filt[[
            "scheme_name","fund_house",
            "category","risk_category",
            "expense_ratio_pct",
            "min_sip_amount"
        ]].reset_index(drop=True),
        use_container_width=True)

# ══════════════════════════════════════════════════════
elif page == "Investor Analytics":
    st.title("👥 Investor Analytics")
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    sip = df_txn[
        df_txn["transaction_type"
               ].str.upper()=="SIP"]
    c1.metric("Investors",
        f"{df_txn['investor_id'].nunique():,}")
    c2.metric("SIP Txns", f"{len(sip):,}")
    c3.metric("Avg SIP",
        f"Rs.{sip['amount_inr'].mean():,.0f}")
    c4.metric("States",
        f"{df_txn['state'].nunique()}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        age_d = df_txn.drop_duplicates(
            "investor_id"
        )["age_group"].value_counts()
        fig = px.pie(
            values=age_d.values,
            names=age_d.index,
            hole=0.4,
            title="Age Group Distribution")
        fig.update_layout(
            template="plotly_dark", height=380)
        st.plotly_chart(
            fig, use_container_width=True)

    with col2:
        gen_d = df_txn.drop_duplicates(
            "investor_id"
        )["gender"].value_counts()
        fig = px.pie(
            values=gen_d.values,
            names=gen_d.index,
            hole=0.4,
            title="Gender Split",
            color_discrete_sequence=[
                "#FF6B9D","#4ECDC4"])
        fig.update_layout(
            template="plotly_dark", height=380)
        st.plotly_chart(
            fig, use_container_width=True)

    st.subheader("SIP by State")
    state_s = sip.groupby("state")[
        "amount_inr"].sum().sort_values(
        ascending=True).reset_index()
    fig = px.bar(
        state_s,
        x="amount_inr", y="state",
        orientation="h",
        color="amount_inr",
        color_continuous_scale="Viridis")
    fig.update_layout(
        template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        tier = df_txn["city_tier"].value_counts()
        fig  = px.pie(
            values=tier.values,
            names=tier.index,
            hole=0.4,
            title="T30 vs B30 City Tier",
            color_discrete_sequence=[
                "#FF6B6B","#4ECDC4"])
        fig.update_layout(
            template="plotly_dark", height=350)
        st.plotly_chart(
            fig, use_container_width=True)
    with col2:
        pay = df_txn["payment_mode"
                     ].value_counts()
        fig = px.bar(
            x=pay.index, y=pay.values,
            color=pay.values,
            color_continuous_scale="Blues",
            title="Payment Mode")
        fig.update_layout(
            template="plotly_dark", height=350)
        st.plotly_chart(
            fig, use_container_width=True)

# ══════════════════════════════════════════════════════
elif page == "Fund Recommender":
    st.title("🤖 Smart Fund Recommender")
    st.markdown("---")

    col1,col2,col3 = st.columns(3)
    with col1:
        risk_inp = st.selectbox(
            "Risk Appetite",
            ["Low","Moderate","High"])
    with col2:
        min_amt = st.number_input(
            "Min SIP (Rs.)",
            min_value=100,
            max_value=10000,
            value=500, step=100)
    with col3:
        max_exp = st.slider(
            "Max Expense Ratio (%)",
            0.1, 2.5, 1.5, 0.1)

    if st.button("Get Recommendations 🚀"):
        risk_map = {
            "Low"     :["Low","Moderately Low"],
            "Moderate":["Moderate",
                        "Moderately High"],
            "High"    :["High","Very High"],
        }
        RF_DAILY = 0.065 / 252
        rows = []
        for code in daily_returns.columns:
            ret = daily_returns[code].dropna()
            if len(ret) < 30:
                continue
            sharpe = (
                (ret-RF_DAILY).mean()/ret.std()
            ) * np.sqrt(252)
            info = df_fund[
                df_fund["amfi_code"]==code]
            if len(info) == 0:
                continue
            rows.append({
                "amfi_code"    : code,
                "scheme_name"  : info["scheme_name"].values[0],
                "fund_house"   : info["fund_house"].values[0],
                "category"     : info["category"].values[0],
                "risk_category": info["risk_category"].values[0],
                "expense_ratio": info["expense_ratio_pct"].values[0],
                "min_sip"      : info["min_sip_amount"].values[0],
                "sharpe_ratio" : round(sharpe,4),
            })
        df_rec = pd.DataFrame(rows)
        matched = risk_map.get(
            risk_inp, ["Moderate"])
        result = df_rec[
            (df_rec["risk_category"].isin(
                matched)) &
            (df_rec["expense_ratio"]<=max_exp) &
            (df_rec["min_sip"]<=min_amt)
        ].sort_values(
            "sharpe_ratio",
            ascending=False).head(3)

        if len(result) == 0:
            result = df_rec.sort_values(
                "sharpe_ratio",
                ascending=False).head(3)
            st.warning(
                "No exact match — top funds shown!")

        st.success(
            f"Top 3 for {risk_inp} Risk!")

        for i,(_, row) in enumerate(
                result.iterrows(), 1):
            with st.expander(
                    f"#{i} {row['scheme_name'][:50]}"):
                a,b,c,d = st.columns(4)
                a.metric("Sharpe",
                    f"{row['sharpe_ratio']:.2f}")
                b.metric("Expense",
                    f"{row['expense_ratio']:.2f}%")
                c.metric("Risk",
                    row["risk_category"])
                d.metric("Min SIP",
                    f"Rs.{row['min_sip']:,.0f}")

        st.subheader("Comparison")
        st.dataframe(
            result[[
                "scheme_name","fund_house",
                "risk_category","sharpe_ratio",
                "expense_ratio","min_sip"
            ]].reset_index(drop=True),
            use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Built by MERLIN J | Teyzix Core 2026")
