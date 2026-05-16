# streamlit_app.py
import streamlit as st
import requests
import pandas as pd

st.title("🚀 ImaraFund - AI-Powered Grant Matching")

BASE_URL = "http://localhost:8000/api/v1"

# Company selection
companies = requests.get(f"{BASE_URL}/companies").json()
company_options = {f"{c['company_name']} ({c['nationality']})": c['id'] 
                  for c in companies}

selected_company = st.selectbox("Select Company:", list(company_options.keys()))

if st.button("Find Matching Grants"):
    company_id = company_options[selected_company]
    result = requests.post(f"{BASE_URL}/match/{company_id}?top_n=5").json()
    
    st.success(f"Found {result['total_matches_found']} matches!")
    
    for i, match in enumerate(result['matches'], 1):
        with st.expander(f"Match #{i}: {match['program_name']} ({match['match_score']}/100)"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Institution:** {match['institution']}")
                st.write(f"**Country:** {match['country']}")
                st.write(f"**Funding Amount:** ${match['funding_amount']:,}")
            with col2:
                breakdown = match['score_breakdown']
                st.write("**Score Breakdown:**")
                st.write(f"Geography: {breakdown['geographic']}/40")
                st.write(f"Sector: {breakdown['sector']}/30") 
                st.write(f"Funding: {breakdown['amount_fit']}/20")
                st.write(f"Stage: {breakdown['stage']}/10")
    
    if result.get('ai_recommendation'):
        st.markdown("### 🤖 AI Recommendation")
        st.markdown(result['ai_recommendation'])

# Run with: streamlit run streamlit_app.py
