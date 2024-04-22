import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.module.extract import get_data


sns.set_theme(style="darkgrid", rc={"figure.figsize": (8, 6), "axes.titlesize": 15})

AGE_COLUMNS = {
    'Under 5 Years': ['Male Population Under 5 Years', 'Female Population Under 5 Years'],
    '5 to 9 Years': ['Male Population 5 to 9 Years', 'Female Population 5 to 9 Years'],
    '10 to 14 Years': ['Male Population 10 to 14 Years', 'Female Population 10 to 14 Years'],
    '15 to 19 Years': ['Male Population 15 to 17 Years', 'Male Population 18 and 19 Years',
                    'Female Population 15 to 17 Years', 'Female Population 18 and 19 Years'],
    '20 to 24 Years': ['Male Population 20 Years', 'Male Population 21 Years', 'Male Population 22 to 24 Years',
                    'Female Population 20 Years', 'Female Population 21 Years', 'Female Population 22 to 24 Years'],
    '25 to 34 Years': ['Male Population 25 to 29 Years', 'Male Population 30 to 34 Years',
                    'Female Population 25 to 29 Years', 'Female Population 30 to 34 Years'],
    '35 to 44 Years': ['Male Population 35 to 39 Years', 'Male Population 40 to 44 Years',
                    'Female Population 35 to 39 Years', 'Female Population 40 to 44 Years'],
    '45 to 54 Years': ['Male Population 45 to 49 Years', 'Male Population 50 to 54 Years',
                    'Female Population 45 to 49 Years', 'Female Population 50 to 54 Years'],
    '55 to 59 Years': ['Male Population 55 to 59 Years', 'Female Population 55 to 59 Years'],
    '60 to 64 Years': ['Male Population 60 and 61 Years', 'Male Population 62 to 64 Years',
                    'Female Population 60 and 61 Years', 'Female Population 62 to 64 Years'],
    '65 to 74 Years': ['Male Population 65 and 66 Years', 'Male Population 67 to 69 Years', 'Male Population 70 to 74 Years',
                    'Female Population 65 and 66 Years', 'Female Population 67 to 69 Years', 'Female Population 70 to 74 Years'],
    '75 to 84 Years': ['Male Population 75 to 79 Years', 'Male Population 80 to 84 Years',
                    'Female Population 75 to 79 Years', 'Female Population 80 to 84 Years'],
    '85 Years and Over': ['Male Population 85 Years and Over', 'Female Population 85 Years and Over']
}
EDUCATION_COLUMNS = {
    'Less Than 9th Grade': [
        'No Schooling Completed', 'Nursery School', 'Kindergarten', '1st Grade', 
        '2nd Grade', '3rd Grade', '4th Grade'
    ],
    '9th to 12th Grade No Diploma': [
        '5th Grade', '6th Grade', '7th Grade', '8th Grade', '9th Grade', '10th Grade', 
        '11th Grade', '12th Grade No Diploma'
    ],
    'High School Graduate and Equivalent': [
        'Regular High School Diploma', 'GED or Alternative Credential'
    ],
    'Some College No Degree': [
        'Some College, Less Than 1 Year', 'Some College, 1 or More Years, No Degree'
    ],
    'Associates Degree': [
        'Associate’s Degree'
    ],
    'Bachelors Degree': [
        'Bachelor’s Degree'
    ],
    'Graduate or Professional Degree': [
        'Master’s Degree', 'Professional School Degree', 'Doctorate Degree'
    ]
}

RACE_COLUMNS = [
    'Population White Alone',
    'Population Black or African American Alone',
    'Population American Indian and Alaska Native Alone',
    'Population Asian Alone',
    'Population Native Hawaiian and Other Pacific Islander Alone',
    'Population Some Other Race Alone',
    'Population Two or More Races',
#     'Population Hispanic or Latino'
]
OCCUPATION_COLUMNS = [
#     'Total Occupations', 
    'Management, Business, Science, and Arts Occupations', 
    'Service Occupations', 
    'Sales and Office Occupations', 
    'Natural Resources, Construction, and Maintenance Occupations', 
    'Production, Transportation, and Material Moving Occupations'
]
HEATING_FUEL_COLUMNS = [
#      'Housing Units that use Heating Fuel',
    'Housing Units with Utility Gas',
    'Housing Units with Bottle/Tank/LP Gas',
    'Housing Units with Electricity',
    'Housing Units with Fuel/Oil/Kerosene',
    'Housing Units with Coal',
    'Housing Units with Wood',
    'Housing Units with Solar Energy',
    'Housing Units with Other Fuel',
    'Housing Units with No Fuel Used',
]


def prepare_category_df(df, category_columns):
    """Aggregate columns based on provided mapping."""
    category_df = pd.DataFrame()
    for group_name, columns in category_columns.items():
        category_df[group_name] = df[columns].sum(axis=1)     
    category_df = category_df.apply(pd.to_numeric, errors='coerce')
    return category_df

def fetch_and_prepare_data(zip_code):
    """Fetch and prepare all data categories."""
    df = get_data(zip_code)
    data = {
        'age_data': prepare_category_df(df, AGE_COLUMNS),
        'education_data': prepare_category_df(df, EDUCATION_COLUMNS),
        'race_data': df[RACE_COLUMNS],
        'occupation_data': df[OCCUPATION_COLUMNS],
        'heating_fuel_data': df[HEATING_FUEL_COLUMNS],
        'master': df
    }
    return data

def age_sex_analysis(data):
    """Perform demographic analysis and return the results."""
    df = data['master']
    demographics = {
        'total_population': df['Total Population'].iloc[0],
        'sex_ratio': round(df['Sex Ratio Males'].iloc[0] / df['Sex Ratio Females'].iloc[0] * 100, 1),
        'median_age': df['Median Age'].iloc[0],
        'age_distribution': data['age_data'].astype(int),
    }
    return demographics

def race_analysis(data):
    """Analyze race distribution and return the results."""
    df = data['master']
    race_data = data['race_data']
    race_data.columns = [col.replace('Population ', '').replace(' Alone', '') for col in race_data.columns]
    top_race = race_data.idxmax(axis=1).iloc[0]
    hispanic_latino_percent = (df['Population Hispanic or Latino'].iloc[0] / df['Total Population'].iloc[0]) * 100

    race_info = {
        'race_distribution': race_data,
        'top_race': top_race,
        'hispanic_latino_percent': hispanic_latino_percent
    }
    return race_info

def educational_analysis(data):
    """Analyze educational levels and return the results."""
    edu_data = data['education_data'].iloc[0].sort_values(ascending=False)
    total_education = data['master']['Education Total'].iloc[0]
    edu_percentage =edu_data.divide(total_education) * 100
    top_education = edu_percentage.idxmax()

    education = {
        'education_data': edu_data,
        'education_percentages': edu_percentage,
        'top_education': top_education,
        'top_education_percentage': edu_percentage.max()
    }
    return education

def employment_analysis(data):
    """Calculate employment rate and return the results."""
    df = data['master']
    occupation_distribution = data['occupation_data']
    employed_population = df['Employed Population 16 and Over'].iloc[0]
    civilian_labor_force = df['Civilian Labor Force 16 and Over'].iloc[0]
    employment_rate = (employed_population / civilian_labor_force) * 100
    poverty_people = df['Poverty Status All People'].iloc[0]
    poverty_below = df['Below Poverty Level All People'].iloc[0]
    poverty_rate = round((poverty_below / poverty_people) * 100, 1)

    employment = {
        'employed_population': employed_population,
        'civilian_labor_force': civilian_labor_force,
        'employment_rate': employment_rate,
        'poverty_rate': poverty_rate,
        'median_workers_income': df['Median Earnings for Workers 16 and Over'].iloc[0],
        'total_occupations': df['Total Occupations'].iloc[0],
        'occupation_distribution': occupation_distribution
    }
    return employment

def housing_analysis(data):
    """Analyze housing data and return the results."""
    df = data['master']
    new_column_data = df['Married-Couple Households'] - df['Married-Couple Households with Children']
    df = pd.concat([df, new_column_data.rename('Married Households Without Children')], axis=1)
    household_data = {
        'Family Type': ['Married with Children', 'Married w/o Children', 'Single Parent w/ Children', 'Individuals'],
        'Count': [
            df['Married-Couple Households with Children'].sum(),
            df['Married Households Without Children'].sum(),
            df['Single Parent Households with Children'].sum(),
            df['Single Households'].sum()
        ]
    }
    household_df = pd.DataFrame(household_data)

    housing = {
        'total_units': df['Total Housing Units'].iloc[0],
        'occupied_units': df['Occupied Housing Units'].iloc[0],
        'vacant_units': df['Vacant Housing Units'].iloc[0],
        'occupied_type_distribution': df[['Owner-Occupied Housing Units', 'Renter-Occupied Housing Units']],
        'median_household_income': df['Median Household Income'].iloc[0],
        'family_household_data': household_df,
    }
    return housing

def sustainability_analysis(data):
    """Analyze sustainability related to heating fuel and return the results."""
    df = data['master']
    sustainability_data = data['heating_fuel_data'].iloc[0].sort_values(ascending=False)
    sustainability_features = (sustainability_data / df['Housing Units that use Heating Fuel'].iloc[0]) * 100
    sustainability_features.index = [col.replace('Housing Units with ', '') for col in sustainability_features.index]

    sustainability_table = pd.DataFrame({
        'Energy Source': sustainability_features.index,
        'Percentage': sustainability_features.values,
        'Number of Units': sustainability_data.values
    }).sort_values(by='Percentage', ascending=False)

    return sustainability_table

def technology_analysis(data):
    """Analyze technology usage in households and return the results."""
    df = data['master']
    tech_data = df[['Households with a Smartphone/Tablet/Portable', 'Households with a Computer', 'Households with Internet']]
    total_occupied_units = df['Occupied Housing Units'].iloc[0]
    tech_percentages = (tech_data / total_occupied_units * 100).iloc[0]

    technology = {
        'technology_data': tech_data,
        'technology_percentages': tech_percentages
    }
    return technology

if __name__ == '__main__':
    zip_code = '32805'  
    data = fetch_and_prepare_data(zip_code)
    demographics = age_sex_analysis(data)
    race_info = race_analysis(data)
    education_info = educational_analysis(data)
    employment_info = employment_analysis(data)
    housing_info = housing_analysis(data)
    sustainability_info = sustainability_analysis(data)
    technology_info = technology_analysis(data)

    print(demographics)
    print(race_info)
    print(education_info)
    print(employment_info)
    print(housing_info)
    print(sustainability_info)
    print(technology_info)
