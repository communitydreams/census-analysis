import streamlit as st

import module.process as process

st.set_page_config(page_title="Census Analysis Dashboard", layout="wide")

st.title('🎈 Census Analysis Dashboard')
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
            st.header(f"**ZIP Code: {zip_code}**")
            st.markdown(f"**Total Population: {demographics['total_population']}**")
            st.markdown(f"**Sex Ratio: {demographics['sex_ratio']}**")
            st.markdown(f"**Median Age: {demographics['median_age']}**")
