from typing import Any

import scrapy
from scrapy.http import Response

from python_vacancies.url_config import DOU_DOMAIN, DOU_SCRAPE_URL
from selenium_vacancy.selenium_chrome import DouChromeDriver


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = [DOU_DOMAIN]
    start_urls = [DOU_SCRAPE_URL]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        with DouChromeDriver() as driver:
            driver.load_html_page(response.url)
            selector = scrapy.Selector(text=driver.page_source)
            vacancies = selector.css("#vacancyListId")
            for vacancy in vacancies.css("li"):
                yield self._parse_vacancy(response, vacancy, driver)

    def _parse_vacancy(
            self,
            response: Response,
            vacancy: scrapy.Selector,
            driver: DouChromeDriver
    ) -> dict:

        detail_url = response.urljoin(vacancy.css("a::attr(href)").get())
        return driver.get_vacancy_data(detail_url)
