import time
from typing import Type

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.webdriver import WebDriver

from config import BASE_DIR
from app.utils.browser_managers import SeleniumManager
from app.utils.downloaders import PhotoManager
from app.utils.file_managers import ExcelManager, FileManager
from selenium.webdriver import Firefox


class ShutterstockDownloader(SeleniumManager, PhotoManager, ExcelManager, FileManager):
    """Парсинг + скачивание фото с сайта shutterstock.com"""

    base_link = "https://www.shutterstock.com/ru"

    def __init__(self, driver_path: str, coordinates: dict, headless: bool = False,
                 driver: Type[WebDriver] = Firefox) -> None:
        super(ShutterstockDownloader, self).__init__(driver_path, driver, headless)
        ExcelManager.__init__(self, coordinates)
        self.page_directory = "pages"
        self.page_path = BASE_DIR / f"{self.page_directory}/data.html"

    @staticmethod
    def to_soup(content: [str, bytes]) -> BeautifulSoup:
        return BeautifulSoup(content, "html.parser")

    def get_url_search_rubric(self, search_rubric: str, delimiter: str) -> str:
        """Переопределяем метод для построения URL"""

        return f"{self.base_link}/search/{search_rubric.strip().replace(' ', delimiter)}"

    def parse_photo_page_and_save(self, search_rubric, delimiter) -> None:
        """Метод для парсинга и сохранения страницы на файл"""

        self.default_driver.get(self.get_url_search_rubric(search_rubric, delimiter))
        time.sleep(3)
        self.scroll_down(150)
        time.sleep(10)
        self.get_directory_or_create(str(BASE_DIR / self.page_directory))
        self.save_file(str(self.page_path), "w", "utf-8", self.default_driver.page_source)
        print("Парсер успешно отработал!")
        self.close_and_quit()

    def read_and_to_soup(self):
        read_html = self.read_file(str(self.page_path), "r", "utf-8")
        return self.to_soup(read_html)

    @staticmethod
    def parse_links(soup: BeautifulSoup) -> list:
        """Метод для чтение и парсинга ссылок с файла"""

        all_links = []
        get_photo_link = soup.select("div.mui-1tx8836-assetItemContainer-assetItemContainer > div.mui-16jc9cy-letterboxingWrapper > img")
        if not get_photo_link:
            print("Ссылок не найдено!")
            return []
        for links in get_photo_link:
            try:
                link = links['src']
                all_links.append(link)
            except KeyError:
                continue
        if not all_links:
            print("Ссылок не найдено!")
            return []
        print(f"Спарсены {len(all_links)} кол-во картинок с второго сайта! переходим к сохранению!")
        return all_links

    def download_and_save_photos(self, links_list: list, save_directory: str) -> list:
        """Метод для скачивания и сохранения фото"""

        photo_info = []
        self.get_directory_or_create(save_directory)
        for link in links_list:
            try:
                photo_name = link.split('/')[-1]
                photo_format = photo_name.split(".")[-1]
                photo_path = f"{save_directory}/{photo_name}"
                self.download_photo(link, photo_path)
                photo_width, photo_height = self.get_photo_sizes(photo_path)
                photo_info.append({
                    "file_name": photo_name,
                    "width": photo_width,
                    "height": photo_height,
                    'file_format': photo_format
                })
            except Exception as e:
                continue
        print(f"Сохранены {len(photo_info)} шт. фото с сайта shutterstock.com!")
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
