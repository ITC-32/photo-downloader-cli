## Проект для авто парсинга(скачивания) картинок с сайтов DepositPhotos и ShutterStock
Вводные данные: 
1. Кол-во страниц для парсинга(1 страница == 100 фотографий)
2. Название файла excel для сохранения расширения и формат фото
3. Поиск(название) рубрики(категории) для поиска

## Установка зависимостей и первый запуск
1. Скачиваем [geckodriver](https://github.com/mozilla/geckodriver/releases) или 
   [chromedriver](https://chromedriver.chromium.org/downloads)
   (смотя какой хотите юзать) и распакуем архив на директорию `./drivers/` в папке проекта
2. Создаём виртуальное окружение и активируем её
```
python -m venv venv
venv\Scripts\activate
or 
source env/bin/activate
```
3. Установим зависимости
```
pip install -r requirements.txt
```
4. Запускаем файлы
```
python parsers/deposit_photos.py
python parsers/shutterstock.py
```
