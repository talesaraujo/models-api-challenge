from tests_base import TestBase
from flask import url_for
from marshmallow.exceptions import ValidationError


class TestAPI(TestBase):

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
