import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_google_maps_reviews(url, num_reviews):
    # Set up the Safari WebDriver
    driver = webdriver.Safari()

    # Open the URL with Selenium
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Initialize a list to store reviews
    reviews_data = []

    # Function to click "Load more reviews" button if it exists
    def click_load_more_button():
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.M77dve'))
            )
            load_more_button.click()
            time.sleep(5)  # Wait for the reviews to load
        except Exception as e:
            print("Load more button not found or not clickable:", e)

    # Click the "Load more reviews" button once initially if present
    click_load_more_button()

    # Scroll and scrape until we get the desired number of reviews
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(reviews_data) < num_reviews:
        # Scroll to the bottom of the page to load more reviews
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Click the "Load more reviews" button if present
        click_load_more_button()

        # Get page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract comments and ratings
        reviews = soup.find_all('div', class_='jftiEf fontBodyMedium')
        for review in reviews:
            reviewer_name = review.find('div', class_='WNxzHc qLhwHc').get_text(strip=True)
            review_text = review.find('span', class_='wiI7pd').get_text(strip=True)
            rating_element = review.find('span', class_='kvMYJc')
            rating = len(rating_element.find_all('span', class_='NhBTye')) if rating_element else 'N/A'
            time_posted = review.find('span', class_='rsqaWe').get_text(strip=True)

            review_data = {
                'Reviewer Name': reviewer_name,
                'Review Text': review_text,
                'Rating': rating,
                'Time Posted': time_posted
            }

            # Append the review data if it's not already in the list
            if review_data not in reviews_data:
                reviews_data.append(review_data)

            # Stop if we've collected the desired number of reviews
            if len(reviews_data) >= num_reviews:
                break

        # Check if the page height has not increased, which means no more reviews are loading
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more reviews are loading.")
            break
        last_height = new_height

    # Close the WebDriver
    driver.quit()

    # Create a DataFrame to store the data
    data = pd.DataFrame(reviews_data[:num_reviews])

    # Save the data to a CSV file
    data.to_csv('google_maps_reviews.csv', index=False)

    print(f'Data for {num_reviews} reviews has been scraped and saved to google_maps_reviews.csv')

# URL to scrape
url = 'https://www.google.com/maps/place/Mall+Grand+Cakung/@-6.1867501,106.9485864,15z/data=!4m6!3m5!1s0x2e698b09ef2ae3ff:0x6e906e182d101bf!8m2!3d-6.1867509!4d106.9588868!16s%2Fg%2F11bw7m0rlm?entry=ttu'

# Number of reviews to scrape
num_reviews = 50

# Scrape reviews
scrape_google_maps_reviews(url, num_reviews)
