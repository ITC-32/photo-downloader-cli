import os


class FileManager:
    """Файловый менеджер"""

    @staticmethod
    def get_directory_or_create(directory_path: str) -> None:
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        return

    @staticmethod
    def save_file(file_path: str, write_mode: str, encoding: str, content: str):
        with open(file_path, write_mode, encoding=encoding) as file:
            file.write(content)

    @staticmethod
    def save_byte_file(file_path: str, content: bytes):
        with open(file_path, "wb") as file:
            file.write(content)

    @staticmethod
    def read_file(file_path: str, read_mode: str, encoding: str):
        with open(file_path, read_mode, encoding=encoding) as file:
            read = file.read()
        return read
