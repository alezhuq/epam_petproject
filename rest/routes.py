import json
import os

from flask import Blueprint, request, flash, redirect, abort
from werkzeug.utils import secure_filename

from flask_cors import cross_origin, CORS

from models.models import Company, db, City, Service

ALLOWED_EXTENTIONS = ('png', 'jpg', 'jpeg',)
UPLOAD_FOLDER = 'static/uploads/'
api = Blueprint('api', __name__)

CORS(api)

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
def one_company(pk):
    requested_company = Company.query.filter_by(id=pk).first()

    if requested_company is None:
        abort(404)

    if request.method == "GET":
        return [requested_company]

    if request.method == "PUT":

        if request.files.get("photo") is not None:
            photo = request.files['photo']
            filename = str(upload_image(photo))
            requested_company.photo = filename
        requested_company.name = request.form.get("name", requested_company.name)
        requested_company.description = request.form.get("description", requested_company.description)
        requested_company.website = request.form.get("website", requested_company.website)
        requested_company.email = request.form.get("email", requested_company.email)
        requested_company.phonenum = request.form.get("phonenum", requested_company.phonenum)

        requested_company.cities = request.form.get("cities", requested_company.cities)

        db.session.commit()

        return [requested_company]

    if request.method == "DELETE":
        db.session.delete(requested_company)
        db.session.commit()

        return json.dumps({"result": True})


@api.route('/company/', methods=["GET", "POST"])
@cross_origin()
def company():
    if request.method == "GET":
        company = Company.query.all()
        return company

    if request.method == "POST":
        try:
            name = request.form['name']
            description = request.form['description']
            website = request.form['website']
            email = request.form['email']
            phonenum = request.form['phonenum']
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
            name = request.form['name']
        except Exception:
            return abort(404)

        new_city = City(
            name=name,
        )
        db.session.add(new_city)
        db.session.commit()
        return [new_city]


@api.route("/city/<int:pk>", methods=["GET", "PUT", "DELETE"])
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


@api.route('/service/<int:id>', methods=['GET'])
@cross_origin()
def get_service(id):
    service = Service.query.filter_by(id=id).first()
    if service is None:
        return {'error': 'Service not found'}, 404
    return [service]


@api.route('/service/<int:id>', methods=['PUT'])
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


@api.route('/service/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_service(id):
    service = Service.query.filter_by(id=id).first()
    if service is None:
        return {'error': 'Service not found'}, 404
    db.session.delete(service)
    db.session.commit()
    return {'result': True}
