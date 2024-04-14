import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid", rc={"figure.figsize": (8, 6), "axes.titlesize": 15})


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

