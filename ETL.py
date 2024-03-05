import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import numpy as np
import pandas as pd

# 1. Extracting data from ebay using python requests and beautiful soup

description = []
lap_state = []
lap_price = []

pages = np.arange(1, 100, 1)
for page in pages:
    url = (r"https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=laptop&_sacat=0&rt=nc&_ipg=60&_pgn=" + str(page))
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('div', {'class': 's-item__info clearfix'})

    for item in data:
        name = item.find('div', {'class': 's-item__title'}).text
        description.append(name)

        state = item.find('span', {'class': 'SECONDARY_INFO'}).text
        lap_state.append(state)

        price = item.find('span', {'class': 's-item__price'}).text
        lap_price.append(price)

df = pd.DataFrame({"Lap Details": description, 'Laptop state': lap_state, 'Laptop price': lap_price})
print(df)
df.to_csv('ebay_laptops.csv', index=None)





# 2. Transforming the data using python pandas and numpy
# 3. Loading the transformed data into postgres database
# 4. Analysis and data storytelling using Powerbi
