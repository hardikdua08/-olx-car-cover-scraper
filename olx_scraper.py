import requests
from bs4 import BeautifulSoup
import csv

def fetch_olx_car_covers(url, output_file):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('li', class_='EIR5N')

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Location', 'Link'])

        for listing in listings:
            title_tag = listing.find('span', {'data-aut-id': 'itemTitle'})
            price_tag = listing.find('span', {'data-aut-id': 'itemPrice'})
            location_tag = listing.find('span', {'data-aut-id': 'item-location'})
            link_tag = listing.find('a', href=True)

            title = title_tag.text if title_tag else 'N/A'
            price = price_tag.text if price_tag else 'N/A'
            location = location_tag.text if location_tag else 'N/A'
            link = "https://www.olx.in" + link_tag['href'] if link_tag else 'N/A'

            writer.writerow([title, price, location, link])

    print(f"Results saved to {output_file}")

# Usage
url = "https://www.olx.in/items/q-car-cover"
output_file = "olx_car_covers.csv"
fetch_olx_car_covers(url, output_file)