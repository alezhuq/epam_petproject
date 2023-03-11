from dataclasses import dataclass

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

migrate = Migrate(db=db)


# models here

@dataclass
class Company(db.Model):
    """
    A dataclass representing a company that provides services.

    Attributes:
        id (int): The unique ID of the company.
        name (str): The name of the company.
        description (str): A description of the company.
        website (str): The URL of the company's website.
        email (str): The email address of the company.
        phonenum (str): The phone number of the company.
        photo (str): The URL of a photo of the company.
        services (list): A list of services provided by the company.

    Relationship:
        A company can have many services associated with it.

    """
    id: int
    name: str
    description: str
    website: str
    email: str
    phonenum: str
    photo: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
    website = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phonenum = db.Column(db.Integer)
    photo = db.Column(db.String(100))
    services = db.relationship('Service', backref='company', lazy=True, cascade='all, delete')


@dataclass
class Service(db.Model):
    """
    A dataclass representing a service provided by a company.

    Attributes:
        id (int): The unique ID of the service.
        name (str): The name of the service.
        description (str): A description of the service.
        price (int): The price of the service.
        company_id (int): The ID of the company that provides the service.

    Relationship:
        A service belongs to a company.

    """
    id: int
    name: str
    description: str
    price: int
    company_id: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id", ondelete='CASCADE'), nullable=False)


cities_companies = db.Table('cities_companies',
    db.Column('city_id', db.Integer, db.ForeignKey('city.id', ondelete='CASCADE'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), primary_key=True)
)


@dataclass
class City(db.Model):
    """
    A dataclass representing a city.

    Attributes:
        id (int): The unique ID of the city.
        name (str): The name of the city.

    Relationship:
        A city can have many companies associated with it.

    """
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    companies = db.relationship(
        'Company',
        secondary=cities_companies,
        lazy='subquery',
        backref=db.backref('cities', lazy=True)
    )
