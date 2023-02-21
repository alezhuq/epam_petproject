import json
import unittest
import io
from PIL import Image
from app import , db
from models.models import Company, Service


class CompanyTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        # create a test company
        self.test_company = Company(
            name='1Test Company new',
            description='Test Company Description',
            website='https://www.example.com',
            email='test@example.com',
            phonenum='1234567890',
            photo='test.jpg'
        )
        db.session.add(self.test_company)
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_get_all_companies(self):
        response = self.app.get('/company')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.test_company.name, str(response.data))

    def test_get_one_company(self):
        response = self.app.get('/company/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.test_company.name, str(response.data))

    def test_create_company(self):
        data = {
            'name': '12 New Test Company newer',
            'description': 'New Test Company Description',
            'website': 'https://www.newexample.com',
            'email': 'newtest@example.com',
            'phonenum': '0987654321',
        }
        image = Image.new('RGB', size=(50, 50), color=(155, 0, 0))
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)

        data['photo'] = (image_bytes, 'test.jpg')

        response = self.app.post('/company', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(data['name'], str(response.data))

    def test_update_company(self):
        data = {
            'name': '1Updated Test Company2',
            'description': 'Updated Test Company Description',
            'website': 'https://www.updatedexample.com',
            'email': 'updatedtest@example.com',
            'phonenum': '0987654321',
        }
        image = Image.new('RGB', size=(50, 50), color=(155, 0, 0))
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)

        data['photo'] = (image_bytes, 'test.jpg')

        response = self.app.put('/company/1', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(data['name'], str(response.data))

    def test_delete_company(self):
        response = self.app.delete('/company/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"result": true}')


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        self.test_company = Company(
            name='1Test Company new',
            description='Test Company Description',
            website='https://www.example.com',
            email='test@example.com',
            phonenum='1234567890',
            photo='test.jpg'
        )
        db.session.add(self.test_company)
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_create_service(self):
        response = self.app.post('/service', json={
            'name': 'Test Service',
            'description': 'This is a test service',
            'price': 100,
            'company_id': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        service = response.json[0]
        self.assertEqual(service['name'], 'Test Service')
        self.assertEqual(service['description'], 'This is a test service')
        self.assertEqual(service['price'], 100)
        self.assertEqual(service['company_id'], 1)

    def test_get_service(self):
        service = Service(name='Test Service', description='This is a test service', price=100, company_id=1)

        db.session.add(service)
        db.session.commit()
        response = self.app.get(f'/service/{service.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        service = response.json[0]
        self.assertEqual(service['name'], 'Test Service')
        self.assertEqual(service['description'], 'This is a test service')
        self.assertEqual(service['price'], 100)
        self.assertEqual(service['company_id'], 1)

    def test_get_services(self):
        service1 = Service(name='Test Service 1', description='This is a test service', price=100, company_id=1)
        service2 = Service(name='Test Service 2', description='This is another test service', price=200, company_id=1)
        db.session.add_all([service1, service2])
        db.session.commit()
        response = self.app.get('/service')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_update_service(self):
        service = Service(name='Test Service', description='This is a test service', price=100, company_id=1)

        db.session.add(service)
        db.session.commit()
        response = self.app.put(f'/service/{service.id}', json={
            'name': 'Updated Test Service',
            'price': 200
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        service = response.json[0]
        self.assertEqual(service['name'], 'Updated Test Service')
        self.assertEqual(service['description'], 'This is a test service')
        self.assertEqual(service['price'], 200)
        self.assertEqual(service['company_id'], 1)

    def test_delete_service(self):
        service = Service(name='Test Service', description='This is a test service', price=100, company_id=1)

        db.session.add(service)
        db.session.commit()
        response = self.app.delete(f'/service/{service.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'result': True})


class CityTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_create_city(self):
        response = self.app.post('/city', data={'name': 'New York'})
        self.assertEqual(response.status_code, 200)
        city = json.loads(response.data)[0]
        self.assertEqual(city['name'], 'New York')

    def test_get_all_cities(self):
        self.app.post('/city', data={'name': 'New York'})
        self.app.post('/city', data={'name': 'San Francisco'})
        response = self.app.get('/city')
        self.assertEqual(response.status_code, 200)
        cities = json.loads(response.data)
        self.assertEqual(len(cities), 2)
        self.assertEqual(cities[0]['name'], 'New York')
        self.assertEqual(cities[1]['name'], 'San Francisco')

    def test_get_city(self):
        self.app.post('/city', data={'name': 'New York'})
        response = self.app.get('/city/1')
        self.assertEqual(response.status_code, 200)
        city = json.loads(response.data)[0]
        self.assertEqual(city['name'], 'New York')

    def test_update_city(self):
        self.app.post('/city', data={'name': 'New York'})
        response = self.app.put('/city/1', json={'name': 'NYC'})
        self.assertEqual(response.status_code, 200)
        city = json.loads(response.data)[0]
        self.assertEqual(city['name'], 'NYC')

    def test_delete_city(self):
        self.app.post('/city', data={'name': 'New York'})
        response = self.app.delete('/city/1')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertTrue(result['result'])


if __name__ == "__main__":
    unittest.main()
