from dataclasses import dataclass

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

migrate = Migrate(db=db)


# models here

@dataclass
class Company(db.Model):
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
    email = db.Column(db.String(100))
    phonenum = db.Column(db.Integer)
    photo = db.Column(db.String(100))
    services = db.relationship('Service', backref='company', lazy=True, cascade='all, delete')


@dataclass
class Service(db.Model):
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
