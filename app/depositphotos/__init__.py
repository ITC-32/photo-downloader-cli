from config import PARSER_DATA_DICT_EXCEL
from .parser import DepositPhotosDownloader


def body_runner_depositphotos(excel_data_dir: str, offset: int, rubric: str, photos_dir: str, excel_file_name: str):
    deposit_photos = DepositPhotosDownloader(PARSER_DATA_DICT_EXCEL)
    deposit_photos.get_directory_or_create(excel_data_dir)
    all_photo_info = []
    for i in range(1, offset + 1):
        photo_soup = deposit_photos.search_and_to_soup(rubric, "-")
        if not photo_soup:
            continue
        photo_links_list = deposit_photos.parse_photo_links(photo_soup)
        if not photo_links_list:
            continue
        all_photo_info += deposit_photos.download_photos(photos_dir, photo_links_list)
    deposit_photos.insert_data(all_photo_info,
                               f"{excel_data_dir}/{excel_file_name}.xlsx")
