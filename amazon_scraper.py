from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADER = ({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

base_url = 'https://www.amazon.in/s?k=redme&crid=1MTPTH7ROZ3F6&sprefix=redm%2Caps%2C286&ref=nb_sb_noss_2'
amazon_scraper = []

for page in range(1, 2):  # Loop through the first page
    url = f"{base_url}&page={page}"
    webpack = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(webpack.content, 'html.parser')
    links = soup.find_all('a', class_='a-link-normal s-no-outline')

    for link in links:
        href = link.get('href')
        if href.startswith('/'):
            product_link = 'https://www.amazon.in' + href
        else:
            product_link = href
        new_webpage = requests.get(product_link, headers=HEADER)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

        price = new_soup.find('span', class_='a-price-whole').text.strip().replace('.', '') if new_soup.find('span', class_='a-price-whole') else 'N/A'

        rating = new_soup.find('span', class_='a-icon-alt').text.strip().replace(' out of ', '/') if new_soup.find('span', class_='a-icon-alt') else 'N/A'

        title = new_soup.find('span', id='productTitle').text.strip() if new_soup.find('span', id='productTitle') else 'N/A'

        amazon_scraper.append((title, price, rating))

# Create a DataFrame from the product details
df = pd.DataFrame(amazon_scraper, columns=['Title', 'Price', 'Rating'])

# Save the DataFrame to a CSV file
df.to_csv('amazon_scraper.csv', index=False)