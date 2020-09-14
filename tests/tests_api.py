from .tests_base import TestBase
from flask import url_for

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


sample_models = [
    {
        'nome': 'CNNDenoisingAutoEncoder',
        'descricao': 'Um modelo de autoencoder que permite limpar imagens ruidosas'
    },
    {
        'nome': 'CNNDenoisingAutoEncoder',
        #'descricao': 'Um outro modelo de autoencoder que permite limpar imagens ruidosas'
    },
    {
        'nome': 'CatsXDogsClassifier',
        'descricao': 'Rede neural convolucional que permite classificar cães e gatos.'
    },
    {
        'nome': 'CatsXDogsClassifier',
        'descricao': 'OUTRA Rede neural convolucional que permite classificar cães e gatos'
    },
    {
        "nome": "Coronavirus Kmeans-classifier",
        "descricao": "Um modelo de Kmeans que agrupa indivíduos suscetíveis à infecção por COVID-19",
    },
    {
        "nome": "CycleGAN",
        "descricao": "Um modelo de rede neural que aplica novos estilos ao gerar novos exemplares de imagem"
    }
]



class TestGetModel(TestBase):

    def test_get_model_by_name_must_return_error_after_looking_for_a_model_that_is_not_in_the_database(self):
        # Picking a model
        model = sample_models[0]

        response = self.client.get(url_for('aimodels.get_model', nome=model['nome']))

        self.assertRaises(NoResultFound)
        self.assertEqual(404, response.status_code)
        self.assertEqual({'error': 'No such model found within the database'}, response.json)


    def test_get_all_models(self):
        # Removing wrong labeled models to avoid errors
        new_sample_models = [model for index, model in enumerate(sample_models) if index not in (1, 3)]
        
        # Populating the database
        for model in new_sample_models:
            self.client.post(url_for('aimodels.create_model'), json=model)

        response = self.client.get(url_for('aimodels.fetch_all'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(new_sample_models, response.json)

    def test_get_model_by_name_must_return_sent_payload(self):
        # Removing wrong labeled models to avoid errors
        new_sample_models = [model for index, model in enumerate(sample_models) if index not in (1, 3)]
        
        # Populating the database
        for model in new_sample_models:
            self.client.post(url_for('aimodels.create_model'), json=model)

        for model in new_sample_models:
            response = self.client.get(url_for('aimodels.get_model', nome=model['nome']))

            self.assertEqual(200, response.status_code)
            self.assertEqual(model , response.json)



class TestCreateModel(TestBase):

    def test_create_model_must_return_sent_payload(self):
        # Picking a model with complete payload
        model = sample_models[0]

        response = self.client.post(url_for('aimodels.create_model'), json=model)

        self.assertEqual(model, response.json)
        self.assertEqual(201, response.status_code)


    def test_create_model_must_return_error_after_sending_incomplete_payload(self):
        # Picking a model with incomplete payload
        model = sample_models[1]

        response = self.client.post(url_for('aimodels.create_model'), json=model)

        self.assertRaises(ValidationError)
        self.assertEqual({'error': 'Invalid input'}, response.json)
        self.assertEqual(400, response.status_code)

    
    def test_create_model_must_return_error_after_sending_duplicated_name(self):
        # Picking two models with same names but different descriptions
        model_1, model_2 = sample_models[2], sample_models[3] 
        
        response_1 = self.client.post(url_for('aimodels.create_model'), json=model_1)
        response_2 = self.client.post(url_for('aimodels.create_model'), json=model_2)

        self.assertRaises(IntegrityError)
        self.assertEqual(201, response_1.status_code)
        self.assertEqual(model_1, response_1.json)
        self.assertEqual(409, response_2.status_code)
        self.assertEqual({'error': 'Given name already found within the database'}, response_2.json)
