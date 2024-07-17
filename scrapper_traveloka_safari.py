import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Hotel:
    def __init__(self, name="Unknown", address="Unknown", stars="Unknown", score="0", price="0", link="Unknown"):
        self.name = name
        self.address = address
        self.stars = stars
        self.score = score
        self.price = price
        self.link = link

    def to_dict(self):
        return vars(self)

class TravelokaScraper:
    def __init__(self, url):
        self.url = url
        self.hotels = []

    def scrape(self):
        driver = self._init_driver()
        driver.get(self.url)
        time.sleep(5)  # Wait for the page to load
        self._dismiss_popup(driver)
        self._scroll_to_load_all_hotels(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        self._extract_hotel_data(soup)
        driver.quit()

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")
        return webdriver.Safari(options=options)

    def _dismiss_popup(self, driver):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='promo-activation-modal']"))
            )
            close_button = driver.find_element(By.CSS_SELECTOR, "div[data-testid='promo-activation-close']")
            close_button.click()
            time.sleep(2)  # Wait for the pop-up to be dismissed
        except Exception as e:
            print(f"No pop-up to dismiss: {e}")

    def _scroll_to_load_all_hotels(self, driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _extract_hotel_data(self, soup):
        hotel_elements = soup.select('div.FinderResult__wrapper___3gKns')
        for element in hotel_elements:
            name = element.select_one("h3.FinderResult__hotelName___2ZzoF").text if element.select_one("h3.FinderResult__hotelName___2ZzoF") else "Unknown"
            stars = element.select_one("span.FinderResult__hotelRating___3mYjD").text if element.select_one("span.FinderResult__hotelRating___3mYjD") else "Unknown"
            score = element.select_one("span.ReviewAverage__number___1UnNA").text if element.select_one("span.ReviewAverage__number___1UnNA") else "0"
            address = element.select_one("span.FinderResult__hotelLocation___m2u8P").text if element.select_one("span.FinderResult__hotelLocation___m2u8P") else "Unknown"
            price = element.select_one("span.FinderResult__finalPrice___1mHge").text if element.select_one("span.FinderResult__finalPrice___1mHge") else "0"
            link = element.select_one('a.FinderResult__hotelLink___1TdCy')['href'] if element.select_one('a.FinderResult__hotelLink___1TdCy') else "Unknown"

            print(f"Scraped: Name: {name}, Address: {address}, Stars: {stars}, Score: {score}, Price: {price}, Link: {link}")

            hotel = Hotel(name, address, stars, score, price, link)
            self.hotels.append(hotel)

    def to_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'address', 'stars', 'score', 'price', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for hotel in self.hotels:
                writer.writerow(hotel.to_dict())

if __name__ == "__main__":
    url = "https://www.traveloka.com/id-id/hotel/search?spec=20-08-2024.23-08-2024.3.1.HOTEL_GEO.102746.Bali.2"
    
    scraper = TravelokaScraper(url)
    scraper.scrape()
    scraper.to_csv("traveloka_bali_hotels.csv")
    print("Scraping completed. Data saved to traveloka_bali_hotels.csv")