import unittest
import json
from app import create_app
from app.blockchain import Blockchain


class TestBlockChainApp(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.app = create_app(self.blockchain)
        self.app.testing = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_create_new_transaction(self):
        response = self.client.post('/transaction',
                                    data=json.dumps({'sender': 'abcdef', 'recipient': 'fedcba', 'amount': 10.0}),
                                    content_type='application/json')

        assert response.status_code == 201

    def test_get_blockchain(self):
        response = self.client.get('/chain')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['length'] == self.blockchain.length
        assert 'chain' in data
        assert len(data['chain']) == self.blockchain.length

    def test_mine(self):
        response = self.client.get('/mine')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'message' in data


if __name__ == '__main__':
    unittest.main()
