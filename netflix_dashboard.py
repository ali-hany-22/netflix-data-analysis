import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Netflix Dashboard", page_icon="📺")

@st.cache_data  # Cache the data load for better performance
def load_data():
    try:
        # Load the Netflix dataset
        df = pd.read_csv('netflix_titles.csv')
        
        # Data cleaning
        df['country'] = df['country'].fillna('Unknown')
        df['rating'] = df['rating'].fillna('Not Rated')
        
        return df
    except FileNotFoundError:
        st.error("Error: Netflix data file not found. Please ensure 'netflix_titles.csv' is in the same folder.")
        return pd.DataFrame()  # Return empty DataFrame if file not found

# Load the data
df = load_data()

# Only proceed if data loaded successfully
if not df.empty:
    st.title("📺 Netflix Content Dashboard")
    st.markdown("Explore Netflix's movie and TV show collection")

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Type filter
    type_filter = st.sidebar.multiselect(
        "Select content type",
        options=df['type'].unique(),
        default=df['type'].unique()
    )
    
    # Country filter
    country_options = sorted(df['country'].unique())
    country_filter = st.sidebar.multiselect(
        "Select countries",
        options=country_options,
        default=['United States', 'India', 'United Kingdom', 'Unknown']
    )
    
    # Year range filter
    min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
    year_range = st.sidebar.slider(
        "Select release year range",
        min_year, max_year, (min_year, max_year)
    )

    # Apply filters
    df_filtered = df[
        (df['type'].isin(type_filter)) &
        (df['country'].isin(country_filter)) &
        (df['release_year'].between(year_range[0], year_range[1]))
    ]

    # Metrics row
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Titles", len(df_filtered))
    col2.metric("Countries Represented", df_filtered['country'].nunique())
    col3.metric("Content Ratings", df_filtered['rating'].nunique())

    # Visualizations
    st.subheader("Content Analysis")

    # Rating distribution
    fig1 = px.bar(
        df_filtered['rating'].value_counts().reset_index(),
        x='index', y='rating',
        title="Content by Rating",
        labels={'index': 'Rating', 'rating': 'Count'}
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Top countries
    top_countries = df_filtered['country'].value_counts().head(10).reset_index()
    fig2 = px.pie(
        top_countries,
        names='index', values='country',
        title="Top 10 Production Countries"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Releases by year
    fig3 = px.histogram(
        df_filtered,
        x='release_year',
        title="Content Releases by Year",
        nbins=max_year-min_year+1
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Raw data view
    if st.checkbox("Show raw data"):
        st.subheader("Filtered Data")
        st.dataframe(df_filtered)

else:
    st.warning("Please ensure the data file is available to load the dashboard.")
