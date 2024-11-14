import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

# Load Walmart store openings dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv"
    df = pd.read_csv(url)
    
    # Ensure the YEAR column is correctly treated as a numerical value
    df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')  # Coerce any errors if present
    
    return df

# Build Streamlit app
def main():
    # Title and description of the app
    st.title('Walmart Store Openings Dashboard (1962-2006)')
    st.markdown("""
        This dashboard visualizes the locations and number of Walmart store openings across the United States from **1962** to **2006**.
        The first plot shows the number of stores opened by year, and the second plot shows the top 5 cities with the most Walmart stores by the end of 2006.
    """)
    
    # Load and display the dataset
    df = load_data()
    
    # --- Section 1: Number of Stores Opened by Year (Line Chart) ---
    st.subheader('Number of Walmart Stores Opened by Year')
    
    # Group the data by 'YEAR' and 'type_store' and count the number of stores opened each year
    store_count_by_year_and_type = df.groupby(['YEAR', 'type_store']).size().reset_index(name='Store Count')
    
    # Create a line chart using Altair, with lines split by 'type_store'
    line_chart = alt.Chart(store_count_by_year_and_type).mark_line().encode(
        x='YEAR:O',  # Treat YEAR as an ordinal (discrete) variable
        y='Store Count:Q',  # Count of stores
        color='type_store:N',  # Different lines for different store types
        tooltip=['YEAR', 'Store Count', 'type_store']
    )
    
    st.altair_chart(line_chart, use_container_width=True)
    
    # --- Section 2: Top 5 Cities with the Most Walmart Stores by End of 2006 (Bar Plot) ---
    st.subheader('Top 5 Cities with the Most Walmart Stores by End of 2006')
    
    # Filter the data to include only stores opened by the end of 2006
    df_2006 = df[df['YEAR'] <= 2006]
    
    # Group the data by 'STRCITY' and count the number of stores in each city
    city_store_count = df_2006.groupby('STRCITY').size().reset_index(name='Store Count')
    
    # Sort the cities by the number of stores and take the top 5
    top_cities = city_store_count.sort_values(by='Store Count', ascending=False).head(5)
    
    # Create a bar chart using Altair
    # Create a bar chart using Altair
    bar_chart = alt.Chart(top_cities).mark_bar().encode(
            x=alt.X('Store Count:Q', axis=alt.Axis(format='d')),  # Show integers on the x-axis
            y=alt.Y('STRCITY:N', sort='-x'),  # Sort by store count in descending order
            tooltip=['STRCITY', 'Store Count']
        )
    
    st.altair_chart(bar_chart, use_container_width=True)

# Run the app
if __name__ == '__main__':
    main()
