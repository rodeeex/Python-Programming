import unittest
from unittest.mock import MagicMock
from controllers.user_controller import UserController


class TestUserController(unittest.TestCase):

    def test_create_user(self):
        """
        Проверка создания пользователя через контроллер
        """
        mock_user_db = MagicMock()
        mock_user_db.create.return_value = 23
        controller = UserController(
            user_crud=mock_user_db
        )

        user_id = controller.create_user('Rodex')

        self.assertEqual(user_id, 23)
        mock_user_db.create.assert_called_once_with('Rodex')

    def test_list_users(self):
        """
        Проверка получения списка пользователей
        """
        mock_user = MagicMock(spec=['id', 'name'])
        mock_user.id = 1
        mock_user.name = 'Hiko'

        mock_user_db = MagicMock()
        mock_user_db.read_all.return_value = [mock_user]

        controller = UserController(
            user_crud=mock_user_db
        )

        users = controller.list_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, 'Hiko')
        mock_user_db.read_all.assert_called_once()

    def test_get_user_found(self):
        """
        Проверка получения существующего пользователя по ID
        """
        mock_user = MagicMock(spec=object)
        mock_user.id = 5
        mock_user.name = 'Techno'

        mock_user_db = MagicMock()
        mock_user_db.read_by_id.return_value = mock_user

        controller = UserController(
            user_crud=mock_user_db
        )

        user = controller.get_user(5)

        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Techno')
        mock_user_db.read_by_id.assert_called_once_with(5)

    def test_get_user_not_found(self):
        """
        Проверка получения несуществующего пользователя
        """
        mock_user_db = MagicMock()
        mock_user_db.read_by_id.return_value = None

        controller = UserController(
            user_crud=mock_user_db
        )

        user = controller.get_user(234234)

        self.assertIsNone(user)
        mock_user_db.read_by_id.assert_called_once_with(234234)
