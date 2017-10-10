import logging
from flask import Flask
from flask_restful import Api
from .resources import Transaction, Chain, Mine
from .blockchain import Blockchain


__all__ = ['create_app']

logger = logging.getLogger('app')


def create_app(block: Blockchain = None):
    logger.debug('creating flask application')
    app = Flask(__name__)
    api = Api(app)

    if block is None:
        block = Blockchain()

    api.add_resource(Transaction, '/transaction', resource_class_kwargs={'blockchain': block})
    api.add_resource(Chain, '/chain', resource_class_kwargs={'blockchain': block})
    api.add_resource(Mine, '/mine', resource_class_kwargs={'blockchain': block})

    return app
