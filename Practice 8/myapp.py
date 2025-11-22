from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency
from utils.currencies_api import get_currency_data

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

TEMPLATES = {
    "index": env.get_template("index.html"),
    "users": env.get_template("users.html"),
    "currencies": env.get_template("currencies.html"),
    "user": env.get_template("user.html"),
    "author": env.get_template("author.html"),
}

author = Author(name="Антон Пушкарев", group="P4150")
app = App(name="CurrenciesListApp", version="1.0", author=author)

users = [
    User(1, "rodex"),
    User(2, "techno"),
    User(3, "h1k0"),
]

subscriptions = {
    1: ["USD", "EUR"],
    2: ["CNY", "BYN"],
    3: ["TRY", "KZT"],
}


def fetch_currencies(char_codes: list[str]) -> list[Currency]:
    """
    Получает данные о валютах из API и создаёт объекты класса Currency

    :param char_codes: список символьных кодов валют
    :return: список объектов Currency
    """
    raw_data = get_currency_data(char_codes)
    result = []
    for code, data in raw_data.items():
        if data is None:
            continue
        try:
            curr = Currency(
                id_=abs(hash(code)) % 100000,
                num_code=data["NumCode"],
                char_code=data["CharCode"],
                name=data["Name"],
                value=data["Value"],
                nominal=data["Nominal"],
            )
            result.append(curr)
        except (ValueError, TypeError):
            continue
    return result


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path == "/":
                html = TEMPLATES["index"].render(myapp=app, author=author)
                self._send_html(html)

            elif path == "/users":
                html = TEMPLATES["users"].render(users=users)
                self._send_html(html)

            elif path == "/currencies":
                default_codes = ["USD", "EUR", "CNY", "BYN", "TRY", "KZT"]
                codes_param = query.get("codes", [""])[0].strip()
                if codes_param:
                    codes = [c.strip().upper() for c in codes_param.split(",") if c.strip()]
                else:
                    codes = default_codes

                try:
                    currencies = fetch_currencies(codes)
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f"Ошибка получения курсов: {e}".encode("utf-8"))
                    return

                html = TEMPLATES["currencies"].render(currencies=currencies)
                self._send_html(html)

            elif path == "/author":
                html = TEMPLATES["author"].render(author=author, app=app)
                self._send_html(html)

            elif path == "/user":
                user_id_str = query.get("id", [""])[0]
                if not user_id_str.isdigit():
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"ID")
                    return

                user_id = int(user_id_str)
                user = next((u for u in users if u.id == user_id), None)
                if not user:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write("Пользователь не найден".encode('utf-8'))
                    return

                char_codes = subscriptions.get(user_id, [])
                try:
                    subscribed_currencies = fetch_currencies(char_codes)
                except Exception as e:
                    subscribed_currencies = []

                html = TEMPLATES["user"].render(
                    user=user,
                    subscriptions=subscribed_currencies
                )
                self._send_html(html)

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write("Страница не найдена".encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Внутренняя ошибка: {e}".encode("utf-8"))

    def _send_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


def run_server(port: int = 8000):
    server = HTTPServer(("", port), MyRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    run_server()
