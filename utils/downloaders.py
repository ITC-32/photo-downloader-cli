import urllib3
from urllib3.exceptions import InsecureRequestWarning

from utils.file_managers import FileManager
from utils.request_manager import RequestManager


class PhotoDownloader(RequestManager, FileManager):
    """Загрузчик фото"""

    def download_photo(self, link: str, file_path: str, headers: dict = None, verify: bool = False) -> None:
        urllib3.disable_warnings(InsecureRequestWarning)
        self.save_byte_file(file_path, self.get(link, headers=headers, verify=verify).content)
