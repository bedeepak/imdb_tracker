import time
import logging
import pandas as pd
from selenium.webdriver.common.by import By


def auto_scroll(driver):
    last_count = 0
    scroll_attempts = 0

    while True:
        elements = driver.find_elements(
            By.CSS_SELECTOR,
            "ul.ipc-metadata-list li.ipc-metadata-list-summary-item",
        )
        current_count = len(elements)

        logging.info(f"Loaded items: {current_count}")

        if current_count == last_count:
            scroll_attempts += 1
        else:
            scroll_attempts = 0

        if scroll_attempts >= 3:
            break

        last_count = current_count
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)

    logging.info(f"Final movie count: {current_count}")
    return current_count


def save_to_csv(data, output_csv):
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    logging.info(f"Data saved to {output_csv}")
    return df
