import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_google_maps_reviews(url, num_reviews):
    driver = setup_webdriver()
    open_url(driver, url)
    
    reviews_data = []
    while len(reviews_data) < num_reviews:
        scroll_the_page(driver)
        reviews_data = extract_reviews(driver, reviews_data, num_reviews)
        
        if not has_more_reviews(driver):
            break
    
    driver.quit()
    save_reviews_to_csv(reviews_data, num_reviews)

def setup_webdriver():
    return webdriver.Safari()

def open_url(driver, url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

def scroll_the_page(driver):
    try:
        scrollable_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde'))
        )
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(2)
    except Exception as e:
        print(f"Error scrolling the page: {e}")

def extract_reviews(driver, reviews_data, num_reviews):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
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

        if review_data not in reviews_data:
            reviews_data.append(review_data)

        if len(reviews_data) >= num_reviews:
            break

    return reviews_data

def has_more_reviews(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height+1500:
        print("No more reviews are loading.")
        return False
    return True

def save_reviews_to_csv(reviews_data, num_reviews):
    data = pd.DataFrame(reviews_data[:num_reviews])
    data.to_csv('google_maps_reviews.csv', index=False)
    print(f'Data for {num_reviews} reviews has been scraped and saved to google_maps_reviews.csv')

# URL to scrape
url = 'https://www.google.com/maps/place/Mall+Grand+Cakung/@-6.1867501,106.9485864,15z/data=!4m8!3m7!1s0x2e698b09ef2ae3ff:0x6e906e182d101bf!8m2!3d-6.1867509!4d106.9588868!9m1!1b1!16s%2Fg%2F11bw7m0rlm?entry=ttu'

# Number of reviews to scrape
num_reviews = 50

# Scrape reviews
scrape_google_maps_reviews(url, num_reviews)
