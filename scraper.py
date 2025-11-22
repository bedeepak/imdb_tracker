import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import IMDB_TOP_250_URL, DEFAULT_TIMEOUT
from utils import auto_scroll, save_to_csv


def scrape_top_250(driver, output_csv):
    driver.get(IMDB_TOP_250_URL)
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul.ipc-metadata-list li.ipc-metadata-list-summary-item")
        )
    )

    logging.info("Page loaded. Starting scroll...")
    auto_scroll(driver)

    movies = driver.find_elements(
        By.CSS_SELECTOR,
        "ul.ipc-metadata-list li.ipc-metadata-list-summary-item"
    )

    data = []
    for index, item in enumerate(movies, start=1):
        try:
            title = item.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text

            # Year
            year = ""
            try:
               year = item.find_element(By.CSS_SELECTOR, "span.cli-title-metadata-item").text

            except:
                pass

            # Rating
            try:
                rating = item.find_element(
                    By.CSS_SELECTOR, "span.ipc-rating-star--rating"
                ).text
            except:
                rating = ""

            # URL
            try:
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = ""

            data.append(
                {
                    "rank": index,
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "url": link,
                }
            )

            time.sleep(random.uniform(0.05, 0.15))

        except Exception as e:
            logging.warning(f"Failed row: {e}")

    return save_to_csv(data, output_csv)
