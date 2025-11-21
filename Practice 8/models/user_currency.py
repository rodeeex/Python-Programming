class UserCurrency:
    def __init__(self, id_: int, user_id: int, currency_id: int):
        self.id = id_
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID связи должен быть положительным целым числом")
        self._id = value

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("user_id должен быть положительным целым числом")
        self._user_id = value

    @property
    def currency_id(self) -> int:
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("currency_id должен быть положительным целым числом")
        self._currency_id = value
