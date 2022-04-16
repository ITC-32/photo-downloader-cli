import time
from pathlib import Path

from PIL import Image
from bs4 import BeautifulSoup

from utils.downloaders import PhotoDownloader


class DepositPhotosDownloader(PhotoDownloader):
    """Парсинг + скачивание фото с сайта depositphotos.com"""

    BASE_LINK = "https://ru.depositphotos.com/stock-photos"
    BASE_DIR = Path(__file__).resolve().parent.parent

    def __init__(self):
        super(DepositPhotosDownloader, self).__init__()

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
                    photo_links.append(link.get('src') or link.get('data-src'))
            else:
                continue
        print(f"Спарсены {len(photo_links)} кол-во картинок с сайта depositphotos.com! переходим к сохранению!")
        return photo_links

    def download_photos(self, directory_path: str, photo_links_list: list):
        photo_info = []
        photo_count = 0
        for link in photo_links_list:
            photo_name = link.split('/')[-1]
            photo_format = photo_name.split(".")[-1]
            photo_path = self.BASE_DIR / f"{directory_path}/{photo_name}"
            self.get_directory_or_create(directory_path)
            self.download_photo(link, photo_path)
            with Image.open(photo_path) as img:
                width, height = img.size
            sizes_data = {
                "file_name": photo_name,
                "width": width,
                "height": height,
                'file_format': photo_format
            }
            photo_info.append(sizes_data)
            photo_count += 1
            time.sleep(1)
        print(f"Скачаны {photo_count} шт. фото с сайта depositphotos.com по пути: {self.BASE_DIR / directory_path}")
        return photo_info


def runner():
    get_rubric = input("Что ищем? Ввод: ")
    get_directory = input("Вводите папку для сохранения(относительно текущей папки): ")
    try:
        get_offset = int(input("Сколько страниц хотим парсить(1 страница - 100 фото)? Ввод: "))
    except ValueError:
        print("Не умеешь вводить цифру?")
        time.sleep(1)
        runner()
    else:
        deposit_photos = DepositPhotosDownloader()
        photo_soup_list = deposit_photos.search_and_to_soup(get_rubric, get_offset)
        photo_links_list = deposit_photos.parse_photo_links(photo_soup_list)
        deposit_photos.download_photos(get_directory, photo_links_list)


if __name__ == "__main__":
    runner()
