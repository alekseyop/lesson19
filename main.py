from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        # page_content = open("index.html", "rb").read()
        # пример получения содержимого html-файла с удаленного репозитория
        url = "https://raw.githubusercontent.com/alekseyop/lesson19/develop/index.html"
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.content

        else:
            print(f"Не удалось получить файл. Код ошибки: {response.status_code}")
            exit()

        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(bytes(page_content))  # Тело ответа


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрам в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
