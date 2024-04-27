import asyncio
import os
import json
import logging
import requests

import dotenv
import aiohttp
import pandas as pd

dotenv.load_dotenv()
logging.basicConfig(
    filename='log.log',
    encoding='utf-8', 
    level=logging.DEBUG, 
    format='%(asctime)s:%(levelname)s:%(name)s:%(filename)s:line %(lineno)d: %(message)s'
)
logger = logging.getLogger()

CENSUS_DATA_API = os.environ['CENSUS_DATA_API']
YEAR = '2022'
# ZIPCODE = '32805'
BASE_URL = f"https://api.census.gov/data/{YEAR}/acs/acs5"


# Get the column names from the JSON file
def load_column_mapping():
    try:
        with open('src/module/data/column_names.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading column names: {e}")
        raise

# Fetch data asynchronously
async def fetch_data(session, variable, zip_code, census_tract, results, reverse_mapping):
    params = {
        'get': variable, 
        'key': CENSUS_DATA_API
    }
    if zip_code:
        params['for'] = f'zip code tabulation area:{zip_code}'
    elif census_tract:
        if len(census_tract) in [11]:
            state_code = census_tract[:2]
            county_code = census_tract[2:5] 
            tract_number = census_tract[5:]

            params['for'] = f'tract:{tract_number}'
            params['in'] = f'state:{state_code} county:{county_code}'
        else:
            logger.warning("Invalid census tract provided.")
            raise Exception("Invalid census tract provided.")
    else:
        logger.warning("Invalid ZIP code or census tract provided.")
        raise Exception("Invalid ZIP code or census tract provided.")
    
    try:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                results[reverse_mapping[variable]] = data[1][0]  # Skip the header
            else:
                results[reverse_mapping[variable]] = f'Status code: {response.status}'
                logger.warning(f"Unexpected status code: {response.status} for variable: {variable}")
                raise Exception(f"Unexpected status code: {response.status} for variable: {variable}")
    except asyncio.TimeoutError:
        results[reverse_mapping[variable]] = 'Timeout'
        logger.warning(f"Timeout occurred for variable: {variable}")
    except Exception as e:
        results[reverse_mapping[variable]] = str(e)
        logger.exception("Error fetching data for variable: {variable}")

# Generate DataFrame from results
def generate_dataframe( results):
    df = pd.DataFrame.from_dict(results, orient='index').transpose()
    df = df.apply(pd.to_numeric, errors='coerce')
    if pd.isnull(df.loc[0, 'Total Population']):
        raise ValueError("Invalid input: Total population is null.\n > Incorrect ZIP code or census tract provided.")
    return df

# Main asynchronous run function
async def run(zip_code=None, census_tract=None):
    column_name_mapping = load_column_mapping()
    variables = list(column_name_mapping.values())
    reverse_mapping = {v: k for k, v in column_name_mapping.items()}
    results = {}
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
        tasks = [fetch_data(session, var, zip_code, census_tract, results, reverse_mapping) for var in variables]
        await asyncio.gather(*tasks)
        return results

def get_location_from_zipcode(zipcode):
    base_url = f"https://api.zippopotam.us/us/{zipcode}"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        if data["places"]:
            place = data["places"][0]
            place_name = place["place name"]
            state = place["state"]
            return f"{place_name}, {state} {zipcode}"
        else:
            logger.warning(f"No location found for the given zip code: {zipcode}")
    else:
        logger.warning(f"Error: {response.status_code} - {response.text}")

    return None

def get_data(zip_code=None, census_tract=None):
    try:
        if census_tract:
            census_tract = census_tract.zfill(11)
            results = asyncio.run(run(census_tract=census_tract))
            location_info = census_tract
        elif zip_code:
            results = asyncio.run(run(zip_code=zip_code))
            location_info = get_location_from_zipcode(zip_code)
        else:
            raise Exception("Invalid ZIP code or census tract provided.")
        df = generate_dataframe(results)
        logger.info("Data extraction and DataFrame creation completed successfully.")
        return df, location_info
    except Exception as e:
        logger.exception(f"Failed to complete the data extraction and DataFrame creation process.\n {e}")
        raise

# if __name__ == '__main__':
#     print(fetch_data(ZIPCODE))