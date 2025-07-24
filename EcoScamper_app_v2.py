# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 10:08:46 2025

@author: jiang
"""

import streamlit as st
import pandas as pd
import json

# --- HIERARCHY DATA ---
# This dictionary defines the relationship between Tier 1 and Tier 2 strategies.
STRATEGY_HIERARCHY = {
    "Dematerialization": [
        "Content reduction",
        "Design for value",
        "Digitisation",
        "Weight reduction",
        "Minimal material and packaging",
        "Generative design"
    ],
    "Next-Best Material Selection": [
        "Renewable and biodegradable material",
        "Recycled material",
        "Recyclable material",
        "Lightweight material"
    ],
    "Green Supply Chain": [
        "Frugal processes and operations",
        "Detoxified processes",
        "Standardisation and modularity",
        "Design for logistics"
    ],
    "Longevity and Effective Usage": [
        "Design for repairability and maintenance",
        "Design for upgradability and adaptability",
        "Design to last",
        "Design for remanufacturing",
        "Design for multiple uses"
    ],
    "Product efficiency": [
        "Variable energy consumption",
        "Energy consumption efficiency",
        "Material consumption efficiency",
        "Change consumer behavior"
    ],
    "Circularity": [
        "Design for disassembly",
        "Design for end-of-life collection",
        "Design for reuse",
        "Enable material traceability",
        "Enable material homogeneity"
    ]
}


# --- Page Configuration (Set this at the top) ---
st.set_page_config(
    page_title="Eco-SCAMPER: A Sustainable Product Design Toolkit",
    page_icon="🛠️",
    layout="wide"
)

# --- Initialize Session State ---
if 'searched' not in st.session_state:
    st.session_state.searched = False

# --- Data Loading and Caching ---
@st.cache_data
def load_data():
    # IMPORTANT: Remember to change this to a relative path for deployment on Streamlit Cloud
    file_path = "EcoScamper.csv" 
    df = pd.read_csv(file_path, encoding='latin-1')
    # Fill any empty cells in the 'Link' column with an empty string to prevent errors
    if 'Link' in df.columns:
        df['Link'] = df['Link'].fillna('')
    return df
    
# Load the data using our cached function
df = load_data()

# --- SIDEBAR FOR FILTERS --- ## <-- CHANGED: Filters moved to sidebar for responsiveness
st.sidebar.header("Filter Options")

# Check if the dataframe loaded successfully before proceeding
if df is not None:
    category_options = ['Any'] + sorted(df['Category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Filter by Product Category:", options=category_options)

    tier1_options = ['Any'] + sorted(list(STRATEGY_HIERARCHY.keys()))
    selected_tier1 = st.sidebar.selectbox("Tier 1 Sustainability Strategy:", options=tier1_options)

    if selected_tier1 == 'Any':
        tier2_options = ['Any'] + sorted(df['Tier2_strategy'].unique().tolist())
    else:
        tier2_options = ['Any'] + sorted(STRATEGY_HIERARCHY[selected_tier1])
    selected_tier2 = st.sidebar.selectbox("Tier 2 Sustainability Strategy:", options=tier2_options)

    scamper_options = ['Any'] + sorted(df['SCAMPER_technique'].unique().tolist())
    selected_scamper = st.sidebar.selectbox("SCAMPER Technique:", options=scamper_options)


# --- MAIN PAGE LAYOUT ---
st.title("🛠️ Eco-SCAMPER: A Sustainable Product Design Toolkit")
# --- CUSTOM BUTTON STYLES ---
st.markdown("""
<style>
/* ... (your existing button styles remain here, no changes needed) ... */
div.stButton > button[kind="primary"] { background-color: #007bff; color: white; border: 2px solid #007bff; }
div.stButton > button[kind="primary"]:hover { background-color: #0056b3; border: 2px solid #0056b3; }
div.stButton > button:not([kind="primary"]) { background-color: #28a745; color: white; border: 2px solid #28a745; }
div.stButton > button:not([kind="primary"]):hover { background-color: #1f7a33; border: 2px solid #1f7a33; }
</style>""", unsafe_allow_html=True)
st.markdown("Use the filters in the sidebar to find sustainable design inspirations from real-world case studies.")


if df is not None:
    # --- Centered Button Layout ---
    btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns([5, 3, 1, 3, 5])

    with btn_col2:
        search_button = st.button("Search for Design Inspirations", type="primary")

    with btn_col4:
        clear_button = st.button("Clear Results")

    # --- Update session state based on button clicks ---
    if search_button:
        st.session_state.searched = True

    if clear_button:
        st.session_state.searched = False

    st.divider()

    # --- BOTTOM HALF: Displaying Results ---
    if st.session_state.searched:
        # Start with the full dataframe and apply filters sequentially
        filtered_df = df.copy()

        if selected_category != 'Any':
            filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        if selected_tier1 != 'Any':
            filtered_df = filtered_df[filtered_df['Tier1_strategy'] == selected_tier1]
        if selected_tier2 != 'Any':
            filtered_df = filtered_df[filtered_df['Tier2_strategy'] == selected_tier2]
        if selected_scamper != 'Any':
            filtered_df = filtered_df[filtered_df['SCAMPER_technique'] == selected_scamper]

        st.header(f"Found {len(filtered_df)} Design Inspirations")

        if filtered_df.empty:
            st.warning("Congratulations! This is a new combination and no real-world implementations yet!")
        else:
            for index, row in filtered_df.iterrows():
                st.markdown("---")
                st.subheader(f"💡 {row['Design_feature']}")
                
                # --- CORRECTED: Logic for creating a clickable hyperlink ---
                case_name = row['Case']
                case_link = row.get('Link', '') # Safely get the link

                # Default to just bold text
                case_display_html = f"<strong>{case_name}</strong>"

                # If a valid link exists, create an HTML hyperlink instead
                if pd.notna(case_link) and case_link.strip():
                    # target="_blank" opens the link in a new tab
                    case_display_html = f'<a href="{case_link}" target="_blank" style="text-decoration: none;"><strong>{case_name}</strong></a>'
                
                # Use st.markdown with unsafe_allow_html to render the raw HTML
                st.markdown(f"##### Category: **{row['Category']}** | Case Study: {case_display_html}", unsafe_allow_html=True)

                # Card Body using columns for a clean layout
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Sustainability Strategy:**")
                    st.markdown(f"*{row['Tier1_strategy']} > {row['Tier2_strategy']}*")
                    st.info(f"**Justification:** {row['Sustainability_justification']}")
                with col2:
                    st.markdown(f"**Creativity Technique (SCAMPER):**")
                    st.markdown(f"*{row['SCAMPER_technique']}*")
                    st.success(f"**Justification:** {row['Creativity_justification']}")
    else:
        st.info("ℹ️ Use the filters in the sidebar and click 'Search' to begin.")

else:
    st.warning("Data could not be loaded. Please check the data file and refresh.")
