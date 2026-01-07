import streamlit as st
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import st_folium

def show(df):
    st.title("🗺️ India Risk Map Analysis")
    st.write("Geospatial distribution of traffic violations across Indian states.")

    if df.empty:
        st.warning("No data available to display maps.")
        return

    # Aggregate data by State (Location)
    state_stats = df.groupby('Location').agg(
        Total_Violations=('Violation_ID', 'count'),
        Total_Fines=('Fine_Amount', 'sum'),
        Avg_Fine=('Fine_Amount', 'mean')
    ).reset_index()
    
    indian_states_coords = {
        "Andhra Pradesh": [15.9129, 79.7400],
        "Arunachal Pradesh": [28.2180, 94.7278],
        "Assam": [26.2006, 92.9376],
        "Bihar": [25.0961, 85.3131],
        "Chhattisgarh": [21.2787, 81.8661],
        "Goa": [15.2993, 74.1240],
        "Gujarat": [22.2587, 71.1924],
        "Haryana": [29.0588, 76.0856],
        "Himachal Pradesh": [31.1048, 77.1734],
        "Jharkhand": [23.6102, 85.2799],
        "Karnataka": [15.3173, 75.7139],
        "Kerala": [10.8505, 76.2711],
        "Madhya Pradesh": [22.9734, 78.6569],
        "Maharashtra": [19.7515, 75.7139],
        "Manipur": [24.6637, 93.9063],
        "Meghalaya": [25.4670, 91.3662],
        "Mizoram": [23.1645, 92.9376],
        "Nagaland": [26.1584, 94.5624],
        "Odisha": [20.9517, 85.0985],
        "Punjab": [31.1471, 75.3412],
        "Rajasthan": [27.0238, 74.2179],
        "Sikkim": [27.5330, 88.5122],
        "Tamil Nadu": [11.1271, 78.6569],
        "Telangana": [18.1124, 79.0193],
        "Tripura": [23.9408, 91.9882],
        "Uttar Pradesh": [26.8467, 80.9462],
        "Uttarakhand": [30.0668, 79.0193],
        "West Bengal": [22.9868, 87.8550],
        "Delhi": [28.7041, 77.1025]
    }

    state_stats['lat'] = state_stats['Location'].map(lambda x: indian_states_coords.get(x, [None, None])[0])
    state_stats['lon'] = state_stats['Location'].map(lambda x: indian_states_coords.get(x, [None, None])[1])
    
    # Filter out locations we couldn't map
    map_data = state_stats.dropna(subset=['lat', 'lon'])

    # --- Folium Map ---
    st.subheader("Geospatial View (Folium)")
    if not map_data.empty:
        # Center map on India
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=4, tiles="CartoDB dark_matter")
        
        for _, row in map_data.iterrows():
            # Add markers
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=row['Total_Violations'] * 0.05, # Scale radius or use log
                popup=f"{row['Location']}: {row['Total_Violations']} Violations",
                color="#ff4b4b",
                fill=True,
                fill_color="#ff4b4b"
            ).add_to(m)
            
        st_folium(m, width=700, height=500, use_container_width=True)
    else:
        st.write("Map data unavailable.")

    if not map_data.empty:
        st.subheader("Interactive Risk Map (Plotly)")
        fig = px.scatter_mapbox(
            map_data, 
            lat="lat", 
            lon="lon", 
            size="Total_Violations", 
            color="Avg_Fine",
            hover_name="Location", 
            hover_data=["Total_Fines", "Total_Violations"],
            color_continuous_scale=px.colors.sequential.Plasma,
            size_max=50, 
            zoom=3.5, 
            mapbox_style="carto-darkmatter",
            title="Violation Hotspots"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Could not map state names to coordinates. Showing stats instead.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk by State (Treemap)")
        fig_tree = px.treemap(state_stats, path=['Location'], values='Total_Violations',
                              color='Total_Fines', color_continuous_scale='RdBu',
                              title="Volume vs Value")
        st.plotly_chart(fig_tree, use_container_width=True)

    with col2:
        st.subheader("State-wise Statistics")
        st.dataframe(state_stats.set_index('Location').style.background_gradient(cmap='Reds'))
