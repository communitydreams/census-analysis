import streamlit as st
import plotly.express as px

import module.process as process

st.set_page_config(page_title="Census Analysis Dashboard", page_icon="🏂", layout="wide")

st.title('🏂 Census Analysis Dashboard')
st.markdown("This app presents a comprehensive analysis of US Census data for a selected ZIP Code.")

zip_code = st.text_input("Enter a ZIP Code:", value="32805", max_chars=5)

if zip_code:
    with st.spinner(f"Fetching data for ZIP Code {zip_code}..."):
        try:
            data = process.fetch_and_prepare_data(zip_code)
            demographics = process.age_sex_analysis(data)
            race_info = process.race_analysis(data)
            education_info = process.educational_analysis(data)
            employment_info = process.employment_analysis(data)
            housing_info = process.housing_analysis(data)
            sustainability_info = process.sustainability_analysis(data)
            technology_info = process.technology_analysis(data)
        except ValueError as e:
            st.error(f"Error fetching data: {e}")
        else:
            pass
        
    st.header(f"**ZIP Code: {zip_code}**")


    st.markdown(f"**Total Population: {demographics['total_population']}**")
    st.markdown(f"**Sex Ratio: {demographics['sex_ratio']}%**")
    st.markdown(f"**Median Age: {demographics['median_age']}**")

    fig = px.bar(
        data_frame=demographics['age_distribution'],
        y='Age_Groups',
        x='Population',
        color='Population',  
        title="Age Distribution",
        orientation='h'
    )
    st.plotly_chart(fig)
    # st.bar_chart(demographics['age_distribution'])

    print(race_info['race_distribution'])
    st.bar_chart(race_info['race_distribution'])
    st.markdown(f"**Top Race: {race_info['top_race']}**")
    st.markdown(f"**Hispanic/Latino Percentage: {race_info['hispanic_latino_percent']}%**")


