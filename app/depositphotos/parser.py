import time
from bs4 import BeautifulSoup

from config import BASE_DIR
from app.utils.downloaders import PhotoManager
from app.utils.file_managers import ExcelManager


class DepositPhotosDownloader(ExcelManager, PhotoManager):
    """Парсинг + скачивание фото с сайта depositphotos.com"""

    base_link = "https://ru.depositphotos.com/stock-photos"

    def __init__(self, coordinates: dict) -> None:
        super(DepositPhotosDownloader, self).__init__(coordinates)

    @staticmethod
    def to_soup(content: [str, bytes]) -> BeautifulSoup:
        return BeautifulSoup(content, "html.parser")

    def get_url_search_rubric(self, search_rubric: str, delimiter: str) -> str:
        """Переопределяем метод для построения URL"""

        return f"{self.base_link}/{search_rubric.replace(' ', delimiter)}.html"

    def search_and_to_soup(self, search_rubric: str, delimiter: str):
        link = self.get_url_search_rubric(search_rubric, delimiter)
        get_page = self.get(link)
        if get_page.status_code != 200:
            return False
        return self.to_soup(get_page.text)

    @staticmethod
    def parse_photo_links(soup: BeautifulSoup) -> list:
        photo_links = []
        get_photo_link = soup.select("a > picture > img")
        if not get_photo_link:
            return []
        for link in get_photo_link:
            photo_links.append(link.get("src") or link.get("data-src"))
        print(f"Спарсены {len(photo_links)} кол-во картинок с сайта depositphotos.com! переходим к сохранению!")
        return photo_links

    def download_photos(self, directory_path: str, photo_links_list: list) -> list:
        photo_info = []
        photo_count = 0
        for link in photo_links_list:
            photo_name = link.split("/")[-1]
            photo_format = photo_name.split(".")[-1]
            photo_path = str(BASE_DIR / f"{directory_path}/{photo_name}")
            self.get_directory_or_create(str(BASE_DIR / directory_path))
            self.download_photo(link, photo_path)
            width, height = self.get_photo_sizes(photo_path)
            photo_info.append({
                "file_name": photo_name,
                "width": width,
                "height": height,
                "file_format": photo_format
            })
            photo_count += 1
            time.sleep(1)
        print(f"Скачаны {photo_count} шт. фото с сайта depositphotos.com по пути: {BASE_DIR / directory_path}")
        return photo_info

    def insert_data(self, data_list: list, file_path: str) -> None:
        """Метод для сохранения данных"""

        row = 2
        for info in data_list:
            self.sheet[row][0].value = info["file_name"]
            self.sheet[row][1].value = info["width"]
            self.sheet[row][2].value = info["height"]
            self.sheet[row][3].value = info["file_format"]
            row += 1
        self.save_and_close(file_path)
        print(f"Данные успешно сохранены в excel по пути: {file_path}")
