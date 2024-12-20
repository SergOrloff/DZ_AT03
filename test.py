import pytest
from main import get_random_cat_image, save_image
import requests
import logging
import os

# Настройка логирования для тестов
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("test_mock.log"),
                        logging.StreamHandler()
                    ]
                    )
logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    logger.info('Starting test: %s', request.node.name)
    yield
    logger.info('Finished test: %s', request.node.name)


def test_save_image_success(mocker):
    """
    Тестирует успешное сохранение изображения.
    """
    # Мокаем requests.get для загрузки изображения
    mock_get = mocker.patch('main.requests.get')
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.raise_for_status = lambda: None
    mock_response.content = b'Test image content'

    # Мокаем open для предотвращения записи на диск
    mocker.patch('builtins.open', mocker.mock_open())

    save_image('https://example.com/test.jpg', 'test.jpg')

    # Проверяем, что requests.get был вызван с правильным URL
    mock_get.assert_called_with('https://example.com/test.jpg')
    logger.info("Тест успешного сохранения изображения пройден успешно")


def test_save_image_failure(mocker):
    """
    Тестирует обработку ошибки при сохранении изображения.
    """
    # Мокаем requests.get так, чтобы он вызывал исключение
    mock_get = mocker.patch('main.requests.get', side_effect=requests.exceptions.HTTPError("404 Client Error"))

    # Мокаем open для предотвращения записи на диск
    mocker.patch('builtins.open', mocker.mock_open())

    save_image('https://example.com/test.jpg', 'test.jpg')

    # Проверяем, что requests.get был вызван
    mock_get.assert_called_with('https://example.com/test.jpg')
    logger.info("Тест обработки ошибки при сохранении изображения пройден успешно")
