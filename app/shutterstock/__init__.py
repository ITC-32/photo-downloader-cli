from config import BASE_DIR, PARSER_DATA_DICT_EXCEL
from .parser import ShutterstockDownloader


def body_runner_shutterstock(excel_data_dir: str, offset: int, rubric: str, photos_dir: str, excel_file_name: str):
    shutterstock = ShutterstockDownloader(
        str(BASE_DIR / "drivers/geckodriver.exe"),
        PARSER_DATA_DICT_EXCEL,
        True
    )
    shutterstock.get_directory_or_create(excel_data_dir)
    all_photo_info = []
    for page in range(1, offset + 1):
        shutterstock.parse_photo_page_and_save(rubric, "+")
        soup = shutterstock.read_and_to_soup()
        photo_links = shutterstock.parse_links(soup)
        if not photo_links:
            continue
        all_photo_info += shutterstock.download_and_save_photos(photo_links, str(BASE_DIR / photos_dir))
        shutterstock.base_link = f"{shutterstock.base_link}?page={page}"
    if all_photo_info:
        shutterstock.insert_data(all_photo_info, f"{excel_data_dir}/{excel_file_name}.xlsx")
