from typing import Dict
from flask_restful import Resource
from flask_restful import reqparse
from .blockchain import Blockchain


class Transaction(Resource):
    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    def post(self) -> Dict:
        """
        Create a new transaction in the chain
        :return: index of added transaction and message
        """

        parser = reqparse.RequestParser()
        parser.add_argument('sender', required=True)
        parser.add_argument('recipient', required=True)
        parser.add_argument('amount', type=float, required=True)

        transaction = parser.parse_args()
        index = self._blockchain.new_transaction(transaction.sender, transaction.recipient, transaction.amount)

        return {
            'message': f'I create a transaction boy, with index {index}',
            'index': index
        }

