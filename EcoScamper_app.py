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
    page_title="Eco-Scamper: A Sustainable Product Design Toolkit",
    page_icon="🛠️",
    layout="wide"
)

# --- Initialize Session State --- ## <-- NEW
# We use st.session_state to keep track of whether a search has been performed.
if 'searched' not in st.session_state:
    st.session_state.searched = False

# --- Data Loading and Caching ---
# Use st.cache_data to prevent reloading data on every interaction
@st.cache_data
def load_data():
    # In a real app, you would load your data from a file (e.g., pd.read_csv('your_data.csv'))
    # For this example, I'm recreating the data preparation steps from Step 0.
    file_path = "EcoScamper.csv" 
    df = pd.read_csv(file_path, encoding='latin-1')
    return df
    
# Load the data using our cached function
df = load_data()

# --- TOP HALF: Title and Search Filters ---

st.title("🛠️ Eco-Scamper: A Sustainable Product Design Toolkit")
# --- CUSTOM BUTTON STYLES --- ## <-- THIS IS THE NEW BLOCK
st.markdown("""
<style>
/* This is for the main "Search" button */
div.stButton > button[kind="primary"] {
    background-color: #007bff; /* A nice blue */
    color: white;
    border: 2px solid #007bff;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #0056b3; /* A darker blue on hover */
    border: 2px solid #0056b3;
}

/* This is for the "Clear" button */
div.stButton > button:not([kind="primary"]) {
    background-color: #28a745; /* A pleasant green */
    color: white;
    border: 2px solid #28a745;
}
div.stButton > button:not([kind="primary"]):hover {
    background-color: #1f7a33; /* A darker green on hover */
    border: 2px solid #1f7a33;
}
</style>""", unsafe_allow_html=True)
st.markdown("Use the filters below to find sustainable design inspirations from real-world case studies.")

# Check if the dataframe loaded successfully before proceeding
if df is not None:
    # Use a container for the filters for better layout
    with st.container():
        # Create columns for the filter widgets
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Get options from the new 'Category' column instead of 'Case'
            category_options = ['Any'] + sorted(df['Category'].unique().tolist()) ## <-- CHANGED
            selected_category = st.selectbox("Filter by Category:", options=category_options) ## <-- CHANGED

        with col2:
            # Tier 1 options are the keys of our hierarchy dictionary
            tier1_options = ['Any'] + sorted(list(STRATEGY_HIERARCHY.keys()))
            selected_tier1 = st.selectbox("Tier 1 Sustainability Strategy:", options=tier1_options)

        with col3:
            # Dynamic logic for Tier 2
            if selected_tier1 == 'Any':
                # If no Tier 1 is selected, show all unique Tier 2 strategies
                tier2_options = ['Any'] + sorted(df['Tier2_strategy'].unique().tolist())
            else:
                # If a Tier 1 is selected, get the sub-list from our dictionary
                tier2_options = ['Any'] + sorted(STRATEGY_HIERARCHY[selected_tier1])
            
            selected_tier2 = st.selectbox("Tier 2 Sustainability Strategy:", options=tier2_options)

        with col4:
            scamper_options = ['Any'] + sorted(df['SCAMPER_technique'].unique().tolist())
            selected_scamper = st.selectbox("SCAMPER Technique:", options=scamper_options)

    # --- Button Layout --- ## <-- CHANGED
    btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns([5, 3, 1, 3, 5])

    with btn_col2:
        search_button = st.button("Search for Design Inspirations", type="primary")

    with btn_col4:
        clear_button = st.button("Clear Results")

    # --- Update session state based on button clicks --- ## <-- NEW
    if search_button:
        st.session_state.searched = True

    if clear_button:
        st.session_state.searched = False

    st.divider()

    # --- BOTTOM HALF: Displaying Results ---

    # Only perform filtering and display results if the search button was clicked
    if st.session_state.searched: ## <-- CHANGED
        # Start with the full dataframe and apply filters sequentially
        filtered_df = df.copy()

        # Filter by the selected category instead of the selected case
        if selected_category != 'Any': ## <-- CHANGED
            filtered_df = filtered_df[filtered_df['Category'] == selected_category] ## <-- CHANGED
        if selected_tier1 != 'Any':
            filtered_df = filtered_df[filtered_df['Tier1_strategy'] == selected_tier1]
        if selected_tier2 != 'Any':
            filtered_df = filtered_df[filtered_df['Tier2_strategy'] == selected_tier2]
        if selected_scamper != 'Any':
            filtered_df = filtered_df[filtered_df['SCAMPER_technique'] == selected_scamper]

        # Display the results header
        st.header(f"Found {len(filtered_df)} Design Inspirations")

        if filtered_df.empty:
            st.warning("Congratulations! This is a new combination and no real-world implementations yet!")
        else:
            # Iterate over the filtered DataFrame and display each item as a card
            for index, row in filtered_df.iterrows():
                st.markdown("---") # Visual separator for cards

                # Card Header: Design Feature
                st.subheader(f"💡 {row['Design_feature']}")
                
                # Caption now includes both the Category and the Case Study for more context
                st.markdown(f"##### Category: **{row['Category']}** | Case Study: **{row['Case']}**") ## <-- CHANGED

                # Card Body using columns for a clean layout
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Sustainability Strategy:**")
                    st.markdown(f"*{row['Tier1_strategy']} > {row['Tier2_strategy']}*")
                    # JUSTIFICATION IS NOW DISPLAYED BY DEFAULT
                    st.info(f"**Justification:** {row['Sustainability_justification']}")

                with col2:
                    st.markdown(f"**Creativity Technique (SCAMPER):**")
                    st.markdown(f"*{row['SCAMPER_technique']}*")
                    # JUSTIFICATION IS NOW DISPLAYED BY DEFAULT
                    st.success(f"**Justification:** {row['Creativity_justification']}")
    else:
        # This is the default state before the user has clicked "Search"
        st.info("👆 Select your criteria above and click 'Search' to begin.")

else:
    # This message shows if df failed to load at all
    st.warning("Data could not be loaded. Please check the data file and refresh.")
                
