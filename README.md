# Автоматизированное скачивание фотографий с запусков SpaceX, фотографий с сайта NASA и автоматический постинг картинок в группу телеграм

## Как установить и запустить

[Установите Python](https://www.python.org/), если этого ещё не сделали.

***Важно! Библиотека Python Telegram Bot не работает под Python 3.12. Гарантировано работает на версии Python 3.10.15***

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Версия Python должна быть не ниже 3.8 и не выше 3.10** 

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. 

- Склонируйте репозиторий:
```shell
git clone https://github.com/spawlov/PostingImage.git
```

#### Если вы используете Poetry

Для установки и активации виртуального окружения запустите последовательно команды:
```shell
poetry install
poetry shell
```

#### Если вы используете pyhon venv

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

Установите зависимости в виртуальное окружение:
```shell
pip install -r requirements.txt
```

Создайте бот в телеграм и получите токен, для этого 
- Напишите боту [@BotFather](https://t.me/BotFather) команду ```/newbot```
- Задайте имя бота:

```text
- Первое — (можно на русском) как он будет отображаться в списке контактов
- Второе — (латинскими буквами) имя, по которому бота можно будет найти в поиске, 
    -- Второе имя должно заканчиваться на _bot 
```

- Получите токен на сайте [NASA](https://api.nasa.gov/)

- Для запуска в корне проекта нужно создать файл .env со следующим содержимым:

```text
SPACEX_PATH=images/spacex - путь для сохранения картинок с запуска SPACE X
SPACEX_FILENAME=spacex - имя файла фото, с номером через символ _ (random - для случайного имени)

NASA_API_KEY= <токен NASA>
NASA_APOD_PATH=images/nasa_apod - путь для сохранения фото космоса
NASA_APOD_FILENAME=apod - имя файла фото, с номером через символ _ (random - для случайного имени)
NASA_APOD_COUNT=50 - количество фото космоса загружаемых за один прием
NASA_EPIC_PATH=images/nasa_epic - путь для сохранения фото Земли из космоса
NASA_EPIC_FILENAME=epic - имя файла фото, с номером через символ _ (random - для случайного имени)

TG_BOT_TOKEN= <токен телеграм бота>
TG_CHANEL_ID=@some_tg_channel - id телеграм канала для публикации фото
TG_POSTING_PERIOD=14400 - периодичность публикации в секундах
```

<hr>

## Как пользоваться

### Загрузка фотографий пусков SpaceX

- фотографии последнего пуска, если фотографии не далались - ничего не будет загружено:
```
python fetch_spacex_images.py
```
или
```
python fetch_spacex_images.py -no=latest 
```
или
```
python fetch_spacex_images.py --launch_no=latest
```
- фотографии определенного пуска, если фотографии не далались - ничего не будет загружено::
```
python fetch_spacex_images.py -no=<id пуска или его порядковый номер>
```
или
```
python fetch_spacex_images.py --launch_no=<id пуска или его порядковый номер>
```
- фотографии всех пусков, при которых делались фотографии:
```
python fetch_spacex_images.py -no=all [-l=<лимит пусков>]
```
или
```
python fetch_spacex_images.py --launch_no=all [--limit=<лимит пусков>]
```
***Важно! Используйте опцию limit иначе будет загружены все фотографии со всех пусков, а это, на январь 2025 года, более 800 фотографий, объемом более 1Гб***

### Загрузка фотографий космоса NASA

```
python fetch_nasa_apod_images.py [-l=<число фотографий>]
```
или
```
python fetch_nasa_apod_images.py [--limit=<число фотографий>]
```
***Если лимит не задан, лимит определяется в файле .env, если не задан и там - равен 50***

### Загрузка фотографий космоса NASA

```
python fetch_nasa_epic_images.py
```
***Запуск без параметров. Будет загружено около 10 фотографий земли из космоса***

### Публикация фотографий в канале телеграм

- публикация определенной ранее скачанной фотографии или внешней фотографии:
```
python post_photos.py -photo=<относительный путь к файлу или url>
```
или
```
python post_photos.py --photo_path=<относительный путь к файлу или url>
```
- публикация одной случайной, ранее загруженной, фотографии:
```
python post_photos.py -cycle=no
```
или
```
python post_photos.py --cycle=no
```
- публикация случайной, ранее загруженной, фотографии в бесконечном цикле:
```
python post_photos.py -cycle=yes [-period=<периодичность в секуднах>]
```
или
```
python post_photos.py --cycle=yes [--posting_period=<периодичность в секуднах>]
```
***Периодичность задается в секундах, если опущен этот параметр - настройка из файла .env***
<hr>

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [https://dvmn.org/](https://dvmn.org/referrals/B9ehIJNk0dwuMb4b8mm7HqIdHWjUo816kuCaKCHI/)
