from unittest import TestCase
from app import create_app


class TestBase(TestCase):
    """This class defines the default test boilerplate meant to run before and after each test"""
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
        self.app.db.session.rollback()
        self.app.db.drop_all()
