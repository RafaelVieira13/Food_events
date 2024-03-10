import requests
import json
import pandas as pd
import numpy as np

def food_events(number_records):

    """
    Note: The maximum limit allowed is 1000 for any single API call.
    """

    # API URL
    url = f'https://api.fda.gov/food/event.json?limit={number_records}'

    r = requests.get(url)

    # Taking a look at the raw data
    #print(r.text)

    # Loading the raw_data as json and Storing it as a variable
    raw_data = json.loads(r.text)

    # Getting only the results and store it as a variable
    results = raw_data['results']

    # Initialiaze an empty dictionary to store the data
    df = []

    # For loop to iterate each list element
    for i in range(0,len(results)):

        # Try to store the data as variables
        try:
            report_number = results[i]['report_number']
            outcomes = results[i]['outcomes']
            date_created = results[i]['date_created']
            reactions = results[i]['reactions']
            consumer_age = results[i]['consumer']['age']
            consumer_age_unit = results[i]['consumer']['age_unit']
            consumer_gender = results[i]['consumer']['gender']
            
            """
    Since there are reports linked to multiple products, we will create a list containing the product data
    and add it to the final dataframe. Subsequently, a new column 'products' will be created which will contain a list of all associated products.
    We will then use the 'explode' function in Python to split each element of the list into separate rows, representing individual products, and then
    extract the product details for analysis.
            """


            # Initiliaze an empty list to store the products data
            products = []

            # getting products data
            for product in results[i]['products']:
                product_role = product['role']
                product_name_brand = product['name_brand']
                product_industry_code = product['industry_code']
                product_industry_name = product['industry_name']

            # append products data into the empty list
                products.append({
                    'product_role': product_role,
                    'product_name_brand': product_name_brand,
                    'product_industry_code': product_industry_code,
                    'product_industry_name': product_industry_name
                })

        # If there is no data store it as missing data (nan)
        except:
            report_number = np.nan
            outcomes = np.nan
            date_created = np.nan
            reactions = np.nan
            consumer_age = np.nan
            consumer_age_unit = np.nan
            consumer_gender = np.nan

        # Append the variables in the dictionary
        df.append({
            'report_number':report_number,
            'outcomes':outcomes,
            'date_created':date_created,
            'reactions': reactions,
            'consumer_age':consumer_age,
            'consumer_age_unit':consumer_age_unit,
            'consumer_gender':consumer_gender,
            'products': products})

    # Transforming the dictionary into a pandas dataframe
    df = pd.DataFrame(df)


    # Using 'explode' function to create a row for each element in the 'products' column list
    df = df.explode('products')

    # Getting the products 'role', 'brand_name' etc... 
    df['product_role'] = df['products'].apply(lambda x: x['product_role'])
    df['product_name_brand'] = df['products'].apply(lambda x: x['product_name_brand'])
    df['product_industry_code'] = df['products'].apply(lambda x: x['product_industry_code'])
    df['product_industry_name'] = df['products'].apply(lambda x: x['product_industry_name'])

    # Droping the 'products' column as we don't need it anymore
    df = df.drop(columns = 'products')

    # The 'outcomes' and 'reactions' are also columns  where those values are inside a list
    # That said let's use the 'explode function again to create a row for each element inside the list
    df = df.explode('outcomes')
    df = df.explode('reactions')

    return df