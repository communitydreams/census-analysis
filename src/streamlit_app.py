import streamlit as st
import plotly.express as px

import module.process as process

st.set_page_config(page_title="Census Analysis Dashboard", page_icon="📊", layout="wide")

st.title('📊 Census Analysis Dashboard')
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
            st.snow()
        except ValueError as e:
            st.error(f"Error fetching data: {e}")
        else:
            pass
        
    st.header(f"**ZIP Code: {zip_code}**")


    st.markdown(f"**Total Population: {demographics['total_population']}**")
    st.markdown(f"**Sex Ratio: {demographics['sex_ratio']}%**")
    st.markdown(f"**Median Age: {demographics['median_age']}**")

    # Age Distribution
    fig = px.bar(
        data_frame=demographics['age_distribution'],
        y='Age_Groups',
        x='Population',
        color='Population',  
        title="Age Distribution",
        orientation='h'
    )
    st.plotly_chart(fig)

    # Race Distribution
    fig = px.pie(
        race_info['race_distribution'], 
        values='Population', 
        names='Race', 
        title='Population Distribution by Race'
    )
    st.plotly_chart(fig)

    st.markdown(f"**Top Race: {race_info['top_race']}**")
    st.markdown(f"**Hispanic/Latino Percentage: {race_info['hispanic_latino_percent']}%**")

    st.markdown(f"**Employment Rate: {employment_info['employment_rate']}%** ({employment_info['employed_population']}/{employment_info['civilian_labor_force']})")
    st.markdown(f"**Poverty Rate (in last 12 months): {employment_info['poverty_rate']}%**")
    st.markdown(f"**Median Workers Income: {employment_info['median_workers_income']}**")

    # Education Distribution
    fig = px.bar(
        data_frame=education_info['education_percentages'],
        title="Education Distribution",
        color=education_info['education_percentages'].index,
        labels={'index': 'Education Type', 'value': 'Percentage'},
        orientation='h'
    )
    fig.update_layout(legend_title='')
    st.plotly_chart(fig)

    # Occupation Distribution
    fig = px.treemap(
        employment_info['occupation_distribution'], 
        path=['Occupation Category'], 
        values='Count',
        title='Occupation Distribution'
    )
    st.plotly_chart(fig)

    st.subheader('Housing')
    st.markdown(f"**Total Units: {housing_info['total_units']}**")
    st.markdown(f"**Occupied/Vacant Housing Units: {housing_info['occupied_units']}/{housing_info['vacant_units']}**")
    st.markdown(f"**Median Household Income: {housing_info['median_household_income']}**")

    # Housing Type Distribution
    fig = px.pie(
        housing_info['occupied_type_distribution'], 
        values='Count', 
        names='Housing Type', 
        hole=0.3,
        title='Occupied Housing Units Distribution'
    )
    st.plotly_chart(fig)

    # Family Type Distribution
    fig = px.bar(
        housing_info['family_household_data'],
        y='Count',
        x='Family Type',
        color='Family Type',
        title='Family Type Distribution',
    )
    st.plotly_chart(fig)

    # Sustainability
    st.table(sustainability_info)

    # Technology
    print(technology_info)
    fig = px.bar(
        technology_info,
        x='Technology',
        y='Count',
        text='Percentage',  # Add percentages as text on the bars
        color='Technology',  # Color by technology type
        title='Technology Usage'
    )

    # Customize the bar chart
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')  # Format the text with 2 decimal places
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')  # Ensure text size is uniform
    fig.update_layout(xaxis_tickangle=-45)  # Angle the x-axis labels for better readability

    st.plotly_chart(fig)



