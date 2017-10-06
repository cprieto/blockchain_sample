import logging
from flask import Flask
from flask_restful import Api
from .resources import Transaction
from .blockchain import Blockchain


__all__ = ['create_app']

logger = logging.getLogger('app')


def create_app():
    logger.debug('creating flask application')
    app = Flask(__name__)
    api = Api(app)

    chain = Blockchain()
    api.add_resource(Transaction, '/transaction',resource_class_kwargs={'blockchain': chain})

    return app
