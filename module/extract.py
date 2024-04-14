import asyncio
import requests
import json

import dotenv
import aiohttp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dotenv.load_dotenv()

# For local ssl certification issue
import ssl

ssl_context=ssl.create_default_context()
ssl_context.check_hostname=False
ssl_context.verify_mode=ssl.CERT_NONE



CENSUS_DATA_API = os.environ['CENSUS_DATA_API']
zipcode = '32805'
year = '2022'
base_url = f"https://api.census.gov/data/{year}/acs/acs5"



column_name_mapping = {
    'Total Population': 'B01003_001E',
    'Sex Ratio Males': 'B01001_002E',
    'Sex Ratio Females': 'B01001_026E',
    'Median Age': 'B01002_001E',
    'Employed Population 16 and Over': 'B23025_004E',
    'Civilian Labor Force 16 and Over': 'B23025_003E',
    'Poverty Status All People': 'B17001_001E',
    'Below Poverty Level All People': 'B17001_002E',
    'Median Earnings for Workers 16 and Over': 'B20002_001E',
    'Total Housing Units': 'B25001_001E',
    'Occupied Housing Units': 'B25003_001E',
    'Vacant Housing Units': 'B25002_003E',
    'Owner-Occupied Housing Units': 'B25003_002E',
    'Renter-Occupied Housing Units': 'B25003_003E',
    'Median Household Income': 'B19013_001E',
    'Married-Couple Households': 'B11001_003E',
    'Married-Couple Households with Children': 'B11005_004E',
    'Single Parent Households with Children': 'B11005_005E',
    'Single Households': 'B11001_007E',
    'Total Households': 'B11001_001E',
    'Households with a Computer': 'B28010_003E',
    'Households with a Smartphone/Tablet/Portable': 'B28010_005E',
    'Households with Internet': 'B28011_002E',
    'Education Total': 'B15003_001E',
    'No Schooling Completed': 'B15003_002E',
    'Nursery School': 'B15003_003E',
    'Kindergarten': 'B15003_004E',
    '1st Grade': 'B15003_005E',
    '2nd Grade': 'B15003_006E',
    '3rd Grade': 'B15003_007E',
    '4th Grade': 'B15003_008E',
    '5th Grade': 'B15003_009E',
    '6th Grade': 'B15003_010E',
    '7th Grade': 'B15003_011E',
    '8th Grade': 'B15003_012E',
    '9th Grade': 'B15003_013E',
    '10th Grade': 'B15003_014E',
    '11th Grade': 'B15003_015E',
    '12th Grade No Diploma': 'B15003_016E',
    'Regular High School Diploma': 'B15003_017E',
    'GED or Alternative Credential': 'B15003_018E',
    'Some College, Less Than 1 Year': 'B15003_019E',
    'Some College, 1 or More Years, No Degree': 'B15003_020E',
    'Associate’s Degree': 'B15003_021E',
    'Bachelor’s Degree': 'B15003_022E',
    'Master’s Degree': 'B15003_023E',
    'Professional School Degree': 'B15003_024E',
    'Doctorate Degree': 'B15003_025E',
    'Total Occupations': 'C24050_001E',
    'Management, Business, Science, and Arts Occupations': 'C24050_015E',
    'Service Occupations': 'C24050_029E',
    'Sales and Office Occupations': 'C24050_043E',
    'Natural Resources, Construction, and Maintenance Occupations': 'C24050_057E',
    'Production, Transportation, and Material Moving Occupations': 'C24050_071E',
    'Housing Units that use Heating Fuel': 'B25040_001E',
    'Housing Units with Utility Gas': 'B25040_002E',
    'Housing Units with Bottle/Tank/LP Gas': 'B25040_003E',
    'Housing Units with Electricity': 'B25040_004E',
    'Housing Units with Fuel/Oil/Kerosene': 'B25040_005E',
    'Housing Units with Coal': 'B25040_006E',
    'Housing Units with Wood': 'B25040_007E',
    'Housing Units with Solar Energy': 'B25040_008E',
    'Housing Units with Other Fuel': 'B25040_009E',
    'Housing Units with No Fuel Used': 'B25040_010E',  
    'Male Population Under 5 Years': 'B01001_003E',
    'Male Population 5 to 9 Years': 'B01001_004E',
    'Male Population 10 to 14 Years': 'B01001_005E',
    'Male Population 15 to 17 Years': 'B01001_006E',
    'Male Population 18 and 19 Years': 'B01001_007E',
    'Male Population 20 Years': 'B01001_008E',
    'Male Population 21 Years': 'B01001_009E',
    'Male Population 22 to 24 Years': 'B01001_010E',
    'Male Population 25 to 29 Years': 'B01001_011E',
    'Male Population 30 to 34 Years': 'B01001_012E',
    'Male Population 35 to 39 Years': 'B01001_013E',
    'Male Population 40 to 44 Years': 'B01001_014E',
    'Male Population 45 to 49 Years': 'B01001_015E',
    'Male Population 50 to 54 Years': 'B01001_016E',
    'Male Population 55 to 59 Years': 'B01001_017E',
    'Male Population 60 and 61 Years': 'B01001_018E',
    'Male Population 62 to 64 Years': 'B01001_019E',
    'Male Population 65 and 66 Years': 'B01001_020E',
    'Male Population 67 to 69 Years': 'B01001_021E',
    'Male Population 70 to 74 Years': 'B01001_022E',
    'Male Population 75 to 79 Years': 'B01001_023E',
    'Male Population 80 to 84 Years': 'B01001_024E',
    'Male Population 85 Years and Over': 'B01001_025E',
    'Female Population Under 5 Years': 'B01001_027E',
    'Female Population 5 to 9 Years': 'B01001_028E',
    'Female Population 10 to 14 Years': 'B01001_029E',
    'Female Population 15 to 17 Years': 'B01001_030E',
    'Female Population 18 and 19 Years': 'B01001_031E',
    'Female Population 20 Years': 'B01001_032E',
    'Female Population 21 Years': 'B01001_033E',
    'Female Population 22 to 24 Years': 'B01001_034E',
    'Female Population 25 to 29 Years': 'B01001_035E',
    'Female Population 30 to 34 Years': 'B01001_036E',
    'Female Population 35 to 39 Years': 'B01001_037E',
    'Female Population 40 to 44 Years': 'B01001_038E',
    'Female Population 45 to 49 Years': 'B01001_039E',
    'Female Population 50 to 54 Years': 'B01001_040E',
    'Female Population 55 to 59 Years': 'B01001_041E',
    'Female Population 60 and 61 Years': 'B01001_042E',
    'Female Population 62 to 64 Years': 'B01001_043E',
    'Female Population 65 and 66 Years': 'B01001_044E',
    'Female Population 67 to 69 Years': 'B01001_045E',
    'Female Population 70 to 74 Years': 'B01001_046E',
    'Female Population 75 to 79 Years': 'B01001_047E',
    'Female Population 80 to 84 Years': 'B01001_048E',
    'Female Population 85 Years and Over': 'B01001_049E',
    'Total Race Population': 'B02001_001E',
    'Population White Alone': 'B02001_002E',
    'Population Black or African American Alone': 'B02001_003E',
    'Population American Indian and Alaska Native Alone': 'B02001_004E',
    'Population Asian Alone': 'B02001_005E',
    'Population Native Hawaiian and Other Pacific Islander Alone': 'B02001_006E',
    'Population Some Other Race Alone': 'B02001_007E',
    'Population Two or More Races': 'B02001_008E',
    'Population Hispanic or Latino': 'B03001_003E',
}



# with open('column_names.json', 'w') as f:
#     json.dump(column_name_mapping, f)
# print('Saved as column_names.json')



reverse_mapping ={}
variables = list(column_name_mapping.values())
reverse_mapping = {v: k for k, v in column_name_mapping.items()}
results = {reverse_mapping[var]: None for var in variables}


async def fetch_variable_data(session, variable, zip_code):
    params = {
        'get': variable,
        'for': 'zip code tabulation area:{}'.format(zip_code),
        'key': CENSUS_DATA_API
    }
    try:
        async with session.get(base_url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                results[reverse_mapping[variable]] = data[1][0]  # Skip the header
            else:
                results[reverse_mapping[variable]] = f'Status code: {response.status}'
    except asyncio.TimeoutError:
        results[reverse_mapping[variable]] = 'Timeout'
    except Exception as e:
        results[reverse_mapping[variable]] = str(e)

async def run(zip_code):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = [fetch_variable_data(session, var, zip_code) for var in variables]
        await asyncio.gather(*tasks)

# Run the async event loop with the ZIP code
# asyncio.run(run(zip_code))
await run(zipcode)

# Now results have the data or error for each variable
results



len(results)




df = pd.DataFrame.from_dict(results, orient='index').transpose()
df.insert(0, 'ZIP Code', zipcode)
df[df.columns[1:]] = df[df.columns[1:]].apply(pd.to_numeric, errors='coerce')
df




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

