import streamlit as st
import plotly.express as px
import plotly.io as pio

import module.process as process

st.set_page_config(page_title="U.S Census Analysis", page_icon="📊", layout="wide")

st.markdown("<h1 style='text-align: center'>📊 U.S Census Analysis</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center'>
                This app presents a comprehensive analysis of US Census data for a selected ZIP Code. 
                The data is fetched from the US Census API and processed using Python for the latest data available.
                </p>""", unsafe_allow_html=True)

formcol1, formcol2, formcol3 = st.columns([1, 3, 1])
with formcol2:
    with st.form("options_form", clear_on_submit=False):
        cols = st.columns(2)
        location_type = "ZIP Code" #st.radio("Select Location Type", ["ZIP Code", "Census Tract"])
        with cols[0]:
            if location_type == "ZIP Code":
                location_value = st.text_input("**Enter a ZIP Code:**", value="32805", max_chars=5)
            else:
                location_value = st.text_input("**Enter a Census Tract:**", value="060370101.00")
        with cols[1]:
            template = st.selectbox("**Select Color Template:**", list(pio.templates.keys()), index=5)
        st.form_submit_button(label='Analyze')

    if template:
        pio.templates.default = template
    else:
        pio.templates.default = 'plotly_dark'

    if location_value:
        with st.spinner(f"Fetching data for {location_type} {location_value}..."):
            try:
                data = process.fetch_and_prepare_data(location_value)
                demographics = process.age_sex_analysis(data)
                race_info = process.race_analysis(data)
                education_info = process.educational_analysis(data)
                employment_info = process.employment_analysis(data)
                housing_info = process.housing_analysis(data)
                sustainability_info = process.sustainability_analysis(data)
                technology_info = process.technology_analysis(data)
                st.toast(f"✅ Sucessfully fetched data for {location_type} {location_value}...'")
                
            except ValueError as e:
                st.error(f"Error fetching data: {e}")
            else:
                st.success(f"✅ Sucessfully fetched data for {location_type} {location_value}...")
                st.snow()
                pass    
    
st.markdown("---")
col1, col2, col3 = st.columns([1, 10, 1])
with col2:    
    st.markdown(f"<h2 style='text-align: center'>Demopraphic Analysis for {data['location_string']}</h2> <br>", unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns([1, 1, 2, 0.5])
    kpi1.metric(label="Total Population", value=f"{demographics['total_population']:,}")
    kpi2.metric(label="Sex Ratio", value=f"{demographics['sex_ratio']}%", delta="Males per 100 Females", delta_color="off")
    kpi3.metric(label="Top Race", value=race_info['top_race'])
    kpi4.metric(label="Median Age", value=demographics['median_age'])

    plot1, plot2 = st.columns([1, 1])
    # Age Distribution
    fig = px.bar(
        data_frame=demographics['age_distribution'],
        y='Age_Groups',
        x='Population',
        color='Population',  
        title="Age Distribution",
        orientation='h'
    )
    plot1.plotly_chart(fig)
    # Race Distribution
    fig = px.pie(
        race_info['race_distribution'], 
        values='Population', 
        names='Race', 
        title='Population Distribution by Race'
    )
    plot2.plotly_chart(fig)
    st.markdown(f"The percentge of Hispanic/Latino population is {round(race_info['hispanic_latino_percent'], 2)}%.")
    st.caption("Hispanic/Latino is considered an ethnicity, not a race, by the Census Bureau, and individuals who identify as Hispanic or Latino can be of any race.")
    st.markdown("---")

    kpi5, kpi6, kpi7, kpi8 = st.columns([1, 1, 2, 0.5])
    kpi5.metric(label="Median Workers Income", value=f"${employment_info['median_workers_income']:,}")
    kpi6.metric(label="Poverty Rate", value=f"{employment_info['poverty_rate']:.2f}%")
    kpi7.metric(label="Education Level", value=f"{education_info['top_education']}", delta=f"{education_info['top_education_percentage']:.2f}%", delta_color="off")
    kpi8.metric(label="Employment Rate", value=f"{employment_info['employment_rate']:.2f}%")

    plot3, plot4 = st.columns([1, 1])
    # Occupation Distribution
    fig = px.treemap(
        employment_info['occupation_distribution'], 
        path=['Occupation Category'], 
        values='Count',
        title='Occupation Distribution'
    )
    plot3.plotly_chart(fig)
    # Education Distribution
    fig = px.bar(
        data_frame=education_info['education_percentages'],
        title="Education Distribution",
        color=education_info['education_percentages'].index,
        labels={'index': 'Education Type', 'value': 'Percentage'},
        orientation='h'
    )
    fig.update_layout(legend_title='')
    plot4.plotly_chart(fig)
    st.markdown("---")

    kpi9, kpi10, kpi11, kpi12 = st.columns([1, 1, 2, 1])
    kpi9.metric(label="Total Units", value=f"{housing_info['total_units']:,}")
    kpi10.metric(label="Occupied/Vacant", value=f"{housing_info['occupied_units']}/{housing_info['vacant_units']}")
    kpi11.metric(label="Occupied Type", value=f"{housing_info['top_occupied_type']}")
    kpi12.metric(label="Median Household Income", value=f"${housing_info['median_household_income']:,}")

    plot5, plot6 = st.columns([1, 1])
    # Housing Type Distribution
    fig = px.pie(
        housing_info['occupied_type_distribution'], 
        values='Count', 
        names='Housing Type', 
        hole=0.3,
        title='Occupied Housing Units Distribution'
    )
    plot5.plotly_chart(fig)
    # Family Type Distribution
    fig = px.bar(
        housing_info['family_household_data'],
        y='Count',
        x='Family Type',
        color='Family Type',
        title='Family Type Distribution',
    )
    plot6.plotly_chart(fig)

    plot7, plot8 = st.columns([1, 1])
    # Sustainability
    plot7.dataframe(
        sustainability_info,
        hide_index=True,
        width=None,
        column_config={
            "Energy Source": st.column_config.TextColumn("Energy Source"),
            "Number of Units": st.column_config.ProgressColumn(
                "Number of Units",
                format="%f",
                min_value=0, 
                max_value=max(sustainability_info['Number of Units'])
            )}                   
    )
    # Technology
    fig = px.bar(
        technology_info,
        x='Technology',
        y='Count',
        text='Percentage', 
        color='Technology',
        title='Technology Usage'
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    plot8.plotly_chart(fig, use_container_width=True)

st.markdown("---")



