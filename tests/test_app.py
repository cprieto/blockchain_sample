import unittest
import json
from app import create_app


class TestBlockChainApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_create_new_transaction(self):
        response = self.client.post('/transaction',
                                    data=json.dumps({'sender': '', 'recipient': '', 'amount': 10.0}),
                                    content_type='application/json')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['index'] > 0
        assert len(data['message']) > 0


if __name__ == '__main__':
    unittest.main()
