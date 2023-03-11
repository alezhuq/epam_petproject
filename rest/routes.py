import json
import os
import logging

mylogs = logging.getLogger(__name__)
mylogs.setLevel(logging.DEBUG)
file = logging.FileHandler("logs.log")
file.setLevel(logging.INFO)
mylogs.addHandler(file)

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
    """
    health check
    :return: A JSON-encoded string containing the 'status' key with value 'working'.
    """
    result = {'status': 'working'}
    mylogs.info(f"{request.url}, OK")
    return json.dumps(result)


# @api.route('/uploads/<filename>')
# def display_image(filename):
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)


# Helping function for upload_image
def allowed_file(filename):
    'check if file extention is valid'
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS


# Uploading images
def upload_image(photo):
    """
    function for saving photos to UPLOAD_FOLDER directory
    :return: path to saved file
    """

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
    """
    Endpoint to get, update, or delete a specific company.

    GET method:
        Returns the details of the requested company and a list of its services.

    PUT method:
        Updates the details of the requested company and returns the updated company details.

    DELETE method:
        Deletes the requested company and returns a JSON response with "result": True.

    Args:
        pk (int): The ID of the company to retrieve, update, or delete.

    Returns:
        A list containing the details of the requested company and its services (for GET),
        or a list containing the updated company details (for PUT), or a JSON response with "result": True (for DELETE).
    """
    if request.method == "GET":
        query = db.session.query(
            Company,
            db.func.group_concat(db.func.json_object(
                'name', Service.name,
                'description', Service.description,
                'price', Service.price)
            ).label("services"),
            db.func.avg(Service.price).label("companies_mean")
        ).outerjoin(
            Service, Service.company_id == Company.id
        ).filter(
            Company.id == pk
        ).group_by(
            Company.id
        ).first()

        if query is None:
            mylogs.error(f"{request.url}, Not found")
            abort(404)
        requested_company = []
        company, service, companies_mean = query
        null = None
        company_dict = {key: value for key, value in company.__dict__.items() if not key.startswith('_')}
        if not service:
            service_list = []
        elif type(eval(service)) is tuple:
            service_list = eval(service)
        else:
            if eval(service)['name'] is None:
                service_list = []
            else:
                service_list = [eval(service)]
        record = {**company_dict, 'services': service_list, 'companies_mean': companies_mean}
        requested_company.append(record)
        mylogs.info(f"{request.url}, OK")
        return requested_company

    requested_company = Company.query.filter_by(id=pk).first()
    if requested_company is None:
        mylogs.error(f"{request.url}, Not found")
        abort(404)

    if request.method == "PUT":
        try:
            if request.files.get("photo") is not None:
                photo = request.files['photo']
                filename = str(upload_image(photo))
                requested_company.photo = filename
            requested_company.name = request.form.get("name", requested_company.name)
            requested_company.description = request.form.get("description", requested_company.description)
            requested_company.website = request.form.get("website", requested_company.website)
            requested_company.email = request.form.get("email", requested_company.email)
            requested_company.phonenum = request.form.get("phonenum", requested_company.phonenum)
            if request.form.get("cities"):
                cities = [int(city_id) for city_id in request.form.get("cities").split()]
            else:
                cities = requested_company.cities

            company_cities = City.query.filter(City.id.in_(cities)).all()
            for city in company_cities:
                requested_company.cities.append(city)
        except Exception as error:
            mylogs.error(f"{error=}, {request.url}, Bad request")
            return abort(400)
        db.session.commit()

        return [requested_company]

    if request.method == "DELETE":
        db.session.delete(requested_company)
        db.session.commit()

        return json.dumps({"result": True})


@api.route('/company/', methods=["GET", "POST"])
@cross_origin()
def company():
    """
    GET method: Retrieves companies with their associated cities based on the query parameters 'city',
    and returns them in JSON format.

    POST method: Adds a new company to the database with the provided information and associated cities,
    and returns the newly created company in JSON format.
    """
    if request.method == "GET":

        args = request.args.to_dict(flat=False)
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
        )

        if args and args['city'] is not None:
            query = query.filter(
                City.id.in_(args['city'])
            )
        query = query.all()
        if query is None:
            mylogs.info(f"{request.url}, OK")
            return []
        requested_company = []
        # converting to JSON serializable format
        null = None
        for company, city in query:
            company_dict = {key: value for key, value in company.__dict__.items() if not key.startswith('_')}
            if not city:
                city_list = []
            elif type(eval(city)) is tuple:
                city_list = eval(city)
            else:
                if eval(city)['name'] is None:
                    city_list = []
                else:
                    city_list = [eval(city)]

            record = {**company_dict, 'city': city_list}
            requested_company.append(record)

        mylogs.info(f"{request.url}, OK")
        return requested_company

    if request.method == "POST":
        try:
            name = request.form['name']
            description = request.form['description']
            website = request.form['website']
            email = request.form['email']
            phonenum = request.form['phonenum']
            if request.form.get("cities"):
                cities = [int(city_id) for city_id in request.form.get("cities").split()]
                company_cities = City.query.filter(City.id.in_(cities)).all()

            photo = request.files.get('photo', None)
        except Exception as error:
            mylogs.error(f"{error=}, {request.url}, Bad request")
            print(f"{error=}, {request.url}, Bad request")
            return abort(400)
        filename = str(upload_image(photo)) if photo else None
        new_company = Company(
            name=name,
            description=description,
            website=website,
            email=email,
            phonenum=phonenum,
            photo=filename,
        )
        if request.form.get("cities"):
            for city in company_cities:
                new_company.cities.append(city)
        db.session.add(new_company)
        db.session.commit()
        mylogs.info(f"{request.url}, OK")
        return [new_company]


# City CRUD
@api.route('/city/', methods=["GET", "POST"])
@cross_origin()
def city():
    """
    GET: Returns a list of all cities in the database.

    POST: Adds a new city to the database.

    JSON Parameters for POST:
    - name (str): The name of the city.

    Returns:
    - GET: A list of all cities in the database.
    - POST: The newly created city.
    """
    if request.method == "GET":
        requested_city = City.query.all()
        mylogs.info(f"{request.url}, OK")
        return requested_city

    if request.method == "POST":
        try:
            name = request.json['name']
        except Exception as error:
            mylogs.error(f"{error=}, {request.url}, Bad request")
            return abort(400)

        new_city = City(
            name=name,
        )
        db.session.add(new_city)
        db.session.commit()
        mylogs.info(f"{request.url}, OK")
        return [new_city]


@api.route("/city/<int:pk>/", methods=["GET", "PUT", "DELETE"])
@cross_origin()
def one_city(pk):
    """
    Get, update, or delete a single city.

    Parameters:

    pk: int
        The primary key of the city to get, update, or delete.

    Returns:

    list or JSON
        If the method is GET or PUT, a list with a single JSON object representing the city is returned.
        If the method is DELETE, a JSON object with the result key set to True is returned.

    Raises:

    404 Not Found
        If no city with the specified primary key is found.
    """

    requested_city = City.query.filter_by(id=pk).first()
    if requested_city is None:
        mylogs.error(f"{request.url}, Not found")
        abort(404)

    if request.method == "GET":
        mylogs.info(f"{request.url}, OK")
        return [requested_city]

    if request.method == "PUT":
        requested_city.name = request.json.get("name", requested_city.name)
        db.session.commit()
        mylogs.info(f"{request.url}, OK")
        return [requested_city]

    if request.method == "DELETE":
        db.session.delete(requested_city)
        db.session.commit()
        mylogs.info(f"{request.url}, OK")
        return json.dumps({"result": True})


@api.route('/service/', methods=['GET'])
@cross_origin()
def get_services():
    """Get a list of all services.

    Returns:
        List of services.
    """
    services = Service.query.all()
    mylogs.info(f"{request.url}, OK")
    return services


@api.route('/service/', methods=['POST'])
@cross_origin()
def create_service():
    """
    Creates a new service.

    Request Args:
        name (str): The name of the service.
        description (str): A description of the service.
        price (int): The price of the service.
        company_id (int): The ID of the company providing the service.

    Returns:
        list: A list containing the newly created service.
    """
    try:
        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        company_id = request.json['company_id']
    except Exception as error:
        mylogs.error(f"{error=}, {request.url}, Bad request")
        abort(400)
    if not Company.query.filter_by(id=company_id).first():
        mylogs.error(f"{request.url}, Not found")
        return abort(404)

    service = Service(name=name, description=description, price=price, company_id=company_id)
    db.session.add(service)
    db.session.commit()
    mylogs.info(f"{request.url}, OK")
    return [service]


@api.route('/service/<int:id>/', methods=['GET'])
@cross_origin()
def get_service(id):
    """
    Endpoint to get a specific service by its ID.

    Args:
        id (int): The ID of the service to retrieve.

    Returns:
        list: A list containing a single dictionary representing the service, with the following keys:
            - id (int): The ID of the service.
            - name (str): The name of the service.
            - description (str): The description of the service.
            - price (float): The price of the service.
            - company_id (int): The ID of the company associated with the service.

    Raises:
        404: If no service is found with the given ID.
    """
    service = Service.query.filter_by(id=id).first()
    if service is None:
        mylogs.error(f"{request.url}, Not found")
        return abort(404)
    return [service]


@api.route('/service/<int:id>/', methods=['PUT'])
@cross_origin()
def update_service(id):
    """
        Update a specific service.

        Args:
            id (int): The ID of the service to update.

        Request Body:
            A JSON object containing any or all of the following fields:
            - name (str): The new name of the service.
            - description (str): The new description of the service.
            - price (float): The new price of the service.
            - company_id (int): The new ID of the company that provides the service.

        Returns:
            A list containing the updated service object.

        Raises:
            404 Not Found: If the service with the specified ID doesn't exist.
            400 Bad Request: If the request body is not a valid JSON object.
        """
    service = Service.query.filter_by(id=id).first()
    if service is None:
        mylogs.error(f"{request.url}, Not found")
        return abort(404)
    try:
        name = request.json.get('name', service.name)
        description = request.json.get('description', service.description)
        price = request.json.get('price', service.price)
        company_id = request.json.get('company_id', service.company_id)
    except Exception as error:
        mylogs.error(f"{error=}, {request.url}, Bad request")
        abort(400)
    service.name = name
    service.description = description
    service.price = price
    service.company_id = company_id
    db.session.commit()
    mylogs.info(f"{request.url}, OK")
    return [service]


@api.route('/service/<int:id>/', methods=['DELETE'])
@cross_origin()
def delete_service(id):
    """
    Delete a specific service.

    Args:
        id (int): The ID of the service to delete.

    Returns:
        A dictionary indicating that the deletion was successful.

    Raises:
        404 Not Found: If the service with the specified ID doesn't exist.
    """
    service = Service.query.filter_by(id=id).first()
    if service is None:
        mylogs.error(f"{request.url}, Not found")
        return abort(404)
    db.session.delete(service)
    db.session.commit()
    mylogs.info(f"{request.url}, OK")
    return {'result': True}
