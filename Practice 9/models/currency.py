class Currency:
    def __init__(self, id_: int, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.id = id_
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('ID валюты должен быть положительным целым числом')
        self._id = value

    @property
    def num_code(self) -> str:
        return self._num_code

    @num_code.setter
    def num_code(self, value: str):
        if not isinstance(value, str) or len(value) != 3:
            raise ValueError('Цифровой код должен быть строкой из 3 цифр')
        if not value.isdigit():
            raise ValueError('Цифровой код должен содержать только цифры')
        self._num_code = value

    @property
    def char_code(self) -> str:
        return self._char_code

    @char_code.setter
    def char_code(self, value: str):
        if not isinstance(value, str) or len(value) != 3:
            raise ValueError('Символьный код должен быть строкой из 3 букв')
        if not value.isalpha():
            raise ValueError('Символьный код должен содержать только буквы')
        self._char_code = value.upper()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Название валюты должно быть непустой строкой')
        self._name = value.strip()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError('Курс валюты должен быть положительным числом')
        self._value = float(value)

    @property
    def nominal(self) -> int:
        return self._nominal

    @nominal.setter
    def nominal(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('Номинал должен быть положительным целым числом')
        self._nominal = value
