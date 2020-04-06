from unittest import TestCase

from context import StatusCode
from fitness_app import app


class TestApp(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.app.get('/manager/clear')

    def tearDown(self) -> None:
        self.app.get('/manager/clear')

    def __create_user(self, pass_id=1):
        pass_dict = {
            "pass_id": pass_id,
            "start": "1/1/2020",
            "finish": "1/10/2020"
        }
        return self.app.post('/manager/create', json=pass_dict)

    def test_manager_create(self):
        response = self.__create_user()
        self.assertEqual(response.status_code, StatusCode.OK)
        response = self.app.get('/manager/get_info/1')
        self.assertEqual(response.status_code, StatusCode.OK)

    def test_manager_update(self):
        response = self.__create_user()
        self.assertEqual(response.status_code, StatusCode.OK)
        pass_dict_new = {
            "pass_id": 1,
            "finish": "1/12/2020"
        }
        response = self.app.post('/manager/update', json=pass_dict_new)
        self.assertEqual(response.status_code, StatusCode.OK)

    def test_user(self):
        self.__create_user()
        response = self.app.post('/user/enter', json={"pass_id": 1})
        self.assertEqual(response.status_code, StatusCode.OK)

        response = self.app.post('/user/enter', json={"pass_id": 1})
        self.assertEqual(response.status_code, StatusCode.ALREADY_IN)

        response = self.app.post('/user/exit', json={"pass_id": 1})
        self.assertEqual(response.status_code, StatusCode.OK)

        response = self.app.post('/user/exit', json={"pass_id": 1})
        self.assertEqual(response.status_code, StatusCode.NOT_ENTER)

    def test_report(self):
        self.__create_user()
        self.__create_user(2)
        response = self.app.post('/user/enter', json={"pass_id": 1})
        response = self.app.post('/user/enter', json={"pass_id": 2})
        response = self.app.get('/report/daily')
        self.assertEqual(response.status_code, StatusCode.OK)
        res = response.get_data().decode()
        print(res)

        response = self.app.post('/user/exit', json={"pass_id": 1})
        response = self.app.post('/user/exit', json={"pass_id": 2})
        response = self.app.get('/report/total')
        res = response.get_data().decode()
        print(res)
        self.assertEqual(response.status_code, StatusCode.OK)
