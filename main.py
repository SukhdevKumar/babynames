import streamlit as st
import pandas as pd
from datetime import datetime
from utils.zodiac import get_zodiac_sign, get_zodiac_symbol
from utils.name_data import filter_names, paginate_names

# Page configuration
st.set_page_config(
    page_title="NewbornNameIdeas.com - Baby Name Generator",
    page_icon="👶",
    layout="wide"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if 'filtered_names' not in st.session_state:
    st.session_state.filtered_names = []

# Header
st.markdown("""
    <div class="main-title">
        👶 NewbornNameIdeas.com
        <br>
        <small>Find the Perfect Name for Your Little One</small>
    </div>
""", unsafe_allow_html=True)

# Create two columns for the filters
col1, col2 = st.columns(2)

with col1:
    # Basic filters
    gender = st.selectbox(
        "Gender",
        ["All", "Male", "Female", "Neutral"]
    )

    region = st.selectbox(
        "Region",
        ["All", "European", "North American", "South American", "East Asian", 
         "South Asian", "Southeast Asian", "Middle Eastern", "African", 
         "Mediterranean", "Nordic", "Celtic", "Slavic", "Pacific Islander"]
    )

    # First letter filter
    starts_with = st.selectbox(
        "Starts with letter",
        ["All"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    )

with col2:
    # Additional filters
    language = st.selectbox(
        "Language",
        ["All", "English", "Spanish", "French", "German", "Italian", "Portuguese",
         "Russian", "Mandarin", "Japanese", "Korean", "Hindi", "Arabic", "Hebrew",
         "Greek", "Turkish", "Vietnamese", "Thai", "Swedish", "Danish", "Norwegian",
         "Polish", "Czech", "Irish", "Welsh", "Sanskrit"]
    )

    # Date of birth selector
    dob = st.date_input(
        "Select Date of Birth",
        min_value=datetime.now().date(),
        max_value=datetime(datetime.now().year + 1, 12, 31).date()
    )

# Search box
search_term = st.text_input("🔍 Search names, meanings, or origins", 
                           help="Enter any part of the name, its meaning, or origin")

# Submit button
if st.button("✨ Show my baby's name!", type="primary"):
    # Calculate zodiac sign
    zodiac_sign = get_zodiac_sign(dob)
    zodiac_symbol = get_zodiac_symbol(zodiac_sign)

    # Display zodiac information
    st.markdown(f"""
        <div class="zodiac-symbol">
            <h2>{zodiac_symbol}</h2>
            <p>Your baby's zodiac sign will be: {zodiac_sign}</p>
        </div>
    """, unsafe_allow_html=True)

    # Apply filters
    st.session_state.filtered_names = filter_names(
        gender=None if gender == "All" else gender,
        region=None if region == "All" else region,
        language=None if language == "All" else language,
        search_term=search_term if search_term else None,
        starts_with=None if starts_with == "All" else starts_with
    )
    st.session_state.page_number = 1  # Reset to first page on new search

# Names per page
names_per_page = 20

# If we have filtered names in session state, display them
if st.session_state.filtered_names:
    paginated_names, total_names = paginate_names(st.session_state.filtered_names, st.session_state.page_number, names_per_page)

    # Display results
    st.markdown(f"### Found {total_names} names matching your criteria")

    # Display names in a grid
    col1, col2 = st.columns(2)
    for idx, name in enumerate(paginated_names):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
                <div class="name-card">
                    <h3>{name['name']}</h3>
                    <p><strong>Origin:</strong> {name['origin']}</p>
                    <p><strong>Meaning:</strong> {name['meaning']}</p>
                </div>
            """, unsafe_allow_html=True)

    # Pagination controls
    total_pages = (total_names + names_per_page - 1) // names_per_page

    # Create columns for pagination controls
    prev_col, page_info_col, next_col = st.columns([1, 2, 1])

    with prev_col:
        if st.session_state.page_number > 1:
            if st.button("⬅️ Previous"):
                st.session_state.page_number -= 1
                st.rerun()

    with page_info_col:
        st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_number} of {total_pages}</div>", unsafe_allow_html=True)

    with next_col:
        if st.session_state.page_number < total_pages:
            if st.button("Next ➡️"):
                st.session_state.page_number += 1
                st.rerun()

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #FFF5F5; border-radius: 0.5rem;">
        <p>© 2024 NewbornNameIdeas.com - Helping parents find perfect names for their little ones</p>
    </div>
""", unsafe_allow_html=True)