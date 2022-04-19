import time

from bs4 import BeautifulSoup

from config.configs import BASE_DIR, PARSER_DATA_DICT_EXCEL
from utils.browser_managers import SeleniumManager
from utils.downloaders import PhotoManager
from utils.file_managers import ExcelManager, FileManager


class ShutterstockDownloader(SeleniumManager, PhotoManager, ExcelManager, FileManager):
    """Парсинг + скачивание фото с сайта shutterstock.com"""

    base_link = "https://www.shutterstock.com/ru"

    def __init__(self, driver_path: str, coordinates: dict) -> None:
        super(ShutterstockDownloader, self).__init__(driver_path)
        ExcelManager.__init__(self, coordinates)
        self.page_path = None

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
        self.get_directory_or_create(str(BASE_DIR / "pages"))
        self.page_path = str(BASE_DIR / "pages/data.html")
        self.save_file(self.page_path, "w", "utf-8", self.default_driver.page_source)
        print("Парсер успешно отработал!")
        self.close_and_quit()

    def read_and_to_soup(self):
        read_html = self.read_file(str(BASE_DIR / "pages/data.html"), "r", "utf-8")
        return self.to_soup(read_html)

    @staticmethod
    def parse_links(soup: BeautifulSoup) -> list:
        """Метод для чтение и парсинга ссылок с файла"""

        all_links = []
        get_photo_link = soup.select("div.jss197 > div.jss201 > img")
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
        self.get_directory_or_create(str(BASE_DIR / save_directory))
        for link in links_list:
            try:
                photo_name = link.split('/')[-1]
                photo_format = photo_name.split(".")[-1]
                photo_path = f"{str(BASE_DIR / save_directory / photo_name)}"
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


def runner() -> None:
    get_rubric = input("Что ищем? Ввод: ")
    get_directory = input("Вводите папку для сохранения фото(относительно текущей папки): ").strip().replace(
        " ", "")
    get_excel_directory = input("Вводите папку для сохранения в excel(относительно текущей папки): ").strip().replace(
        " ", "")
    get_file_name = input("Вводите название файла excel(без .xlsx): ").strip()
    try:
        get_offset = int(input("Сколько страниц хотим парсить(1 страница - 100 фото)? Ввод: "))
    except ValueError:
        print("Не умеешь вводить цифру?")
        time.sleep(1)
        runner()
    else:
        excel_file_folder = str(BASE_DIR / get_excel_directory)
        shutterstock = ShutterstockDownloader(str(BASE_DIR / "drivers/geckodriver.exe"), PARSER_DATA_DICT_EXCEL)
        shutterstock.get_directory_or_create(excel_file_folder)
        all_photo_info = []
        for page in range(1, get_offset + 1):
            shutterstock.parse_photo_page_and_save(get_rubric, "+")
            soup = shutterstock.read_and_to_soup()
            photo_links = shutterstock.parse_links(soup)
            if not photo_links:
                continue
            all_photo_info += shutterstock.download_and_save_photos(photo_links, get_directory)
            shutterstock.base_link = f"{shutterstock.base_link}?page={page}"
        if all_photo_info:
            shutterstock.insert_data(all_photo_info, f"{excel_file_folder}/{get_file_name}.xlsx")


if __name__ == "__main__":
    runner()
