import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid", rc={"figure.figsize": (8, 6), "axes.titlesize": 15})

age_group_mapping = {
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
age_group_df = pd.DataFrame()

# Sum the columns for each age group
for group_name, columns in age_group_mapping.items():
    age_group_df[group_name] = df[columns].sum(axis=1)
    
age_group_df = age_group_df.apply(pd.to_numeric, errors='coerce')
age_group_df.insert(0, 'ZIP Code', zipcode)
age_group_df



# Define the education groupings
education_grouping = {
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
edu_group_df = pd.DataFrame()

# Sum the columns for each education group
for group_name, columns in education_grouping.items():
    edu_group_df[group_name] = df[columns].sum(axis=1)

edu_group_df = edu_group_df.apply(pd.to_numeric, errors='coerce')
edu_group_df.insert(0, 'ZIP Code', zipcode)
edu_group_df



race_columns = [
    'Population White Alone',
    'Population Black or African American Alone',
    'Population American Indian and Alaska Native Alone',
    'Population Asian Alone',
    'Population Native Hawaiian and Other Pacific Islander Alone',
    'Population Some Other Race Alone',
    'Population Two or More Races',
#     'Population Hispanic or Latino'
]
occupation_columns = [
#     'Total Occupations', 
    'Management, Business, Science, and Arts Occupations', 
    'Service Occupations', 
    'Sales and Office Occupations', 
    'Natural Resources, Construction, and Maintenance Occupations', 
    'Production, Transportation, and Material Moving Occupations'
]
heating_fuel_columns = [    
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



for zip_code in df['ZIP Code'].unique():
    print(f"\033[1m-----------------Analysis for ZIP Code: {zip_code}-------------------\033[0m \n")
    print("\033[1m--------------------Demographic Analysis------------------------\033[0m \n")
    df_zip = df[df['ZIP Code'] == zip_code]
    
    # Sex
    total_population = df_zip['Total Population'].iloc[0]
    sex_ratio = round(df_zip['Sex Ratio Males'].iloc[0] / df_zip['Sex Ratio Females'].iloc[0] * 100,1)
    print(f"Total Population: \033[1m{total_population}\033[0m")
    print(f"Sex Ratio (Males per 100 Females): \033[1m{sex_ratio}%\033[0m")
    
    # Age
    age_distribution = age_group_df[age_group_df['ZIP Code'] == zip_code].iloc[0]
    age_distribution = age_distribution.drop('ZIP Code').astype(int)
    top_5_ages = age_distribution.nlargest(5)
    median_age = df_zip['Median Age'].iloc[0]
    
    sns.barplot(x=age_distribution.values, y=age_distribution.index)
    plt.title(f'Age Distribution in ZIP {zip_code}')
    plt.xlabel('Population')
    plt.ylabel('Age Groups')
    plt.show()
    print(f"Top 5 age groups are: \n")
    for age_group, population in top_5_ages.items():
        print(f"\033[1m{age_group}\033[0m: {population}")
    print(f"\nThe median age is \033[1m{median_age}\033[0m.\n")

    # Race
    race_distribution = df_zip[race_columns].iloc[0]
    race_distribution.index = [col.replace('Population ', '').replace(' Alone', '') for col in race_distribution.index]
    top_race = race_distribution.idxmax()
    hispanic_latino_percent = (df_zip['Population Hispanic or Latino'].iloc[0] / total_population) * 100

    race_distribution.plot(kind='pie',
                           autopct=lambda p: '{:.1f}%'.format(p) if p > 10 else '',  
                           legend=True,
                           figsize=(8,8),
                           startangle=120)
    plt.title(f'Race Composition in ZIP {zip_code}', fontsize=20)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()
    print(f"The percentage of Hispanic or Latino population is \033[1m{hispanic_latino_percent:.2f}%\033[0m.\n\"Hispanic or Latino\" is considered an ethnicity, not a race, by the Census Bureau, and individuals who identify as Hispanic or Latino can be of any race.\n")
    print(f"The majority race is \033[1m{top_race}\033[0m.\n")
    
    # Education
    edu_data = edu_group_df[edu_group_df['ZIP Code'] == zip_code].iloc[0]
    edu_data = edu_data.drop('ZIP Code').astype(int).sort_values(ascending=False)
    edu_percentage = edu_data.divide(df_zip['Education Total'].iloc[0]) * 100
    top_edu = edu_percentage.idxmax()  

    fig, ax = plt.subplots()
    sns.barplot(x=edu_percentage.values, y=edu_percentage.index, palette="viridis", ax=ax)
    plt.title(f'Educational Attainment in ZIP {zip_code}')
    plt.xlabel('Percentage')
    plt.ylabel('Education Level')
    ax.yaxis.tick_right()
    plt.show()
    print(f"The majority of the population (ages 25 and above) have the education level \033[1m{top_edu}\033[0m with \033[1m{round(edu_percentage.max(),1)}%\033[0m.\n")
    
    # Employment
    employed_population = df_zip['Employed Population 16 and Over'].iloc[0]
    civilian_labor_force = df_zip['Civilian Labor Force 16 and Over'].iloc[0]
    employment_rate = (employed_population / civilian_labor_force) * 100
    print(f"Employment Rate: \033[1m{employment_rate:.2f}%\033[0m ({employed_population}/{civilian_labor_force})")
    
    poverty_people = df_zip['Poverty Status All People'].iloc[0]
    poverty_below = df_zip['Below Poverty Level All People'].iloc[0]
    poverty_rate = round((poverty_below / poverty_people) * 100, 1)
    print(f"Poverty Rate (in last 12 months): \033[1m{poverty_rate}%\033[0m")
    
    median_household_income = df_zip['Median Earnings for Workers 16 and Over'].iloc[0]
    print(f"Median Income for a worker: \033[1m${median_household_income}\033[0m")
    
        
    occupation_distribution = df_zip[occupation_columns].iloc[0]
    total_occupations = df_zip['Total Occupations']
    
    occupation_distribution.plot(kind='pie', 
                                 autopct='%1.1f%%', 
                                 startangle=120, 
                                 labels=None,
                                 legend=True,
                                 pctdistance=0.85, 
                                 radius=1.2)
    plt.title(f'Occupation Distribution in ZIP {zip_code}', pad=20, fontsize=20)
    
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.axis('equal') 
    plt.tight_layout()
    plt.legend(labels=occupation_distribution.index, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    plt.show()
    
    
    
    print("\033[1m------------------------------------------------------------\033[0m \n")
    print("\033[1m--------------------Housing Analysis------------------------\033[0m \n")
    
    total_units = df_zip['Total Housing Units'].iloc[0]
    occupied_units = df_zip['Occupied Housing Units'].iloc[0]
    vacant_units = df_zip['Vacant Housing Units'].iloc[0]
    median_household_income = df_zip['Median Household Income'].iloc[0]
    print(f"Total Housing Units: \033[1m{total_units}\033[0m")
    print(f"Occupied/Vacant Housing Units: \033[1m{occupied_units}/{vacant_units}\033[0m")
    print(f"Median Household Income: \033[1m${median_household_income}\033[0m")
    

    
    occupied_type = df_zip[['Owner-Occupied Housing Units','Renter-Occupied Housing Units']].iloc[0]
    occupied_type.plot(kind='pie',
                        explode=(0.1, 0),
                        autopct='%1.1f%%', 
                        figsize=(8,8),
                        startangle=120,
                        colors=sns.color_palette("deep"))
    plt.title(f'Owners vs Renters in ZIP {zip_code}', fontsize=20)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()
    print(f"Majority of the housing units are \033[1m{occupied_type.idxmax()}\033[0m")
    

    # Households type
    df_zip['Married Households Without Children'] = df_zip['Married-Couple Households'] - df_zip['Married-Couple Households with Children']
    household_data = {
        'Family Type': ['Married with Children', 'Married w/o Children', 'Single Parent w/ Children', 'Individuals'],
        'Count': [
            df_zip['Married-Couple Households with Children'].sum(),
            df_zip['Married Households Without Children'].sum(),
            df_zip['Single Parent Households with Children'].sum(),
            df_zip['Single Households'].sum()
        ]
    }
    household_df = pd.DataFrame(household_data)
    
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(
        x='Family Type', 
        y='Count', 
        data=household_df, 
        palette='pastel'
    )
    for p in barplot.patches:
        barplot.annotate(
            format(p.get_height(), '.0f'), 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', 
            va = 'center', 
            xytext = (0, 9), 
            textcoords = 'offset points'
        )

    plt.title('Household Types')
    plt.xlabel('Household Category')
    plt.ylabel('Number of Households')
    plt.tight_layout()
    plt.show()
    
    sustainability_data = df_zip[heating_fuel_columns].iloc[0].sort_values(ascending=False)
    sustainability_features = (sustainability_data / df_zip['Housing Units that use Heating Fuel'].iloc[0]) * 100
    sustainability_features.index = [col.replace('Housing Units with ', '') for col in sustainability_features.index]

    sustainability_table = pd.DataFrame({
        'Energy Source': sustainability_features.index,
        'Percentage': sustainability_features.values,
        'Number of Units': sustainability_data.values
    }).sort_values(by='Percentage', ascending=False)
    
    sustainability_table['Percentage'] = sustainability_table.apply(
        lambda row: f"{row['Percentage']:.2f}%", axis=1)
    sustainability_table.reset_index(drop=True, inplace=True)
    print(sustainability_table.to_string(index=False))

    # Computer and internet
    household_tech_data = df_zip[['Households with a Smartphone/Tablet/Portable', 'Households with a Computer', 'Households with Internet']].iloc[0]
    household_tech_percentages = (household_tech_data / occupied_units) * 100
    sns.barplot(x=household_tech_data.index, y=household_tech_data.values, palette="viridis")
    plt.title(f'Technology in Households in ZIP {zip_code}')
    plt.xlabel('Technology')
    plt.ylabel('Number of Households')

    for index, value in enumerate(household_tech_data.values):
        percentage = household_tech_percentages[index]
        plt.text(index, value, f'{percentage:.1f}% ({value})', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()
    print(f'Percentage is based on the total occupied households \033[1m{occupied_units}\033[0m.')
    
    print("\033[1m------------------------------------------------------------\033[0m \n")

