import asyncio
import os
import json
import logging

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

# For local ssl certification issue
import ssl

ssl_context=ssl.create_default_context()
ssl_context.check_hostname=False
ssl_context.verify_mode=ssl.CERT_NONE


CENSUS_DATA_API = os.environ['CENSUS_DATA_API']
YEAR = '2022'
ZIPCODE = '32805'
BASE_URL = f"https://api.census.gov/data/{YEAR}/acs/acs5"


# Get the column names from the JSON file
def load_column_mapping():
    try:
        with open('column_names.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading column names: {e}")
        raise

# Fetch data asynchronously
async def fetch_data(session, variable, zip_code, results, reverse_mapping):
    params = {
        'get': variable, 
        'for': f'zip code tabulation area:{zip_code}', 
        'key': CENSUS_DATA_API
    }
    try:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                results[reverse_mapping[variable]] = data[1][0]  # Skip the header
            else:
                results[reverse_mapping[variable]] = f'Status code: {response.status}'
                logger.warning(f"Unexpected status code: {response.status} for variable: {variable}")
    except asyncio.TimeoutError:
        results[reverse_mapping[variable]] = 'Timeout'
        logger.warning(f"Timeout occurred for variable: {variable}")
    except Exception as e:
        results[reverse_mapping[variable]] = str(e)
        logger.exception("Error fetching data for variable: {variable}")

# Generate DataFrame from results
def generate_dataframe(zip_code, results):
    df = pd.DataFrame.from_dict(results, orient='index').transpose()
    df.insert(0, 'ZIP Code', zip_code)
    df[df.columns[1:]] = df[df.columns[1:]].apply(pd.to_numeric, errors='coerce')
    return df

# Main asynchronous run function
async def run(zip_code):
    column_name_mapping = load_column_mapping()
    variables = list(column_name_mapping.values())
    reverse_mapping = {v: k for k, v in column_name_mapping.items()}
    results = {}
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = [fetch_data(session, var, zip_code, results, reverse_mapping) for var in variables]
        await asyncio.gather(*tasks)
        return results

def get_data(zip_code):
    try:
        results = asyncio.run(run(zip_code))
        df = generate_dataframe(zip_code, results)
        logger.info("Data extraction and DataFrame creation completed successfully.")
        return df
    except Exception as e:
        logger.exception("Failed to complete the data extraction and DataFrame creation process.")
        raise

# if __name__ == '__main__':
#     print(fetch_data(ZIPCODE))