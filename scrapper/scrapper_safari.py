import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_google_maps_places(url, num_places):
    driver = setup_webdriver()
    
    current_url = url

    places_data = []
    seen_urls = set()
    max_scroll_attempts = 20
    scroll_attempts = 0

    while len(places_data) < num_places and scroll_attempts < max_scroll_attempts:
        driver.get(current_url)
        new_places = extract_places(driver, seen_urls)

        if new_places:
            places_data.extend(new_places)
            seen_urls.update(place['url'] for place in new_places)
            print(f"Found {len(new_places)} new places, total: {len(places_data)}")
        else:
            scroll_attempts += 1
            print(f"No new places found, attempt {scroll_attempts}/{max_scroll_attempts}")
            scroll_the_page(driver)  # Scroll the page to attempt loading new content

        if len(places_data) < num_places and scroll_attempts < max_scroll_attempts:
            current_url = adjust_coordinates(current_url)  # Adjust coordinates from the last position
            time.sleep(5)  # Wait for the page to reload

    driver.quit()
    save_places_to_csv(places_data, num_places)

def setup_webdriver():
    """Set up and return a Selenium WebDriver."""
    options = webdriver.SafariOptions()
    # Add options if needed, e.g., options.add_argument('--headless')
    return webdriver.Safari(options=options)

def scroll_the_page(driver):
    """Scrolls the page to load more content."""
    try:
        scrollable_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd'))
        )
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(2)
    except Exception as e:
        print(f"Error scrolling the page: {e}")

def extract_places(driver, seen_urls):
    """Extracts places data from the page source."""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    new_places = []
    place_links = soup.select('a.hfpxzc')

    for link in place_links:
        url = link.get('href')
        title = link.get('aria-label')

        if url and title and url not in seen_urls:
            place_details = extract_place_details(driver, url)
            if place_details:
                new_places.append(place_details)

    return new_places

def extract_place_details(driver, url):
    """Visits each place link and extracts additional details."""
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.title.text.replace('- Google Maps', '').strip()

    details = {
        'url': url,
        'title': title,
        'Address': '',
        'Pincode': '',
        'PhoneNo': '',
        'Plus_code': '',
        'Website': '',
        'Rating': '',
        'UserReviews': ''
    }

    # Extract details
    try:
        details['Address'] = soup.select_one('span.LrzXr').text
        details['Pincode'] = ''.join(filter(str.isdigit, details['Address'].split(',')[-1]))
    except AttributeError:
        details['Address'] = 'N/A'

    try:
        details['PhoneNo'] = soup.select_one('span.LrzXr.zdqRlf.kno-fv').text
    except AttributeError:
        details['PhoneNo'] = 'N/A'

    try:
        details['Plus_code'] = soup.select_one('span.CtHWSd').text
    except AttributeError:
        details['Plus_code'] = 'N/A'

    try:
        website = soup.select_one('a.CsEnBe')
        details['Website'] = website['href'] if website else 'N/A'
    except AttributeError:
        details['Website'] = 'N/A'

    try:
        details['Rating'] = soup.select_one('div.F7nice span[aria-hidden="true"]').text
    except AttributeError:
        details['Rating'] = 'N/A'

    try:
        details['UserReviews'] = soup.select_one('span[aria-label$="reviews"]').text.strip('()')
    except AttributeError:
        details['UserReviews'] = 'N/A'

    return details

def adjust_coordinates(url):
    """Adjust the coordinates in the URL slightly to explore nearby areas."""
    # Extract the current latitude and longitude from the URL
    lat_lng_str = url.split('@')[1].split(',')[0:2]
    lat = float(lat_lng_str[0])
    lng = float(lat_lng_str[1])

    # Define the range for random movement (e.g., within ±0.005 degrees)
    lat += random.uniform(-0.55, 0.55)
    lng += random.uniform(-0.55, 0.55)

    # Replace the old coordinates with the new ones in the URL
    new_coords = f"{lat},{lng}"
    new_url = url.replace(','.join(lat_lng_str), new_coords)

    print(f"Adjusted coordinates to: {new_coords}")
    return new_url

def save_places_to_csv(places_data, num_places):
    """Saves the scraped places data to a CSV file."""
    with open('google_maps_places.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['url', 'title', 'Address', 'Pincode', 'PhoneNo', 'Plus_code', 'Website', 'Rating', 'UserReviews']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for place in places_data[:num_places]:
            writer.writerow(place)

    print(f'Data for {num_places} places has been scraped and saved to google_maps_places.csv')

# URL to scrape
url = 'https://www.google.com/maps/search/restaurants/@-6.2570141,106.7845955,11.27z?entry=ttu'

# Number of places to scrape
num_places = 20

# Scrape places
scrape_google_maps_places(url, num_places)
