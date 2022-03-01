import importlib
from unittest import TestCase
from unittest.mock import Mock

from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from entities import Order, User
from services.datasource import Datasource
from usecases.add_to_db import AddClientWithSourceUseCase, AddOrderUseCase
from usecases.log_analytics import AnalyseLogUseCase
from usecases.update_db import UpdateSourceForClientUseCase


class TestAddClientWithSourceUseCase(TestCase):
    def setUp(self) -> None:
        self.usecases = importlib.import_module("usecases.add_to_db")
        self.mock_datasource = Datasource()
        self.session = UnifiedAlchemyMagicMock()
        self.mock_datasource.session = self.session
        self.usecases.datasource = self.mock_datasource

    def test_execute__ok_data__processed_correctly(self):
        data = {"client_id": "test", "document.referer": "test"}
        expected_user = User("test", "test")
        usecase = AddClientWithSourceUseCase()
        usecase.execute(data)
        with self.subTest(name="checking that session was called"):
            self.session.add.assert_called_once()
        with self.subTest(name="checking that user entity generated correctly"):
            user_after_execute = self.session.query(User).filter(User.client_id == data["client_id"]).first()
            self.assertEqual(expected_user.client_id, user_after_execute.client_id)
            self.assertEqual(expected_user.last_paid_source, user_after_execute.last_paid_source)
        with self.subTest(name="checking that commit is called"):
            self.session.commit.assert_called_once()

    def test_execute__error_raised__rollback_called(self):
        data = {"client_id": "test", "document.referer": "test"}
        usecase = AddClientWithSourceUseCase()
        self.session.add.side_effect = Exception("test_exeption")
        usecase.execute(data)
        self.session.rollback.assert_called_once()


class TestAddOrderUseCase(TestCase):
    def setUp(self) -> None:
        self.usecases = importlib.import_module("usecases.add_to_db")
        self.mock_datasource = Datasource()
        self.session = UnifiedAlchemyMagicMock()
        self.mock_datasource.session = self.session
        self.usecases.datasource = self.mock_datasource

    def test_execute__ok_data__processed_correctly(self):
        data = {"client_id": "test", "date": "2021-05-23T18:59:13.286000Z", "document.referer": "test"}
        expected_order = Order(client_id="test", date="2021-05-23T18:59:13.286000Z", source="test")
        usecase = AddOrderUseCase()
        usecase.execute(data)
        with self.subTest(name="checking that session was called"):
            self.session.add.assert_called_once()
        with self.subTest(name="checking that order entity generated correctly"):
            order_after_execute = self.session.query(Order).filter(Order.client_id == data["client_id"]).first()
            self.assertEqual(expected_order.client_id, order_after_execute.client_id)
            self.assertEqual(expected_order.date, order_after_execute.date)
            self.assertEqual(expected_order.source, order_after_execute.source)
        with self.subTest(name="checking that commit is called"):
            self.session.commit.assert_called_once()

    def test_execute__error_raised__rollback_called(self):
        data = {"client_id": "test", "date": "test", "document.referer": "test"}
        usecase = AddOrderUseCase()
        self.session.add.side_effect = Exception("test_exeption")
        usecase.execute(data)
        self.session.rollback.assert_called_once()


class TestUpdateSourceForClientUseCase(TestCase):
    def setUp(self) -> None:
        self.usecases = importlib.import_module("usecases.update_db")
        self.mock_datasource = Datasource()
        self.session = UnifiedAlchemyMagicMock()
        self.mock_datasource.session = self.session
        self.usecases.datasource = self.mock_datasource

    def test_execute__ok_data__processed_correctly(self):
        data = {"client_id": "test", "document.referer": "new_data"}
        usecase = UpdateSourceForClientUseCase()
        self.session.add(User("test", "test"))
        usecase.execute(data)
        user_after_execute = self.session.query(User).filter(User.client_id == data["client_id"]).first()
        self.assertEqual(data["document.referer"], user_after_execute.last_paid_source)
        self.session.commit.assert_called_once()

    def test_execute__error_raised__rollback_called(self):
        data = {"client_id": "test", "document.referer": "test"}
        usecase = UpdateSourceForClientUseCase()
        self.session.add.side_effect = Exception("test_exeption")
        usecase.execute(data)
        self.session.rollback.assert_called_once()


class TestAnalyseLogUseCase(TestCase):
    def setUp(self) -> None:
        self.usecases = importlib.import_module("usecases.log_analytics")

        self.usecases.UpdateSourceForClientUseCase = Mock()
        self.usecases.AddClientWithSourceUseCase = Mock()
        self.usecases.AddOrderUseCase = Mock()

        self.mock_datasource = Datasource()
        self.session = UnifiedAlchemyMagicMock()
        self.mock_datasource.session = self.session
        self.usecases.datasource = self.mock_datasource

    def test_update_user_source__user_row_present__update_used(self):
        data = {"client_id": "test", "document.referer": "https://referal.ours.com/?ref=0xc0ffee"}
        user = User(client_id="test", last_paid_source="test")
        usecase = AnalyseLogUseCase()
        usecase.update_user_source(data, user)
        self.usecases.UpdateSourceForClientUseCase.assert_called_once()

    def test_update_user_source__user_row_missing__add_used(self):
        data = {"client_id": "test", "document.referer": "https://referal.ours.com/?ref=0xc0ffee"}
        usecase = AnalyseLogUseCase()
        usecase.update_user_source(data, None)
        self.usecases.AddClientWithSourceUseCase.assert_called_once()

    def test_update_user_source__domain_not_in_paid_source__nothing_called(self):
        data = {"client_id": "test", "document.referer": "new_data"}
        user = User(client_id="test", last_paid_source="test")
        usecase = AnalyseLogUseCase()
        usecase.update_user_source(data, user)
        self.usecases.UpdateSourceForClientUseCase.assert_not_called()
        self.usecases.AddClientWithSourceUseCase.assert_not_called()

    def test_update_user__domain_from_paid_source__domain_updated(self):
        data_from_log = {"client_id": "test", "document.referer": "https://referal.ours.com/?ref=0xc0ffee"}
        expected_result = {'client_id': 'test', 'document.referer': 'referal.ours.com'}
        AnalyseLogUseCase().update_user_source(data_from_log, User(client_id="test", last_paid_source="test"))
        self.assertEqual(data_from_log, expected_result)

    def test_execute__source_user_row_present__update_used(self):
        data = {"client_id": "test", "document.referer": "https://referal.ours.com/?ref=0xc0ffee"}
        usecase = AnalyseLogUseCase()
        self.session.add(User("test", "test"))
        usecase.execute(data)
        # класс UpdateSourceForClientUseCase вызывается только в функции update_user_source,
        # соответсвенно вызов этого класса означает, что была вызвана функция
        self.usecases.UpdateSourceForClientUseCase.assert_called_once()

    def test_execute_user__source_user_row_missing__add_used(self):
        data = {"client_id": "test", "document.referer": "https://referal.ours.com/?ref=0xc0ffee"}
        updated_data = {"client_id": "test", "document.referer": "referal.ours.com"}
        usecase = AnalyseLogUseCase()
        usecase.execute(data)
        self.usecases.AddClientWithSourceUseCase.assert_called_once()
        self.usecases.AddClientWithSourceUseCase.return_value.execute.assert_called_with(updated_data)

    def test_execute__is_order__added_row(self):
        data = {"client_id": "test",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/cart"}
        updated_data = {"client_id": "test", "document.location": "https://shop.com/checkout",
                        "document.referer": "referal.ours.com"}
        self.session.add(User("test", "referal.ours.com"))
        usecase = AnalyseLogUseCase()
        usecase.execute(data)
        self.usecases.AddOrderUseCase.assert_called_once()
        self.usecases.AddOrderUseCase.return_value.execute.assert_called_with(updated_data)
