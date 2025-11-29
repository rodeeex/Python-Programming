import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape

from controllers.user_currency_controller import UserCurrencyController
from controllers.user_db import UserDB
from controllers.user_currency_db import UserCurrencyDB
from controllers.user_controller import UserController
from models.author import Author
from models.app import App
from utils.database import Database
from controllers.currency_controller import CurrencyController
from controllers.currency_db import CurrencyDB
from controllers.pages_controller import PagesController

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape())

db = Database()
currency_db = CurrencyDB(db)
user_db = UserDB(db)
user_currency_db = UserCurrencyDB(db)

author = Author(name='Антон Пушкарев', group='P4150')
app = App(name='Currencies', version='2.0', author=author)

currency_ctrl = CurrencyController(currency_db)
user_ctrl = UserController(user_db)
user_currency_ctrl = UserCurrencyController(user_db, user_currency_db, currency_db)
pages_ctrl = PagesController(env, currency_ctrl)

user1_id = user_ctrl.create_user('rodex')
user2_id = user_ctrl.create_user('techno')
user3_id = user_ctrl.create_user('h1k0')

usd_id = currency_ctrl.create_currency('840', 'USD', 'Доллар США', 75.5, 1)
eur_id = currency_ctrl.create_currency('978', 'EUR', 'Евро', 82.1, 1)
cny_id = currency_ctrl.create_currency('156', 'CNY', 'Юань', 10.97, 10)

user_currency_ctrl.subscribe_to_currency(user1_id, usd_id)
user_currency_ctrl.subscribe_to_currency(user1_id, eur_id)
user_currency_ctrl.subscribe_to_currency(user2_id, cny_id)


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Обрабатывает все GET-запросы

        :raises Exception: при внутренней ошибке
        """
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        try:
            if path == '/':
                currencies = currency_ctrl.list_currencies()
                html = pages_ctrl.render_index(app=app, author=author, currencies=currencies)
                self._send_html(html)

            elif path == '/author':
                html = pages_ctrl.render_author(author=author, app=app)
                self._send_html(html)

            elif path == '/users':
                users = user_ctrl.list_users()
                html = pages_ctrl.render_users(users=users)
                self._send_html(html)

            elif path == '/user':
                user_id_str = query.get('id', [''])[0]
                if not user_id_str.isdigit():
                    self.send_error(400, 'ID должен быть целым числом')
                    return
                user_id = int(user_id_str)
                user = user_ctrl.get_user(user_id)
                if not user:
                    self.send_error(404, 'Пользователь не найден')
                    return
                subscriptions = user_currency_ctrl.get_user_subscriptions(user_id)
                html = pages_ctrl.render_user(user=user, subscriptions=subscriptions)
                self._send_html(html)

            elif path == '/currencies':
                currencies = currency_ctrl.list_currencies()
                html = pages_ctrl.render_currencies(currencies=currencies)
                self._send_html(html)

            elif path == '/currency/delete':
                currency_id_str = query.get('id', [''])[0]
                if not currency_id_str.isdigit():
                    self.send_error(400, 'ID валюты должен быть целым числом')
                    return
                currency_ctrl.delete_currency(int(currency_id_str))
                self._redirect('/currencies')

            elif path == '/currency/update':
                for char_code, values in query.items():
                    if char_code and values:
                        try:
                            new_value = float(values[0])
                            currency_ctrl.update_currency(char_code, new_value)
                        except ValueError:
                            continue
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'OK')

            elif path == '/currency/show':
                currencies = currency_ctrl.list_currencies()
                for c in currencies:
                    print(f'[DEBUG] {c.char_code}: {c.value} RUB (id={c.id})')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('См. консоль сервера'.encode('utf-8'))

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
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write('Файл не найден'.encode('utf-8'))

                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(f'Error: {e}'.encode('utf-8'))
                return

            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('Страница не найдена'.encode('utf-8'))

        except Exception as e:
            self.send_error(500, f'Внутренняя ошибка: {e}')

    def _send_html(self, content: str):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def _redirect(self, location: str):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()


def run_server(port: int = 8000):
    server = HTTPServer(('', port), MyRequestHandler)
    print(f'Сервер запущен и работает по адресу: http://localhost:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Сервер остановлен')
        db.close()
        server.server_close()


if __name__ == '__main__':
    run_server()
