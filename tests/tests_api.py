import unittest
from flask import url_for
from marshmallow.exceptions import ValidationError
from app import create_app


class TestAPI(unittest.TestCase):

    def setUp(self):
        """Runs before all tests"""
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()


    def tearDown(self):
        """Runs after all tests"""
        self.app.db.drop_all()


    def test_create_model_must_return_sent_payload(self):
        ai_model = {
            'nome': 'DenoisingAutoEncoder',
            'descricao': 'Um modelo de autoencoder que permite limpar imagens ruidosas'
        }

        response = self.client.post(url_for('aimodels.create_model'), json=ai_model)
        self.assertEqual(ai_model, response.json)


    def test_create_model_must_return_error_after_send_incomplete_payload(self):
        ai_model = {
            'nome': 'DenoisingAutoEncoder',
            #'descricao': 'Um modelo de autoencoder que permite limpar imagens ruidosas'
        }

        self.client.post(url_for('aimodels.create_model'), json=ai_model)
        self.assertRaises(ValidationError)
