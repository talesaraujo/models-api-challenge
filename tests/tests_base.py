from unittest import TestCase
from app import create_app

class TestBase(TestCase):

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
