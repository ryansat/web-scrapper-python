import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.safari.options import Options
from bs4 import BeautifulSoup
import csv

# Function to extract items from the page source
def extract_items(soup):
    extracted_elements = soup.select('a.hfpxzc')
    items = []
    for element in extracted_elements:
        aria_label = element.get('aria-label')
        href = element.get('href')
        if href and aria_label:
            items.append({'ele': aria_label, 'url': href})
    return items

# Function to scrape items by scrolling and loading more content
def scrape_items(driver, item_count, scroll_delay=2):
    items = []
    seen_urls = set()
    while len(items) < item_count:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        new_items = extract_items(soup)
        new_items = [item for item in new_items if item['url'] not in seen_urls]
        if not new_items:
            break  # If no new items found, exit the loop
        items.extend(new_items)
        seen_urls.update(item['url'] for item in new_items)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_delay)
    return items[:item_count]

# Function to visit each link and extract additional details
def goto_links(driver, items):
    new_items = []
    for item in items:
        result_obj = {}
        time.sleep(3)
        driver.get(item['url'])
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result_obj['url'] = item['url']
        result_obj['title'] = soup.title.text.replace('- Google Maps', '').strip()

        result_selector = soup.select('.CsEnBe')
        field_obj = {}
        for element in result_selector:
            aria_label = element.get('aria-label')
            if aria_label:
                if aria_label.startswith('Address'):
                    field_obj['Address'] = element.select_one('.AeaXub .rogA2c').text
                    field_obj['Pincode'] = ''.join(filter(str.isdigit, field_obj['Address'].split(',')[-1]))
                elif aria_label.startswith('Phone'):
                    field_obj['PhoneNo'] = element.select_one('.AeaXub .rogA2c').text
                elif aria_label.startswith('Plus code'):
                    field_obj['Plus_code'] = element.select_one('.AeaXub .rogA2c').text
                elif aria_label.startswith('Website'):
                    field_obj['Website'] = element.get('href')

        # Extract ratings and user reviews
        try:
            field_obj['Rating'] = soup.select_one('div.F7nice span[aria-hidden="true"]').text
        except AttributeError:
            field_obj['Rating'] = None

        try:
            field_obj['UserReviews'] = soup.select_one('span[aria-label$="reviews"]').text.strip('()')
        except AttributeError:
            field_obj['UserReviews'] = None

        result_obj.update(field_obj)
        new_items.append(result_obj)
    return new_items

if __name__ == "__main__":
    base_url = 'https://www.google.com/maps/search/restaurants/@-6.1826306,106.9476663,15z/data=!3m1!4b1?entry=ttu'
    item_count = 15  # Define how many items you want to scrape
    scroll_delay = 2  # Time to wait before the next scroll

    # Initialize the Safari WebDriver
    driver = webdriver.Safari()
    driver.set_page_load_timeout(300)  # Increase timeout to handle slow loading pages
    driver.get(base_url)
    time.sleep(5)  # Wait for the page to load

    # Scrape items
    print("Starting to scrape items...")
    items = scrape_items(driver, item_count, scroll_delay)
    print(f"Total items scraped: {len(items)}")

    # Go to links and extract additional details
    print("Extracting details from each link...")
    detailed_items = goto_links(driver, items)
    print("Finished extracting details.")

    # Save the result to a CSV file with UTF-8 encoding
    print("Saving data to CSV...")
    with open('places_ratings.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['url', 'title', 'Address', 'Pincode', 'PhoneNo', 'Plus_code', 'Website', 'Rating', 'UserReviews'])
        writer.writeheader()
        for item in detailed_items:
            writer.writerow(item)

    # Close the WebDriver
    driver.quit()
    print("Script completed successfully.")
