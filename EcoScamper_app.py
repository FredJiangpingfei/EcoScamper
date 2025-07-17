# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 10:08:46 2025

@author: jiang
"""

import streamlit as st
import pandas as pd
import json

# --- Page Configuration (Set this at the top) ---
st.set_page_config(
    page_title="Eco-Scamper: A Sustainable Product Design Toolkit",
    page_icon="🛠️",
    layout="wide"
)

# --- Data Loading and Caching ---
# Use st.cache_data to prevent reloading data on every interaction
@st.cache_data
def load_data():
    # In a real app, you would load your data from a file (e.g., pd.read_csv('your_data.csv'))
    # For this example, I'm recreating the data preparation steps from Step 0.
    file_path = "C:/Users/jiang/OneDrive - University of Exeter/RESEARCH/Python Scripts/EcoScamper.csv" 
    df = pd.read_csv(file_path, encoding='latin-1')
    return df
    
# Load the data using our cached function
df = load_data()

# --- TOP HALF: Title and Search Filters ---

st.title("🛠️ Eco-Scamper: A Sustainable Product Design Toolkit")
st.markdown("Use the filters below to find sustainable design inspirations from real-world case studies.")

# Check if the dataframe loaded successfully before proceeding
if df is not None:
    # Use a container for the filters for better layout
    with st.container():
        # Create columns for the filter widgets
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            case_options = ['Any'] + sorted(df['Case'].unique().tolist())
            selected_case = st.selectbox("Case Study:", options=case_options)

        with col2:
            tier1_options = ['Any'] + sorted(df['tier1_strategy'].unique().tolist())
            selected_tier1 = st.selectbox("Tier 1 Sustainable Strategy:", options=tier1_options)

        with col3:
            tier2_options = ['Any'] + sorted(df['tier2_strategy'].unique().tolist())
            selected_tier2 = st.selectbox("Tier 2 Sustainable Strategy:", options=tier2_options)

        with col4:
            scamper_options = ['Any'] + sorted(df['SCAMPER'].unique().tolist())
            selected_scamper = st.selectbox("SCAMPER Technique:", options=scamper_options)

    # The search button is now central to the interaction
    search_button = st.button("Search for Design Inspirations", type="primary")

    st.divider() # Visual separator between top and bottom halves

    # --- BOTTOM HALF: Displaying Results ---

    # Only perform filtering and display results if the search button was clicked
    if search_button:
        # Start with the full dataframe and apply filters sequentially
        filtered_df = df.copy()

        if selected_case != 'Any':
            filtered_df = filtered_df[filtered_df['Case'] == selected_case]
        if selected_tier1 != 'Any':
            filtered_df = filtered_df[filtered_df['tier1_strategy'] == selected_tier1]
        if selected_tier2 != 'Any':
            filtered_df = filtered_df[filtered_df['tier2_strategy'] == selected_tier2]
        if selected_scamper != 'Any':
            filtered_df = filtered_df[filtered_df['SCAMPER'] == selected_scamper]

        # Display the results header
        st.header(f"Found {len(filtered_df)} Design Inspirations")

        if filtered_df.empty:
            st.warning("Congratulations! This is a new combination and no real-world implementations yet!")
        else:
            # Iterate over the filtered DataFrame and display each item as a card
            for index, row in filtered_df.iterrows():
                st.markdown("---") # Visual separator for cards

                # Card Header: Design Feature and Case Study
                st.subheader(f"💡 {row['design_feature']}")
                st.markdown(f"##### From Case Study: **{row['Case']}**")

                # Card Body using columns for a clean layout
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Sustainability Strategy:**")
                    st.markdown(f"*{row['tier1_strategy']} > {row['tier2_strategy']}*")
                    # JUSTIFICATION IS NOW DISPLAYED BY DEFAULT
                    st.info(f"**Justification:** {row['Sustainability justification']}")

                with col2:
                    st.markdown(f"**Creativity Technique (SCAMPER):**")
                    st.markdown(f"*{row['SCAMPER']}*")
                    # JUSTIFICATION IS NOW DISPLAYED BY DEFAULT
                    st.success(f"**Justification:** {row['Creativity justification']}")
    else:
        # This is the default state before the user has clicked "Search"
        st.info("👆 Select your criteria above and click 'Search' to begin.")

else:
    # This message shows if df failed to load at all
    st.warning("Data could not be loaded. Please check the data file and refresh.")
                
                
