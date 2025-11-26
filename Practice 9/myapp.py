import html
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency
from utils.currencies_api import get_currency_data, get_historical_rates

env = Environment(
    loader=PackageLoader('myapp'),
    autoescape=select_autoescape()
)

TEMPLATES = {
    'index': env.get_template('index.html'),
    'users': env.get_template('users.html'),
    'currencies': env.get_template('currencies.html'),
    'author': env.get_template('author.html'),
}

author = Author(name='Антон Пушкарев', group='P4150')
app = App(name='CurrenciesApp', version='1.0', author=author)


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path == '/':
                html = TEMPLATES['index'].render(myapp=app, author=author)
                self._send_html(html)

            elif path == '/users':
                html = TEMPLATES["users"].render(users=users)
                self._send_html(html)

            elif path == '/currencies':
                default_codes = ['USD', 'EUR', 'CNY', 'BYN', 'TRY', 'KZT']
                codes_param = query.get('codes', [''])[0].strip()
                if codes_param:
                    codes = [c.strip().upper() for c in codes_param.split(',') if c.strip()]
                else:
                    codes = default_codes

                try:
                    currencies = fetch_currencies(codes)
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f'Ошибка получения курсов: {e}'.encode('utf-8'))
                    return

                html = TEMPLATES['currencies'].render(currencies=currencies)
                self._send_html(html)

            elif path == '/author':
                html = TEMPLATES['author'].render(author=author, app=app)
                self._send_html(html)


            elif path.startswith('/static/'):
                relative_path = path[len('/static/'):]
                if '..' in relative_path or relative_path.startswith('/'):
                    self.send_response(403)
                    self.end_headers()
                    self.wfile.write(b'Forbidden')
                    return

                import os
                static_dir = os.path.join(os.path.dirname(__file__), 'static')
                file_path = os.path.join(static_dir, relative_path)

                mime_types = {
                    '.js': 'application/javascript',
                    '.css': 'text/css',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.svg': 'image/svg+xml',
                    '.json': 'application/json',
                    '.html': 'text/html',
                }

                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()

                    _, ext = os.path.splitext(file_path)
                    content_type = mime_types.get(ext.lower(), 'application/octet-stream')

                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)

                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'File not found')
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f'Error: {e}'.encode('utf-8'))
                return

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write('Страница не найдена'.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Внутренняя ошибка: {e}'.encode('utf-8'))

    def _send_html(self, content: str):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))


def run_server(port: int = 8000):
    server = HTTPServer(('', port), MyRequestHandler)
    try:
        print(f'Сервер запущен, работает по адресу http://127.0.0.1:{port}')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Сервер остановлен')
        server.server_close()


if __name__ == '__main__':
    run_server()
