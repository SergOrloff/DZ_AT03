import requests
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("test_main.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


def get_random_cat_image():
    """
    Делает запрос к TheCatAPI для получения случайного изображения кошки.
    Возвращает URL изображения при успешном запросе или None при неуспешном.
    """
    url = 'https://api.thecatapi.com/v1/images/search'
    try:
        # Логируем отправку запроса
        logger.info(f"Отправка GET-запроса к {url}")
        response = requests.get(url)

        # Проверяем на наличие HTTP ошибок (4xx и 5xx)
        response.raise_for_status()
        logger.info(f"Успешный ответ от API с кодом состояния {response.status_code}")

        # Получаем данные в формате JSON
        data = response.json()
        logger.debug(f"Полученные данные: {data}")

        # Проверяем, что данные не пустые
        if data:
            image_url = data[0]['url']
            logger.info(f"Получен URL изображения: {image_url}")
            return image_url
        else:
            logger.warning("Ответ от API не содержит данных")
            return None
    except requests.exceptions.RequestException as e:
        # Логируем ошибки, связанные с запросом
        logger.error(f"Произошла ошибка при выполнении запроса: {e}")
        return None


def save_image(url, filename):
    """
    Скачивает изображение по заданному URL и сохраняет его с указанным именем файла.
    """
    try:
        logger.info(f"Скачивание изображения с {url}")
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        logger.info(f"Изображение сохранено как {filename}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Не удалось скачать изображение: {e}")


if __name__ == "__main__":
    image_url = get_random_cat_image()
    if image_url:
        # Извлекаем имя файла из URL
        filename = os.path.basename(image_url)
        save_image(image_url, filename)
    else:
        logger.error("Не удалось получить URL изображения")