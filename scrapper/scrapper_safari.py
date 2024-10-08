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
    all_places_data = []
    seen_urls = set()
    max_scroll_attempts = 5  # Increase scroll attempts to ensure movement to new coordinates
    scroll_attempts = 0

    while len(all_places_data) < num_places and scroll_attempts < max_scroll_attempts:
        driver.get(current_url)
        ensure_checkbox_checked(driver)

        new_places = extract_places(driver, seen_urls)

        if new_places:
            all_places_data.extend(new_places)
            seen_urls.update(place['url'] for place in new_places)
            print(f"Found {len(new_places)} new unique places, total collected: {len(all_places_data)}")
        else:
            scroll_attempts += 1
            print(f"No new places found, attempt {scroll_attempts}/{max_scroll_attempts}")
            # Adjust the coordinates to explore a new area if not enough data
            if scroll_attempts < max_scroll_attempts:
                current_url = adjust_coordinates(current_url, scroll_attempts)
                time.sleep(5)  # Wait for the page to reload

    driver.quit()
    
    # Save unique places based on URLs
    save_places_to_csv(all_places_data, num_places)

def setup_webdriver():
    """Set up and return a Selenium WebDriver."""
    options = webdriver.SafariOptions()
    return webdriver.Safari(options=options)

def ensure_checkbox_checked(driver):
    """Ensure the 'Update results when map moves' checkbox is checked."""
    try:
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@role='checkbox']"))
        )
        if checkbox.get_attribute("aria-checked") == "false":
            checkbox.click()
            print("Checkbox checked.")
    except Exception as e:
        print(f"Error ensuring checkbox is checked: {e}")

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
                seen_urls.add(url)  # Add to seen URLs to avoid duplicates

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

    # Extract Address
    try:
        address_button = soup.find('button', {'data-item-id': 'address'})
        if address_button:
            address_text = address_button.get('aria-label')
            if address_text:
                details['Address'] = address_text.replace('Address: ', '').strip()
                details['Pincode'] = ''.join(filter(str.isdigit, details['Address'].split(',')[-1]))
    except AttributeError:
        details['Address'] = 'N/A'

    # Extract Phone Number
    try:
        phone_button = soup.find('button', {'data-item-id': lambda x: x and x.startswith('phone:')})
        if phone_button:
            phone_text = phone_button.get('aria-label')
            if phone_text:
                details['PhoneNo'] = phone_text.replace('Phone: ', '').strip()
    except AttributeError:
        details['PhoneNo'] = 'N/A'

    # Extract Plus Code
    try:
        details['Plus_code'] = soup.select_one('span.CtHWSd').text
    except AttributeError:
        details['Plus_code'] = 'N/A'

    # Extract Website
    try:
        website = soup.select_one('a.CsEnBe')
        details['Website'] = website['href'] if website else 'N/A'
    except AttributeError:
        details['Website'] = 'N/A'

    # Extract Rating
    try:
        details['Rating'] = soup.select_one('div.F7nice span[aria-hidden="true"]').text
    except AttributeError:
        details['Rating'] = 'N/A'

    # Extract User Reviews
    try:
        details['UserReviews'] = soup.select_one('span[aria-label$="reviews"]').text.strip('()')
    except AttributeError:
        details['UserReviews'] = 'N/A'

    return details

def adjust_coordinates(url, scroll_attempts):
    """Adjust the coordinates in the URL slightly to explore nearby areas."""
    # Extract the current latitude and longitude from the URL
    lat_lng_str = url.split('@')[1].split(',')[0:2]
    lat = float(lat_lng_str[0])
    lng = float(lat_lng_str[1])

    # Define the range for incremental movement (e.g., within ±0.010 degrees)
    lat_offset = (0.010 * scroll_attempts) * random.choice([-1, 1])
    lng_offset = (0.010 * scroll_attempts) * random.choice([-1, 1])

    # Apply the offset to the current coordinates
    lat += lat_offset
    lng += lng_offset

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
        count = 0
        for place in places_data:
            if count >= num_places:
                break
            writer.writerow(place)
            count += 1

    print(f'Data for {count} unique places has been scraped and saved to google_maps_places.csv')

# URL to scrape
url = 'https://www.google.com/maps/search/Restoran/@-7.2753584,112.6714843,13z/data=!3m1!4b1?entry=ttu'

# Number of places to scrape
num_places = 30

# Scrape places
scrape_google_maps_places(url, num_places)
