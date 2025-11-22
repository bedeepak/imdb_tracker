from driver_setup import create_driver
from scraper import scrape_top_250
from config import DEFAULT_OUTPUT_CSV


if __name__ == "__main__":
    driver = create_driver(headless=True)
    scrape_top_250(driver, DEFAULT_OUTPUT_CSV)
    driver.quit()
