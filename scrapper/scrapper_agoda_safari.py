import time
import csv
from selenium import webdriver
from selenium.webdriver.safari.options import Options
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

class AgodaScraper:
    def __init__(self, url):
        self.url = url
        self.hotels = []

    def scrape(self):
        driver = self._init_driver()
        driver.get(self.url)
        time.sleep(5)  # Wait for the page to load
        self._scroll_to_load_all_hotels(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        self._extract_hotel_data(soup)
        driver.quit()

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")
        return webdriver.Safari(options=options)

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
        hotel_elements = soup.select('a.PropertyCard__Link')
        for element in hotel_elements:
            name = element.select_one("h3[data-selenium='hotel-name']").text if element.select_one("h3[data-selenium='hotel-name']") else "Unknown"
            stars = element.select_one(".ficon-star-3, .ficon-star-4, .ficon-star-5").text if element.select_one(".ficon-star-3, .ficon-star-4, .ficon-star-5") else "Unknown"
            score = element.select_one("span[data-selenium='review-score']").text if element.select_one("span[data-selenium='review-score']") else "0"
            address = element.select_one("span[data-selenium='area-city-text']").text if element.select_one("span[data-selenium='area-city-text']") else "Unknown"
            price = element.select_one("span[data-selenium='display-price']").text if element.select_one("span[data-selenium='display-price']") else "0"
            link = element.get('href', 'Unknown')

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
    url = "https://www.agoda.com/en-gb/search?city=17193&checkIn=2024-07-28&los=34&rooms=1&adults=2&children=0&locale=en-us&ckuid=dc2ad956-98cb-411c-99df-915f0cb439c7&prid=0&gclid=CjwKCAjwtNi0BhA1EiwAWZaANFn_Da_U95edYuZjLLoMH3fdtQneQttc_HFiyaoE1XNil4fh1ZoYBRoCsg8QAvD_BwE&currency=IDR&correlationId=6a080409-1a0d-42e5-8c24-40b253374987&analyticsSessionId=-8247870591558697504&pageTypeId=5&realLanguageId=1&languageId=1&origin=ID&stateCode=JK&cid=1922884&tag=6da0c587-ac74-45f1-9a0a-d908d27c6f8d&userId=dc2ad956-98cb-411c-99df-915f0cb439c7&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=25&currencyCode=IDR&htmlLanguage=en-us&cultureInfoName=en-us&machineName=sg-pc-6f-geo-web-user-85cf87bd84-mw8zl&trafficGroupId=5&sessionId=vz2nafjjolwyte043cxvm5ax&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&cdnDomain=agoda.net&checkOut=2024-08-31&priceCur=IDR&textToSearch=Bali&travellerType=1&familyMode=off&ds=alDssHzQbUZTz4XZ"
    
    scraper = AgodaScraper(url)
    scraper.scrape()
    scraper.to_csv("bali_hotels.csv")
    print("Scraping completed. Data saved to bali_hotels.csv")