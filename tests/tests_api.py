from flask import url_for
from .tests_base import TestBase

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


# Models used for testing
sample_models = [
    {
        'nome': 'CNNDenoisingAutoEncoder',
        'descricao': 'Um modelo de autoencoder que permite limpar imagens ruidosas'
    },
    {
        'nome': 'CNNDenoisingAutoEncoder',
    },
    {
        'nome': 'CatsXDogsClassifier',
        'descricao': 'Rede neural convolucional que permite classificar cães e gatos com X camadas convolucionais'
    },
    {
        'nome': 'CatsXDogsClassifier',
        'descricao': 'Rede neural convolucional que permite classificar cães e gatos com Y camadas convolucionais'
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
    """A class used to perform tests on getting data transactions"""
    def test_get_all_models(self):
        """Tests whether all models are correctly sent by the server"""
        # Removing wrong labeled models to avoid errors
        new_sample_models = [model for index, model in enumerate(sample_models) if index not in (1, 3)]
        # Populating the database
        for model in new_sample_models:
            self.client.post(url_for('aimodels.create_model'), json=model)
        # Performing GET request to /modelo
        response = self.client.get(url_for('aimodels.fetch_all'))
        # Ensure that all models from response match with 'original' list
        self.assertEqual(200, response.status_code)
        self.assertEqual(new_sample_models, response.json)


    def test_get_model_by_name_must_return_sent_model(self):
        """Performs GET requests looking for models in order to assure each model corresponds what is expected to"""
        # Removing wrong labeled models to avoid errors
        new_sample_models = [model for index, model in enumerate(sample_models) if index not in (1, 3)]
        # Populating the database
        for model in new_sample_models:
            self.client.post(url_for('aimodels.create_model'), json=model)
        # For each request, save currently response state
        for model in new_sample_models:
            response = self.client.get(url_for('aimodels.get_model', nome=model['nome']))
            # Ensure that response matches expected format 
            self.assertEqual(200, response.status_code)
            self.assertEqual(model , response.json)


    def test_get_model_by_name_must_return_error_after_looking_for_a_model_that_is_not_in_the_database(self):
        """Checks whether an error is raised after searching for a non-existent model"""
        # Picking a model
        model = sample_models[0]
        # Perform GET request to /modelo with 'nome' as url parameter
        response = self.client.get(url_for('aimodels.get_model', nome=model['nome']))
        # Ensure matching conditions to response received
        self.assertRaises(NoResultFound)
        self.assertEqual(404, response.status_code)
        self.assertEqual({'error': 'No such model found within the database'}, response.json)



class TestCreateModel(TestBase):
    """A class used to perform tests on creating data transactions"""
    def test_create_model_must_return_sent_payload(self):
        """Checks whether created model has been successfuly sent to server"""
        # Picking a model with complete payload
        model = sample_models[0]
        # Perform POST request with model as payload
        response = self.client.post(url_for('aimodels.create_model'), json=model)
        # Ensure response matches data that has been sent previously
        self.assertEqual(model, response.json)
        self.assertEqual(201, response.status_code)


    def test_create_model_must_return_error_after_sending_incomplete_payload(self):
        """Checks whether an error is sent after providing an incomplete payload"""
        # Picking a model with incomplete data
        model = sample_models[1]
        # Perform POST request with model as payload
        response = self.client.post(url_for('aimodels.create_model'), json=model)
        # Ensure response contains correct error message and status code
        self.assertRaises(ValidationError)
        self.assertEqual({'error': 'Invalid input'}, response.json)
        self.assertEqual(400, response.status_code)

    
    def test_create_model_must_return_error_after_sending_duplicated_name(self):
        """Checks whether an error is sent after providing a name that is already in the database"""
        # Picking two models with same names but different descriptions
        model_1, model_2 = sample_models[2], sample_models[3] 
        # Perform post requests with chosen models as payload
        response_1 = self.client.post(url_for('aimodels.create_model'), json=model_1)
        response_2 = self.client.post(url_for('aimodels.create_model'), json=model_2)
        # Ensure first response is well received by the server
        self.assertEqual(201, response_1.status_code)
        self.assertEqual(model_1, response_1.json)
        # Certify that second response holds an error message and a exception has been raised
        self.assertRaises(IntegrityError)
        self.assertEqual(409, response_2.status_code)
        self.assertEqual({'error': 'Given name already found within the database'}, response_2.json)



class TestRemoveModel(TestBase):
    """A class that performs tests on removing data transactions"""
    def test_remove_model_must_send_error_message_after_sending_inexistent_model(self):
        """Ensures that an error message is sent after sending a model that does not exist"""
        # Picking a model from list
        model = sample_models[0]
        # Removing the model from database
        response = self.client.delete(url_for('aimodels.remove_model', nome=model['nome']))
        # Ensuring correct response is received
        self.assertRaises(NoResultFound)
        self.assertEqual({"error": "No such model in the database"}, response.json)
        self.assertEqual(404, response.status_code)
    

    def test_remove_model_must_delete_data_from_database(self):
        """Checks whether model deletion really removed the intended row from the database table"""
        # Picking a model from list
        model = sample_models[5]
        # Inserting the model into the database
        self.client.post(url_for('aimodels.create_model'), json=model)
        # Removing the very same model from database
        response_delete = self.client.delete(url_for('aimodels.remove_model', nome=model['nome']))
        # Querying for this model
        response_query = self.client.get(url_for('aimodels.get_model', nome=model['nome']))
        # Ensure that model deletion messages have been sent
        self.assertEqual({'status': 'Given model has been deleted'}, response_delete.json)
        self.assertEqual(200, response_delete.status_code)
        # Ensure that removed model is not in the database anymore
        self.assertRaises(NoResultFound)
        self.assertEqual({'error': 'No such model found within the database'}, response_query.json)
        self.assertEqual(404, response_query.status_code)
