from abc import ABC, abstractmethod


class VacancyDriverBase(ABC):
    @abstractmethod
    def get_vacancy_data(self, vacancy_detail_url: str) -> dict:
        ...
