import time
from typing import Callable

from config import BASE_DIR


def get_file_paths() -> tuple:
    get_rubric = input("Что ищем? Ввод: ")
    get_directory = input("Вводите папку для сохранения фото(относительно текущей папки): ").strip().replace(
        " ", "")
    get_excel_directory = input("Вводите папку для сохранения в excel(относительно текущей папки): ").strip().replace(
        " ", "")
    excel_file_name = input("Вводите название файла excel(без .xlsx): ").strip()
    return get_rubric, get_directory, get_excel_directory, excel_file_name


def root_run(func: Callable):
    def inner_runner():
        get_rubric, photos_dir, get_excel_directory, excel_filename = get_file_paths()
        try:
            get_offset = int(input("Сколько страниц хотим парсить(1 страница - 100 фото)? Ввод: "))
        except ValueError:
            print("Не умеешь вводить цифру?")
            time.sleep(1)
            inner_runner()
        else:
            excel_file_folder = str(BASE_DIR / get_excel_directory)
            func(excel_file_folder, get_offset, get_rubric, photos_dir, excel_filename)
    return inner_runner
