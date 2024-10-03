import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import os

@st.cache_data
def load_all_data():
    data_frames = []
    dataset_dir = 'dataset'
    for file in os.listdir(dataset_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(dataset_dir, file)
            df = pd.read_csv(file_path)
            data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

df = load_all_data()

unique_stations = df['station'].unique()

st.title('Air Quality Analysis Dashboard')

selected_station = st.sidebar.selectbox("Select a Station", options=unique_stations)

station_data = df[df['station'] == selected_station]

if station_data.empty:
    st.write(f"No data available for {selected_station}.")
else:
    st.write(f"### Data Overview for {selected_station}")
    st.write(station_data)

    if 'WSPM' in station_data.columns:
        pm_columns = ['PM2.5', 'PM10']
        gas_columns = ['NO2', 'SO2']

        for pm in pm_columns:
            if pm in station_data.columns:
                st.write(f"### Scatter Plot of Wind Speed vs {pm}")
                fig, ax = plt.subplots()
                sns.scatterplot(x='WSPM', y=pm, data=station_data, alpha=0.6, ax=ax)
                sns.regplot(x='WSPM', y=pm, data=station_data, scatter=False, color='red', ax=ax)
                plt.title(f'Wind Speed vs {pm} for {selected_station}')
                plt.xlabel('Wind Speed (WSPM)')
                plt.ylabel(f'{pm} Level')
                st.pyplot(fig)

        if 'TEMP' in station_data.columns:
            for gas in gas_columns:
                if gas in station_data.columns:
                    st.write(f"### Scatter Plot of Temperature vs {gas}")
                    fig, ax = plt.subplots()
                    sns.scatterplot(x='TEMP', y=gas, data=station_data, alpha=0.6, ax=ax)
                    sns.regplot(x='TEMP', y=gas, data=station_data, scatter=False, color='red', ax=ax)
                    plt.title(f'Temperature vs {gas} for {selected_station}')
                    plt.xlabel('Temperature (TEMP)')
                    plt.ylabel(f'{gas} Level')
                    st.pyplot(fig)

st.write("### Map of Selected Station")

stations = {
    "Aotizhongxin": [39.981, 116.337],
    "Changping": [40.221, 116.195],
    "Dingling": [40.29, 116.221],
    "Dongsi": [39.935, 116.418],
    "Guanyuan": [39.908, 116.315],
    "Gucheng": [39.910, 116.361],
    "Huairou": [40.432, 116.634],
    "Nongzhanguan": [39.993, 116.309],
    "Shunyi": [40.129, 116.657],
    "Tiantan": [39.883, 116.414],
    "Wanliu": [39.974, 116.282],
    "Wanshouxigong": [39.905, 116.319],
}

station_coords = stations[selected_station]

map_center = station_coords
m = folium.Map(location=map_center, zoom_start=12)

folium.Marker(
    location=station_coords,
    popup=f"{selected_station} Station",
    icon=folium.Icon(color='blue')
).add_to(m)

st.components.v1.html(m._repr_html_(), height=500)
