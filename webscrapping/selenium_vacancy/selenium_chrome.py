from selenium import webdriver
from selenium.common import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from selenium_vacancy.driver_base import VacancyDriverBase


class DouChromeDriver(VacancyDriverBase, webdriver.Chrome):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_vacancy_data(self, vacancy_detail_url: str) -> dict:
        self.get(vacancy_detail_url)
        company_article = self.find_element(By.CLASS_NAME, "b-compinfo")
        vacancy_article = self.find_element(By.CLASS_NAME, "l-vacancy")

        return {
                "Company-name": company_article.find_elements(
                    By.CSS_SELECTOR, ".l-n > a"
                )[0].text,
                "Company-description": company_article.find_element(
                    By.CLASS_NAME, "l-t"
                ).text,
                "Created": vacancy_article.find_element(
                    By.CLASS_NAME, "date"
                ).text,
                "Vacancy-name": vacancy_article.find_element(
                    By.CLASS_NAME, "g-h2"
                ).text,
                "Description": vacancy_article.find_element(
                    By.CLASS_NAME, "vacancy-section"
                ).text
            }

    def load_html_page(self, response_url: str) -> None:
        self.get(response_url)
        try:
            while True:
                button = WebDriverWait(self, 2).until(
                    expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.more-btn > a'))
                )
                if button:
                    button.click()
                else:
                    return

        except (TimeoutException, ElementNotInteractableException):
            return
