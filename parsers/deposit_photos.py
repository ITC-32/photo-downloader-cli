import time
from pathlib import Path

from PIL import Image
from bs4 import BeautifulSoup

from utils.downloaders import PhotoDownloader
from utils.file_managers import ExcelManager


class DepositPhotosDownloader(PhotoDownloader, ExcelManager):
    """Парсинг + скачивание фото с сайта depositphotos.com"""

    BASE_LINK = "https://ru.depositphotos.com/stock-photos"
    BASE_DIR = Path(__file__).resolve().parent.parent

    def __init__(self, coordinates: dict) -> None:
        super(DepositPhotosDownloader, self).__init__(coordinates)

    @staticmethod
    def to_soup(content: [str, bytes]) -> BeautifulSoup:
        return BeautifulSoup(content, "html.parser")

    def search_and_to_soup(self, search_rubric: str, offset: int) -> list:
        link = f"{self.BASE_LINK}/{search_rubric.replace(' ', '-')}.html"
        soups_list = []
        for page in range(1, offset + 1):
            get_page = self.get(link)
            if get_page.status_code != 200:
                time.sleep(3)
                continue
            soups_list.append(self.to_soup(get_page.text))
            link = f"{link}?offset={page * 100}"
        return soups_list

    @staticmethod
    def parse_photo_links(soup_list: list) -> list:
        photo_links = []
        for soup in soup_list:
            get_photo_link = soup.select("a > picture > img")
            if get_photo_link:
                for link in get_photo_link:
                    photo_links.append(link.get("src") or link.get("data-src"))
            else:
                continue
        print(f"Спарсены {len(photo_links)} кол-во картинок с сайта depositphotos.com! переходим к сохранению!")
        return photo_links

    def download_photos(self, directory_path: str, photo_links_list: list) -> list:
        photo_info = []
        photo_count = 0
        for link in photo_links_list:
            photo_name = link.split("/")[-1]
            photo_format = photo_name.split(".")[-1]
            photo_path = str(self.BASE_DIR / f"{directory_path}/{photo_name}")
            self.get_directory_or_create(str(self.BASE_DIR / directory_path))
            self.download_photo(link, photo_path)
            with Image.open(photo_path) as img:
                width, height = img.size
            sizes_data = {
                "file_name": photo_name,
                "width": width,
                "height": height,
                "file_format": photo_format
            }
            photo_info.append(sizes_data)
            photo_count += 1
            time.sleep(1)
        print(f"Скачаны {photo_count} шт. фото с сайта depositphotos.com по пути: {self.BASE_DIR / directory_path}")
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


def runner():
    get_rubric = input("Что ищем? Ввод: ")
    get_directory = input("Вводите папку для сохранения фото(относительно текущей папки): ")
    get_excel_directory = input("Вводите папку для сохранения в excel(относительно текущей папки): ")
    get_file_name = input("Вводите название файла excel(без .xlsx): ")
    try:
        get_offset = int(input("Сколько страниц хотим парсить(1 страница - 100 фото)? Ввод: "))
    except ValueError:
        print("Не умеешь вводить цифру?")
        time.sleep(1)
        runner()
    else:
        deposit_photos = DepositPhotosDownloader({
            "A1": "Название фото",
            "B1": "Ширина фото(px)",
            "C1": "Высота фото(px)",
            "D1": "Формат фото"
        })
        deposit_photos.get_directory_or_create(
            str(deposit_photos.BASE_DIR / get_excel_directory.strip().replace(" ", "")))
        photo_soup_list = deposit_photos.search_and_to_soup(get_rubric, get_offset)
        photo_links_list = deposit_photos.parse_photo_links(photo_soup_list)
        photos_info = deposit_photos.download_photos(get_directory, photo_links_list)
        deposit_photos.insert_data(photos_info,
                                   str(deposit_photos.BASE_DIR / f"{get_excel_directory}/{get_file_name}.xlsx"))


if __name__ == "__main__":
    runner()
