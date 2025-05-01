import subprocess
import sys


def install_package(package_name):
    """Устанавливает пакет с PyPI с помощью pip."""
    try:
        # Запускаем pip как подпроцесс
        # sys.executable гарантирует использование pip из того же окружения Python
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            check=True,  # Вызовет исключение CalledProcessError, если pip завершится с ошибкой
            capture_output=True, # Захватывает stdout и stderr
            text=True # Декодирует stdout и stderr как текст
        )
        print(f"Пакет '{package_name}' успешно установлен.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке пакета '{package_name}':")
        print(e.stderr)
    except FileNotFoundError:
        print("Ошибка: 'pip' не найден. Убедитесь, что Python и pip установлены и доступны в PATH.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# Пример использования:
package_to_install = "requests" # Замените на имя нужного пакета
install_package(package_to_install)

# После установки вы можете попытаться импортировать пакет
# (может потребоваться перезапуск скрипта или более сложные манипуляции с sys.path
# в зависимости от того, как и куда pip устанавливает пакет)
try:
    import requests
    print(f"Пакет '{package_to_install}' успешно импортирован после установки.")
except ImportError:
    print(f"Не удалось импортировать пакет '{package_to_install}' сразу после установки.")
