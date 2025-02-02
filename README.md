
## Steps to Run the Script

### 1. **Install Python**
Ensure **Python 3.x** is installed. You can download it from [python.org](https://www.python.org/downloads/).

### 2. **Install Required Libraries**
Open a terminal or command prompt and install the required libraries using `pip`:

```bash
pip install requests beautifulsoup4 pandas
```

### 3. **Download the Script**
Save the following Python code into a file, e.g., `amazon_scraper.py`:

```python
from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADER = ({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

base_url = 'https://www.amazon.in/s?k=oneplus&crid=38KI8D9OMMWOC&sprefix=oneplus%2Caps%2C419&ref=nb_sb_noss_2'
oneplus = []

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
        warranty = new_soup.find('span', class_='a-size-small a-color-link a-text-normal').text.strip() if new_soup.find('span', class_='a-size-small a-color-link a-text-normal') else 'N/A'

        oneplus.append((price, rating, warranty))

# Create a DataFrame from the product details
df = pd.DataFrame(oneplus, columns=['Price', 'Rating', 'Warranty'])

# Save the DataFrame to a CSV file
df.to_csv('oneplus.csv', index=False)
```

### 4. **Run the Script**
In your terminal or command prompt, navigate to the folder where `amazon_scraper.py` is saved and run:

```bash
python amazon_scraper.py
```

This will run the script and save the scraped data to a `oneplus.csv` file.

---


#
