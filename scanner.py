import socket
import threading
from tqdm import tqdm  # Импортируем библиотеку tqdm для прогресс-бара


# Функция для сканирования порта
def scan_port(ip, port, results, pbar):
    try:
        # Создаем сокет
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Устанавливаем тайм-аут
        sock.settimeout(1)
        # Пытаемся подключиться к порту
        result = sock.connect_ex((ip, port))
        if result == 0:
            results.append(port)  # Добавляем открытый порт в список
    except Exception:
        pass  # Игнорируем ошибки, такие как прерванные подключения
    finally:
        sock.close()
        pbar.update(1)  # Обновляем прогресс-бар после завершения работы потока


# Основная функция для сканирования
def scan_ports(host):
    results = []
    threads = []
    total_ports = 65535  # Максимальное количество портов для сканирования

    # Создаем прогресс-бар с помощью tqdm
    with tqdm(total=total_ports, desc='Сканирование портов по IP') as pbar:
        for port in range(1, total_ports + 1):
            # Создаем новый поток для каждого порта
            thread = threading.Thread(target=scan_port, args=(host, port, results, pbar))
            threads.append(thread)
            thread.start()  # Запускаем поток

        # Ожидаем завершения всех потоков
        for thread in threads:
            thread.join()

    # Выводим открытые порты в порядке
    if results:
        print(f"Открытые порты на {host}: {', '.join(map(str, sorted(results)))}")
    else:
        print(f"Нет открытых портов на {host}.")


# Тестирование функции
if __name__ == "__main__":
    target = input("Введите адрес для сканирования:")
    scan_ports(target)
