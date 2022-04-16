## Проект для авто парсинга(скачивания) картинок с сайтов DepositPhotos и ShutterStock
Вводные данные: 
1. Кол-во страниц для парсинга 
2. Название файла excel для сохранения расширения и формат фото
3. Поиск(название) рубрики(категории) для поиска

## Установка зависимостей и первый запуск
1. Создаём виртуальное окружение и активируем её
```
python -m venv venv
venv\Scripts\activate
```
2. Установим зависимости
```
pip install -r requirements.txt
```
3. Запускаем файл
```
python main.py
```
## Развернуть в .ехе файл
1.`pyinstaller main.py`
