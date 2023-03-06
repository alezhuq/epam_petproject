import json
import os

from flask import Blueprint, request, flash, redirect, abort
from werkzeug.utils import secure_filename
from sqlalchemy.orm import subqueryload
from flask_cors import cross_origin, CORS

from models.models import Company, db, City, Service

from models.models import cities_companies

ALLOWED_EXTENTIONS = ('png', 'jpg', 'jpeg',)
UPLOAD_FOLDER = 'static/uploads/'
api = Blueprint('api', __name__)


@api.route('/')
@cross_origin()
def index():
    result = {'status': 'working'}
    return json.dumps(result)


# @api.route('/uploads/<filename>')
# def display_image(filename):
#     # print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)


# Helping function for upload_image
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS


# Uploading images
def upload_image(photo):
    if photo.filename == '':
        flash("No image selected")
        return redirect(request.url)

    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(UPLOAD_FOLDER, filename))

        flash("uploaded")
        return os.path.join(UPLOAD_FOLDER, filename)


# Company CRUD

@api.route("/company/<int:pk>/", methods=["GET", "PUT", "DELETE"])
@cross_origin()
def one_company(pk):
    if request.method == "GET":

        # query = db.session.query(
        #     Company, db.func.group_concat(db.func.json_object(
        #         'name', Service.name,
        #         'description', Service.description,
        #         'price', Service.price).label("services"))
        # ).outerjoin(
        #     Service, Service.company_id == Company.id
        # ).filter_by(
        #     id=pk
        # ).group_by(
        #     Company.id
        # ).first()
        query = db.session.query(
            Company, db.func.group_concat(db.func.json_object(
                'name', Service.name,
                'description', Service.description,
                'price', Service.price)).label("services")
        ).outerjoin(
            Service, Service.company_id == Company.id
        ).filter(
            Company.id == pk
        ).group_by(
            Company.id
        ).first()

        if query is None:
            abort(404)
        requested_company = []
        company, service = query
        company_dict = {key: value for key, value in company.__dict__.items() if not key.startswith('_')}
        service_dict = eval(service) if service is not None else {}

        record = {**company_dict, 'services': service_dict}
        requested_company.append(record)


        return requested_company
    requested_company = Company.query.filter_by(id=pk).first()
    if request.method == "PUT":
        print(requested_company)
        if request.files.get("photo") is not None:
            photo = request.files['photo']
            filename = str(upload_image(photo))
            requested_company.photo = filename
        requested_company.name = request.json.get("name", requested_company.name)
        requested_company.description = request.json.get("description", requested_company.description)
        requested_company.website = request.json.get("website", requested_company.website)
        requested_company.email = request.json.get("email", requested_company.email)
        requested_company.phonenum = request.json.get("phonenum", requested_company.phonenum)

        cities = request.json.get("cities", requested_company.cities)
        print(cities)
        company_cities = City.query.filter(City.id.in_(cities)).all()
        print(company_cities, "comp cities")
        for city in company_cities:
            requested_company.cities.append(city)

        db.session.commit()
        print(requested_company.cities)

        return json.dumps({"result": True})

    if request.method == "DELETE":
        db.session.delete(requested_company)
        db.session.commit()

        return json.dumps({"result": True})


@api.route('/company/', methods=["GET", "POST"])
@cross_origin()
def company():
    if request.method == "GET":

        query = db.session.query(
            Company, db.func.group_concat(db.func.json_object(
                'name', City.name,
            ).label("cities"))
        ).select_from(
            Company
        ).outerjoin(
            cities_companies, Company.id == cities_companies.c.company_id
        ).outerjoin(
            City, cities_companies.c.city_id == City.id
        ).group_by(
            Company.id
        ).all()
        print(query)
        requested_company = []
        # converting to JSON serializable format
        null = None
        for company, city in query:
            company_dict = {key: value for key, value in company.__dict__.items() if not key.startswith('_')}
            service_dict = eval(city) if city is not None else {}
            record = {**company_dict, 'city': service_dict}
            requested_company.append(record)
        return requested_company

    if request.method == "POST":
        try:
            name = request.json['name']
            description = request.json['description']
            website = request.json['website']
            email = request.json['email']
            phonenum = request.json['phonenum']
            photo = request.files['photo']
        except Exception:
            return abort(404)

        filename = str(upload_image(photo))
        new_company = Company(
            name=name,
            description=description,
            website=website,
            email=email,
            phonenum=phonenum,
            photo=filename,
        )
        db.session.add(new_company)
        db.session.commit()
        return [new_company]


# City CRUD
@api.route('/city/', methods=["GET", "POST"])
@cross_origin()
def city():
    if request.method == "GET":
        requested_city = City.query.all()
        return requested_city

    if request.method == "POST":
        try:
            name = request.json['name']
        except Exception:
            return abort(404)

        new_city = City(
            name=name,
        )
        db.session.add(new_city)
        db.session.commit()
        return [new_city]


@api.route("/city/<int:pk>/", methods=["GET", "PUT", "DELETE"])
@cross_origin()
def one_city(pk):
    requested_city = City.query.filter_by(id=pk).first()
    if requested_city is None:
        abort(404)

    if request.method == "GET":
        return [requested_city]

    if request.method == "PUT":
        requested_city.name = request.json.get("name", requested_city.name)
        db.session.commit()

        return [requested_city]

    if request.method == "DELETE":
        db.session.delete(requested_city)
        db.session.commit()

        return json.dumps({"result": True})


@api.route('/service/', methods=['GET'])
@cross_origin()
def get_services():
    services = Service.query.all()
    return services


@api.route('/service/', methods=['POST'])
@cross_origin()
def create_service():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    company_id = request.json['company_id']
    service = Service(name=name, description=description, price=price, company_id=company_id)
    db.session.add(service)
    db.session.commit()
    return [service]


@api.route('/service/<int:id>/', methods=['GET'])
@cross_origin()
def get_service(id):
    service = Service.query.filter_by(id=id).first()
    if service is None:
        return {'error': 'Service not found'}, 404
    return [service]


@api.route('/service/<int:id>/', methods=['PUT'])
@cross_origin()
def update_service(id):
    service = Service.query.filter_by(id=id).first()
    if service is None:
        return {'error': 'Service not found'}, 404
    name = request.json.get('name', service.name)
    description = request.json.get('description', service.description)
    price = request.json.get('price', service.price)
    company_id = request.json.get('company_id', service.company_id)
    service.name = name
    service.description = description
    service.price = price
    service.company_id = company_id
    db.session.commit()
    return [service]


@api.route('/service/<int:id>/', methods=['DELETE'])
@cross_origin()
def delete_service(id):
    service = Service.query.filter_by(id=id).first()
    if service is None:
        return {'error': 'Service not found'}, 404
    db.session.delete(service)
    db.session.commit()
    return {'result': True}
