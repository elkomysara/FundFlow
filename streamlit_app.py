"""
FundFlow - Grant Matching Platform
Ultra-Simple Frontend | Direct CSV Reader | No Gemini | No Advice
Run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import os

# ─────────────────────────────────────────────
# CONFIG & FILE PATHS
# ─────────────────────────────────────────────
GRANTS_CSV = r"C:\Users\komy2\Downloads\Projects\FundFlow\data\grants_cleaned_latest.csv"
COMPANIES_CSV = r"C:\Users\komy2\Downloads\Projects\FundFlow\data\synthetic_companies.csv"

st.set_page_config(page_title="FundFlow", page_icon="💸", layout="wide")

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
@st.cache_data
def load_local_data():
    """Reads the CSV files directly from your hard drive."""
    grants = pd.read_csv(GRANTS_CSV) if os.path.exists(GRANTS_CSV) else pd.DataFrame()
    companies = pd.read_csv(COMPANIES_CSV) if os.path.exists(COMPANIES_CSV) else pd.DataFrame()
    return grants, companies

def fmt_usd(v):
    if pd.isna(v) or v is None:
        return "N/A"
    v = float(v)
    if v >= 1_000_000: return f"${v/1_000_000:.1f}M"
    if v >= 1_000: return f"${v/1_000:.0f}K"
    return f"${v:,.0f}"

# Load data immediately
df_grants, df_companies = load_local_data()

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💸 FundFlow")
    st.caption("Grant Matching for African SMEs")
    st.divider()
    page = st.radio("Navigate", ["🔍 Find Grants", "📋 Browse Grants"])
    st.divider()
    st.markdown(f"""
**Local Database Status**
- 🌍 Grants Loaded: **{len(df_grants)}**
- 🏢 Companies Loaded: **{len(df_companies)}**
    """)

st.title("💸 FundFlow")
st.caption("Simplified direct-data grant matching engine")
st.divider()

# ═══════════════════════════════════════════════
# PAGE 1: FIND GRANTS (THE MATCHING ALGORITHM)
# ═══════════════════════════════════════════════
if page == "🔍 Find Grants":
    if df_companies.empty or df_grants.empty:
        st.error("Missing CSV data files. Please check your file paths.")
        st.stop()

    # Create a clean dropdown list for selection
    company_options = [
        f"{row['company_name']} ({row.get('nationality', 'Unknown')} · {row['sector']})"
        for _, row in df_companies.iterrows()
    ]
    
    col1, col2 = st.columns([4, 1])
    with col1:
        selected_option = st.selectbox("Select a Company to Match:", company_options)
    with col2:
        top_n = st.selectbox("Top Results", [3, 5, 10], index=1)

    # Find the chosen company data row
    selected_index = company_options.index(selected_option)
    company = df_companies.iloc[selected_index]

    # Calculate match scores directly using basic logic (No Backend/AI needed!)
    with st.spinner("Calculating matching criteria..."):
        matches = []
        for _, grant in df_grants.iterrows():
            geo_score = 40 if str(company.get('nationality')).lower() in str(grant.get('country')).lower() or str(grant.get('country')).lower() == 'all' else 10
            sector_score = 30 if str(company.get('sector')).lower() in str(grant.get('target_sectors')).lower() else 5
            
            # Simple total calculation
            total_score = geo_score + sector_score + 20 # adding default base fitting points
            
            matches.append({
                "program_name": grant.get("program_name"),
                "institution": grant.get("institution") or grant.get("institution_name"),
                "country": grant.get("country"),
                "funding_amount": grant.get("funding_amount") or grant.get("estimated_value_amount"),
                "sectors": grant.get("target_sectors"),
                "repayment": grant.get("repayment_required"),
                "score": total_score
            })
        
        # Sort results by highest score
        sorted_matches = sorted(matches, key=lambda x: x['score'], reverse=True)[:top_n]

    # Display match metrics summary
    m1, m2 = st.columns(2)
    m1.metric("Highest Match Found", f"{sorted_matches[0]['score']} / 100")
    m2.metric("Total Opportunities Screened", len(df_grants))

    st.subheader("Top Matching Recommendations")
    for i, m in enumerate(sorted_matches, 1):
        with st.container(border=True):
            left, right = st.columns([5, 1])
            with left:
                st.markdown(f"#### 🟢 #{i} — {m['program_name']}")
                st.caption(f"🏦 {m['institution']}  ·  🌍 {m['country']}  ·  💰 {fmt_usd(m['funding_amount'])}")
                st.write(f"**Targeted Sectors:** {m['sectors']}")
            with right:
                st.metric("Match Fit", f"{m['score']}/100")

# ═══════════════════════════════════════════════
# PAGE 2: BROWSE GRANTS
# ═══════════════════════════════════════════════
elif page == "📋 Browse Grants":
    st.subheader("📋 Complete Grant Database")
    
    if df_grants.empty:
        st.warning("No grant records found.")
        st.stop()

    # Search filter bar
    search = st.text_input("🔍 Quick Search Catalog", placeholder="Type a sector, country, or program name...")
    filtered_df = df_grants.copy()
    
    if search.strip():
        s = search.strip()
        mask = (
            filtered_df["program_name"].astype(str).str.contains(s, case=False, na=False) |
            filtered_df.get("target_sectors", pd.Series(dtype=str)).astype(str).str.contains(s, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    st.dataframe(filtered_df, use_container_width=True, height=450)