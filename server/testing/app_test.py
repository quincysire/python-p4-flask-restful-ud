import json
import unittest

from app import app, db
from models import Plant

class TestPlant(unittest.TestCase):
    '''Flask application in app.py'''

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        self.assertEqual(response.status_code, 200)

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        data = json.loads(response.data.decode())

        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertIn("name", data)

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        plant_1 = Plant.query.filter_by(id=1).first()
        plant_1.is_in_stock = True
        db.session.add(plant_1)
        db.session.commit()

        response = self.client.patch(
            '/plants/1',
            json={
                "is_in_stock": False,
            }
        )
        data = json.loads(response.data.decode())

        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertFalse(data["is_in_stock"])

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''returns JSON representing updated Plant object at "/plants/<int:id>".'''
        lo = Plant(
            name="Live Oak",
            image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
            price=250.00,
            is_in_stock=False,
        )

        db.session.add(lo)
        db.session.commit()

        response = self.client.delete(f'/plants/{lo.id}')

        # Check if the plant is no longer in the database
        self.assertIsNone(db.session.query(Plant).get(lo.id))

    def setUp(self):
        # Create a test client and push an application context
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop the application context after each test
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()