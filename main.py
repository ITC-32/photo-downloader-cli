# import datetime
# import os
# import random
# import time
#
# import openpyxl
# import requests
# import urllib3
# from PIL import Image
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from urllib3.exceptions import InsecureRequestWarning
#
#
# user_agents_list = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 "
#     "Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 "
#     "Safari/537.36 "
# ]
#
# headers = {
#     "User-Agent": random.choice(user_agents_list)
# }
#
# BASE_LINK_SHUTTER_STOCK = 'https://www.shutterstock.com/ru'
#
#
# def save_photo_info(info_list: list, file_name, file_path):
#     book = openpyxl.Workbook()
#     sheet = book.active
#     sheet['A1'] = 'Название фото'
#     sheet['B1'] = 'Ширина фото(px)'
#     sheet['C1'] = 'Высота фото(px)'
#     sheet['D1'] = 'Формат фото'
#
#     row = 2
#
#     for info in info_list:
#         sheet[row][0].value = info['file_name']
#         sheet[row][1].value = info['width']
#         sheet[row][2].value = info['height']
#         sheet[row][3].value = info['file_format']
#         row += 1
#
#     if not os.path.exists(file_path):
#         os.mkdir(file_path)
#     book.save(f"{file_path}{file_name.replace(' ', '-')}-{datetime.date.today()}.xlsx")
#     book.close()
#     print("Информация сохранена успешно!")
#     return True
#
#
# def parse_with_selenium(link):
#     options = webdriver.FirefoxOptions()
#     options.set_preference('general.useragent.override', random.choice(user_agents_list))
#     options.set_preference("dom.webdriver.enabled", False)
#     options.headless = True
#     link_data = []
#     driver = webdriver.Firefox(
#         executable_path='geckodriver.exe',
#         options=options
#     )
#     try:
#         driver.get(url=link)
#         time.sleep(5)
#         html_page = driver.find_element_by_tag_name("html")
#         for i in range(150):
#             html_page.send_keys(Keys.DOWN)
#         time.sleep(10)
#         with open("file.html", 'w', encoding='utf-8') as file:
#             file.write(driver.page_source)
#         with open("file.html", 'r', encoding='utf-8') as f:
#             parser_file = f.read()
#         soup = BeautifulSoup(parser_file, 'html.parser')
#         get_link = soup.select("div.z_h_b900b > a.z_h_81637 > img")
#         if get_link:
#             try:
#                 for links_ in get_link:
#                     link = links_['src']
#                     link_data.append(link)
#             except KeyError:
#                 print('')
#     finally:
#         driver.close()
#         driver.quit()
#         if not link_data:
#             return False
#         print(f"Спарсены {len(link_data)} кол-во картинок с второго сайта! переходим к сохранению!")
#         return link_data
#
#
# def save_shutter(link_list: list):
#     photo_info = []
#     for link in link_list:
#         try:
#             photo_name = link.split('/')[-1]
#             photo_format = photo_name.split(".")[-1]
#             file_path = './site_shutter_photos'
#             if not os.path.exists(file_path):
#                 os.mkdir('./site_shutter_photos')
#             urllib3.disable_warnings(InsecureRequestWarning)
#             save_data = requests.get(link, verify=False, headers=headers)
#             with open(f"{file_path}/{photo_name}", 'wb') as file:
#                 file.write(save_data.content)
#             with Image.open(f"{file_path}/{photo_name}") as img:
#                 width, height = img.size
#             photo_info.append({
#                 "file_name": photo_name,
#                 "width": width,
#                 "height": height,
#                 'file_format': photo_format
#             })
#         except Exception as e:
#             print("Что то пошло не так.. пропустил этот файл и перешёл на следующий!")
#
#     return photo_info
#
#
# def run():
#     get_rubric = input("Что ищем? Ввод: ")
#     try:
#         get_offset = int(input("Сколько страниц хотим парсить? Ввод: "))
#     except ValueError:
#         print("Не умеешь вводить цифру?")
#         run()
#     get_file_name = input("Вводите название файла excel(без .xlsx): ")
#     get_url = f"{BASE_LINK_SHUTTER_STOCK}/search/{get_rubric.replace(' ', '+')}"
#     link_data = []
#     for get in range(1, get_offset + 1):
#         links = parse_with_selenium(get_url)
#         get_url = f"{BASE_LINK_SHUTTER_STOCK}/search/{get_rubric.replace(' ', '+')}?page={get + 1}"
#         link_data += links
#     if link_data:
#         shutter = save_shutter(link_data)
#         save_photo_info(shutter, get_file_name, "./site_shutter_photos/photo_info/")
#
#
# if __name__ == "__main__":
#     run()
