import asyncio
import os
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
year = '2022'
zipcode = '32805'
base_url = f"https://api.census.gov/data/{year}/acs/acs5"



with open('../column_names.json', 'r') as f:
    column_name_mapping = json.load(f)


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
# await run(zipcode)
asyncio.run(run(zipcode))

# Now results have the data or error for each variable
results



len(results)




df = pd.DataFrame.from_dict(results, orient='index').transpose()
df.insert(0, 'ZIP Code', zipcode)
df[df.columns[1:]] = df[df.columns[1:]].apply(pd.to_numeric, errors='coerce')
df
